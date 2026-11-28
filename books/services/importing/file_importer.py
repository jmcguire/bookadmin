from abc import ABC, abstractmethod
from typing import ClassVar

from books.models import ProvenanceImport

from .results import FileImportStats


class FileImporter(ABC):
    imp: ClassVar[ProvenanceImport | None] = None

    @abstractmethod
    def __init__(self, filename: str):
        pass

    @abstractmethod
    def check_file(self) -> bool:
        pass

    @abstractmethod
    def unzip_file(self) -> bool:
        pass

    @abstractmethod
    def load_file(self) -> bool:
        pass

    @abstractmethod
    def file_stats(self) -> FileImportStats:
        pass
