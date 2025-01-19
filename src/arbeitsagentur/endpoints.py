from enum import StrEnum


class ArbeitsagenturApiEndpoints(StrEnum):
    SEARCH = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v5/jobs"
    DETAILS = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v3/jobs/{id}/bewerbung"
    CHALLENGE = "https://rest.arbeitsagentur.de/idaas/id-aas-service/pc/v1/assignment"
    CAPTCHA = "https://rest.arbeitsagentur.de/idaas/id-aas-service/ct/v1/captcha/{challenge_id}"
    FULL_INFO = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobdetails/{id}"
