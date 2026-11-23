import csv
import gzip
import json
from datetime import datetime
from enum import IntEnum

from django.conf import settings
from django.db import DatabaseError, transaction

from books.models import (
    ProvenanceAuthor,
    ProvenanceEdition,
    ProvenanceImport,
    ProvenanceWork,
)
from books.services.fileimport.data_in_provenance import (
    AuthorInProvenance,
    EditionInProvenance,
    WorkInProvenance,
)
from books.services.fileimport.FileImportStats import FileImportStats


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
                    # todo: only create if the external_id+revision doesn't already exist

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
                    elif content["type"] == "/type/edition":
                        edition = convert_edition(content["data"])
                        if not edition:
                            self.failed += 1
                            continue
                        self.success += 1
                        ProvenanceEdition.objects.create(
                            external_id=edition.external_id,
                            revision=edition.revision,
                            data=edition.data.__dict__,
                            provenance_import=imp,
                        )
                    elif content["type"] == "/type/author":
                        author = convert_author(content["data"])
                        if not author:
                            self.failed += 1
                            continue
                        self.success += 1
                        ProvenanceAuthor.objects.create(
                            external_id=author.external_id,
                            revision=author.revision,
                            data=author.data.__dict__,
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
    work = WorkInProvenance()
    try:
        work.external_id = work_json["key"]
        work.revision = work_json["revision"]
        work.data.title = work_json["title"]
    except KeyError, IndexError, TypeError:
        return None

    try:
        if work_json["description"]["type"] == "/type/text":
            work.data.description = work_json["description"]["value"]
    except KeyError, IndexError, TypeError:
        pass

    try:
        year = work_json["first_publish_date"][-4:]
        if len(year) == 4 and year.isdigit():
            work.data.year_first_published = year
    except KeyError, IndexError, TypeError:
        pass

    try:
        if work_json["authors"][0]["type"]["key"] == "/type/author_role":
            work.data.author_id = work_json["authors"][0]["author"]["key"]
    except KeyError, IndexError, TypeError:
        pass

    return work


def convert_edition(edition_json) -> EditionInProvenance | None:
    edition = EditionInProvenance()
    try:
        edition.external_id = edition_json["key"]
        edition.revision = edition_json["revision"]
        edition.data.title = edition_json["title"]
    except KeyError, IndexError, TypeError:
        return None

    try:
        # todo could have multiple, see edition /books/OL17721466M
        if edition_json.get["contributor"][0]["role"] == "Translator":
            edition.data.translator = edition_json.get["contributor"][0]["name"]
    except KeyError, IndexError, TypeError:
        pass

    edition.data.year_published = edition_json.get("publish_date", None)

    edition.data.publisher = edition_json.get("publishers", [])[0]
    # todo is this ever multiple?

    edition.data.pages = edition_json.get("number_of_pages", 0)

    try:
        edition.data.language = edition_json.get["languages"][0]["key"]
        # this might not match the work language, even if there's no translator listed, should deal with that later
    except KeyError, IndexError, TypeError:
        pass

    try:
        edition.data.work = edition_json["works"][0]["key"]
        # for the edition-to-work table
    except KeyError, IndexError, TypeError:
        pass

    if edition_json.get("isbn_13", None):
        edition.data.language.append(edition_json["isbn_13"])
    if edition_json.get("identifiers", None):
        edition.data.language.extend(edition_json["identifiers"])

    edition_json["subtitle"]

    # other fields to consider later
    # edition_json["other_titles"]
    # edition_json["physical_format"]
    # edition_json["publish_country"]
    # edition_json["edition_name"]
    # edition_json["by_statement"] how the byline appears

    return edition


def convert_author(author_json) -> AuthorInProvenance | None:
    author = AuthorInProvenance()
    try:
        author.external_id = author_json["key"]
        author.revision = author_json["revision"]
        author.data.name = author_json["name"]  # or author_json["personal_name"]
    except KeyError, IndexError, TypeError:
        return None

    author.data.bio = author_json.get("bio", "")

    try:
        date_obj = datetime.strptime(author_json["birth_date"], "%d %B %Y")
        author.data.birthday = date_obj.strftime("%Y-%m-%d")
    except KeyError, IndexError, TypeError:
        pass

    try:
        date_obj = datetime.strptime(author_json["death_date"], "%d %B %Y")
        author.data.deathday = date_obj.strftime("%Y-%m-%d")
    except KeyError, IndexError, TypeError:
        pass

    # author.data.given_name = ""
    # author.data.family_name = ""
    # author.data.nationality = []
    # author.data.language = []

    return author
