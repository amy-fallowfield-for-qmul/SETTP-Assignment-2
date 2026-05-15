import pytest
import os
import csv
from datetime import datetime
import Data.Logging.logRepository as log_repo_module
from Data.Logging.logRepository import LogRepository
from Data.Logging.log import Log, Action
from Data.DigitalID.digitalID import DigitalID
from Tests.shared_test_data import new_person_dict

EXPECTED_HEADERS = [
    "id", "timestamp", "accepted", "organisation", "digitalID",
    "action", "justification", "currentValue", "newValue", "attribute",
    "comparativeValue"
]

@pytest.fixture
def log_repo() -> LogRepository:
    LogRepository.clear_instance()
    return LogRepository()

class TestLogRepositoryAddAndGet:
    """Tests for adding and retrieving logs"""

    def test_add(self, log_repo: LogRepository) -> None:
        digital_id = DigitalID(new_person_dict)
        log = Log.for_create("NHS", 1, "New registration", digital_id)
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
        assert isinstance(stored_log.current_value, DigitalID)
        assert stored_log.current_value.first_name == "John"
        assert stored_log.current_value.surname == "Smith"
        assert stored_log.new_value is None

    def test_add_multiple_logs(self, log_repo: LogRepository) -> None:
        log1 = Log.for_create("NHS", 1, "New registration", DigitalID(new_person_dict))
        log2 = Log.for_failure("HMRC", 2, Action.READ, "Tax check", "Access denied")
        log_repo.add(log1)
        log_repo.add(log2)
        assert len(log_repo.get_all()) == 2

    def test_get_all_empty(self, log_repo: LogRepository) -> None:
        assert log_repo.get_all() == {}

    def test_get_from_id(self, log_repo: LogRepository) -> None:
        log = Log.for_create("NHS", 1, "New registration", DigitalID(new_person_dict))
        log_repo.add(log)
        retrieved_log = log_repo.get_from_id(log.id)
        assert retrieved_log == log

    def test_get_from_id_not_found(self, log_repo: LogRepository) -> None:
        with pytest.raises(KeyError):
            log_repo.get_from_id(999)

    def test_add_duplicate_id_raises(self, log_repo: LogRepository) -> None:
        log = Log.for_create("NHS", 1, "New registration", DigitalID(new_person_dict))
        log_repo.add(log)
        with pytest.raises(ValueError, match="already exists"):
            log_repo.add(log)

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
        digital_id = DigitalID(new_person_dict)
        start_time = datetime.now()
        log = Log.for_create("NHS", 1, "New registration", digital_id)
        self.log_repo.add(log)
        self.log_repo.save_to_csv()
        assert os.path.exists(self.TEST_CSV_PATH)

        with open(self.TEST_CSV_PATH, newline="") as file:
            rows = list(csv.reader(file))

        assert rows[0] == EXPECTED_HEADERS
        data_row = rows[1]
        assert data_row[0] == str(log.id)
        csv_timestamp = datetime.strptime(data_row[1], "%d/%m/%Y - %H:%M:%S")
        assert csv_timestamp >= start_time.replace(microsecond=0)
        assert csv_timestamp <= datetime.now()
        assert data_row[2] == "True"
        assert data_row[3] == "NHS"
        assert data_row[4] == "1"
        assert data_row[5] == "create"
        assert data_row[6] == "New registration"
        assert data_row[7] == str(digital_id)
        assert data_row[8] == "None"
        assert data_row[9] == "None"
        assert data_row[10] == "None"

    def test_save_empty_csv(self, monkeypatch) -> None:
        monkeypatch.setattr(self.log_repo, "_get_csv_path", lambda: self.TEST_CSV_PATH)
        self.log_repo.save_to_csv()
        assert os.path.exists(self.TEST_CSV_PATH)

        with open(self.TEST_CSV_PATH, newline="") as file:
            rows = list(csv.reader(file))

        assert rows == [EXPECTED_HEADERS]

    def test_load_from_csv(self, monkeypatch) -> None:
        monkeypatch.setattr(self.log_repo, "_get_csv_path", lambda: self.TEST_CSV_PATH)
        log1 = Log.for_create("NHS", 1, "New registration", DigitalID(new_person_dict))
        log2 = Log.for_failure("HMRC", 2, Action.UPDATE, "Name change", "Validation error", "first_name")
        self.log_repo.add(log1)
        self.log_repo.add(log2)
        self.log_repo.save_to_csv()

        LogRepository.clear_instance()
        new_repo = LogRepository()
        monkeypatch.setattr(new_repo, "_get_csv_path", lambda: self.TEST_CSV_PATH)
        new_repo.load_from_csv()

        assert len(new_repo.get_all()) == 2
        loaded_log1 = new_repo.get_from_id(log1.id)
        loaded_log2 = new_repo.get_from_id(log2.id)
        assert loaded_log1.organisation == "NHS"
        assert loaded_log1.accepted == True
        assert loaded_log1.action == Action.CREATE

        assert loaded_log2.organisation == "HMRC"
        assert loaded_log2.accepted == False
        assert loaded_log2.action == Action.UPDATE
        assert loaded_log2.attribute == "first_name"

    def test_load_empty_csv(self, monkeypatch) -> None:
        monkeypatch.setattr(self.log_repo, "_get_csv_path", lambda: self.TEST_CSV_PATH)
        self.log_repo.save_to_csv()
        
        LogRepository.clear_instance()
        new_repo = LogRepository()
        monkeypatch.setattr(new_repo, "_get_csv_path", lambda: self.TEST_CSV_PATH)
        new_repo.load_from_csv()

        assert len(new_repo.get_all()) == 0

    def test_reordering_headers_does_not_break(self, monkeypatch) -> None:
        monkeypatch.setattr(self.log_repo, "_get_csv_path", lambda: self.TEST_CSV_PATH)
        reversed_headers = list(reversed(EXPECTED_HEADERS))
        monkeypatch.setattr(log_repo_module, "LOG_HEADERS", reversed_headers)

        original = Log.for_update("NHS", 1, "Name change", "first_name", "John", "Alicia")
        self.log_repo.add(original)
        self.log_repo.save_to_csv()

        with open(self.TEST_CSV_PATH, newline="") as file:
            rows = list(csv.reader(file))
        assert rows[0] == reversed_headers

        LogRepository.clear_instance()
        new_repo = LogRepository()
        monkeypatch.setattr(new_repo, "_get_csv_path", lambda: self.TEST_CSV_PATH)
        new_repo.load_from_csv()

        loaded = new_repo.get_from_id(original.id)
        assert loaded.to_dict() == original.to_dict()
