from .mainABC import MainABC
from Data.Attributes.attributeRegistry import AttributeRegistry

class CentralAuthorityMain(MainABC):
    """Singleton entry point for the Digital ID System used by the Central Authority"""

    @classmethod
    def organisation_name(cls) -> str:
        return "Central Authority"

    @classmethod
    def accessible_attributes(cls) -> list:
        return AttributeRegistry().get_queryable_attributes()

    @classmethod
    def permitted_operations(cls) -> list:
        return [
            "create_id",
            "query_attribute",
            "update_id",
            "verify_identity",
            "verify_minimum_age",
            "verify_attribute",
            "verify_suspended_in_period",
        ]

    def generate_options(self) -> None:
        print("\nPlease select an option:")
        print("1. Create a new Digital ID")
        print("2. Query Digital ID by ID")
        print("3. Update a Digital ID")
        print("4. Verify Digital ID suspended in given period")
        print("5. View all Digital ID data")
        print("6. View all log data")
        print("7. Exit\n")

        try:
            choice = int(input())
        except ValueError:
            print("Invalid choice")
            return

        match(choice):
            case 1:
                self.REQUESTS.create_id(self.organisation())
            case 2:
                self.REQUESTS.query_id(self.organisation())
            case 3:
                self.REQUESTS.update_id(self.organisation())
            case 4:
                self.REQUESTS.verify_suspended_in_period(self.organisation())
            case 5:
                self.REQUESTS.view_all_ids()
            case 6:
                self.REQUESTS.view_all_logs()
            case 7:
                self.REQUESTS.exit_program()
            case _:
                print("Invalid choice")

if __name__ == "__main__":
    program = CentralAuthorityMain()