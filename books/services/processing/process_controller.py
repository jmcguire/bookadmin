from abc import ABC, abstractmethod
from datetime import datetime

import isbnlib

from books.common import CatalogType
from books.models import (
    ProcessedAuthor,
    ProcessedEdition,
    ProcessedWork,
    ProvenanceAuthor,
    ProvenanceEdition,
    ProvenanceWork,
)

from .processed_data_schemas import (
    ProcessedAuthorData,
    ProcessedCatalogType,
    ProcessedEditionData,
    ProcessedWorkData,
)
from .results import ProcessingStats


class ProcessCatalogType(ABC):
    @abstractmethod
    def process(self, id: int) -> bool:
        pass

    @abstractmethod
    def convert(self, json: dict) -> ProcessedCatalogType | None:
        pass


# todo: convert the "return False" into a structured error message


class Process:
    def __init__(self):
        self.process_author = ProcessAuthor()
        self.process_edition = ProcessEdition()
        self.process_work = ProcessWork()

    def from_imp(self, import_id: int) -> ProcessingStats:
        stats = ProcessingStats()

        for catalogtype in CatalogType:
            results = self.from_type_from_import(import_id, catalogtype)
            stats.success += results.success
            stats.failure += results.failure

        return stats

    def from_type(self, catalogtype: CatalogType) -> ProcessingStats:
        stats = ProcessingStats()

        match catalogtype:
            case CatalogType.AUTHOR:
                for id in ProvenanceAuthor.objects.ids():
                    if self.process_author.process(id):
                        stats.success += 1
                    else:
                        stats.failure += 1
            case CatalogType.WORK:
                for id in ProvenanceWork.objects.ids():
                    if self.process_work.process(id):
                        stats.success += 1
                    else:
                        stats.failure += 1
            case CatalogType.EDITION:
                for id in ProvenanceEdition.objects.ids():
                    if self.process_edition.process(id):
                        stats.success += 1
                    else:
                        stats.failure += 1

        return stats

    def from_type_from_import(self, import_id: int, catalogtype: CatalogType) -> ProcessingStats:
        stats = ProcessingStats()

        match catalogtype:
            case CatalogType.AUTHOR:
                for id in ProvenanceAuthor.objects.ids_by_import(import_id):
                    if self.process_author.process(id):
                        stats.success += 1
                    else:
                        stats.failure += 1
            case CatalogType.WORK:
                for id in ProvenanceWork.objects.ids_by_import(import_id):
                    if self.process_work.process(id):
                        stats.success += 1
                    else:
                        stats.failure += 1
            case CatalogType.EDITION:
                for id in ProvenanceEdition.objects.ids_by_import(import_id):
                    if self.process_edition.process(id):
                        stats.success += 1
                    else:
                        stats.failure += 1

        return stats

    def from_single(self, catalogtype: CatalogType, id: int) -> ProcessingStats:
        match catalogtype:
            case CatalogType.AUTHOR:
                return self.process_author.process(id)
            case CatalogType.WORK:
                return self.process_work.process(id)
            case CatalogType.EDITION:
                return self.process_edition.process(id)


class ProcessAuthor(ProcessCatalogType):
    def __init__(self):
        pass

    def process(self, id: int) -> bool:
        provenance = ProvenanceAuthor.objects.get(pk=id)
        if not provenance:
            return False

        data = self.convert(provenance.unprocessed_data)
        if not data:
            return False

        ProcessedAuthor.objects.update_or_create(
            provenance_author=provenance,
            defaults={"data": data.model_dump(), "record_title": data.name},
        )

        return True

    def convert(self, author_json: dict | None) -> ProcessedAuthorData | None:
        # https://github.com/internetarchive/openlibrary-client/blob/master/olclient/schemata/author.schema.json
        if not author_json:
            return None

        author = ProcessedAuthorData()
        try:
            author.external_id = author_json["key"]
            author.revision = author_json["revision"]
            author.name = author_json["name"]  # or author_json["personal_name"]
        except KeyError, IndexError, TypeError, ValueError:
            return None

        # get the given name and family name
        if "," in author.name:
            author.family_name, author.given_name = author.name.split(",", 1)
        elif " " in author.name:
            author.family_name, author.given_name = author.name.split(" ", 1)
        else:
            author.family_name = author.name
            author.given_name = ""

        author.family_name.strip()
        author.given_name.strip()

        author.bio = author_json.get("bio", "")

        try:
            date_obj = datetime.strptime(author_json["birth_date"], "%d %B %Y")
            author.birthday = date_obj.strftime("%Y-%m-%d")
            # todo birth_date is sometimes just a year
            # need a second column birthyear
        except KeyError, IndexError, TypeError, ValueError:
            pass

        # todo this is temporary, for testing
        author.birthyear = None
        author.century_active = None

        try:
            date_obj = datetime.strptime(author_json["death_date"], "%d %B %Y")
            author.deathday = date_obj.strftime("%Y-%m-%d")
        except KeyError, IndexError, TypeError, ValueError:
            pass

        # author.nationality = []
        # author.language = []

        return author


