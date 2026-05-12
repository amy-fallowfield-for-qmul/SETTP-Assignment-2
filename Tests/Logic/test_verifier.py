import pytest
from unittest.mock import Mock
from datetime import datetime
from Logic.verifier import Verifier
from Logic.service import DigitalIDService
from Data.Logging.log import Action
from Data.Logging.logRepository import LogRepository
from Data.DigitalID.digitalID import DigitalID
from Data.DigitalID.digitalIDRepository import DigitalIDRepository
from Tests.shared_test_data import new_person_dict, justification_person_dict

@pytest.fixture
def service() -> DigitalIDService:
    DigitalID._next_id = 1
    DigitalIDRepository.clear_instance()
    DigitalIDService.clear_instance()
    LogRepository.clear_instance()
    Verifier.clear_instance()
    return DigitalIDService()

@pytest.fixture
def verifier() -> Verifier:
    return Verifier()

def get_create_log() -> Mock:
    create_log = Mock()
    create_log.id_number = 1
    create_log.action = Action.CREATE
    create_log.timestamp = datetime(2026, 1, 1, 0, 0, 0)
    create_log.new_value = None
    create_log.current_value = id
    create_log.attribute = None
    return create_log

def get_suspend_log() -> Mock:
    suspend_log = Mock()
    suspend_log.id_number = 1
    suspend_log.action = Action.UPDATE
    suspend_log.timestamp = datetime(2026, 1, 2, 0, 0, 0)
    suspend_log.new_value = "suspended"
    suspend_log.current_value = "active"
    suspend_log.attribute = "status"
    return suspend_log

def get_active_log() -> Mock:
    active_log = Mock()
    active_log.id_number = 1
    active_log.action = Action.UPDATE
    active_log.timestamp = datetime(2026, 1, 3, 0, 0, 0)
    active_log.new_value = "active"
    active_log.current_value = "suspended"
    active_log.attribute = "status"
    return active_log

class TestVerifierVerifyIdentity:
    """Tests for verifying a Digital ID's identity via the verifier"""

    def test_verify_identity_match(self, service: DigitalIDService, verifier: Verifier) -> None:
        service.create_id(justification_person_dict)
        result = verifier.verify_identity(1, "John", "Smith", "2000-01-01", "Account opening", "Bank")
        assert result is True

    def test_verify_identity_mismatch(self, service: DigitalIDService, verifier: Verifier) -> None:
        service.create_id(justification_person_dict)
        result = verifier.verify_identity(1, "Alice", "Smith", "2000-01-01", "Account opening", "Bank")
        assert result is False

    def test_verify_identity_normalises_input(self, service: DigitalIDService, verifier: Verifier) -> None:
        service.create_id(justification_person_dict)
        result = verifier.verify_identity(1, "  john  ", "SMITH", "2000-01-01", "Account opening", "Bank")
        assert result is True

    def test_verify_identity_creates_log(self, service: DigitalIDService, verifier: Verifier) -> None:
        service.create_id(justification_person_dict)
        verifier.verify_identity(1, "John", "Smith", "2000-01-01", "Account opening", "Bank")
        logs = service.LOG_REPOSITORY.get_all()
        verify_log = list(logs.values())[1]
        assert verify_log.action == Action.VERIFY
        assert verify_log.attribute == "identity"
        assert verify_log.current_value == "True"

class TestVerifierVerifyMinimumAge:
    """Tests for verifying a Digital ID's minimum age via the verifier"""

    def test_verify_minimum_age_meets(self, service: DigitalIDService, verifier: Verifier) -> None:
        service.create_id(justification_person_dict)
        result = verifier.verify_minimum_age(1, 18, "ISA eligibility", "Bank")
        assert result is True

    def test_verify_minimum_age_does_not_meet(self, service: DigitalIDService, verifier: Verifier) -> None:
        service.create_id(justification_person_dict)
        result = verifier.verify_minimum_age(1, 99, "Pension eligibility", "Bank")
        assert result is False

    def test_verify_minimum_age_accepts_string_input(self, service: DigitalIDService, verifier: Verifier) -> None:
        service.create_id(justification_person_dict)
        result = verifier.verify_minimum_age(1, "18", "ISA eligibility", "Bank")
        assert result is True

    def test_verify_minimum_age_creates_log(self, service: DigitalIDService, verifier: Verifier) -> None:
        service.create_id(justification_person_dict)
        verifier.verify_minimum_age(1, 18, "ISA eligibility", "Bank")
        logs = service.LOG_REPOSITORY.get_all()
        verify_log = list(logs.values())[1]
        assert verify_log.action == Action.VERIFY
        assert verify_log.attribute == "minimum_age"
        assert verify_log.current_value == "True"
        assert verify_log.comparative_value == "18"

