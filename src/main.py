import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from UI.requests import Requests
from constants import SEPARATION_WIDTH

class Program:
    """Singleton entry point for the Digital ID System"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, '_initialised'):
            self._initialised = True
            self.REQUESTS = Requests()
            self.start_program()
            self.main()

    def main(self):
        while True:
            self.generate_options()

    def start_program(self):
        print("=" * SEPARATION_WIDTH)
        print("Welcome to the Digital ID System")
        print("=" * SEPARATION_WIDTH)
        
        self.REQUESTS.start_program()

    def generate_options(self) -> None:
        print("\nPlease select an option:")
        print("1. Create a new Digital ID")
        print("2. Query Digital ID by ID")
        print("3. Update a Digital ID")
        print("===== Central Authority Only =====")
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
    program = Program()