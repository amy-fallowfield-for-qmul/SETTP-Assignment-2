import pytest
import os
import Data.digitalIDRepository as repo_module
import Logic.service as service_module
import constants
from Logic.service import DigitalIDService
from Data.digitalID import DigitalID, Status
from Data.digitalIDRepository import DigitalIDRepository

@pytest.fixture
def service() -> DigitalIDService:
    DigitalID._next_id = 1
    DigitalIDRepository._instance = None
    DigitalIDService._instance = None
    return DigitalIDService()

class TestServiceCreateID:
    """Tests for creating a Digital ID via the service"""

    def test_create_id(self, service: DigitalIDService) -> None:
        digital_id = service.create_id({"firstName": "John", "surname": "Smith", "dateOfBirth": "2000-01-01"})
        assert digital_id.id == 1
        assert digital_id.status == Status.ACTIVE
        assert digital_id.first_name == "John"
        assert digital_id.surname == "Smith"
        assert digital_id.date_of_birth == "2000-01-01"
        assert len(service.get_all()) == 1

class TestServiceGetAllIDs:
    """Tests for retrieving all Digital IDs"""

    def test_get_all_empty(self, service: DigitalIDService) -> None:
        assert service.get_all() == {}

    def test_get_all(self, service: DigitalIDService) -> None:
        service.create_id({"firstName": "John", "surname": "Smith", "dateOfBirth": "2000-01-01"})
        service.create_id({"firstName": "Bob", "surname": "Jones", "dateOfBirth": "2005-01-01"})
        assert len(service.get_all()) == 2

class TestServiceFilterIDs:
    """Tests for filtering Digital IDs by attributes"""

    def test_filter_by_attribute(self, service: DigitalIDService) -> None:
        service.create_id({"firstName": "John", "surname": "Smith", "dateOfBirth": "2000-01-01"})
        service.create_id({"firstName": "Bob", "surname": "Jones", "dateOfBirth": "2005-01-01"})
        filtered = service.get_filtered_ids({"firstName": "John"})
        assert len(filtered) == 1

    def test_filter_no_matches(self, service: DigitalIDService) -> None:
        service.create_id({"firstName": "John", "surname": "Smith", "dateOfBirth": "2000-01-01"})
        filtered = service.get_filtered_ids({"firstName": "Bob"})
        assert len(filtered) == 0

    def test_filter_case_insensitive_name(self, service: DigitalIDService) -> None:
        service.create_id({"firstName": "John", "surname": "Smith", "dateOfBirth": "2000-01-01"})
        assert len(service.get_filtered_ids({"firstName": "JOHN"})) == 1
        assert len(service.get_filtered_ids({"firstName": "john"})) == 1
        assert len(service.get_filtered_ids({"firstName": "jOhN"})) == 1

    def test_filter_case_insensitive_status(self, service: DigitalIDService) -> None:
        service.create_id({"firstName": "John", "surname": "Smith", "dateOfBirth": "2000-01-01"})
        assert len(service.get_filtered_ids({"status": "ACTIVE"})) == 1
        assert len(service.get_filtered_ids({"status": "Active"})) == 1

    def test_filter_invalid_field(self, service: DigitalIDService) -> None:
        with pytest.raises(ValueError, match="Invalid filter field"):
            service.get_filtered_ids({"badAttribute": "hello123"})

class TestServiceGetIDByNumber:
    """Tests for retrieving a Digital ID by its number"""

    def test_get_id_by_number(self, service: DigitalIDService) -> None:
        service.create_id({"firstName": "John", "surname": "Smith", "dateOfBirth": "2000-01-01"})
        assert service.get_id_by_number(1).first_name == "John"

    def test_get_id_not_found(self, service: DigitalIDService) -> None:
        with pytest.raises(ValueError, match="not found"):
            service.get_id_by_number(99)

class TestServiceUpdateID:
    """Tests for updating Digital ID attributes via the service"""

    def test_update_attribute(self, service: DigitalIDService) -> None:
        service.create_id({"firstName": "John", "surname": "Smith", "dateOfBirth": "2000-01-01"})
        service.update_id(1, "firstName", "Alicia")
        assert service.get_id_by_number(1).first_name == "Alicia"

    def test_update_nonexistent_id(self, service: DigitalIDService) -> None:
        with pytest.raises(ValueError, match="not found"):
            service.update_id(99, "firstName", "Alicia")

    def test_update_immutable_field_rejected(self, service: DigitalIDService) -> None:
        service.create_id({"firstName": "John", "surname": "Smith", "dateOfBirth": "2000-01-01"})
        with pytest.raises(ValueError, match="Cannot update field"):
            service.update_id(1, "dateOfBirth", "2010-01-01")

class TestServiceCSV:
    """Tests for loading and saving CSV data via the service"""

    TEST_CSV_PATH = "test_service_ids.csv"

    def setup_method(self) -> None:
        DigitalID._next_id = 1
        DigitalIDRepository._instance = None
        DigitalIDService._instance = None
        constants.ID_PATH = self.TEST_CSV_PATH
        repo_module.ID_PATH = self.TEST_CSV_PATH
        service_module.ID_PATH = self.TEST_CSV_PATH

    def teardown_method(self) -> None:
        if os.path.exists(self.TEST_CSV_PATH):
            os.remove(self.TEST_CSV_PATH)

    def test_save_and_load_csv(self) -> None:
        service = DigitalIDService()
        service.create_id({"firstName": "John", "surname": "Smith", "dateOfBirth": "2000-01-01"})
        service.save_csv_data()

        DigitalID._next_id = 1
        DigitalIDRepository._instance = None
        DigitalIDService._instance = None
        new_service = DigitalIDService()
        new_service.load_csv_data()

        assert new_service.get_id_by_number(1).first_name == "John"

    def test_load_csv_no_file(self, capsys) -> None:
        service = DigitalIDService()
        service.load_csv_data()
        captured = capsys.readouterr()
        assert "No existing data found" in captured.out

    def test_save_csv_empty_repository(self, capsys) -> None:
        service = DigitalIDService()
        service.save_csv_data()
        captured = capsys.readouterr()
        assert "No digital IDs to save" in captured.out
