import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from UI.Controllers.hmrc import HMRC

class TestHMRC:
    """Tests for HMRC class properties and functionality"""

    def test_organisation_name(self) -> None:
        assert HMRC.organisation_name() == "HMRC"

    def test_accessible_attributes(self) -> None:
        expected_attributes = ["status", "address", "national_insurance"]
        assert HMRC.accessible_attributes() == expected_attributes
