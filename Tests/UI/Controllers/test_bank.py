import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from UI.Controllers.bank import Bank

class TestBank:
    """Tests for Bank class properties and functionality"""

    def test_organisation_name(self) -> None:
        assert Bank.organisation_name() == "Bank"

    def test_allowed_attributes(self) -> None:
        expected_attributes = ["status", "first_name", "surname", "date_of_birth", "address"]
        assert Bank.allowed_attributes() == expected_attributes
