from otherOrganisationsMain import OtherOrganisationMain

class HMRC(OtherOrganisationMain):
    @property
    def allowed_attributes(self) -> list:
        return ["status", "address", "national_insurance"]

    @property
    def organisation_name(self) -> str:
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
                self._query_permissions()
            case 2:
                self._query_suspended_in_period()
            case 3:
                self.REQUESTS.exit_program()
            case _:
                print("Invalid choice")

    def _query_suspended_in_period(self) -> None:
        try:
            result = self.REQUESTS.id_suspended_in_period()
            
            if result:
                print("Result: Digital ID was suspended during specified period")
            else:
                print("Result: Digital ID was NOT suspended during specified period")
                
        except ValueError as e:
            print(f"Error checking suspension history: {e}")

if __name__ == "__main__":
    program = HMRC()
