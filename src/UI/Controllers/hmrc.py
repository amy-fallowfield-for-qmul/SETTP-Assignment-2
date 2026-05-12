from .otherOrganisationsMain import OtherOrganisationMain

class HMRC(OtherOrganisationMain):
    @classmethod
    def accessible_attributes(cls) -> list:
        return ["status", "address", "national_insurance"]

    @classmethod
    def organisation_name(cls) -> str:
        return "HMRC"
    
    def generate_options(self) -> None:
        print("\nPlease select an option:")
        print("1. Query Digital ID by ID")
        print("2. Query Digital ID suspended in given period")
        print("3. Exit\n")

        try:
            choice = int(input())
        except ValueError:
            print("Invalid choice")
            return

        match(choice):
            case 1:
                self.REQUESTS.query_id(self.organisation_name(), self.accessible_attributes())
            case 2:
                self._query_suspended_in_period()
            case 3:
                self.REQUESTS.exit_program()
            case _:
                print("Invalid choice")

if __name__ == "__main__":
    program = HMRC()
