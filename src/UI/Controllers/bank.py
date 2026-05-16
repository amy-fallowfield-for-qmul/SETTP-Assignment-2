from typing import List
from .otherOrganisationsMain import OtherOrganisationMain
from .mainABC import MenuOption

class Bank(OtherOrganisationMain):
    @classmethod
    def accessible_attributes(cls) -> List[str]:
        return ["status", "address"]

    @classmethod
    def permitted_operations(cls) -> List[str]:
        return ["query_attribute", "verify_identity", "verify_minimum_age"]

    @classmethod
    def organisation_name(cls) -> str:
        return "Bank"

    def menu_options(self) -> List[MenuOption]:
        return [
            ("Query Digital ID by ID", lambda: self.REQUESTS.query_id(self.organisation())),
            ("Verify Digital ID identity", lambda: self.REQUESTS.verify_identity(self.organisation())),
            ("Verify Digital ID minimum age", lambda: self.REQUESTS.verify_minimum_age(self.organisation())),
        ]
