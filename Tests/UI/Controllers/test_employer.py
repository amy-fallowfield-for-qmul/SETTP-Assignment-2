import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from UI.Controllers.employer import Employer

class TestEmployer:
    """Tests for Employer class properties and functionality"""

    def test_organisation_name(self) -> None:
        assert Employer.organisation_name() == "Employer"

    def test_accessible_attributes(self) -> None:
        expected_attributes = ["status", "address"]
        assert Employer.accessible_attributes() == expected_attributes

    def test_verifiable_attributes(self) -> None:
        expected_attributes = ["national_insurance"]
        assert Employer.verifiable_attributes() == expected_attributes
