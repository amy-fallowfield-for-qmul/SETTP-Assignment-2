from abc import abstractmethod
from typing import Generic, TypeVar, Dict, List
from Common.singleton import SingletonABCMeta
from Data import dataStorage

T = TypeVar("T")

class RepositoryABC(Generic[T], metaclass=SingletonABCMeta):

    def __init__(self) -> None:
        self._initialise()

    @abstractmethod
    def _initialise(self) -> None: pass

    @abstractmethod
    def add(self, entity: T) -> None: pass

    @abstractmethod
    def get_from_id(self, id: int) -> T: pass

    @abstractmethod
    def get_all(self) -> Dict[int, T]: pass

    @abstractmethod
    def _get_csv_path(self) -> str: pass
    
    @abstractmethod
    def _get_csv_headers(self) -> List[str]: pass
    
    @abstractmethod
    def _get_rows_for_csv(self) -> List[List[str]]: pass
    
    @abstractmethod
    def _create_object_from_csv_row(self, row: List[str]) -> T: pass

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
