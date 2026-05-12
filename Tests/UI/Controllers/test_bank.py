import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from UI.Controllers.bank import Bank

class TestBank:
    """Tests for Bank class properties and functionality"""

    def test_organisation_name(self) -> None:
        assert Bank.organisation_name() == "Bank"

    def test_accessible_attributes(self) -> None:
        expected_attributes = ["status", "address"]
        assert Bank.accessible_attributes() == expected_attributes

    def test_verifiable_attributes(self) -> None:
        assert Bank.verifiable_attributes() == []
