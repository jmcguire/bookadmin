from datetime import datetime

from ...common import CatalogType
from ...models import (
    ProcessedAuthor,
    ProcessedEdition,
    ProcessedWork,
    ProvenanceAuthor,
    ProvenanceEdition,
    ProvenanceWork,
)
from .processed_data import ProcessedAuthorData, ProcessedEditionData, ProcessedWorkData
from .results import ProcessingStats

# todo: convert the "return False" into a structured error message


class Process:
    def __init__(self):
        pass

    def from_imp(self, import_id: int) -> ProcessingStats:
        stats = ProcessingStats()

        for type in CatalogType:
            results = self.from_type_from_import(import_id, type)
            stats.success += results.success
            stats.failure += results.failure

        return stats

    def from_type(self, type: CatalogType) -> ProcessingStats:
        stats = ProcessingStats()

        match type:
            case CatalogType.AUTHOR:
                for id in ProvenanceAuthor.objects.all().values_list("id", flat=True):
                    if self._process_author(CatalogType.AUTHOR, id):
                        stats.success += 1
                    else:
                        stats.failure += 1
            case CatalogType.WORK:
                for id in ProvenanceWork.objects.all().values_list("id", flat=True):
                    if self._process_work(CatalogType.WORK, id):
                        stats.success += 1
                    else:
                        stats.failure += 1
            case CatalogType.EDITION:
                for id in ProvenanceEdition.objects.all().values_list("id", flat=True):
                    if self._process_edition(CatalogType.EDITION, id):
                        stats.success += 1
                    else:
                        stats.failure += 1

        return stats

    def from_type_from_import(self, import_id: int, type: CatalogType) -> ProcessingStats:
        stats = ProcessingStats()

        match type:
            case CatalogType.AUTHOR:
                for id in ProvenanceAuthor.objects.filter(import_id=import_id).values_list(
                    "id", flat=True
                ):
                    if self._process_author(CatalogType.AUTHOR, id):
                        stats.success += 1
                    else:
                        stats.failure += 1
            case CatalogType.WORK:
                for id in ProvenanceAuthor.objects.filter(import_id=import_id).values_list(
                    "id", flat=True
                ):
                    if self._process_work(CatalogType.WORK, id):
                        stats.success += 1
                    else:
                        stats.failure += 1
            case CatalogType.EDITION:
                for id in ProvenanceAuthor.objects.filter(import_id=import_id).values_list(
                    "id", flat=True
                ):
                    if self._process_edition(CatalogType.EDITION, id):
                        stats.success += 1
                    else:
                        stats.failure += 1

        return stats

    def from_single(self, type: CatalogType, id: int) -> ProcessingStats:
        match type:
            case CatalogType.AUTHOR:
                return self._process_author(id)
            case CatalogType.WORK:
                return self._process_work(id)
            case CatalogType.EDITION:
                return self._process_edition(id)

    def _process_author(self, id: int) -> bool:
        provenance = ProvenanceAuthor.objects.get(id)
        if not provenance:
            return False

        data = convert_author(provenance.unprocessed_data)
        if not data:
            return False

        ProcessedAuthor.objects.create(provenance_author=provenance, data=data)

        return True

    def _process_work(self, id: int) -> bool:
        provenance = ProvenanceWork.objects.get(id)
        if not provenance:
            return False

        data = convert_work(provenance.unprocessed_data)
        if not data:
            return False

        ProcessedWork.objects.create(provenance_work=provenance, data=data)

        return True

    def _process_edition(self, id: int) -> bool:
        provenance = ProvenanceEdition.objects.get(id)
        if not provenance:
            return False

        data = convert_edition(provenance.unprocessed_data)
        if not data:
            return False

        ProcessedEdition.objects.create(provenance_edition=provenance, data=data)

        return True


def convert_work(work_json) -> ProcessedWorkData | None:
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


def convert_edition(edition_json) -> ProcessedEditionData | None:
    edition = ProcessedEditionData()
    try:
        edition.external_id = edition_json["key"]
        edition.revision = edition_json["revision"]
        edition.title = edition_json["title"]
    except KeyError, IndexError, TypeError:
        return None

    try:
        # todo could have multiple, see edition /books/OL17721466M
        if edition_json.get["contributor"][0]["role"] == "Translator":
            edition.translator = edition_json.get["contributor"][0]["name"]
    except KeyError, IndexError, TypeError:
        pass

    edition.year_published = edition_json.get("publish_date", None)

    edition.publisher = edition_json.get("publishers", [])[0]
    # todo is this ever multiple?

    edition.pages = edition_json.get("number_of_pages", 0)

    try:
        edition.language = edition_json.get["languages"][0]["key"]
        # this might not match the work language, even if there's no translator listed, should deal with that later
    except KeyError, IndexError, TypeError:
        pass

    try:
        edition.work = edition_json["works"][0]["key"]
        # for the edition-to-work table
    except KeyError, IndexError, TypeError:
        pass

    if edition_json.get("isbn_13", None):
        edition.language.append(edition_json["isbn_13"])
    if edition_json.get("identifiers", None):
        edition.language.extend(edition_json["identifiers"])

    edition_json["subtitle"]

    # other fields to consider later
    # edition_json["other_titles"]
    # edition_json["physical_format"]
    # edition_json["publish_country"]
    # edition_json["edition_name"]
    # edition_json["by_statement"] how the byline appears

    return edition


def convert_author(author_json) -> ProcessedAuthorData | None:
    author = ProcessedAuthorData()
    try:
        author.external_id = author_json["key"]
        author.revision = author_json["revision"]
        author.name = author_json["name"]  # or author_json["personal_name"]
    except KeyError, IndexError, TypeError, ValueError:
        return None

    author.bio = author_json.get("bio", "")

    try:
        date_obj = datetime.strptime(author_json["birth_date"], "%d %B %Y")
        author.birthday = date_obj.strftime("%Y-%m-%d")
        # todo birth_date is sometimes just a year
        # need a second column birthyear
    except KeyError, IndexError, TypeError, ValueError:
        pass

    try:
        date_obj = datetime.strptime(author_json["death_date"], "%d %B %Y")
        author.deathday = date_obj.strftime("%Y-%m-%d")
    except KeyError, IndexError, TypeError, ValueError:
        pass

    # author.given_name = ""
    # author.family_name = ""
    # author.nationality = []
    # author.language = []

    return author
