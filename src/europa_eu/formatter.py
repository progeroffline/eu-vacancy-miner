import re
from typing import Any


class ApiResponseFormatter:
    def extract_phone_numbers(self, vacancy_description: str) -> str:
        """
        Extracts phone numbers from a given text.
        """
        phone_pattern = (
            r"\b(?:\+?\d{1,3})?\s?(?:\(?\d{3,5}\)?|\d{3,5})\s?\d{3,7}\s?\d{0,5}\b"
        )
        phone_numbers = re.findall(phone_pattern, vacancy_description)
        return " ".join(re.sub(r"[^\d+]", "", number) for number in phone_numbers)

    def get_phones_string(self, contact: dict[str, Any], description: str) -> str:
        """
        Extracts or formats phone numbers from contact details.
        """
        phones = contact["communications"].get("telephoneNumbers", [])
        if phones:
            return ", ".join(f"{phone[0]} {phone[1]} {phone[2]}" for phone in phones)
        return self.extract_phone_numbers(description)

    def get_address_lines(self, addresses: list[dict[str, Any]]) -> str:
        """
        Formats address lines from a list of address dictionaries.
        """
        return ", ".join(
            line for address in addresses for line in address.get("addressLines", [])
        )

    def get_address_details(self, addresses: list[dict[str, Any]]) -> str:
        """
        Formats detailed address information.
        """
        return ", ".join(
            " ".join(
                [
                    address.get("countryCode", ""),
                    address.get("region", ""),
                    address.get("cityName", ""),
                    address.get("postalCode", ""),
                ]
            )
            for address in addresses
        )

    def get_emails(self, contact: dict[str, Any]) -> str:
        """
        Extracts email addresses from contact details.
        """
        return ", ".join(
            email["uri"] for email in contact["communications"].get("emails", [])
        )

    def get_contact_name(self, contact: dict[str, Any]) -> str:
        """
        Formats the contact name.
        """
        return f"{contact.get('givenName', '')} {contact.get('familyName', '')}".strip()

    def convert_vacancy_details_response(
        self,
        details: dict[str, Any],
    ) -> list[dict[str, str]]:
        """
        Converts vacancy details into a structured response.
        """
        profile = details["jvProfiles"][details["preferredLanguage"]]
        result = []

        for contact in profile["personContacts"]:
            addresses = contact["communications"]["addresses"]

            result.append(
                {
                    "title": profile["title"],
                    "address_lines": self.get_address_lines(addresses),
                    "address_details": self.get_address_details(addresses),
                    "phone_numbers": self.get_phones_string(
                        contact, profile["description"]
                    ),
                    "emails": self.get_emails(contact),
                    "details_url": f"https://europa.eu/eures/portal/jv-se/jv-details/{details.get('id', '')}",
                    "contact_name": self.get_contact_name(contact),
                }
            )

        return result
