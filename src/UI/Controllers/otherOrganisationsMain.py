from typing import List
from .mainABC import MainABC, MenuOption

class OtherOrganisationMain(MainABC):
    """Abstract base class for specific other organisations"""

    def menu_options(self) -> List[MenuOption]:
        return [
            ("Query Digital ID by ID", lambda: self.REQUESTS.query_id(self.organisation())),
        ]
