from Common.singleton import SingletonMeta
from Logic.service import DigitalIDService
from Logic.suspendedChecker import SuspendedChecker
from Data.DigitalID.digitalID import DigitalID
from Config.constants import SEPARATION_WIDTH, LOG_HEADERS

class Requests(metaclass=SingletonMeta):
    """Singleton request handler for the UI layer"""

    MUTABLE_FIELDS = ["status", "firstName", "surname"]

    def __init__(self) -> None:
        self.DIGITAL_ID_SERVICE = DigitalIDService()
        self.SUSPENDED_CHECKER = SuspendedChecker()

    def create_id(self) -> None:
        data = {}
        
        for attr_name in self.DIGITAL_ID_SERVICE.get_required_attributes_for_creation():
            prompt = self.DIGITAL_ID_SERVICE.get_attribute_input_prompt(attr_name)
            data[attr_name] = input(prompt)

        data["justification"] = input("Enter justification for creation: ")

        try:
            self.DIGITAL_ID_SERVICE.create_id(data)
            print("Digital ID created successfully")
        except Exception as e:
            print(f"Error creating Digital ID: {e}")

    def view_all(self, data: str) -> None:
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

        attribute_list = self.DIGITAL_ID_SERVICE.get_all_digital_id_attributes() if data == "digitalID" else LOG_HEADERS
        
        if choice == 1:
            all_ids = self.DIGITAL_ID_SERVICE.get_all_ids() if data == "digitalID" else self.DIGITAL_ID_SERVICE.get_all_logs()
        else:
            params = {}
            params["data"] = data
            for attribute in attribute_list:
                filter_choice = input(f"Filter data by {attribute} value [Y/N]: ")
                if filter_choice.lower() == "y":
                    params[attribute] = input(f"Enter value for {attribute}: ")
            all_ids = self.DIGITAL_ID_SERVICE.get_filtered_data(params)

        if not all_ids:
            data_type_name = "Digital IDs" if data == "digitalID" else "logs"
            print(f"No {data_type_name} found")
            return

        print("=" * SEPARATION_WIDTH)
        for id in all_ids.values():
            id.print()
        print("=" * SEPARATION_WIDTH)

    def query_id(self) -> None:
        try:
            id_subject = self._get_id_subject()
            attribute_choice = self._get_attribute_subject("query")
            justification = input("Enter justification for query: ")
            
            current_value = self.DIGITAL_ID_SERVICE.query_attribute(id_subject.id, attribute_choice, justification)

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

            justification = input("Enter justification for update: ")
            self.DIGITAL_ID_SERVICE.update_id(id_subject.id, attribute_choice, new_value, justification)

            print("=" * SEPARATION_WIDTH)
            print(f"ID: {id_subject.id}, {attribute_choice}: {current_value} -> {new_value}")
            print("=" * SEPARATION_WIDTH)
        except ValueError as e:
            print(f"{e}")

    def start_program(self) -> None:
        self.DIGITAL_ID_SERVICE.load_csv_data()

    def exit_program(self) -> None:
        try:
            self.DIGITAL_ID_SERVICE.save_csv_data()
            print("Data saved successfully")
        except Exception as e:
            print(f"Warning, failed to save data: {e}")
            response = input("Continue with exit anyway? [Y/N]: ")
            if response.lower() != "y":
                return
        exit()

    def _get_id_subject(self) -> DigitalID:
        try:
            id_number = int(input("Enter Digital ID number: "))
            id_subject = self.DIGITAL_ID_SERVICE.get_id_by_number(id_number)
            return id_subject
        except (ValueError, KeyError):
            raise ValueError("Invalid ID")

    def _get_attribute_subject(self, action: str) -> str:
        fields = self.DIGITAL_ID_SERVICE.get_queryable_attributes() if action == "query" else self.DIGITAL_ID_SERVICE.get_mutable_attributes()

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

    def id_suspended_in_period(self) -> bool:
        try:
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            id_number = int(input("Enter Digital ID number: "))

            self.DIGITAL_ID_SERVICE.get_id_by_number(id_number)
            
            validated_start = self.DIGITAL_ID_SERVICE.VALIDATOR.validate_date(start_date)
            validated_end = self.DIGITAL_ID_SERVICE.VALIDATOR.validate_date(end_date)

            return self.SUSPENDED_CHECKER.id_suspended_in_period(validated_start, validated_end, id_number)
            
        except Exception as e:
            raise ValueError(f"Error checking suspension period: {str(e)}")
