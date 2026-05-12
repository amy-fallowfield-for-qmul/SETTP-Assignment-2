import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from Common.singleton import SingletonABCMeta
from UI.requests import Requests
from Config.constants import SEPARATION_WIDTH
from abc import abstractmethod
from typing import List

class MainABC(metaclass=SingletonABCMeta):

    def __init__(self) -> None:
        self.REQUESTS = Requests()
        self.start_program()
        self.main()

    def main(self) -> None:
        while True:
            self.generate_options()

    def start_program(self) -> None:
        print("=" * SEPARATION_WIDTH)
        print("Welcome to the Digital ID System")
        print("=" * SEPARATION_WIDTH)
        
        self.REQUESTS.start_program()

    @classmethod
    @abstractmethod
    def organisation_name(cls) -> str: pass

    @classmethod
    @abstractmethod
    def accessible_attributes(cls) -> List[str]: pass

    @classmethod
    def verifiable_attributes(cls) -> List[str]:
        return cls.accessible_attributes()

    @abstractmethod
    def generate_options(self) -> None: pass

    def _query_suspended_in_period(self) -> None:
        try:
            result = self.REQUESTS.id_suspended_in_period()
            
            if result:
                print("Result: Digital ID was suspended during specified period")
            else:
                print("Result: Digital ID was NOT suspended during specified period")
                
        except ValueError as e:
            print(f"Error checking suspension history: {e}")