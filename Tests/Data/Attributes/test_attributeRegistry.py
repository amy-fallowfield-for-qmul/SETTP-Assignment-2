import pytest
from Data.Attributes.attributeRegistry import AttributeRegistry, CORE_ATTRIBUTE_OBJECTS
from Data.Attributes.attributeMetadata import AttributeMetadata, AttributeType
from Tests.shared_test_data import from_csv_person_dict

class TestAttributeRegistryCreation:
    """Tests for AttributeRegistry singleton constructor"""

    def test_create_registry_singleton(self) -> None:
        AttributeRegistry.clear_instance()
        registry1 = AttributeRegistry()
        registry2 = AttributeRegistry()
        assert registry1 is registry2

class TestAttributeRegistryAdd:
    """Tests for registering attributes"""

    def setup_method(self) -> None:
        AttributeRegistry.clear_instance()
        self._original_core_attributes = list(CORE_ATTRIBUTE_OBJECTS)

    def teardown_method(self) -> None:
        CORE_ATTRIBUTE_OBJECTS[:] = self._original_core_attributes
        AttributeRegistry.clear_instance()

    def test_register_new_attribute(self) -> None:
        current_attributes = {attribute.name for attribute in self._original_core_attributes}
        AttributeRegistry.clear_instance()

        test_attr = AttributeMetadata(
            name="test_field",
            display_name="Test Field",
            attribute_type=AttributeType.STRING,
            is_mutable=True,
            is_required_for_creation=False
        )
        CORE_ATTRIBUTE_OBJECTS.append(test_attr)

        updated = set(AttributeRegistry().get_all_attributes())
        assert "test_field" in updated
        assert current_attributes.issubset(updated)

class TestAttributeRegistryAddAndGet:
    """Tests for registering and retrieving attributes"""

    def setup_method(self) -> None:
        AttributeRegistry.clear_instance()
        self.registry = AttributeRegistry()

    def test_get_existing_attribute(self) -> None:
        attr = self.registry.get_attribute("first_name")
        assert attr.name == "first_name"
        assert attr.display_name == "First Name"
        assert attr.attribute_type == AttributeType.STRING
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
        AttributeRegistry.clear_instance()
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
        AttributeRegistry.clear_instance()
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
