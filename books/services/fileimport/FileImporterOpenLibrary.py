import csv
import gzip
import json
from enum import IntEnum

from django.conf import settings
from django.db import DatabaseError, transaction

from books.models import ProvenanceImport, ProvenanceWork
from books.services.fileimport.FileImportStats import FileImportStats
from books.services.fileimport.WorkInProvenance import WorkInProvenance


class OpenLibraryColumns(IntEnum):
    TYPE = 0
    EXTERNAL_ID = 1
    REVISION = 2
    MODIFIED = 3
    JSON = 4


class FileImporterOpenLibrary:
    def __init__(self, filename: str):
        self.filename: str = filename
        self.full_file_path = None
        self.contents: list[WorkInProvenance] = []
        self.imp: ProvenanceImport = None
        self.provider = "openlibrary"
        self.success: int = 0
        self.failed: int = 0

    def check_file(self):
        file = settings.DOWNLOAD_DIR / self.filename
        file.resolve()
        if settings.DOWNLOAD_DIR != file.parent:
            return False

        if file.suffix != ".gz":
            return False

        self.full_file_path = file
        return True

    def unzip_file(self):
        if not self.full_file_path:
            return False

        with gzip.open(self.full_file_path, "rt", encoding="utf-8", newline="") as f:
            reader = csv.reader(f, delimiter="\t")
            for r in reader:
                self.contents.append(
                    {
                        "type": r[OpenLibraryColumns.TYPE],
                        "data": json.loads(r[OpenLibraryColumns.JSON]),
                    }
                )

        return True

    def load_file(self):
        if not self.contents:
            return False

        try:
            with transaction.atomic():
                imp = ProvenanceImport.objects.create(
                    filename=self.filename, provider="openlibrary"
                )

                for content in self.contents:
                    if content["type"] == "/type/work":
                        work = convert_work(content["data"])
                        if not work:
                            self.failed += 1
                            continue
                        self.success += 1
                        ProvenanceWork.objects.create(
                            external_id=work.external_id,
                            revision=work.revision,
                            data=work.data.__dict__,
                            provenance_import=imp,
                        )
                    else:
                        print("unknown type: " + content["type"])
                        self.failed += 1

                imp.results = self.file_stats().__dict__
                imp.save()

                self.imp = imp
        except DatabaseError as e:
            print(f"Database error: {e}")
            return False

        return True

    def file_stats(self):
        return FileImportStats(0, len(self.contents), self.success, self.failed)


def convert_work(work_json) -> WorkInProvenance | None:
    workdata = WorkInProvenance()
    try:
        workdata.external_id = work_json.get("key", None)
        workdata.revision = work_json.get("revision", None)
        workdata.data.title = work_json["title"]
    except KeyError, IndexError, TypeError:
        return None

    try:
        if work_json["description"]["type"] == "/type/text":
            workdata.data.description = work_json["description"]["value"]
    except KeyError, IndexError, TypeError:
        pass

    try:
        year = work_json["first_publish_date"][-4:]
        if len(year) == 4 and year.isdigit():
            workdata.data.year_first_published = year
    except KeyError, IndexError, TypeError:
        pass

    try:
        if work_json["authors"][0]["type"]["key"] == "/type/author_role":
            workdata.data.author_id = work_json["authors"][0]["author"]["key"]
    except KeyError, IndexError, TypeError:
        pass

    return workdata
