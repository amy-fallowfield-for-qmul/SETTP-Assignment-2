from Logic.service import DigitalIDService
from Data.digitalID import DigitalID
from constants import SEPARATION_WIDTH

class Requests:
    """Singleton request handler for the UI layer"""

    DIGITAL_ID_FIELDS = ["id", "status", "firstName", "surname", "dateOfBirth"]
    MUTABLE_FIELDS = ["status", "firstName", "surname"]
    SEPARATION_WIDTH = 100
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, '_initialised'):
            self._initialised = True
            self.DIGITAL_ID_SERVICE = DigitalIDService()

    def create_id(self) -> None:
        first_name = input("Enter first name: ")
        surname = input("Enter surname: ")
        date_of_birth = input("Enter date of birth (YYYY-MM-DD): ")
        justification = input("Enter justification for creation: ")

        data = {
            "firstName": first_name,
            "surname": surname,
            "dateOfBirth": date_of_birth,
            "justification": justification
        }

        try:
            self.DIGITAL_ID_SERVICE.create_id(data)
            print("Digital ID created successfully")
        except Exception as e:
            print(f"Error creating Digital ID: {e}")

    def view_all_ids(self) -> None:
        print("\nPlease select an option:")
        print("1. View all data")
        print("2. Filter data")

        try:
            choice = int(input())
            if choice != 1 and choice != 2:
                raise ValueError
        except ValueError:
            print("Invalid choice")
            return
        
        if choice == 1:
            all_ids = self.DIGITAL_ID_SERVICE.get_all()
        else:
            params = {}
            for attribute in self.DIGITAL_ID_FIELDS:
                filter_choice = input(f"Filter data by {attribute} value [Y/N]: ")
                if filter_choice.lower() == "y":
                    params[attribute] = input(f"Enter value for {attribute}: ")
            all_ids = self.DIGITAL_ID_SERVICE.get_filtered_ids(params)

        if not all_ids:
            print("No Digital IDs found")
            return

        print("=" * SEPARATION_WIDTH)
        for id in all_ids.values():
            id.print()
        print("=" * SEPARATION_WIDTH)

    def query_id(self) -> None:
        try:
            id_subject = self._get_id_subject()
            attribute_choice = self._get_attribute_subject("query")
            current_value = id_subject.to_dict()[attribute_choice]

            print("=" * SEPARATION_WIDTH)
            print(f"ID: {id_subject.id}, {attribute_choice}: {current_value}")
            print("=" * SEPARATION_WIDTH)
        except ValueError as e:
            print(f"{e}")

    def update_id(self) -> None:
        try:
            id_subject = self._get_id_subject()
            attribute_choice = self._get_attribute_subject("update")
            current_value = id_subject.to_dict()[attribute_choice]

            print(f"Current value: {current_value}")
            new_value = input("Enter new value: ")
            if new_value == "":
                print("No value entered")
                return

            self.DIGITAL_ID_SERVICE.update_id(id_subject.id, attribute_choice, new_value)

            print("=" * SEPARATION_WIDTH)
            print(f"ID: {id_subject.id}, {attribute_choice}: {current_value} -> {new_value}")
            print("=" * SEPARATION_WIDTH)
        except ValueError as e:
            print(f"{e}")

    def start_program(self) -> None:
        self.DIGITAL_ID_SERVICE.load_csv_data()

    def exit_program(self) -> None:
        self.DIGITAL_ID_SERVICE.save_csv_data()
        exit()

    def _get_id_subject(self) -> DigitalID:
        try:
            id_number = int(input("Enter Digital ID number: "))
            id_subject = self.DIGITAL_ID_SERVICE.get_id_by_number(id_number)
            return id_subject
        except (ValueError, KeyError):
            raise ValueError("Invalid ID")

    def _get_attribute_subject(self, action: str) -> str:
        fields = self.DIGITAL_ID_FIELDS[1:] if action == "query" else self.MUTABLE_FIELDS

        try:
            print(f"Please select the attribute you wish to {action}:")
            for i, field in enumerate(fields, start=1):
                print(f"{i}. {field}")

            user_choice = int(input())
            if user_choice < 1 or user_choice > len(fields):
                raise IndexError

            attribute_choice = fields[user_choice - 1]
            return attribute_choice

        except (ValueError, IndexError):
            raise ValueError("Invalid input")
