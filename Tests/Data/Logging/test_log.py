import pytest
from datetime import datetime
from Data.Logging.log import Log, Action
from Data.DigitalID.digitalID import DigitalID
from Tests.shared_test_data import new_person_dict

class TestAction:
    """Tests for the Action enum"""

    def test_action_values(self) -> None:
        assert Action.CREATE.value == "create"
        assert Action.READ.value == "read"
        assert Action.UPDATE.value == "update"
        assert Action.VERIFY.value == "verify"

    def test_action_members(self) -> None:
        assert set(Action.__members__.keys()) == {"CREATE", "READ", "UPDATE", "VERIFY"}

class TestLogModel:
    """Tests for Log data model"""

    def setup_method(self) -> None:
        DigitalID._next_id = 1
        Log._next_id = 1
        self.start_time = datetime.now()

    def test_create_log_for_create(self) -> None:
        digital_id = DigitalID(new_person_dict)
        log = Log.for_create("NHS", 1, "New registration", digital_id)
        row = log.get_row()
        assert row[0] == str(log.id)
        timestamp = datetime.strptime(row[1], "%d/%m/%Y - %H:%M:%S")
        assert timestamp >= self.start_time.replace(microsecond=0)
        assert timestamp <= datetime.now()
        assert row[2] == "True"
        assert row[3] == "NHS"
        assert row[4] == "1"
        assert row[5] == "create"
        assert row[6] == "New registration"
        assert row[7] == str(digital_id)
        assert row[8] == "None"
        assert row[9] == "None"

    def test_create_log_for_read(self) -> None:
        log = Log.for_read("NHS", 1, "Medical history check", "active")
        row = log.get_row()
        assert row[0] == str(log.id)
        timestamp = datetime.strptime(row[1], "%d/%m/%Y - %H:%M:%S")
        assert timestamp >= self.start_time.replace(microsecond=0)
        assert timestamp <= datetime.now()
        assert row[2] == "True"
        assert row[3] == "NHS"
        assert row[4] == "1"
        assert row[5] == "read"
        assert row[6] == "Medical history check"
        assert row[7] == "active"
        assert row[8] == "None"
        assert row[9] == "None"

    def test_create_log_for_update(self) -> None:
        log = Log.for_update("NHS", 1, "Name change", "first_name", "John", "Alicia")
        row = log.get_row()
        assert row[0] == str(log.id)
        timestamp = datetime.strptime(row[1], "%d/%m/%Y - %H:%M:%S")
        assert timestamp >= self.start_time.replace(microsecond=0)
        assert timestamp <= datetime.now()
        assert row[2] == "True"
        assert row[3] == "NHS"
        assert row[4] == "1"
        assert row[5] == "update"
        assert row[6] == "Name change"
        assert row[7] == "John"
        assert row[8] == "Alicia"
        assert row[9] == "first_name"

    def test_create_log_for_verify(self) -> None:
        log = Log.for_verify("Bank", 1, "Account opening", "identity", True)
        row = log.get_row()
        assert row[0] == str(log.id)
        timestamp = datetime.strptime(row[1], "%d/%m/%Y - %H:%M:%S")
        assert timestamp >= self.start_time.replace(microsecond=0)
        assert timestamp <= datetime.now()
        assert row[2] == "True"
        assert row[3] == "Bank"
        assert row[4] == "1"
        assert row[5] == "verify"
        assert row[6] == "Account opening"
        assert row[7] == "True"
        assert row[8] == "None"
        assert row[9] == "identity"

    def test_create_log_for_verify_with_context(self) -> None:
        log = Log.for_verify("Bank", 1, "ISA eligibility", "minimum_age", False, "18")
        row = log.get_row()
        assert row[5] == "verify"
        assert row[6] == "ISA eligibility"
        assert row[7] == "False"
        assert row[8] == "None"
        assert row[9] == "minimum_age"
        assert row[10] == "18"

    def test_from_csv(self) -> None:
        attributes = {
            "id": "5",
            "timestamp": "15/03/2024 - 10:30:45",
            "accepted": "True",
            "organisation": "NHS",
            "digitalID": "1",
            "action": "create",
            "justification": "New registration",
            "currentValue": "John Smith",
            "newValue": "None",
            "attribute": "None",
            "comparativeValue": "None"
        }
        log = Log.from_csv(attributes)
        assert log.id == 5
        assert log.timestamp == datetime.strptime("15/03/2024 - 10:30:45", "%d/%m/%Y - %H:%M:%S")
        assert log.accepted == True
        assert log.organisation == "NHS"
        assert log.id_number == 1
        assert log.action == Action.CREATE
        assert log.justification == "New registration"
        assert log.current_value == "John Smith"
        assert log.new_value is None
        assert log.attribute is None
        assert log.comparative_value is None

    def test_from_csv_with_new_value(self) -> None:
        attributes = {
            "id": "6",
            "timestamp": "15/03/2024 - 10:30:45",
            "accepted": "False",
            "organisation": "HMRC",
            "digitalID": "2",
            "action": "update",
            "justification": "Name change",
            "currentValue": "John",
            "newValue": "Alicia",
            "attribute": "first_name",
            "comparativeValue": "None"
        }
        log = Log.from_csv(attributes)
        assert log.id == 6
        assert log.accepted == False
        assert log.new_value == "Alicia"
        assert log.attribute == "first_name"
        assert log.comparative_value is None

