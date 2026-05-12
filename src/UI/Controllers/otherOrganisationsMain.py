from .mainABC import MainABC

class OtherOrganisationMain(MainABC):
    """Abstract base class for specific other organisations"""

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
                self.REQUESTS.query_id(self.organisation_name(), self.allowed_attributes())
            case 2:
                self.REQUESTS.exit_program()
            case _:
                print("Invalid choice")
