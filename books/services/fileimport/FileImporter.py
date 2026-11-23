from abc import abstractmethod

from books.services.fileimport.FileImportStats import FileImportStats
from books.services.fileimport.WorkInProvenance import WorkInProvenance


class FileImporter:
    # todo define abstract parameters provider, imp
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
