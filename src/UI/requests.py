from typing import List, Optional, Sequence
from Common.singleton import SingletonMeta
from Logic.service import DigitalIDService
from Logic.verifier import Verifier
from Logic.organisation import Organisation
from Logic.requestContext import RequestContext
from Logic.identityClaim import IdentityClaim
from Logic.period import Period
from Data.DigitalID.digitalID import DigitalID
from Config.constants import SEPARATION_WIDTH, LOG_HEADERS

class Requests(metaclass=SingletonMeta):
    """Singleton request handler for the UI layer"""

    def __init__(self) -> None:
        self.DIGITAL_ID_SERVICE = DigitalIDService()
        self.VERIFIER = Verifier()

    def create_id(self, organisation: Organisation) -> None:
        data = {}
        
        for attr_name in self.DIGITAL_ID_SERVICE.get_required_attributes_for_creation():
            prompt = self.DIGITAL_ID_SERVICE.get_attribute_input_prompt(attr_name)
            data[attr_name] = input(prompt)

        data["justification"] = input("Enter justification for creation: ")

        try:
            context = RequestContext(organisation=organisation, justification=data["justification"])
            self.DIGITAL_ID_SERVICE.create_id(data, context)
            print("Digital ID created successfully")
        except Exception as e:
            print(f"Error creating Digital ID: {e}")

    def view_all_ids(self) -> None:
        try:
            choice, filters = self._get_filter_choice(self.DIGITAL_ID_SERVICE.get_all_digital_id_attributes())
        except ValueError:
            print("Invalid choice")
            return

        if choice == 1:
            all_data = self.DIGITAL_ID_SERVICE.get_all_ids()
        else:
            all_data = self.DIGITAL_ID_SERVICE.get_filtered_ids(filters)

        self._print_results(all_data, "Digital IDs")

    def view_all_logs(self) -> None:
        try:
            choice, filters = self._get_filter_choice(LOG_HEADERS)
        except ValueError:
            print("Invalid choice")
            return

        if choice == 1:
            all_data = self.DIGITAL_ID_SERVICE.get_all_logs()
        else:
            all_data = self.DIGITAL_ID_SERVICE.get_filtered_logs(filters)

        self._print_results(all_data, "logs")

    def _get_filter_choice(self, attribute_list):
        print("\nPlease select an option:")
        print("1. View all data")
        print("2. Filter data")

        choice = int(input())
        if choice != 1 and choice != 2:
            raise ValueError

        filters = {}
        if choice == 2:
            for attribute in attribute_list:
                filter_choice = input(f"Filter data by {attribute} value [Y/N]: ")
                if filter_choice.lower() == "y":
                    filters[attribute] = input(f"Enter value for {attribute}: ")

        return choice, filters

    def _print_results(self, all_data, empty_label: str) -> None:
        if not all_data:
            print(f"No {empty_label} found")
            return

        print("=" * SEPARATION_WIDTH)
        for item in all_data.values():
            item.print()
        print("=" * SEPARATION_WIDTH)

    def query_id(self, organisation: Organisation) -> None:
        try:
            id_subject = self._get_id_subject()
            attribute_choice = self._get_attribute_subject("query", organisation.accessible_attributes)
            justification = input("Enter justification for query: ")
            context = RequestContext(organisation=organisation, justification=justification)
            
            current_value = self.DIGITAL_ID_SERVICE.query_attribute(
                id_subject.id, attribute_choice, context
            )

            print("=" * SEPARATION_WIDTH)
            print(f"ID: {id_subject.id}, {attribute_choice}: {current_value}")
            print("=" * SEPARATION_WIDTH)
        except ValueError as e:
            print(f"{e}")

    def verify_identity(self, organisation: Organisation) -> None:
        try:
            id_number = int(input("Enter Digital ID number: "))
            first_name = input("Enter first name: ")
            surname = input("Enter surname: ")
            date_of_birth = input("Enter date of birth (YYYY-MM-DD): ")
            justification = input("Enter justification for verification: ")
            claim = IdentityClaim(first_name=first_name, surname=surname, date_of_birth=date_of_birth)
            context = RequestContext(organisation=organisation, justification=justification)

            result = self.VERIFIER.verify_identity(id_number, claim, context)

            print("=" * SEPARATION_WIDTH)
            if result:
                print(f"Result: Identity verified for Digital ID {id_number}")
            else:
                print(f"Result: Identity NOT verified for Digital ID {id_number}")
            print("=" * SEPARATION_WIDTH)
        except ValueError as e:
            print(f"Request rejected: {e}")

    def verify_minimum_age(self, organisation: Organisation) -> None:
        try:
            id_number = int(input("Enter Digital ID number: "))
            minimum_age = input("Enter minimum age: ")
            justification = input("Enter justification for verification: ")
            context = RequestContext(organisation=organisation, justification=justification)

            result = self.VERIFIER.verify_minimum_age(
                id_number, minimum_age, context
            )

            print("=" * SEPARATION_WIDTH)
            if result:
                print(f"Result: Digital ID {id_number} meets the minimum age of {minimum_age}")
            else:
                print(f"Result: Digital ID {id_number} does NOT meet the minimum age of {minimum_age}")
            print("=" * SEPARATION_WIDTH)
        except ValueError as e:
            print(f"Request rejected: {e}")

    def verify_attribute(self, organisation: Organisation) -> None:
        try:
            id_number = int(input("Enter Digital ID number: "))
            attribute_choice = self._get_attribute_subject("verify", organisation.verifiable_attributes)
            claimed_value = input(f"Enter claimed {attribute_choice}: ")
            justification = input("Enter justification for verification: ")
            context = RequestContext(organisation=organisation, justification=justification)

            result = self.VERIFIER.verify_attribute(
                id_number, attribute_choice, claimed_value, context
            )

            print("=" * SEPARATION_WIDTH)
            if result:
                print(f"Result: {attribute_choice} matches for Digital ID {id_number}")
            else:
                print(f"Result: {attribute_choice} does NOT match for Digital ID {id_number}")
            print("=" * SEPARATION_WIDTH)
        except ValueError as e:
            print(f"Request rejected: {e}")

    def update_id(self, organisation: Organisation) -> None:
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
            context = RequestContext(organisation=organisation, justification=justification)
            self.DIGITAL_ID_SERVICE.update_id(id_subject.id, attribute_choice, new_value, context)

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

    def _get_attribute_subject(self, action: str, accessible_attributes: Optional[Sequence[str]] = None) -> str:
        if accessible_attributes is not None:
            fields = accessible_attributes
        elif action == "query":
            fields = self.DIGITAL_ID_SERVICE.get_queryable_attributes()
        else:
            fields = self.DIGITAL_ID_SERVICE.get_mutable_attributes()

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

    def verify_suspended_in_period(self, organisation: Organisation) -> None:
        try:
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            id_number = int(input("Enter Digital ID number: "))
            justification = input("Enter justification for verification: ")

            validated_start = self.DIGITAL_ID_SERVICE.VALIDATOR.validate_date(start_date)
            validated_end = self.DIGITAL_ID_SERVICE.VALIDATOR.validate_date(end_date)
            validated_justification = self.DIGITAL_ID_SERVICE.VALIDATOR.validate_attribute("justification", justification)
            period = Period(validated_start,validated_end)

            result = self.VERIFIER.verify_suspended_in_period(period, id_number, RequestContext(organisation=organisation, justification=validated_justification))

            print("=" * SEPARATION_WIDTH)
            if result:
                print(f"Result: Digital ID {id_number} was suspended during specified period")
            else:
                print(f"Result: Digital ID {id_number} was NOT suspended during specified period")
            print("=" * SEPARATION_WIDTH)
        except ValueError as e:
            print(f"Request rejected: {e}")
