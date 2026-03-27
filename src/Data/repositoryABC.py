from abc import ABC, abstractmethod
from Data.dataStorage import DataStorage
from typing import Union, Dict, List

class RepositoryABC(ABC):
    
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if not hasattr(self, '_initialised'):
            self._initialised = True
            self._storage = DataStorage()
            self._initialise()

    @abstractmethod
    def _initialise(self) -> None: pass

    @abstractmethod
    def add(self, object: object) -> None: pass

    @abstractmethod
    def get_all(self) -> Union[Dict, List]: pass

    @abstractmethod
    def _get_csv_path(self) -> str: pass
    
    @abstractmethod  
    def _get_csv_headers(self) -> List[str]: pass
    
    @abstractmethod
    def _get_rows_for_csv(self) -> List[List[str]]: pass
    
    @abstractmethod
    def _create_object_from_csv_row(self, row: List[str]): pass

    def save_to_csv(self) -> None:
        path = self._get_csv_path()
        headers = self._get_csv_headers()
        rows = self._get_rows_for_csv()
        self._storage.save_to_csv(path, headers, rows)
    
    def load_from_csv(self) -> None:
        path = self._get_csv_path()
        rows = self._storage.load_from_csv(path)
        for row in rows:
            object = self._create_object_from_csv_row(row)
            self.add(object)