from typing import Any
import httpx

from .endpoints import EuropeEuApiEndpoints
from .formatter import ApiResponseFormatter


class EuropeEuApi:
    def __init__(self):
        self.cookies = {
            "EURES_JVSE_SESSIONID": "A61E8598A34AA3D3A062DEC25029EFC6",
            "XSRF-TOKEN": "7cb6382d-39b3-4028-a575-155455ec7ebb",
            "cck1": "%7B%22cm%22%3Atrue%2C%22all1st%22%3Atrue%2C%22closed%22%3Afalse%7D",
        }

        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "ru",
            "X-XSRF-TOKEN": "7cb6382d-39b3-4028-a575-155455ec7ebb",
            "Content-Type": "application/json",
            "Origin": "https://europa.eu",
            "Connection": "keep-alive",
            "Referer": "https://europa.eu/eures/portal/jv-se/search?page=2&resultsPerPage=10&orderBy=BEST_MATCH&locationCodes=at,de&keywordsEverywhere=Sp%C3%BCler%20%20K%C3%BCchenhelfer%20%20Housekeeping%20%20Reinigungskraft%20%20Public%20cleaner%20%20Zimmerm%C3%A4dchen%20%20K%C3%BCchenhilfe%20%20Reinigung%20%20W%C3%A4schereimitarbeiter%20%20Helfer%20Hotel%20%20Erntehelfer%20%20%20Saisonkraft%20%20Saison%20Mitarbeiter%20%20Helfer%20Landwirtschaft&positionScheduleCodes=fulltime&sector=a,i&educationAndQualificationLevel=NS&publicationPeriod=LAST_DAY&lang=de",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }

    def _make_post_request(self, url: str, json: dict[str, Any] = {}) -> httpx.Response:
        response = httpx.post(
            url,
            json=json,
            timeout=60,
            headers=self.headers,
            cookies=self.cookies,
        )
        return response

    def _make_get_request(
        self, url: str, params: dict[str, Any] = {}
    ) -> httpx.Response:
        return httpx.get(
            url,
            params=params,
            timeout=60,
            headers=self.headers,
            cookies=self.cookies,
        )

    def search(
        self,
        page: int = 1,
        size: int = 50,
    ) -> list[str]:
        response = self._make_post_request(
            EuropeEuApiEndpoints.SEARCH,
            json={
                "resultsPerPage": size,
                "page": page,
                "sortSearch": "BEST_MATCH",
                "keywords": [],
                "publicationPeriod": "LAST_DAY",
                "occupationUris": [
                    "http://data.europa.eu/esco/isco/C9",
                ],
                "skillUris": [],
                "requiredExperienceCodes": [],
                "positionScheduleCodes": [
                    "NS",
                    "fulltime",
                ],
                "sectorCodes": [
                    "i",
                ],
                "educationAndQualificationLevelCodes": [],
                "positionOfferingCodes": [],
                "locationCodes": [
                    "at",
                ],
                "euresFlagCodes": [],
                "otherBenefitsCodes": [
                    "1",
                ],
                "requiredLanguages": [],
                "minNumberPost": None,
                "sessionId": "t8y2effv1rb0pma47adsku",
            },
        ).json()
        return [vacancy["id"] for vacancy in response["jvs"]]

    def details(self, id: str) -> list[dict[str, Any]]:
        return ApiResponseFormatter().convert_vacancy_details_response(
            self._make_get_request(
                url=EuropeEuApiEndpoints.DETAILS + "/" + id,
                params={"lang": "en"},
            ).json()
        )
