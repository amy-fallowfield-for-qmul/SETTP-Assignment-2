import pytest
import os
from Data.Logging.logRepository import LogRepository
from Data.Logging.log import Log, Action
from datetime import datetime

@pytest.fixture
def log_repo() -> LogRepository:
    LogRepository.clear_instance()
    return LogRepository()

class TestLogRepositoryAddAndGet:
    """Tests for adding and retrieving logs"""

    def test_add(self, log_repo: LogRepository) -> None:
        log = Log(True, "NHS", 1, Action.CREATE, "New registration", "John Smith", None, None)
        log_repo.add(log)
        assert len(log_repo.get_all()) == 1
        stored_log = log_repo.get_from_id(log.id)

        start_time = datetime.now()
        assert stored_log.timestamp >= start_time.replace(microsecond=0)
        assert stored_log.timestamp <= datetime.now()
        assert stored_log.accepted == True
        assert stored_log.organisation == "NHS"
        assert stored_log.id_number == 1
        assert stored_log.action == Action.CREATE
        assert stored_log.justification == "New registration"
        assert stored_log.current_value == "John Smith"
        assert stored_log.new_value is None

    def test_add_multiple_logs(self, log_repo: LogRepository) -> None:
        log1 = Log(True, "NHS", 1, Action.CREATE, "New registration", "John Smith", None, None)
        log2 = Log(False, "HMRC", 2, Action.READ, "Tax check", "active", None, None)
        log_repo.add(log1)
        log_repo.add(log2)
        assert len(log_repo.get_all()) == 2

    def test_get_all_empty(self, log_repo: LogRepository) -> None:
        assert log_repo.get_all() == {}

    def test_get_from_id(self, log_repo: LogRepository) -> None:
        log = Log(True, "NHS", 1, Action.CREATE, "New registration", "John Smith", None, None)
        log_repo.add(log)
        retrieved_log = log_repo.get_from_id(log.id)
        assert retrieved_log == log

    def test_get_from_id_not_found(self, log_repo: LogRepository) -> None:
        with pytest.raises(KeyError):
            log_repo.get_from_id(999)

class TestLogRepositoryCSV:
    """Tests for CSV save and load"""

    TEST_CSV_PATH = "test_logs.csv"

    def setup_method(self) -> None:
        LogRepository.clear_instance()
        self.log_repo = LogRepository()

    def teardown_method(self) -> None:
        if os.path.exists(self.TEST_CSV_PATH):
            os.remove(self.TEST_CSV_PATH)

    def test_save_to_csv(self, monkeypatch) -> None:
        monkeypatch.setattr(self.log_repo, "_get_csv_path", lambda: self.TEST_CSV_PATH)
        log = Log(True, "NHS", 1, Action.CREATE, "New registration", "John Smith", None, None)
        self.log_repo.add(log)
        self.log_repo.save_to_csv()
        assert os.path.exists(self.TEST_CSV_PATH)

        with open(self.TEST_CSV_PATH, "r") as file:
            lines = file.readlines()

        assert lines[0].strip() == "id,timestamp,accepted,organisation,digitalID,action,justification,currentValue,newValue,attribute"
        data_line = lines[1].strip().split(",")
        start_time = datetime.now()
        assert data_line[0] == str(log.id)
        csv_timestamp = datetime.strptime(data_line[1], "%d/%m/%Y - %H:%M:%S")
        assert csv_timestamp >= start_time.replace(microsecond=0)
        assert csv_timestamp <= datetime.now()
        assert data_line[2] == "True"
        assert data_line[3] == "NHS"
        assert data_line[4] == "1"
        assert data_line[5] == "create"
        assert data_line[6] == "New registration"
        assert data_line[7] == "John Smith"
        assert data_line[8] == ""
        assert data_line[9] == ""

    def test_save_empty_csv(self, monkeypatch) -> None:
        monkeypatch.setattr(self.log_repo, "_get_csv_path", lambda: self.TEST_CSV_PATH)
        self.log_repo.save_to_csv()
        assert os.path.exists(self.TEST_CSV_PATH)

        with open(self.TEST_CSV_PATH, "r") as file:
            lines = file.readlines()

        assert len(lines) == 1
        assert lines[0].strip() == "id,timestamp,accepted,organisation,digitalID,action,justification,currentValue,newValue,attribute"

    def test_load_from_csv(self, monkeypatch) -> None:
        monkeypatch.setattr(self.log_repo, "_get_csv_path", lambda: self.TEST_CSV_PATH)
        log1 = Log(True, "NHS", 1, Action.CREATE, "New registration", "John Smith", None, None)
        log2 = Log(False, "HMRC", 2, Action.UPDATE, "Name change", "John", "Alicia", "first_name")
        self.log_repo.add(log1)
        self.log_repo.add(log2)
        self.log_repo.save_to_csv()

        LogRepository.clear_instance()
        new_repo = LogRepository()
        monkeypatch.setattr(new_repo, "_get_csv_path", lambda: self.TEST_CSV_PATH)
        new_repo.load_from_csv()

        assert len(new_repo.get_all()) == 2
        logs = list(new_repo.get_all().values())
        assert logs[0].organisation == "NHS"
        assert logs[0].accepted == True
        assert logs[1].organisation == "HMRC"
        assert logs[1].accepted == False

    def test_load_empty_csv(self, monkeypatch) -> None:
        monkeypatch.setattr(self.log_repo, "_get_csv_path", lambda: self.TEST_CSV_PATH)
        self.log_repo.save_to_csv()
        
        LogRepository.clear_instance()
        new_repo = LogRepository()
        monkeypatch.setattr(new_repo, "_get_csv_path", lambda: self.TEST_CSV_PATH)
        new_repo.load_from_csv()

        assert len(new_repo.get_all()) == 0