class TestVerifierVerifyAttribute:
    """Tests for verifying a single Digital ID attribute via the verifier"""

    def test_verify_attribute_match(self, service: DigitalIDService, verifier: Verifier) -> None:
        service.create_id(justification_person_dict)
        result = verifier.verify_attribute(1, "national_insurance", "AB123456C", "New hire", "Employer", ["national_insurance"])
        assert result is True

    def test_verify_attribute_mismatch(self, service: DigitalIDService, verifier: Verifier) -> None:
        service.create_id(justification_person_dict)
        result = verifier.verify_attribute(1, "national_insurance", "BC123456C", "New hire", "Employer", ["national_insurance"])
        assert result is False

    def test_verify_attribute_status_on_suspended(self, service: DigitalIDService, verifier: Verifier) -> None:
        service.create_id(justification_person_dict)
        service.update_id(1, "status", "suspended", "Investigation")
        result = verifier.verify_attribute(1, "status", "active", "Hiring check", "Employer", ["status"])
        assert result is False

    def test_verify_attribute_creates_log(self, service: DigitalIDService, verifier: Verifier) -> None:
        service.create_id(justification_person_dict)
        verifier.verify_attribute(1, "national_insurance", "AB123456C", "New hire", "Employer", ["national_insurance"])
        logs = service.LOG_REPOSITORY.get_all()
        verify_log = list(logs.values())[1]
        assert verify_log.action == Action.VERIFY
        assert verify_log.attribute == "national_insurance"
        assert verify_log.current_value == "True"

    def test_verify_attribute_access_denied(self, service: DigitalIDService, verifier: Verifier) -> None:
        service.create_id(justification_person_dict)
        with pytest.raises(ValueError, match="Access denied"):
            verifier.verify_attribute(1, "first_name", "John", "New hire", "Employer", ["national_insurance"])

class TestVerifierVerifySuspendedInPeriod:
    """Tests for verifying suspension history via the verifier"""

    def setup_method(self):
        LogRepository.clear_instance()
        DigitalIDRepository.clear_instance()
        Verifier.clear_instance()
        DigitalID._next_id = 1

        self.verifier = Verifier()
        self.verifier.LOG_REPOSITORY = Mock()

    def test_verify_suspended_in_period_no_suspension_during_period(self):
        self.verifier.LOG_REPOSITORY.get_all.return_value = {}
        assert self.verifier.verify_suspended_in_period("2026-01-01", "2026-01-02", 1, "Audit check", "HMRC") == False

    def test_verify_suspended_in_period_with_suspension_during_period(self):
        suspend_log = get_suspend_log()
        self.verifier.LOG_REPOSITORY.get_all.return_value = {1: suspend_log}
        assert self.verifier.verify_suspended_in_period("2026-01-01", "2026-01-03", 1, "Audit check", "HMRC") == True

    def test_verify_suspended_in_period_suspended_before_period(self):
        DigitalID(new_person_dict)
        mock_logs = {1: get_create_log(), 2: get_suspend_log()}
        self.verifier.LOG_REPOSITORY.get_all.return_value = mock_logs
        assert self.verifier.verify_suspended_in_period("2026-01-01", "2026-01-04", 1, "Audit check", "HMRC") == True

    def test_verify_suspended_in_period_suspended_and_activated_before_period(self):
        DigitalID(new_person_dict)
        mock_logs = {1: get_create_log(), 2: get_suspend_log(), 3: get_active_log()}
        self.verifier.LOG_REPOSITORY.get_all.return_value = mock_logs
        assert self.verifier.verify_suspended_in_period("2026-01-04", "2026-01-05", 1, "Audit check", "HMRC") == False

    def test_verify_suspended_in_period_no_logs_for_id(self):
        self.verifier.LOG_REPOSITORY.get_all.return_value = {}
        assert self.verifier.verify_suspended_in_period("2026-01-01", "2026-01-02", 999, "Audit check", "HMRC") == False

    def test_revoked_during_period_counts_as_suspended(self):
        revoke_log = Mock()
        revoke_log.id_number = 1
        revoke_log.action = Action.UPDATE
        revoke_log.timestamp = datetime(2026, 1, 15, 12, 0, 0)
        revoke_log.new_value = "revoked"
        revoke_log.current_value = "active"
        revoke_log.attribute = "status"
        self.verifier.LOG_REPOSITORY.get_all.return_value = {1: revoke_log}
        assert self.verifier.verify_suspended_in_period("2026-01-12", "2026-01-18", 1, "Audit check", "HMRC") == True

    def test_verify_suspended_in_period_creates_log_on_success(self):
        self.verifier.LOG_REPOSITORY.get_all.return_value = {}

        self.verifier.verify_suspended_in_period("2026-01-01", "2026-01-02", 1, "Audit check", "HMRC")

        self.verifier.LOG_REPOSITORY.add.assert_called_once()
        added_log = self.verifier.LOG_REPOSITORY.add.call_args[0][0]
        assert added_log.action == Action.VERIFY
        assert added_log.accepted is True
        assert added_log.attribute == "suspended_in_period"
        assert added_log.current_value == "False"
        assert added_log.comparative_value == "2026-01-01 to 2026-01-02"
        assert added_log.organisation == "HMRC"
        assert added_log.justification == "Audit check"
        assert added_log.id_number == 1

    def test_verify_suspended_in_period_creates_log_on_failure(self):
        self.verifier.LOG_REPOSITORY.get_all.side_effect = RuntimeError("Storage error")

        with pytest.raises(RuntimeError):
            self.verifier.verify_suspended_in_period("2026-01-01", "2026-01-02", 1, "Audit check", "HMRC")

        self.verifier.LOG_REPOSITORY.add.assert_called_once()
        added_log = self.verifier.LOG_REPOSITORY.add.call_args[0][0]
        assert added_log.action == Action.VERIFY
        assert added_log.accepted is False
        assert added_log.attribute == "suspended_in_period"
        assert added_log.current_value == "Storage error"
        assert added_log.organisation == "HMRC"
        assert added_log.justification == "Audit check"
        assert added_log.id_number == 1
