import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from UI.requests import Requests
from constants import SEPARATION_WIDTH
from enum import Enum
from abc import ABC, abstractmethod

class Users(Enum):
    CENTRAL_AUTHORITY = 1
    HMRC = 2

class MainABC(ABC):

    _instance = None

    def __new__(cls) -> "MainABC":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, '_initialised'):
            self._initialised = True
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