from europa_eu import EuropeEuApi
from arbeitsagentur import ArbeitsagenturApi
import csv
from loguru import logger
from settings import STOP_WORDS, SEARCH_FILTERS, TWO_CAPTCHA_API_KEY


def has_stop_words_in_content(content: str) -> bool:
    for stop_word in STOP_WORDS:
        if stop_word in content:
            return True
    return False


def parse_europe_eu() -> list[list[str]]:
    logger.info("Starting parse_europe_eu function")
    europe_eu_api = EuropeEuApi()
    page = 1
    result = []

    while True:
        logger.debug(f"Fetching IDs from EuropeEuApi, page {page}")
        ids = europe_eu_api.search(page=page)
        page += 1

        if len(ids) == 0:
            logger.info("No more IDs found, ending loop")
            break

        for id in ids:
            logger.debug(f"Fetching details for ID {id}")
            details = europe_eu_api.details(id)
            result.extend([list(detail.values()) for detail in details])

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
        response = arbeitsagentur_api.search(page=page, params=SEARCH_FILTERS)
        page += 1
        vacancies.extend(response.result)

    filtered_vacancies = []
    for vacancy in vacancies:
        logger.debug(f"Fetching full info for vacancy ID {vacancy.id}")
        full_info = arbeitsagentur_api.full_info(vacancy.id)

        if has_stop_words_in_content(str(full_info)):
            logger.warning(f"Vacancy ID {vacancy.id} contains stop words, skipping")
            continue

        logger.debug(f"Fetching details for vacancy ID {vacancy.id}")
        details_response = arbeitsagentur_api.details(vacancy.id)

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
    rows.extend(parse_europe_eu())
    rows.extend(parse_arbeitsagentur())

    with open("vacancies.csv", "w", encoding="utf-8") as file_obj:
        csv_writer = csv.writer(file_obj)
        csv_writer.writerows(rows)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
