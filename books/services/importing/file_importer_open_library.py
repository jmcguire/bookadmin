import csv
import gzip
import json
from enum import IntEnum

from django.conf import settings
from django.db import DatabaseError, transaction

from books.models import (
    ProvenanceAuthor,
    ProvenanceEdition,
    ProvenanceImport,
    ProvenanceWork,
)

from .file_importer import FileImporter
from .results import FileImportStats


class OpenLibraryColumns(IntEnum):
    TYPE = 0
    EXTERNAL_ID = 1
    REVISION = 2
    MODIFIED = 3
    JSON = 4


class FileImporterOpenLibrary(FileImporter):
    def __init__(self, filename: str):
        self.filename: str = filename
        self.full_file_path = None
        self.contents: list = []
        self.provider = "openlibrary"
        self.success: int = 0
        self.failed: int = 0
        self.size: int = 0

    def check_file(self):
        file = settings.DOWNLOAD_DIR / self.filename
        file.resolve()
        if settings.DOWNLOAD_DIR != file.parent:
            return False

        if file.suffix != ".gz":
            return False

        self.full_file_path = file
        self.size = file.stat().st_size
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
                    # todo: only create if the external_id+revision doesn't already exist

                    if content["type"] == "/type/work":
                        ids = self.get_external_id_and_revision(content["data"])
                        if not ids:
                            self.failed += 1
                            continue
                        self.success += 1
                        ProvenanceWork.objects.create(
                            external_id=ids["external_id"],
                            revision=ids["revision"],
                            unprocessed_data=content["data"],
                            provenance_import=imp,
                        )

                    elif content["type"] == "/type/edition":
                        ids = self.get_external_id_and_revision(content["data"])
                        if not ids:
                            self.failed += 1
                            continue
                        self.success += 1
                        ProvenanceEdition.objects.create(
                            external_id=ids["external_id"],
                            revision=ids["revision"],
                            unprocessed_data=content["data"],
                            provenance_import=imp,
                        )

                    elif content["type"] == "/type/author":
                        ids = self.get_external_id_and_revision(content["data"])
                        if not ids:
                            self.failed += 1
                            continue
                        self.success += 1
                        ProvenanceAuthor.objects.create(
                            external_id=ids["external_id"],
                            revision=ids["revision"],
                            unprocessed_data=content["data"],
                            provenance_import=imp,
                        )

                    else:
                        print("unknown type: " + content["type"])
                        self.failed += 1

                imp.results = self.file_stats().model_dump()
                imp.save()

                self.imp = imp

        except DatabaseError as e:
            # todo dont do this, re-throw instead, let the api toss a 500
            print(f"Database error: {e}")
            return False

        return True

    def file_stats(self):
        return FileImportStats(
            size=self.size, lines=len(self.contents), success=self.success, failed=self.failed
        )

    def get_external_id_and_revision(self, data_json) -> dict | None:
        try:
            return {"external_id": data_json["key"], "revision": data_json["revision"]}
        except KeyError, IndexError, TypeError:
            return None
