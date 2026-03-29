from mainABC import MainABC

class CentralAuthorityMain(MainABC):
    """Singleton entry point for the Digital ID System used by the Central Authority"""

    def generate_options(self) -> None:
        print("\nPlease select an option:")
        print("1. Create a new Digital ID")
        print("2. Query Digital ID by ID")
        print("3. Update a Digital ID")
        print("4. View all Digital ID data")
        print("5. View all log data")
        print("6. Exit\n")

        try:
            choice = int(input())
        except ValueError:
            print("Invalid choice")
            return

        match(choice):
            case 1:
                self.REQUESTS.create_id()
            case 2:
                self.REQUESTS.query_id()
            case 3:
                self.REQUESTS.update_id()
            case 4:
                self.REQUESTS.view_all("digitalID")
            case 5:
                self.REQUESTS.view_all("log")
            case 6:
                self.REQUESTS.exit_program()
            case _:
                print("Invalid choice")

if __name__ == "__main__":
    program = CentralAuthorityMain()