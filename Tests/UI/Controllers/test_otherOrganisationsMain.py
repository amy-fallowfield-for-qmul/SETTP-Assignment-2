import pytest
from Logic.service import DigitalIDService
from Logic.organisation import Organisation
from Data.DigitalID.digitalID import DigitalID
from Data.DigitalID.digitalIDRepository import DigitalIDRepository
from Data.Logging.logRepository import LogRepository
from Data.Logging.log import Action
from UI.Controllers.otherOrganisationsMain import OtherOrganisationMain
from Tests.shared_test_data import justification_person_dict, CENTRAL_AUTHORITY_ORG

class TestServicePermissionSystem:
    """Tests for the new permission-based query system in DigitalIDService"""

    @pytest.fixture
    def service(self) -> DigitalIDService:
        DigitalID._next_id = 1
        DigitalIDRepository.clear_instance()
        DigitalIDService.clear_instance()
        LogRepository.clear_instance()

        service = DigitalIDService()
        service.create_id(justification_person_dict, CENTRAL_AUTHORITY_ORG)
        return service

    def test_query_with_allowed_attribute(self, service: DigitalIDService) -> None:
        nhs = Organisation(name="NHS", accessible_attributes=("first_name", "surname"))
        result = service.query_attribute(1, "first_name", "Test query", nhs)
        assert result == justification_person_dict["first_name"]

    def test_query_with_forbidden_attribute(self, service: DigitalIDService) -> None:
        nhs = Organisation(name="NHS", accessible_attributes=("first_name", "surname"))
        with pytest.raises(ValueError, match="Access denied: NHS is not authorized to access 'date_of_birth' attribute"):
            service.query_attribute(1, "date_of_birth", "Unauthorized query", nhs)

    def test_permission_denied_creates_rejected_log(self, service: DigitalIDService) -> None:
        nhs = Organisation(name="NHS", accessible_attributes=("first_name",))

        try:
            service.query_attribute(1, "date_of_birth", "Unauthorized access attempt", nhs)
        except ValueError:
            pass

        logs = service.get_all_logs()
        assert len(logs) == 2

        failed_log = list(logs.values())[1]
        assert failed_log.accepted == False
        assert failed_log.organisation == "NHS"
        assert failed_log.action == Action.READ
        assert isinstance(failed_log.current_value, str)
        assert "Access denied" in failed_log.current_value

    def test_successful_query_creates_accepted_log(self, service: DigitalIDService) -> None:
        nhs = Organisation(name="NHS", accessible_attributes=("first_name", "surname"))
        service.query_attribute(1, "first_name", "Authorized query", nhs)

        logs = service.get_all_logs()
        read_log = list(logs.values())[1]
        assert read_log.accepted == True
        assert read_log.organisation == "NHS"
        assert read_log.action == Action.READ
        assert read_log.current_value == justification_person_dict["first_name"]

class TestOtherOrganisationAbstractClass:
    """Tests for the abstract OtherOrganisationMain base class"""

    def test_cannot_instantiate_abstract_class_directly(self) -> None:
        with pytest.raises(TypeError):
            OtherOrganisationMain()