class ProcessEdition(ProcessCatalogType):
    def __init__(self):
        pass

    def process(self, id: int) -> bool:
        provenance = ProvenanceEdition.objects.get(pk=id)
        if not provenance:
            return False

        data = self.convert(provenance.unprocessed_data)
        if not data:
            return False

        ProcessedEdition.objects.update_or_create(
            provenance_edition=provenance,
            defaults={"data": data.model_dump(), "record_title": data.title},
        )

        return True

    def convert(self, edition_json: dict) -> ProcessedEditionData | None:
        if not edition_json:
            return None

        edition = ProcessedEditionData()
        try:
            edition.external_id = edition_json["key"]
            edition.revision = edition_json["revision"]
            edition.title = edition_json["title"]
        except KeyError, IndexError, TypeError:
            return None

        try:
            # todo could have multiple, see edition /books/OL17721466M
            if edition_json["contributor"][0]["role"] == "Translator":
                edition.translator = edition_json["contributor"][0]["name"]
        except KeyError, IndexError, TypeError:
            pass

        edition.year_published = edition_json.get("publish_date", None)

        edition.publisher = edition_json.get("publishers", [""])[0]
        # todo is this ever multiple?

        edition.pages = edition_json.get("number_of_pages", None)

        try:
            edition.language = edition_json["languages"][0]["key"]
            # this might not match the work language, even if there's no translator listed, should deal with that later
        except KeyError, IndexError, TypeError:
            pass

        try:
            edition.work = edition_json["works"][0]["key"]
            # for the edition-to-work table
        except KeyError, IndexError, TypeError:
            pass

        edition.identifiers["isbn_13"] = []
        if edition_json.get("isbn_13", None):
            edition.identifiers["isbn_13"].extend(edition_json["isbn_13"])
        if edition_json.get("isbn", None):
            isbns = [isbnlib.to_isbn13(isbn) for isbn in edition_json["isbn"]]
        if edition_json.get("identifiers", None):
            edition.identifiers.update(edition_json["identifiers"])
            edition.identifiers["isbn_13"].extend(isbns)

        # other fields to consider later
        # edition_json["full_title"]
        # edition_json["subtitle"]
        # edition_json["other_titles"]
        # edition_json["authors"]
        # edition_json["physical_format"]
        # edition_json["publish_country"]
        # edition_json["edition_name"]
        # edition_json["by_statement"] how the byline appears
        # edition_json["notes"] misc information

        return edition


class ProcessWork(ProcessCatalogType):
    def __init__(self):
        pass

    def process(self, id: int) -> bool:
        provenance = ProvenanceWork.objects.get(pk=id)
        if not provenance:
            return False

        data = self.convert(provenance.unprocessed_data)
        if not data:
            return False

        ProcessedWork.objects.update_or_create(
            provenance_work=provenance,
            defaults={"data": data.model_dump(), "record_title": data.title},
        )

        return True

    def convert(self, work_json: dict) -> ProcessedWorkData | None:
        if not work_json:
            return None

        work = ProcessedWorkData()
        try:
            work.external_id = work_json["key"]
            work.revision = work_json["revision"]
            work.title = work_json["title"]
        except KeyError, IndexError, TypeError:
            return None

        try:
            if work_json["description"]["type"] == "/type/text":
                work.description = work_json["description"]["value"]
        except KeyError, IndexError, TypeError:
            pass

        try:
            year = work_json["first_publish_date"][-4:]
            if len(year) == 4 and year.isdigit():
                work.year_first_published = year
        except KeyError, IndexError, TypeError:
            pass

        try:
            if work_json["authors"][0]["type"]["key"] == "/type/author_role":
                work.author_id = work_json["authors"][0]["author"]["key"]
        except KeyError, IndexError, TypeError:
            pass

        return work
