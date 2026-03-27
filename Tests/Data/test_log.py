import pytest
from datetime import datetime
from Data.log import Log, Action
from Data.digitalID import DigitalID

class TestAction:
    """Tests for the Action enum"""

    def test_action_values(self) -> None:
        assert Action.CREATE.value == "create"
        assert Action.READ.value == "read"
        assert Action.UPDATE.value == "update"

    def test_action_members(self) -> None:
        assert set(Action.__members__.keys()) == {"CREATE", "READ", "UPDATE"}

class TestLogModel:
    """Tests for Log data model"""

    def setup_method(self) -> None:
        DigitalID._next_id = 1
        self.start_time = datetime.now()

    def test_create_log_for_create(self) -> None:
        digital_id = DigitalID("John", "Smith", "2000-01-01")
        log = Log("NHS", 1, Action.CREATE, "New registration", digital_id, None)
        row = log.get_row()
        timestamp = datetime.strptime(row[0], "%d/%m/%Y - %H:%M:%S")
        assert timestamp >= self.start_time.replace(microsecond=0)
        assert timestamp <= datetime.now()
        assert row[1] == "NHS"
        assert row[2] == "1"
        assert row[3] == "create"
        assert row[4] == "New registration"
        assert row[5]["firstName"] == "John"
        assert row[6] is None
    
    def test_create_log_for_read(self) -> None:
        log = Log("NHS", 1, Action.READ, "Medical history check", "active", None)
        row = log.get_row()
        timestamp = datetime.strptime(row[0], "%d/%m/%Y - %H:%M:%S")
        assert timestamp >= self.start_time.replace(microsecond=0)
        assert timestamp <= datetime.now()
        assert row[1] == "NHS"
        assert row[2] == "1"
        assert row[3] == "read"
        assert row[4] == "Medical history check"
        assert row[5] == "active"
        assert row[6] is None

    def test_create_log_for_update(self) -> None:
        log = Log("NHS", 1, Action.UPDATE, "Name change", "John", "Alicia")
        row = log.get_row()
        timestamp = datetime.strptime(row[0], "%d/%m/%Y - %H:%M:%S")
        assert timestamp >= self.start_time.replace(microsecond=0)
        assert timestamp <= datetime.now()
        assert row[1] == "NHS"
        assert row[2] == "1"
        assert row[3] == "update"
        assert row[4] == "Name change"
        assert row[5] == "John"
        assert row[6] == "Alicia"

    def test_from_csv_row(self) -> None:
        row = ["15/03/2024 - 10:30:45", "NHS", "1", "create", "New registration", "John Smith", "None"]
        log = Log.from_csv_row(row)
        assert log.timestamp == datetime.strptime("15/03/2024 - 10:30:45", "%d/%m/%Y - %H:%M:%S")
        assert log.organisation == "NHS"
        assert log.id_number == 1
        assert log.action == Action.CREATE
        assert log.justification == "New registration"
        assert log.current_value == "John Smith"
        assert log.new_value is None

    def test_from_csv_row_with_new_value(self) -> None:
        row = ["15/03/2024 - 10:30:45", "HMRC", "2", "update", "Name change", "John", "Alicia"]
        log = Log.from_csv_row(row)
        assert log.new_value == "Alicia"

class TestLogProperties:
    """Tests for Log getters"""

    def setup_method(self) -> None:
        DigitalID._next_id = 1
        self.digital_id = DigitalID("John", "Smith", "2000-01-01")
        self.log = Log("NHS", 1, Action.CREATE, "New registration", self.digital_id, None)

    def test_get_timestamp(self) -> None:
        start_time = datetime.now()
        log = Log("NHS", 1, Action.UPDATE, "Update Medical Records", "Healthy", "Unhealthy")
        assert log.timestamp >= start_time.replace(microsecond=0)
        assert log.timestamp <= datetime.now()
        assert isinstance(self.log.timestamp, datetime)

    def test_get_organisation(self) -> None:
        assert self.log.organisation == "NHS"

    def test_get_id_number(self) -> None:
        assert self.log.id_number == 1

    def test_get_action(self) -> None:
        assert self.log.action == Action.CREATE

    def test_get_justification(self) -> None:
        assert self.log.justification == "New registration"

    def test_get_current_value_dict(self) -> None:
        assert self.log.current_value["firstName"] == "John"

    def test_get_current_value_string(self) -> None:
        log = Log("NHS", 1, Action.UPDATE, "Name change", "John", "Alicia")
        assert log.current_value == "John"

    def test_get_new_value(self) -> None:
        log = Log("NHS", 1, Action.UPDATE, "Name change", "John", "Alicia")
        assert log.new_value == "Alicia"

    def test_get_new_value_none(self) -> None:
        assert self.log.new_value is None
