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
