import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from Config.constants import SEPARATION_WIDTH
from UI.requests import Requests
from UI.Controllers.centralAuthorityMain import CentralAuthorityMain
from UI.Controllers.hmrc import HMRC
from UI.Controllers.employer import Employer
from UI.Controllers.bank import Bank

USER_OPTIONS = [
    CentralAuthorityMain,
    HMRC,
    Employer,
    Bank
]

def select_user_type() -> None:
    print("=" * SEPARATION_WIDTH)
    print("Welcome to the Digital ID System")
    print("=" * SEPARATION_WIDTH)

    exit_option = len(USER_OPTIONS) + 1

    while True:
        print("\nPlease select your organisation type:")
        for number, cls in enumerate(USER_OPTIONS, start=1):
            print(f"{number}. {cls.organisation_name()}")
        print(f"{exit_option}. Exit")

        try:
            choice = int(input("Enter your choice: "))

            if choice == exit_option:
                Requests().exit_program()

            if choice < 1 or choice > len(USER_OPTIONS):
                raise ValueError

            controller_class = USER_OPTIONS[choice - 1]
            controller_class().run()  # type: ignore[abstract]

        except ValueError:
            print("Invalid input")

if __name__ == "__main__":
    try:
        select_user_type()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram interrupted. Saving data before exit")
        Requests().exit_program()
