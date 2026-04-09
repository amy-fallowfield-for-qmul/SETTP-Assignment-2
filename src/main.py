import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from constants import SEPARATION_WIDTH
from centralAuthorityMain import CentralAuthorityMain
from otherOrganisationsMain import OtherOrganisationMain
from hmrc import HMRC

def select_user_type():
    print("=" * SEPARATION_WIDTH)
    print("Welcome to the Digital ID System")
    print("=" * SEPARATION_WIDTH)
    
    while True:
        print("\nPlease select your organisation type:")
        print("1. Central Authority")
        print("2. HMRC")
        print("3. Exit")
        
        try:
            choice = int(input())
            match(choice):
                case 1:
                    CentralAuthorityMain()
                case 2:
                    HMRC()
                case 3:
                    exit()
                case default:
                    raise()
        except ValueError:
            print("Invalid input")

if __name__ == "__main__":
    select_user_type()