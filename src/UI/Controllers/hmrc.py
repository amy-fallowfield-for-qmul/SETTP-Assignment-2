from .otherOrganisationsMain import OtherOrganisationMain

class HMRC(OtherOrganisationMain):
    @classmethod
    def accessible_attributes(cls) -> list:
        return ["address"]

    @classmethod
    def verifiable_attributes(cls) -> list:
        return ["national_insurance"]

    @classmethod
    def organisation_name(cls) -> str:
        return "HMRC"

    def generate_options(self) -> None:
        print("\nPlease select an option:")
        print("1. Query Digital ID by ID")
        print("2. Verify Digital ID attribute")
        print("3. Verify Digital ID suspended in given period")
        print("4. Exit\n")

        try:
            choice = int(input())
        except ValueError:
            print("Invalid choice")
            return

        match(choice):
            case 1:
                self.REQUESTS.query_id(self.organisation_name(), self.accessible_attributes())
            case 2:
                self.REQUESTS.verify_attribute(self.organisation_name(), self.verifiable_attributes())
            case 3:
                self.REQUESTS.verify_suspended_in_period(self.organisation_name())
            case 4:
                self.REQUESTS.exit_program()
            case _:
                print("Invalid choice")

if __name__ == "__main__":
    program = HMRC()
