import pytest
import os
from Data.DigitalID.digitalID import DigitalID
from Data.DigitalID.digitalIDRepository import DigitalIDRepository
from Tests.shared_test_data import new_person_dict, from_csv_person_dict

class TestDigitalIDRepositoryCreation:
    """Tests for DigitalIDRepository constructor"""

    def test_create_empty_repository(self) -> None:
        DigitalIDRepository.clear_instance()
        repo = DigitalIDRepository()
        assert repo.get_all() == {}

class TestDigitalIDRepositoryAddAndGet:
    """Tests for adding and retrieving Digital IDs"""

    def setup_method(self) -> None:
        DigitalID._next_id = 1
        DigitalIDRepository.clear_instance()
        self.repo = DigitalIDRepository()

    def test_add(self) -> None:
        id = DigitalID(new_person_dict)
        self.repo.add(id)
        assert self.repo.get_from_id(1) == id

    def test_add_multiple_ids(self) -> None:
        id1 = DigitalID(new_person_dict)
        id2 = DigitalID(from_csv_person_dict)
        self.repo.add(id1)
        self.repo.add(id2)
        assert len(self.repo.get_all()) == 2

    def test_get_from_id(self) -> None:
        id1 = DigitalID(new_person_dict)
        id2 = DigitalID(from_csv_person_dict)
        self.repo.add(id1)
        self.repo.add(id2)
        assert self.repo.get_from_id(2).first_name == from_csv_person_dict["first_name"]

    def test_get_id_missing_raises_key_error(self) -> None:
        with pytest.raises(KeyError):
            self.repo.get_from_id(99)

    def test_get_all(self) -> None:
        id1 = DigitalID(new_person_dict)
        id2 = DigitalID(from_csv_person_dict)
        self.repo.add(id1)
        self.repo.add(id2)

        all_ids = self.repo.get_all()

        assert all_ids[1].first_name == new_person_dict["first_name"]
        assert all_ids[2].first_name == from_csv_person_dict["first_name"]

class TestDigitalIDRepositoryCSV:
    """Tests for CSV save and load"""

    TEST_CSV_PATH = "test_digital_ids.csv"

    def setup_method(self) -> None:
        DigitalID._next_id = 1
        DigitalIDRepository.clear_instance()
        self.repo = DigitalIDRepository()

    def teardown_method(self) -> None:
        if os.path.exists(self.TEST_CSV_PATH):
            os.remove(self.TEST_CSV_PATH)

    def test_save_to_csv(self, monkeypatch) -> None:
        monkeypatch.setattr(self.repo, "_get_csv_path", lambda: self.TEST_CSV_PATH)
        id = DigitalID(new_person_dict)
        self.repo.add(id)
        self.repo.save_to_csv()
        assert os.path.exists(self.TEST_CSV_PATH)

        with open(self.TEST_CSV_PATH, "r") as file:
            lines = file.readlines()

        for key in new_person_dict.keys():
            assert key in lines[0]

        for value in new_person_dict.values():
            assert str(value) in lines[1]

    def test_load_from_csv_restores_data(self, monkeypatch) -> None:
        monkeypatch.setattr(self.repo, "_get_csv_path", lambda: self.TEST_CSV_PATH)
        id1 = DigitalID(new_person_dict)
        id2 = DigitalID(from_csv_person_dict)
        
        self.repo.add(id1)
        self.repo.add(id2)
        self.repo.save_to_csv()

        DigitalID._next_id = 1
        DigitalIDRepository.clear_instance()
        new_repo = DigitalIDRepository()
        monkeypatch.setattr(new_repo, "_get_csv_path", lambda: self.TEST_CSV_PATH)
        new_repo.load_from_csv()

        assert new_repo.get_from_id(1).first_name == new_person_dict["first_name"]
        assert new_repo.get_from_id(2).first_name == from_csv_person_dict["first_name"]

    def test_load_from_csv_updates_next_id(self, monkeypatch) -> None:
        monkeypatch.setattr(self.repo, "_get_csv_path", lambda: self.TEST_CSV_PATH)
        id1 = DigitalID(new_person_dict)
        id2 = DigitalID(from_csv_person_dict)
        self.repo.add(id1)
        self.repo.add(id2)
        self.repo.save_to_csv()

        DigitalID._next_id = 1
        DigitalIDRepository.clear_instance()
        new_repo = DigitalIDRepository()
        monkeypatch.setattr(new_repo, "_get_csv_path", lambda: self.TEST_CSV_PATH)
        new_repo.load_from_csv()
        assert DigitalID._next_id == 3
