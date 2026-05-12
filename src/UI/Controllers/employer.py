from .otherOrganisationsMain import OtherOrganisationMain

class Employer(OtherOrganisationMain):
    @classmethod
    def accessible_attributes(cls) -> list:
        return ["status", "address"]

    @classmethod
    def verifiable_attributes(cls) -> list:
        return ["national_insurance"]

    @classmethod
    def organisation_name(cls) -> str:
        return "Employer"

    def generate_options(self) -> None:
        print("\nPlease select an option:")
        print("1. Verify Digital ID attribute")
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
                self.REQUESTS.verify_attribute(self.organisation_name(), self.verifiable_attributes())
            case 2:
                self.REQUESTS.verify_identity(self.organisation_name())
            case 3:
                self.REQUESTS.verify_minimum_age(self.organisation_name())
            case 4:
                self.REQUESTS.exit_program()
            case _:
                print("Invalid choice")

if __name__ == "__main__":
    program = Employer()
