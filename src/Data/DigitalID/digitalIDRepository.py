from typing import Dict, List
from .digitalID import DigitalID
from Config.constants import ID_PATH
from ..repositoryABC import RepositoryABC
from ..Attributes.attributeRegistry import AttributeRegistry

class DigitalIDRepository(RepositoryABC[DigitalID]):
    """Singleton repository for storing and managing Digital IDs"""

    def _initialise(self) -> None:
        self._repository: Dict[int, DigitalID] = {}
        self._attribute_registry = AttributeRegistry()

    def get_from_id(self, id: int) -> DigitalID:
        try:
            return super().get_from_id(id)
        except KeyError:
            raise ValueError(f"DigitalID with id {id} not found")

    def _get_csv_path(self) -> str:
        return ID_PATH

    def _get_csv_headers(self) -> List[str]:
        return self._attribute_registry.get_all_attributes()

    def _get_rows_for_csv(self) -> List[List[str]]:
        rows: List[List[str]] = []
        for digital_id in self._repository.values():
            row: List[str] = []
            digital_id_dict = digital_id.to_dict()
            for attribute_name in self._attribute_registry.get_all_attributes():
                row.append(str(digital_id_dict[attribute_name]))
            rows.append(row)
        return rows

    def _from_dict(self, attributes: Dict[str, str]) -> DigitalID:
        return DigitalID(attributes)
