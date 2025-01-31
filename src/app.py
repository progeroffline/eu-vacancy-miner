import csv
import urllib.parse
from loguru import logger
from settings import (
    STOP_WORDS,
    TWO_CAPTCHA_API_KEY,
    EUROPA_EU_SERACH_LINKS,
)
from europa_eu import EuropeEuApi
from arbeitsagentur import ArbeitsagenturApi


SEARCH_FILTERS = {
    "angebotsart": 1,
    "arbeitszeit": "vz",
    "beruf": "Agrarwirtschaftlich-technische/r Assistent/in;Fischverarbeiter/in;Flugzeugreiniger/in;Forstwirt/in;Garten-/Landschaftsgestalter/in;Gebäudereiniger/in;Glasreiniger/in;Gärtner/in - Friedhofsgärtnerei;Gärtner/in - Garten- und Landschaftsbau;Gärtner/in - Gemüsebau;Hausdame/Housekeeper;Helfer/in - Forstwirtschaft;Helfer/in - Gartenbau;Helfer/in - Hotel;Helfer/in - Landwirtschaft;Helfer/in - Lebensmittelherstellung;Helfer/in - Reinigung;Helfer/in - Tierpflege;Landwirt/in;Textilreiniger/in;Bügler/in;Greenkeeper-Assistent/in;Spezialreiniger/in",
    "berufsfeld": "Fischwirtschaft;Forstwirtschaft, Jagdwirtschaft, Landschaftspflege;Gartenbau;Hotellerie;Landwirtschaft;Lebensmittel- und Genussmittelherstellung;Reinigung;Tierpflege",
    "externestellenboersen": "false",
    "facetten": "veroeffentlichtseit,arbeitszeit,arbeitsort",
    "pav": False,
    "sort": "veroeffdatum",
    "veroeffentlichtseit": 0,
    "zeitarbeit": False,
}


def has_stop_words_in_content(content: str) -> bool:
    for stop_word in STOP_WORDS.split():
        if stop_word.lower() in content.lower():
            return True
    return False


def parse_url_params(url: str) -> dict[str, str]:
    parsed_url = urllib.parse.urlparse(url)
    return dict(urllib.parse.parse_qsl(parsed_url.query))


def parse_europe_eu(search_link: str) -> list[list[str]]:
    logger.info(f"Starting parse_europe_eu function url: {search_link}")
    europe_eu_api = EuropeEuApi()
    page = 1
    result = []

    ids, total_results = europe_eu_api.search(
        page=page,
        params=parse_url_params(search_link),
    )
    for id in ids:
        logger.debug(f"Fetching details for ID {id}")
        details = europe_eu_api.details(id)
        result.extend([list(detail.values()) for detail in details])

    while len(result) < total_results:
        page += 1
        logger.debug(f"Fetching IDs from EuropeEuApi, page {page}")
        ids, total_results = europe_eu_api.search(
            page=page, params=parse_url_params(search_link)
        )
        for id in ids:
            logger.debug(f"Fetching details for ID {id}")
            details = europe_eu_api.details(id)
            result.extend([list(detail.values()) for detail in details])

        if len(ids) == 0:
            break

    logger.info("Finished parse_europe_eu function")
    return result


def parse_arbeitsagentur() -> list[list[str]]:
    logger.info("Starting parse_arbeitsagentur function")
    arbeitsagentur_api = ArbeitsagenturApi(TWO_CAPTCHA_API_KEY)

    page = 1
    vacancies = []
    logger.debug(f"Fetching initial search results, page {page}")
    response = arbeitsagentur_api.search(page=page, params=SEARCH_FILTERS)

    while len(vacancies) < response.total:
        logger.debug(f"Fetching search results, page {page}")
        page += 1
        response = arbeitsagentur_api.search(page=page, params=SEARCH_FILTERS)
        vacancies.extend(response.result)
        if len(response.result) == 0:
            break

    filtered_vacancies = []
    for vacancy in vacancies:
        logger.debug(f"Fetching full info for vacancy ID {vacancy.id}")
        full_info = arbeitsagentur_api.full_info(vacancy.id)

        if has_stop_words_in_content(str(full_info)):
            logger.warning(f"Vacancy ID {vacancy.id} contains stop words, skipping")
            continue

        logger.debug(f"Fetching details for vacancy ID {vacancy.id}")
        details_response = arbeitsagentur_api.details(vacancy.id)
        if details_response is None:
            continue

        if details_response.phone_number:
            logger.debug(f"Adding details for vacancy ID {vacancy.id} to results")
            details_response.title = vacancy.title
            filtered_vacancies.append(details_response)

    logger.info("Finished parse_arbeitsagentur function")

    return list(
        {
            vacancy.phone_number: [
                vacancy.title,
                vacancy.company,
                vacancy.address,
                vacancy.phone_number,
                vacancy.email,
                vacancy.url,
                "",
            ]
            for vacancy in filtered_vacancies
        }.values()
    )


def main():
    rows = [
        [
            "Название вакансии",  # 1
            "Название компании",  # 2
            "Адрес",  # 3
            "Номер телефона",  # 4
            "Эл. почта",  # 5
            "Ссылка на вакансию",  # 6
            "ФИО",  # 7
        ]
    ]

    for search_link in EUROPA_EU_SERACH_LINKS:
        rows.extend(parse_europe_eu(search_link))

    rows.extend(parse_arbeitsagentur())

    with open("vacancies.csv", "w", encoding="utf-8") as file_obj:
        csv_writer = csv.writer(file_obj)
        csv_writer.writerows(rows)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
