import pytest
from Logic.service import DigitalIDService
from Data.digitalID import DigitalID
from Data.digitalIDRepository import DigitalIDRepository
from Data.logRepository import LogRepository
from Data.log import Log, Action
from otherOrganisationsMain import OtherOrganisationMain

class TestServicePermissionSystem:
    """Tests for the new permission-based query system in DigitalIDService"""

    @pytest.fixture
    def service(self) -> DigitalIDService:
        DigitalID._next_id = 1
        DigitalIDRepository._instance = None
        DigitalIDService._instance = None
        LogRepository._instance = None

        service = DigitalIDService()
        service.create_id({
            "firstName": "John", 
            "surname": "Smith", 
            "dateOfBirth": "2000-01-01", 
            "justification": "Test setup"
        })
        return service

    def test_query_with_no_restrictions(self, service: DigitalIDService) -> None:
        result = service.query_attribute(1, "firstName", "Test query", "Test Org")
        assert result == "John"

    def test_query_with_allowed_attribute(self, service: DigitalIDService) -> None:
        allowed = ["firstName", "surname"]
        result = service.query_attribute(1, "firstName", "Test query", "NHS", allowed)
        assert result == "John"

    def test_query_with_forbidden_attribute(self, service: DigitalIDService) -> None:
        allowed = ["firstName", "surname"]
        with pytest.raises(ValueError, match="Access denied: NHS is not authorized to access 'dateOfBirth' attribute"):
            service.query_attribute(1, "dateOfBirth", "Unauthorized query", "NHS", allowed)

    def test_permission_denied_creates_rejected_log(self, service: DigitalIDService) -> None:
        allowed = ["firstName"]
        
        try:
            service.query_attribute(1, "dateOfBirth", "Unauthorized access attempt", "NHS", allowed)
        except ValueError:
            pass
        
        logs = service.get_all_logs()
        assert len(logs) == 2
        
        failed_log = list(logs.values())[1]
        assert failed_log.accepted == False
        assert failed_log.organisation == "NHS"
        assert failed_log.action == Action.READ
        assert "Access denied" in failed_log.current_value

    def test_successful_query_creates_accepted_log(self, service: DigitalIDService) -> None:
        allowed = ["firstName", "surname"]
        service.query_attribute(1, "firstName", "Authorized query", "NHS", allowed)
        
        logs = service.get_all_logs()
        read_log = list(logs.values())[1]
        assert read_log.accepted == True
        assert read_log.organisation == "NHS"
        assert read_log.action == Action.READ
        assert read_log.current_value == "John"

class TestOtherOrganisationAbstractClass:
    """Tests for the abstract OtherOrganisationMain base class"""

    def test_cannot_instantiate_abstract_class_directly(self) -> None:
        with pytest.raises(TypeError):
            OtherOrganisationMain()
