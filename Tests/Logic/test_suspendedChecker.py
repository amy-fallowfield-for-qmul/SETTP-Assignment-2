import pytest
from unittest.mock import Mock
from datetime import datetime
from Logic.suspendedChecker import SuspendedChecker
from Data.Logging.log import Action
from Data.Logging.logRepository import LogRepository
from Data.DigitalID.digitalID import DigitalID
from Data.DigitalID.digitalIDRepository import DigitalIDRepository
from Tests.shared_test_data import new_person_dict

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

def get_revoke_log() -> Mock:
    revoke_log = Mock()
    revoke_log.id_number = 1
    revoke_log.action = Action.UPDATE
    revoke_log.timestamp = datetime(2026, 1, 4, 0, 0, 0)
    revoke_log.new_value = "active"
    revoke_log.current_value = "suspended"
    revoke_log.attribute = "status"

    return revoke_log

class TestSuspendedChecker:
    """Tests for SuspendedChecker"""

    def setup_method(self):
        LogRepository._instance = None
        DigitalIDRepository._instance = None
        DigitalID._next_id = 1
        
        self.checker = SuspendedChecker()
        self.checker.LOG_REPOSITORY = Mock()

    def test_id_suspended_in_period_no_suspension_during_period(self):
        self.checker.LOG_REPOSITORY.get_all.return_value = {}
        
        assert self.checker.id_suspended_in_period("2026-01-01", "2026-01-02", 1) == False


    def test_id_suspended_in_period_with_suspension_during_period(self):
        suspend_log = get_suspend_log()
        
        mock_logs = {1: suspend_log}
        self.checker.LOG_REPOSITORY.get_all.return_value = mock_logs

        assert self.checker.id_suspended_in_period("2026-01-01", "2026-01-03", 1) == True

    def test_id_suspended_in_period_suspended_before_period(self):
        id = DigitalID(new_person_dict)

        create_log = get_create_log()  
        suspend_log = get_suspend_log()
        
        mock_logs = {1: create_log, 2: suspend_log}
        self.checker.LOG_REPOSITORY.get_all.return_value = mock_logs
        
        assert self.checker.id_suspended_in_period("2026-01-01", "2026-01-04", 1) == True

    def test_id_suspended_in_period_suspended_and_activated_before_period(self):
        id = DigitalID(new_person_dict)

        create_log = get_create_log()
        suspend_log = get_suspend_log()
        active_log = get_active_log()
        
        mock_logs = {1: create_log, 2: suspend_log, 3: active_log}
        self.checker.LOG_REPOSITORY.get_all.return_value = mock_logs
        
        assert self.checker.id_suspended_in_period("2026-01-04", "2026-01-05", 1) == False


    def test_id_suspended_in_period_no_logs_for_id(self):
        self.checker.LOG_REPOSITORY.get_all.return_value = {}
        assert self.checker.id_suspended_in_period("2026-01-01", "2026-01-02", 999) == False

    def test_id_revoked_during_period_counts_as_suspended(self):
        """Test that revoked status is treated the same as suspended"""
        revoke_log = Mock()
        revoke_log.id_number = 1
        revoke_log.action = Action.UPDATE
        revoke_log.timestamp = datetime(2026, 1, 15, 12, 0, 0)
        revoke_log.new_value = "revoked"
        revoke_log.current_value = "active"
        revoke_log.attribute = "status"
        
        mock_logs = {1: revoke_log}
        self.checker.LOG_REPOSITORY.get_all.return_value = mock_logs

        assert self.checker.id_suspended_in_period("2026-01-12", "2026-01-18", 1) == True
