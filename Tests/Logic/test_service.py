import pytest
import os
import Data.DigitalID.digitalIDRepository as repo_module
import Logic.service as service_module
from Config import constants
from Logic.service import DigitalIDService
from Data.DigitalID.digitalID import DigitalID, Status
from Data.DigitalID.digitalIDRepository import DigitalIDRepository
from Data.Logging.log import Action
from Data.Logging.logRepository import LogRepository
from Data.Attributes.attributeRegistry import AttributeRegistry
from Tests.shared_test_data import justification_person_dict

@pytest.fixture
def service() -> DigitalIDService:
    DigitalID._next_id = 1
    DigitalIDRepository.clear_instance()
    DigitalIDService.clear_instance()
    LogRepository.clear_instance()
    return DigitalIDService()

class TestServiceCreateID:
    """Tests for creating a Digital ID via the service"""

    def test_create_id(self, service: DigitalIDService) -> None:
        digital_id = service.create_id(justification_person_dict)
        id_dict = digital_id.to_dict()

        for key, value in justification_person_dict.items():
            if key != "justification":
                assert id_dict[key] == value
        assert len(service.get_all_ids()) == 1

    def test_create_id_creates_log(self, service: DigitalIDService) -> None:
        digital_id = service.create_id(justification_person_dict)
        logs = service.LOG_REPOSITORY.get_all()
        assert len(logs) == 1
        create_log = list(logs.values())[0]
        assert create_log.action == Action.CREATE
        assert create_log.id_number == digital_id.id
        assert create_log.organisation == "Central Authority"
        assert create_log.justification == "New Registration"
        assert create_log.current_value.first_name == justification_person_dict["first_name"]
        assert create_log.new_value is None

class TestServiceGetAllIDs:
    """Tests for retrieving all Digital IDs"""

    def test_get_all_empty(self, service: DigitalIDService) -> None:
        assert service.get_all_ids() == {}

    def test_get_all(self, service: DigitalIDService) -> None:
        service.create_id(justification_person_dict)
        id2 = justification_person_dict.copy()
        id2["justification"] = "Second creation"
        service.create_id(id2)
        assert len(service.get_all_ids()) == 2

class TestServiceFilterIDs:
    """Tests for filtering Digital IDs by attributes"""

    def test_filter_by_attribute(self, service: DigitalIDService) -> None:
        service.create_id(justification_person_dict)
        id2 = justification_person_dict.copy()
        id2["first_name"] = "DifferentName"
        id2["justification"] = "Second creation"
        service.create_id(id2)
        filtered = service.get_filtered_ids({"first_name": justification_person_dict["first_name"]})
        assert len(filtered) == 1

    def test_filter_no_matches(self, service: DigitalIDService) -> None:
        service.create_id(justification_person_dict)
        filtered = service.get_filtered_ids({"first_name": "FakeName"})
        assert len(filtered) == 0

    def test_filter_case_insensitive_name(self, service: DigitalIDService) -> None:
        service.create_id(justification_person_dict)
        uppercase_name = justification_person_dict["first_name"].upper()
        lowercase_name = justification_person_dict["first_name"].lower()

        assert len(service.get_filtered_ids({"first_name": uppercase_name})) == 1
        assert len(service.get_filtered_ids({"first_name": lowercase_name})) == 1

    def test_filter_case_insensitive_status(self, service: DigitalIDService) -> None:
        service.create_id(justification_person_dict)
        assert len(service.get_filtered_ids({"status": "ACTIVE"})) == 1
        assert len(service.get_filtered_ids({"status": "Active"})) == 1

    def test_filter_invalid_field(self, service: DigitalIDService) -> None:
        with pytest.raises(ValueError, match="Invalid filter field"):
            service.get_filtered_ids({"badAttribute": "hello123"})

class TestServiceFilterLogs:
    """Tests for filtering logs by attributes"""

    def test_filter_by_attribute(self, service: DigitalIDService) -> None:
        service.create_id(justification_person_dict)
        id2 = justification_person_dict.copy()
        id2["justification"] = "Second creation"
        service.create_id(id2)
        filtered = service.get_filtered_logs({"digitalID": "1"})
        assert len(filtered) == 1

