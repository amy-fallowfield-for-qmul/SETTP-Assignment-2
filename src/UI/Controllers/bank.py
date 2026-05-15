from .otherOrganisationsMain import OtherOrganisationMain

class Bank(OtherOrganisationMain):
    @classmethod
    def accessible_attributes(cls) -> list:
        return ["status", "address"]

    @classmethod
    def organisation_name(cls) -> str:
        return "Bank"

    def generate_options(self) -> None:
        print("\nPlease select an option:")
        print("1. Query Digital ID by ID")
        print("2. Verify Digital ID identity")
        print("3. Verify Digital ID minimum age")
        print("4. Exit\n")

        try:
            choice = int(input())
        except ValueError:
            print("Invalid choice")
            return

        match(choice):
            case 1:
                self.REQUESTS.query_id(self.organisation())
            case 2:
                self.REQUESTS.verify_identity(self.organisation())
            case 3:
                self.REQUESTS.verify_minimum_age(self.organisation())
            case 4:
                self.REQUESTS.exit_program()
            case _:
                print("Invalid choice")

if __name__ == "__main__":
    program = Bank()