class TestLogProperties:
    """Tests for Log getters"""

    def setup_method(self) -> None:
        DigitalID._next_id = 1
        self.digital_id = DigitalID(new_person_dict)
        self.log = Log.for_create("NHS", 1, "New registration", self.digital_id)

    def test_get_timestamp(self) -> None:
        start_time = datetime.now()
        log = Log.for_update("NHS", 1, "Update Medical Records", "status", "Healthy", "Unhealthy")
        assert log.timestamp >= start_time.replace(microsecond=0)
        assert log.timestamp <= datetime.now()
        assert isinstance(self.log.timestamp, datetime)

    def test_get_organisation(self) -> None:
        assert self.log.organisation == "NHS"

    def test_get_id_number(self) -> None:
        assert self.log.id_number == 1

    def test_get_action(self) -> None:
        assert self.log.action == Action.CREATE

    def test_get_accepted(self) -> None:
        assert self.log.accepted == True

    def test_get_justification(self) -> None:
        assert self.log.justification == "New registration"

    def test_get_current_value_digitalid(self) -> None:
        assert self.log.current_value.first_name == "John"
        assert isinstance(self.log.current_value, DigitalID)

    def test_get_current_value_string(self) -> None:
        log = Log.for_update("NHS", 1, "Name change", "first_name", "John", "Alicia")
        assert log.current_value == "John"

    def test_get_new_value(self) -> None:
        log = Log.for_update("NHS", 1, "Name change", "first_name", "John", "Alicia")
        assert log.new_value == "Alicia"

    def test_get_new_value_none(self) -> None:
        assert self.log.new_value is None

    def test_get_id(self) -> None:
        assert isinstance(self.log.id, int)
        assert self.log.id > 0

    def test_to_dict(self) -> None:
        log_dict = self.log.to_dict()
        assert log_dict["id"] == str(self.log.id)
        assert log_dict["accepted"] == "True"
        assert log_dict["organisation"] == "NHS"
        assert log_dict["digitalID"] == "1"
        assert log_dict["action"] == "create"
        assert log_dict["justification"] == "New registration"
        assert log_dict["currentValue"] == str(self.log.current_value)
        assert log_dict["newValue"] == "None"
        assert log_dict["attribute"] == "None"

    def test_to_dict_string_values(self) -> None:
        log = Log.for_update("HMRC", 2, "Name change", "first_name", "John", "Alicia")
        log_dict = log.to_dict()
        assert log_dict["accepted"] == "True"
        assert log_dict["currentValue"] == "John"
        assert log_dict["newValue"] == "Alicia"
        assert log_dict["attribute"] == "first_name"

    def test_print_create_action(self, capsys) -> None:
        self.log.print()
        captured = capsys.readouterr()
        output = captured.out
        
        assert "Requested to create ID 1" in output
        assert "New registration was ACCEPTED" in output
        assert "ID: 1" in output
        assert "First Name: John" in output
        assert "Surname: Smith" in output
        assert "Date of Birth: 2000-01-01" in output
        assert "Status: active" in output

    def test_print_read_action(self, capsys) -> None:
        read_log = Log.for_read("HMRC", 2, "Tax verification", "active")
        read_log.print()
        captured = capsys.readouterr()
        output = captured.out
        
        assert "Requested to read ID 2" in output
        assert "Tax verification was ACCEPTED" in output

    def test_print_update_action(self, capsys) -> None:
        update_log = Log.for_update("NHS", 3, "Status change", "status", "active", "suspended")
        update_log.print()
        captured = capsys.readouterr()
        output = captured.out
        
        assert "Requested to update ID 3" in output
        assert "Status change was ACCEPTED" in output

    def test_print_verify_action(self, capsys) -> None:
        verify_log = Log.for_verify("Bank", 5, "Account opening", "identity", True)
        verify_log.print()
        captured = capsys.readouterr()
        output = captured.out

        assert "Requested to verify ID 5" in output
        assert "identity: True" in output
        assert "Account opening was ACCEPTED" in output

    def test_print_verify_action_with_context(self, capsys) -> None:
        verify_log = Log.for_verify("Bank", 5, "ISA eligibility", "minimum_age", False, "18")
        verify_log.print()
        captured = capsys.readouterr()
        output = captured.out

        assert "Requested to verify ID 5" in output
        assert "minimum_age (threshold: 18): False" in output
        assert "ISA eligibility was ACCEPTED" in output

    def test_print_create_with_non_digitalid(self, capsys) -> None:
        create_log = Log(True, "NHS", 4, Action.CREATE, "Manual entry", "John Doe Profile", None, None)
        create_log.print()
        captured = capsys.readouterr()
        output = captured.out
        
        assert "Requested to create ID 4" in output
        assert "Manual entry was ACCEPTED" in output

    def test_print_rejected_action(self, capsys) -> None:
        rejected_log = Log.for_failure("NHS", 0, Action.CREATE, "Invalid data", "Error: Invalid name")
        rejected_log.print()
        captured = capsys.readouterr()
        output = captured.out
        
        assert "Requested to create ID 0" in output
        assert "Invalid data was REJECTED" in output
