import pytest
from Data.Attributes.attributeMetadata import AttributeMetadata, AttributeType

class TestAttributeType:
    """Tests for the AttributeType enum"""

    def test_attribute_type_values(self) -> None:
        assert AttributeType.STRING.value == "string"
        assert AttributeType.DATE.value == "date"
        assert AttributeType.STATUS.value == "status"
        assert AttributeType.INTEGER.value == "integer"
        assert AttributeType.NATIONAL_INSURANCE.value == "national_insurance"
        assert AttributeType.ADDRESS.value == "address"

    def test_attribute_type_members(self) -> None:
        assert set(AttributeType.__members__.keys()) == {"STRING", "DATE", "STATUS", "INTEGER", "NATIONAL_INSURANCE", "ADDRESS"}

class TestAttributeMetadataCreation:
    """Tests for AttributeMetadata constructor"""

    def test_create_metadata_with_all_parameters(self) -> None:
        metadata = AttributeMetadata(
            name="test_attr",
            display_name="Test Attribute",
            attribute_type=AttributeType.STRING,
            is_mutable=True,
            is_required_for_creation=False,
            input_prompt="Enter test value: "
        )
        
        assert metadata.name == "test_attr"
        assert metadata.display_name == "Test Attribute"
        assert metadata.attribute_type == AttributeType.STRING
        assert metadata.is_mutable == True
        assert metadata.is_required_for_creation == False
        assert metadata.input_prompt == "Enter test value: "

    def test_create_metadata_with_default_prompt(self) -> None:
        metadata = AttributeMetadata(
            name="test_attr",
            display_name="Test Attribute",
            attribute_type=AttributeType.STRING,
            is_mutable=True,
            is_required_for_creation=False,
        )

        assert metadata.input_prompt == "Enter test attribute: "

    def test_create_metadata_all_types(self) -> None:
        for attr_type in AttributeType:
            metadata = AttributeMetadata(
                name=f"test_{attr_type.value}",
                display_name=f"Test {attr_type.value.title()}",
                attribute_type=attr_type,
                is_mutable=True,
                is_required_for_creation=False
            )
            assert metadata.attribute_type == attr_type

class TestAttributeMetadataProperties:
    """Tests for AttributeMetadata properties"""

    def setup_method(self) -> None:
        self.metadata = AttributeMetadata(
            name="test_attr",
            display_name="Test Attribute",
            attribute_type=AttributeType.STRING,
            is_mutable=True,
            is_required_for_creation=False,
            input_prompt="Enter test value: "
        )

    def test_get_name(self) -> None:
        assert self.metadata.name == "test_attr"

    def test_get_display_name(self) -> None:
        assert self.metadata.display_name == "Test Attribute"

    def test_get_type(self) -> None:
        assert self.metadata.attribute_type == AttributeType.STRING

    def test_get_is_mutable(self) -> None:
        assert self.metadata.is_mutable == True

    def test_get_is_required_for_creation(self) -> None:
        assert self.metadata.is_required_for_creation == False

    def test_get_input_prompt(self) -> None:
        assert self.metadata.input_prompt == "Enter test value: "
