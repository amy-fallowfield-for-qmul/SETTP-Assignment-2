import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from Config.constants import SEPARATION_WIDTH
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

def select_user_type():
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
            choice = int(input())

            if choice == exit_option:
                exit()

            if choice < 1 or choice > len(USER_OPTIONS):
                raise ValueError

            controller_class = USER_OPTIONS[choice - 1]
            controller_class().run()

        except ValueError:
            print("Invalid input")

if __name__ == "__main__":
    select_user_type()
