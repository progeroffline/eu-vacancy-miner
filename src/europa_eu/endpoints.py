from enum import StrEnum


class EuropeEuApiEndpoints(StrEnum):
    DOMAIN = "https://europa.eu"
    SEARCH = f"{DOMAIN}/eures/eures-apps/searchengine/page/jv-search/search"
    DETAILS = f"{DOMAIN}/eures/eures-apps/searchengine/page/jv/id"
