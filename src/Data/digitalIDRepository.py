from typing import Dict, List
from Data.digitalID import DigitalID
from constants import ID_PATH
from Data.repositoryABC import RepositoryABC
from Data.attributeRepository import AttributeRegistry

class DigitalIDRepository(RepositoryABC):
    """Singleton repository for storing and managing Digital IDs"""

    def _initialise(self) -> None:
        self._repository: Dict[int, DigitalID] = {}
        self._attribute_registry = AttributeRegistry()

    def add(self, digitalID: DigitalID) -> None:
        self._repository[digitalID.id] = digitalID

    def get_from_id(self, id: int) -> DigitalID:
        return self._repository[id]
    
    def get_all(self) -> Dict[int, DigitalID]:
        return self._repository

    def _get_csv_path(self) -> str:
        return ID_PATH

    def _get_csv_headers(self) -> List[str]:
        return self._attribute_registry.get_all_attributes()

    def _get_rows_for_csv(self) -> List[List[str]]:
        rows = []
        for digitalID in self._repository.values():
            row = []
            digital_id_dict = digitalID.to_dict()
            for attribute_name in self._attribute_registry.get_all_attributes():
                row.append(str(digital_id_dict[attribute_name]))
            rows.append(row)
        return rows

    def _create_object_from_csv_row(self, row: List[str]) -> DigitalID:
        attributes = {}
        attribute_names = self._attribute_registry.get_all_attributes()
        for i, attribute_name in enumerate(attribute_names):
            attributes[attribute_name] = row[i]
        return DigitalID(attributes)
