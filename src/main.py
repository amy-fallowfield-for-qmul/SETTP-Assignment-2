import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from Config.constants import SEPARATION_WIDTH
from UI.Controllers.centralAuthorityMain import CentralAuthorityMain
from UI.Controllers.otherOrganisationsMain import OtherOrganisationMain
from UI.Controllers.hmrc import HMRC
from UI.Controllers.employer import Employer
from UI.Controllers.bank import Bank

def select_user_type():
    print("=" * SEPARATION_WIDTH)
    print("Welcome to the Digital ID System")
    print("=" * SEPARATION_WIDTH)
    
    while True:
        print("\nPlease select your organisation type:")
        print("1. Central Authority")
        print("2. HMRC")
        print("3. Employer")
        print("4. Bank")
        print("5. Exit")
        
        try:
            choice = int(input())
            match(choice):
                case 1:
                    CentralAuthorityMain()
                case 2:
                    HMRC()
                case 3:
                    Employer()
                case 4:
                    Bank()
                case 5:
                    exit()
                case default:
                    raise()
        except ValueError:
            print("Invalid input")

if __name__ == "__main__":
    select_user_type()