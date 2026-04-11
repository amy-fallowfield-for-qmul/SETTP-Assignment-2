from abc import abstractmethod
from typing import List
from .mainABC import MainABC
from Config.constants import SEPARATION_WIDTH

class OtherOrganisationMain(MainABC):
    """Abstract base class for specific other organisations"""

    @property
    @abstractmethod
    def allowed_attributes(self) -> List[str]: pass

    @property
    @abstractmethod
    def organisation_name(self) -> str: pass

    def generate_options(self) -> None:
        print("\nPlease select an option:")
        print("1. Query Digital ID by ID")
        print("2. Exit\n")

        try:
            choice = int(input())
        except ValueError:
            print("Invalid choice")
            return

        match(choice):
            case 1:
                self._query_permissions()
            case 2:
                self.REQUESTS.exit_program()
            case _:
                print("Invalid choice")

    def _query_permissions(self) -> None:
        try:
            id_subject = self.REQUESTS._get_id_subject()
            attribute_choice = self._get_attribute_choice()
            justification = input("Enter justification for query: ")
            
            current_value = self.REQUESTS.DIGITAL_ID_SERVICE.query_attribute(
                id_subject.id, attribute_choice, justification, self.organisation_name, self.allowed_attributes
            )

            print("=" * SEPARATION_WIDTH)
            print(f"ID: {id_subject.id}, {attribute_choice}: {current_value}")
            print("=" * SEPARATION_WIDTH)
        except ValueError as e:
            print(f"Error querying allowed attribtues: {e}")

    def _get_attribute_choice(self) -> str:
        try:
            print(f"Please select the attribute you wish to query:")
            for i, field in enumerate(self.allowed_attributes, start=1):
                print(f"{i}. {field}")

            user_choice = int(input())
            if user_choice < 1 or user_choice > len(self.allowed_attributes):
                raise

            attribute_choice = self.allowed_attributes[user_choice - 1]
            return attribute_choice

        except:
            raise ValueError("Invalid input")
