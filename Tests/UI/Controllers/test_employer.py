import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from UI.Controllers.employer import Employer

class TestEmployer:
    """Tests for Employer class properties and functionality"""

    def test_organisation_name(self) -> None:
        assert Employer.organisation_name() == "Employer"

    def test_allowed_attributes(self) -> None:
        expected_attributes = ["status", "first_name", "surname", "date_of_birth", "address", "national_insurance"]
        assert Employer.allowed_attributes() == expected_attributes
