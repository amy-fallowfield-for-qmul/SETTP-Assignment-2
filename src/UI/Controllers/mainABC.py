from Common.singleton import SingletonABCMeta
from UI.requests import Requests
from Logic.organisation import Organisation
from abc import abstractmethod
from typing import List, Tuple, Callable

MenuOption = Tuple[str, Callable[[], None]]

class MainABC(metaclass=SingletonABCMeta):

    def __init__(self) -> None:
        self.REQUESTS = Requests()

    def run(self) -> None:
        self.start_program()
        self.main()

    def main(self) -> None:
        while True:
            self.generate_options()

    def start_program(self) -> None:
        self.REQUESTS.start_program()

    def generate_options(self) -> None:
        options = self.menu_options() + [("Exit", self.REQUESTS.exit_program)]

        print(f"\n--- {self.organisation_name()} ---")
        print("Please select an option:")
        for index, (label, _) in enumerate(options, start=1):
            print(f"{index}. {label}")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid choice")
            return

        if choice < 1 or choice > len(options):
            print("Invalid choice")
            return

        options[choice - 1][1]()

    @classmethod
    @abstractmethod
    def organisation_name(cls) -> str: pass

    @classmethod
    @abstractmethod
    def accessible_attributes(cls) -> List[str]: pass

    @classmethod
    def verifiable_attributes(cls) -> List[str]:
        return []

    @classmethod
    def permitted_operations(cls) -> List[str]:
        return []

    @classmethod
    def organisation(cls) -> Organisation:
        return Organisation(
            name=cls.organisation_name(),
            accessible_attributes=tuple(cls.accessible_attributes()),
            verifiable_attributes=tuple(cls.verifiable_attributes()),
            permitted_operations=tuple(cls.permitted_operations()),
        )

    @abstractmethod
    def menu_options(self) -> List[MenuOption]: pass
