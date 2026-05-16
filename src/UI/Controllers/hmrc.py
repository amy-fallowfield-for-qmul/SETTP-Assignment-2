from typing import List
from .otherOrganisationsMain import OtherOrganisationMain
from .mainABC import MenuOption

class HMRC(OtherOrganisationMain):
    @classmethod
    def accessible_attributes(cls) -> List[str]:
        return ["address"]

    @classmethod
    def verifiable_attributes(cls) -> List[str]:
        return ["national_insurance"]

    @classmethod
    def permitted_operations(cls) -> List[str]:
        return ["query_attribute", "verify_attribute", "verify_suspended_in_period"]

    @classmethod
    def organisation_name(cls) -> str:
        return "HMRC"

    def menu_options(self) -> List[MenuOption]:
        return [
            ("Query Digital ID by ID", lambda: self.REQUESTS.query_id(self.organisation())),
            ("Verify Digital ID attribute", lambda: self.REQUESTS.verify_attribute(self.organisation())),
            ("Verify Digital ID suspended in given period", lambda: self.REQUESTS.verify_suspended_in_period(self.organisation())),
        ]
