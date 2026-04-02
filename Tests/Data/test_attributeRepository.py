import pytest
from Data.attributeRepository import AttributeRegistry
from Data.attributeMetadata import AttributeMetadata, AttributeType

from_csv_person_dict = {
    "id": 2,
    "status": "active",
    "first_name": "Alice",
    "surname": "Johnson",
    "date_of_birth": "1995-05-15"
}

class TestAttributeRegistryCreation:
    """Tests for AttributeRegistry singleton constructor"""

    def test_create_registry_singleton(self) -> None:
        AttributeRegistry._instance = None
        registry1 = AttributeRegistry()
        registry2 = AttributeRegistry()
        assert registry1 is registry2

class TestAttributeRegistryAddAndGet:
    """Tests for registering and retrieving attributes"""

    def setup_method(self) -> None:
        AttributeRegistry._instance = None
        self.registry = AttributeRegistry()

    def test_register_new_attribute(self) -> None:
        test_attr = AttributeMetadata(
            name="test_field",
            display_name="Test Field",
            attribute_type=AttributeType.STRING,
            is_mutable=True,
            is_required_for_creation=False
        )
        
        initial_count = len(self.registry.get_all_attributes())
        self.registry.register_attribute(test_attr)
        
        assert len(self.registry.get_all_attributes()) == initial_count + 1
        assert "test_field" in self.registry.get_all_attributes()

    def test_get_existing_attribute(self) -> None:
        attr = self.registry.get_attribute("first_name")
        assert attr.name == "first_name"
        assert attr.display_name == "First Name"
        assert attr.type == AttributeType.STRING
        assert attr.is_mutable == True
        assert attr.is_required_for_creation == True
        assert attr.input_prompt == "Enter first name: "

    def test_get_unknown_attribute_raises_error(self) -> None:
        with pytest.raises(ValueError, match="Unknown attribute: nonexistent"):
            self.registry.get_attribute("nonexistent")

    def test_get_all_attributes(self) -> None:
        all_attrs = self.registry.get_all_attributes()

        for attribute in from_csv_person_dict.keys():
            assert attribute in all_attrs

class TestAttributeRegistryFiltering:
    """Tests for attribute filtering methods"""

    def setup_method(self) -> None:
        AttributeRegistry._instance = None
        self.registry = AttributeRegistry()

    def test_get_required_for_creation(self) -> None:
        required = self.registry.get_required_for_creation()
        assert isinstance(required, list)
        assert "first_name" in required
        assert "id" not in required

    def test_get_mutable_attributes(self) -> None:
        mutable = self.registry.get_mutable_attributes()
        assert isinstance(mutable, list)
        assert "first_name" in mutable
        assert "date_of_birth" not in mutable

    def test_get_queryable_attributes(self) -> None:
        queryable = self.registry.get_queryable_attributes()
        assert isinstance(queryable, list)
        assert "first_name" in queryable
        assert "id" not in queryable

class TestAttributeRegistryUtilities:
    """Tests for utility methods"""

    def setup_method(self) -> None:
        AttributeRegistry._instance = None
        self.registry = AttributeRegistry()

    def test_get_input_prompt(self) -> None:
        prompt = self.registry.get_input_prompt("first_name")
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert "first name" in prompt.lower()

    def test_get_display_name(self) -> None:
        display_name = self.registry.get_display_name("first_name")
        assert isinstance(display_name, str)
        assert display_name == "First Name"

    def test_get_input_prompt_unknown_attribute(self) -> None:
        with pytest.raises(ValueError, match="Unknown attribute"):
            self.registry.get_input_prompt("nonexistent")

    def test_get_display_name_unknown_attribute(self) -> None:
        with pytest.raises(ValueError, match="Unknown attribute"):
            self.registry.get_display_name("nonexistent")
