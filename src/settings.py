import configparser


config = configparser.ConfigParser()
config.read("settings.ini")

EUROPELOCATION_CODES = ["de", "at"]
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

STOP_WORDS = config["Search"]["stop_words"].split()
TWO_CAPTCHA_API_KEY = config["TwoCaptcha"]["api_key"]
