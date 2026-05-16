from typing import List
from .mainABC import MainABC, MenuOption
from Data.Attributes.attributeRegistry import AttributeRegistry

class CentralAuthorityMain(MainABC):
    """Singleton entry point for the Digital ID System used by the Central Authority"""

    @classmethod
    def organisation_name(cls) -> str:
        return "Central Authority"

    @classmethod
    def accessible_attributes(cls) -> List[str]:
        return AttributeRegistry().get_queryable_attributes()

    @classmethod
    def permitted_operations(cls) -> List[str]:
        return [
            "create_id",
            "query_attribute",
            "update_id",
            "verify_identity",
            "verify_minimum_age",
            "verify_attribute",
            "verify_suspended_in_period",
        ]

    def menu_options(self) -> List[MenuOption]:
        return [
            ("Create a new Digital ID", lambda: self.REQUESTS.create_id(self.organisation())),
            ("Query Digital ID by ID", lambda: self.REQUESTS.query_id(self.organisation())),
            ("Update a Digital ID", lambda: self.REQUESTS.update_id(self.organisation())),
            ("Verify Digital ID suspended in given period", lambda: self.REQUESTS.verify_suspended_in_period(self.organisation())),
            ("View all Digital ID data", self.REQUESTS.view_all_ids),
            ("View all log data", self.REQUESTS.view_all_logs),
        ]
