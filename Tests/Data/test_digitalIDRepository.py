import pytest
import os
import Data.digitalIDRepository as repo_module
import constants
from Data.digitalID import DigitalID
from Data.digitalIDRepository import DigitalIDRepository

class TestDigitalIDRepositoryCreation:
    """Tests for DigitalIDRepository constructor"""

    def test_create_empty_repository(self) -> None:
        DigitalIDRepository._instance = None
        repo = DigitalIDRepository()
        assert repo.get_all() == {}

class TestDigitalIDRepositoryAddAndGet:
    """Tests for adding and retrieving Digital IDs"""

    def setup_method(self) -> None:
        DigitalID._next_id = 1
        DigitalIDRepository._instance = None
        self.repo = DigitalIDRepository()

    def test_add(self) -> None:
        id = DigitalID("John", "Smith", "2000-01-01")
        self.repo.add(id)
        assert self.repo.get_from_id(1) == id

    def test_add_multiple_ids(self) -> None:
        id1 = DigitalID("John", "Smith", "2000-01-01")
        id2 = DigitalID("Bob", "Jones", "2005-01-01")
        self.repo.add(id1)
        self.repo.add(id2)
        assert len(self.repo.get_all()) == 2

    def test_get_from_id(self) -> None:
        id1 = DigitalID("John", "Smith", "2000-01-01")
        id2 = DigitalID("Bob", "Jones", "2005-01-01")
        self.repo.add(id1)
        self.repo.add(id2)
        assert self.repo.get_from_id(2).first_name == "Bob"

    def test_get_id_missing_raises_key_error(self) -> None:
        with pytest.raises(KeyError):
            self.repo.get_from_id(99)

    def test_get_all(self) -> None:
        id1 = DigitalID("John", "Smith", "2000-01-01")
        id2 = DigitalID("Bob", "Jones", "2005-01-01")
        self.repo.add(id1)
        self.repo.add(id2)

        all_ids = self.repo.get_all()

        assert all_ids[1].first_name == "John"
        assert all_ids[2].first_name == "Bob"

class TestDigitalIDRepositoryCSV:
    """Tests for CSV save and load"""

    TEST_CSV_PATH = "test_digital_ids.csv"

    def setup_method(self) -> None:
        DigitalID._next_id = 1
        DigitalIDRepository._instance = None
        constants.CSV_PATH = self.TEST_CSV_PATH
        repo_module.CSV_PATH = self.TEST_CSV_PATH
        self.repo = DigitalIDRepository()

    def teardown_method(self) -> None:
        if os.path.exists(self.TEST_CSV_PATH):
            os.remove(self.TEST_CSV_PATH)

    def test_save_to_csv(self) -> None:
        id = DigitalID("John", "Smith", "2000-01-01")
        self.repo.add(id)
        self.repo.save_to_csv()
        assert os.path.exists(self.TEST_CSV_PATH)

        with open(self.TEST_CSV_PATH, "r") as file:
            lines = file.readlines()

        assert lines[0].strip() == "id,status,firstName,surname,dateOfBirth"
        assert lines[1].strip() == "1,active,John,Smith,2000-01-01"

    def test_load_from_csv_restores_data(self) -> None:
        id1 = DigitalID("John", "Smith", "2000-01-01")
        id2 = DigitalID("Bob", "Jones", "2005-01-01")
        
        self.repo.add(id1)
        self.repo.add(id2)
        self.repo.save_to_csv()

        DigitalID._next_id = 1
        DigitalIDRepository._instance = None
        new_repo = DigitalIDRepository()
        new_repo.load_from_csv()

        assert new_repo.get_from_id(1).first_name == "John"
        assert new_repo.get_from_id(2).first_name == "Bob"

    def test_load_from_csv_updates_next_id(self) -> None:
        id1 = DigitalID("John", "Smith", "2000-01-01")
        id2 = DigitalID("Bob", "Jones", "2005-01-01")
        self.repo.add(id1)
        self.repo.add(id2)
        self.repo.save_to_csv()

        DigitalID._next_id = 1
        DigitalIDRepository._instance = None
        new_repo = DigitalIDRepository()
        new_repo.load_from_csv()
        assert DigitalID._next_id == 3
