import pytest
import os
from Data.digitalID import DigitalID
from Data.digitalIDRepository import DigitalIDRepository

class TestDigitalIDRepositoryCreation:
    """Tests for DigitalIDRepository constructor"""

    def test_create_empty_repository(self) -> None:
        DigitalIDRepository._instance = None
        repo = DigitalIDRepository()
        assert repo.get_all_ids() == {}

class TestDigitalIDRepositoryAddAndGet:
    """Tests for adding and retrieving Digital IDs"""

    def setup_method(self) -> None:
        DigitalID._next_id = 1
        DigitalIDRepository._instance = None
        self.repo = DigitalIDRepository()

    def test_add_id(self) -> None:
        id = DigitalID("John", "Smith", "2000-01-01")
        self.repo.add_id(id)
        assert self.repo.get_id(1) == id

    def test_add_multiple_ids(self) -> None:
        id1 = DigitalID("John", "Smith", "2000-01-01")
        id2 = DigitalID("Bob", "Jones", "2005-01-01")
        self.repo.add_id(id1)
        self.repo.add_id(id2)
        assert len(self.repo.get_all_ids()) == 2

    def test_get_id(self) -> None:
        id1 = DigitalID("John", "Smith", "2000-01-01")
        id2 = DigitalID("Bob", "Jones", "2005-01-01")
        self.repo.add_id(id1)
        self.repo.add_id(id2)
        assert self.repo.get_id(2).first_name == "Bob"

    def test_get_id_missing_raises_key_error(self) -> None:
        with pytest.raises(KeyError):
            self.repo.get_id(99)

    def test_get_all_ids(self) -> None:
        id1 = DigitalID("John", "Smith", "2000-01-01")
        id2 = DigitalID("Bob", "Jones", "2005-01-01")
        self.repo.add_id(id1)
        self.repo.add_id(id2)

        all_ids = self.repo.get_all_ids()

        assert all_ids[1].first_name == "John"
        assert all_ids[2].first_name == "Bob"

class TestDigitalIDRepositoryCSV:
    """Tests for CSV save and load"""

    TEST_CSV_PATH = "test_digital_ids.csv"

    def setup_method(self) -> None:
        DigitalID._next_id = 1
        DigitalIDRepository._instance = None
        DigitalIDRepository.CSV_PATH = self.TEST_CSV_PATH
        self.repo = DigitalIDRepository()

    def teardown_method(self) -> None:
        DigitalIDRepository.CSV_PATH = "../../digital_ids.csv"
        if os.path.exists(self.TEST_CSV_PATH):
            os.remove(self.TEST_CSV_PATH)

    def test_save_to_csv(self) -> None:
        id = DigitalID("John", "Smith", "2000-01-01")
        self.repo.add_id(id)
        self.repo.save_to_csv()
        assert os.path.exists(self.TEST_CSV_PATH)

        with open(self.TEST_CSV_PATH, "r") as file:
            lines = file.readlines()

        assert lines[0].strip() == "ID,Status,First Name,Surname,Date of Birth"
        assert lines[1].strip() == "1,active,John,Smith,2000-01-01"

    def test_load_from_csv_restores_data(self) -> None:
        id1 = DigitalID("John", "Smith", "2000-01-01")
        id2 = DigitalID("Bob", "Jones", "2005-01-01")
        
        self.repo.add_id(id1)
        self.repo.add_id(id2)
        self.repo.save_to_csv()

        DigitalID._next_id = 1
        DigitalIDRepository._instance = None
        new_repo = DigitalIDRepository()
        new_repo.load_from_csv()

        assert new_repo.get_id(1).first_name == "John"
        assert new_repo.get_id(2).first_name == "Bob"

    def test_load_from_csv_updates_next_id(self) -> None:
        id1 = DigitalID("John", "Smith", "2000-01-01")
        id2 = DigitalID("Bob", "Jones", "2005-01-01")
        self.repo.add_id(id1)
        self.repo.add_id(id2)
        self.repo.save_to_csv()

        DigitalID._next_id = 1
        DigitalIDRepository._instance = None
        new_repo = DigitalIDRepository()
        new_repo.load_from_csv()
        assert DigitalID._next_id == 3
