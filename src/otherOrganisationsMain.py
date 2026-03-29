from mainABC import MainABC

class OtherOrganisationMain(MainABC):
    """Singleton entry point for the Digital ID System used by other organisations"""

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
                self.REQUESTS.query_id()
            case 2:
                self.REQUESTS.exit_program()
            case _:
                print("Invalid choice")

if __name__ == "__main__":
    program = OtherOrganisationMain()