import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from constants import SEPARATION_WIDTH
from centralAuthorityMain import CentralAuthorityMain
from otherOrganisationsMain import OtherOrganisationMain

def select_user_type():
    print("=" * SEPARATION_WIDTH)
    print("Welcome to the Digital ID System")
    print("=" * SEPARATION_WIDTH)
    
    while True:
        print("\nPlease select your organization type:")
        print("1. Central Authority")
        print("2. Other Organisation")
        print("3. Exit")
        
        try:
            choice = int(input())
            if choice == 1:
                CentralAuthorityMain()
            elif choice == 2:
                OtherOrganisationMain()
            elif choice == 3:
                exit()
            else:
                raise()
        except ValueError:
            print("Invalid input")

if __name__ == "__main__":
    select_user_type()