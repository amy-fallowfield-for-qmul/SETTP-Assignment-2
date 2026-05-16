from typing import List
from .otherOrganisationsMain import OtherOrganisationMain
from .mainABC import MenuOption

class Employer(OtherOrganisationMain):
    @classmethod
    def accessible_attributes(cls) -> List[str]:
        return ["status", "address"]

    @classmethod
    def verifiable_attributes(cls) -> List[str]:
        return ["national_insurance"]

    @classmethod
    def permitted_operations(cls) -> List[str]:
        return ["verify_identity", "verify_minimum_age", "verify_attribute"]

    @classmethod
    def organisation_name(cls) -> str:
        return "Employer"

    def menu_options(self) -> List[MenuOption]:
        return [
            ("Verify Digital ID attribute", lambda: self.REQUESTS.verify_attribute(self.organisation())),
            ("Verify Digital ID identity", lambda: self.REQUESTS.verify_identity(self.organisation())),
            ("Verify Digital ID minimum age", lambda: self.REQUESTS.verify_minimum_age(self.organisation())),
        ]
