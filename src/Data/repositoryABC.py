from abc import abstractmethod
from typing import Generic, TypeVar, Dict, List, Protocol
from Common.singleton import SingletonABCMeta
from Data import dataStorage

class HasID(Protocol):
    @property
    def id(self) -> int: ...

T = TypeVar("T", bound=HasID)

class RepositoryABC(Generic[T], metaclass=SingletonABCMeta):
    """Generic singleton base class for repositories"""

    def __init__(self) -> None:
        self._repository: Dict[int, T] = {}
        self._initialise()

    @abstractmethod
    def _initialise(self) -> None: pass

    def add(self, entity: T) -> None:
        if entity.id in self._repository:
            raise ValueError(f"{type(entity).__name__} with id {entity.id} already exists")
        self._repository[entity.id] = entity

    def get_from_id(self, id: int) -> T:
        return self._repository[id]

    def get_all(self) -> Dict[int, T]:
        return dict(self._repository)

    @abstractmethod
    def _get_csv_path(self) -> str: pass
    
    @abstractmethod
    def _get_csv_headers(self) -> List[str]: pass
    
    @abstractmethod
    def _get_rows_for_csv(self) -> List[List[str]]: pass
    
    @abstractmethod
    def _from_dict(self, attributes: Dict[str, str]) -> T: pass

    def _create_object_from_csv_row(self, row: List[str]) -> T:
        attributes = dict(zip(self._get_csv_headers(), row))
        return self._from_dict(attributes)

    def save_to_csv(self) -> None:
        path = self._get_csv_path()
        headers = self._get_csv_headers()
        rows = self._get_rows_for_csv()
        dataStorage.save_to_csv(path, headers, rows)
    
    def load_from_csv(self) -> None:
        path = self._get_csv_path()
        rows = dataStorage.load_from_csv(path)
        for row in rows:
            entity = self._create_object_from_csv_row(row)
            self.add(entity)