class TestServiceGetIDByNumber:
    """Tests for retrieving a Digital ID by its number"""

    def test_get_id_by_number(self, service: DigitalIDService) -> None:
        service.create_id(justification_person_dict)
        assert service.get_id_by_number(1).first_name == justification_person_dict["first_name"]

    def test_get_id_not_found(self, service: DigitalIDService) -> None:
        with pytest.raises(ValueError, match="not found"):
            service.get_id_by_number(99)

class TestServiceQueryAttribute:
    """Tests for querying a Digital ID attribute via the service"""

    central_authority_attributes = AttributeRegistry().get_queryable_attributes()

    def test_query_attribute(self, service: DigitalIDService) -> None:
        service.create_id(justification_person_dict)
        result = service.query_attribute(1, "first_name", "External audit", "Central Authority", self.central_authority_attributes)
        assert result == "John"

    def test_query_attribute_creates_log(self, service: DigitalIDService) -> None:
        service.create_id(justification_person_dict)
        service.query_attribute(1, "status", "Status verification", "Central Authority", self.central_authority_attributes)
        
        logs = service.LOG_REPOSITORY.get_all()
        assert len(logs) == 2
        query_log = list(logs.values())[1]
        assert query_log.action == Action.READ
        assert query_log.current_value == "active"
        assert query_log.new_value is None
        assert query_log.justification == "Status Verification"
        assert query_log.organisation == "Central Authority"

    def test_query_attribute_not_found(self, service: DigitalIDService) -> None:
        with pytest.raises(ValueError, match="not found"):
            service.query_attribute(99, "first_name", "External audit", "Central Authority", self.central_authority_attributes)

class TestServiceUpdateID:
    """Tests for updating Digital ID attributes via the service"""

    def test_update_attribute(self, service: DigitalIDService) -> None:
        service.create_id(justification_person_dict)
        service.update_id(1, "first_name", "Alicia", "Name change requested")
        assert service.get_id_by_number(1).first_name == "Alicia"

    def test_update_creates_log(self, service: DigitalIDService) -> None:
        service.create_id(justification_person_dict)
        service.update_id(1, "first_name", "Alicia", "Name change requested")
        
        logs = service.LOG_REPOSITORY.get_all()
        assert len(logs) == 2
        update_log = list(logs.values())[1]
        assert update_log.action == Action.UPDATE
        assert update_log.current_value == "John"
        assert update_log.new_value == "Alicia"
        assert update_log.justification == "Name Change Requested"

    def test_update_nonexistent_id(self, service: DigitalIDService) -> None:
        with pytest.raises(ValueError, match="not found"):
            service.update_id(99, "first_name", "Alicia", "Name change")

    def test_update_immutable_field_rejected(self, service: DigitalIDService) -> None:
        service.create_id(justification_person_dict)
        with pytest.raises(ValueError, match="is immutable and cannot be updated"):
            service.update_id(1, "date_of_birth", "2010-01-01", "Date correction")

class TestServiceCSV:
    """Tests for loading and saving CSV data via the service"""

    TEST_CSV_PATH = "test_service_ids.csv"

    def setup_method(self) -> None:
        DigitalID._next_id = 1
        DigitalIDRepository.clear_instance()
        DigitalIDService.clear_instance()
        constants.ID_PATH = self.TEST_CSV_PATH
        repo_module.ID_PATH = self.TEST_CSV_PATH
        service_module.ID_PATH = self.TEST_CSV_PATH

    def teardown_method(self) -> None:
        if os.path.exists(self.TEST_CSV_PATH):
            os.remove(self.TEST_CSV_PATH)

    def test_save_and_load_csv(self) -> None:
        service = DigitalIDService()
        service.create_id(justification_person_dict)
        service.save_csv_data()

        DigitalID._next_id = 1
        DigitalIDRepository.clear_instance()
        DigitalIDService.clear_instance()
        new_service = DigitalIDService()
        new_service.load_csv_data()

        assert new_service.get_id_by_number(1).first_name == justification_person_dict["first_name"]

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
