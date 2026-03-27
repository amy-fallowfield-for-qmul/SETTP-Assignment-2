import pytest
import os
from Data.logRepository import LogRepository
from Data.log import Log, Action
from datetime import datetime

@pytest.fixture
def log_repo() -> LogRepository:
    LogRepository._instance = None
    return LogRepository()

class TestLogRepositoryAddAndGet:
    """Tests for adding and retrieving logs"""

    def test_add_log(self, log_repo: LogRepository) -> None:
        log = Log("NHS", 1, Action.CREATE, "New registration", "John Smith", None)
        log_repo.add_log(log)
        assert len(log_repo.get_all_logs()) == 1
        stored_log = log_repo.get_all_logs()[0]

        start_time = datetime.now()
        assert stored_log.timestamp >= start_time.replace(microsecond=0)
        assert stored_log.timestamp <= datetime.now()
        assert stored_log.organisation == "NHS"
        assert stored_log.id_number == 1
        assert stored_log.action == Action.CREATE
        assert stored_log.justification == "New registration"
        assert stored_log.current_value == "John Smith"
        assert stored_log.new_value is None

    def test_add_multiple_logs(self, log_repo: LogRepository) -> None:
        log1 = Log("NHS", 1, Action.CREATE, "New registration", "John Smith", None)
        log2 = Log("HMRC", 2, Action.READ, "Tax check", "active", None)
        log_repo.add_log(log1)
        log_repo.add_log(log2)
        assert len(log_repo.get_all_logs()) == 2

    def test_get_all_logs_empty(self, log_repo: LogRepository) -> None:
        assert log_repo.get_all_logs() == []

class TestLogRepositoryCSV:
    """Tests for CSV save and load"""

    TEST_CSV_PATH = "test_logs.csv"

    def setup_method(self) -> None:
        LogRepository._instance = None
        LogRepository.CSV_PATH = self.TEST_CSV_PATH
        self.log_repo = LogRepository()

    def teardown_method(self) -> None:
        if os.path.exists(self.TEST_CSV_PATH):
            os.remove(self.TEST_CSV_PATH)

    def test_save_to_csv(self) -> None:
        log = Log("NHS", 1, Action.CREATE, "New registration", "John Smith", None)
        self.log_repo.add_log(log)
        self.log_repo.save_to_csv()
        assert os.path.exists(self.TEST_CSV_PATH)

        with open(self.TEST_CSV_PATH, "r") as file:
            lines = file.readlines()

        assert lines[0].strip() == "timestamp,organisation,digitalID,action,justification,currentValue,newValue"
        data_line = lines[1].strip().split(",")
        start_time = datetime.now()
        csv_timestamp = datetime.strptime(data_line[0], "%d/%m/%Y - %H:%M:%S")
        assert csv_timestamp >= start_time.replace(microsecond=0)
        assert csv_timestamp <= datetime.now()
        assert data_line[1] == "NHS"
        assert data_line[2] == "1"
        assert data_line[3] == "create"
        assert data_line[4] == "New registration"
        assert data_line[5] == "John Smith"
        assert data_line[6] == ""

    def test_save_empty_csv(self) -> None:
        self.log_repo.save_to_csv()
        assert os.path.exists(self.TEST_CSV_PATH)

        with open(self.TEST_CSV_PATH, "r") as file:
            lines = file.readlines()

        assert len(lines) == 1
        assert lines[0].strip() == "timestamp,organisation,digitalID,action,justification,currentValue,newValue"

    def test_load_from_csv(self) -> None:
        log1 = Log("NHS", 1, Action.CREATE, "New registration", "John Smith", None)
        log2 = Log("HMRC", 2, Action.UPDATE, "Name change", "John", "Alicia")
        self.log_repo.add_log(log1)
        self.log_repo.add_log(log2)
        self.log_repo.save_to_csv()

        LogRepository._instance = None
        LogRepository.CSV_PATH = self.TEST_CSV_PATH
        new_repo = LogRepository()
        new_repo.load_from_csv()

        assert len(new_repo.get_all_logs()) == 2
        assert new_repo.get_all_logs()[0].organisation == "NHS"
        assert new_repo.get_all_logs()[1].organisation == "HMRC"

    def test_load_empty_csv(self) -> None:
        self.log_repo.save_to_csv()
        
        LogRepository._instance = None
        LogRepository.CSV_PATH = self.TEST_CSV_PATH
        new_repo = LogRepository()
        new_repo.load_from_csv()

        assert len(new_repo.get_all_logs()) == 0
