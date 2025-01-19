from typing import Any
import base64
import httpx
import uuid

from .dtypes import SearchResponse, VacancyDetails, VacancySearchResponse
from .endpoints import ArbeitsagenturApiEndpoints
from .captcha import resolve_simple_captcha


class ArbeitsagenturApi:
    def __init__(self, two_captcha_api_key: str, cookies: dict[str, str] = {}):
        self.two_captcha_api_key = two_captcha_api_key
        self.captcha_image_filename = "captcha.png"
        self.cookies = cookies
        self.session_id = "C0D6FDDA-355B-457F-99CF-5FB303B9CC2D"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "ru",
            "correlation-id": "217639f3-ac86-1e6c-1fdb-2ae4b58134c1",
            "X-API-Key": "jobboerse-jobsuche",
            "Origin": "https://www.arbeitsagentur.de",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Priority": "u=0",
        }

    def encode_string_to_base64(self, string: str) -> str:
        return base64.b64encode(string.encode("utf-8")).decode("utf-8")

    def _make_get_request(
        self,
        url: str,
        params: dict[str, Any] = {},
        headers: dict[str, str] = {},
    ) -> httpx.Response:
        response = httpx.get(
            url=url,
            params=params,
            headers=headers if len(headers) > 0 else self.headers,
            cookies=self.cookies,
        )
        return response

    def _make_post_request(self, url: str, data: dict[str, Any]) -> httpx.Response:
        return httpx.post(
            url=url,
            json=data,
            headers=self.headers,
            cookies=self.cookies,
        )

    def search(
        self,
        page: int = 0,
        size: int = 25,
        params: dict[str, int | bool | str] = {},
    ) -> SearchResponse:
        params["page"] = page
        params["size"] = size

        response = self._make_get_request(
            ArbeitsagenturApiEndpoints.SEARCH,
            params=params,
        ).json()
        return SearchResponse(
            total=response["maxErgebnisse"],
            page=response["page"],
            size=response["size"],
            result=[
                VacancySearchResponse(
                    id=vacancy["refnr"],
                    title=vacancy.get("titel", vacancy["beruf"]),
                )
                for vacancy in response["stellenangebote"]
            ]
            if response.get("stellenangebote") is not None
            else [],
        )

    def save_captcha_image(self, challenge_id: str) -> str:
        response = self._make_get_request(
            url=ArbeitsagenturApiEndpoints.CAPTCHA.format(challenge_id=challenge_id),
            params={"type": "image", "languageIso639Code": "de"},
        )

        with open(self.captcha_image_filename, "wb") as f:
            f.write(response.content)

        return "captcha.png"

    def get_challenge_uuid(self) -> tuple[str, str | None]:
        response = self._make_post_request(
            url=ArbeitsagenturApiEndpoints.CHALLENGE,
            data={
                "formId": "ARBEITGEBERDATEN",
                "formProtectionLevel": "JB_JOBSUCHE_20",
                "sessionId": self.session_id,
            },
        ).json()
        self.session_id = response["sessionId"]

        if response["challengeType"] == "captcha":
            self.save_captcha_image(response["challengeId"])
            captcha_answer = resolve_simple_captcha(
                self.captcha_image_filename,
                self.two_captcha_api_key,
            )
            return response["challengeId"], captcha_answer
        return response["challengeId"], None

    def details(self, id: str) -> VacancyDetails:
        headers = self.headers.copy()

        challenge_id, captcha_answer = self.get_challenge_uuid()
        headers["aas-info"] = f"sessionId={self.session_id},,challengeId={challenge_id}"
        headers["correlation-id"] = str(uuid.uuid4())

        if captcha_answer:
            headers["aas-answer"] = captcha_answer

        response = self._make_get_request(
            headers=headers,
            url=ArbeitsagenturApiEndpoints.DETAILS.format(
                id=self.encode_string_to_base64(id)
            ),
        ).json()

        if response.get("angebotskontakt") is None:
            return self.details(id)

        contact = response["angebotskontakt"]
        return VacancyDetails(
            title="",
            company=contact["firma"],
            address=" ".join(contact["postadresse"].values()),
            phone_number="".join(contact["telefonnummer"].values())
            if contact.get("telefonnummer") is not None
            else "",
            email=contact["emailadresse"],
            url=f"https://www.arbeitsagentur.de/jobsuche/jobdetail/{id}",
        )

    def full_info(self, id: str) -> dict[str, Any]:
        return self._make_get_request(
            url=ArbeitsagenturApiEndpoints.FULL_INFO.format(
                id=self.encode_string_to_base64(id)
            ),
        ).json()
