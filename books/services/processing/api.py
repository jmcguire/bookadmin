from ninja import NinjaAPI
from ninja.errors import HttpError

from ...common import CatalogType
from .process_controller import Process
from .results import ProcessingStats, UnprocessedFromImport, UnprocessedRecords, UnprocessedStats
from .unprocessed_controller import UnprocessedController

process_api = NinjaAPI()


@process_api.get("stats", response=UnprocessedStats)
def processed_stats(request):
    unconverted_controller = UnprocessedController()
    return unconverted_controller.stats()


@process_api.get("unprocessed/import/{import_id}", response=UnprocessedFromImport)
def list_unprocessed_from_import(request, import_id: int):
    unprocessed_controller = UnprocessedController()
    r = unprocessed_controller.list_all_from_import(import_id)
    if r is None:
        raise HttpError(404, "import not found")

    return r


@process_api.get("unprocessed/import/all/type/{catalogtype}", response=UnprocessedRecords)
def list_unprocessed_type(request, catalogtype: CatalogType):
    unprocessed_controller = UnprocessedController()
    records = None
    match catalogtype:
        case CatalogType.AUTHOR:
            records = unprocessed_controller.list_authors()
        case CatalogType.WORK:
            records = unprocessed_controller.list_works()
        case CatalogType.EDITION:
            records = unprocessed_controller.list_editions()

    return UnprocessedRecords(unprocessed_records=records)


@process_api.get("unprocessed/import/{import_id}/type/{catalogtype}", response=UnprocessedRecords)
def list_unprocessed_typ_from_import(request, import_id: int, catalogtype: CatalogType):
    unprocessed_controller = UnprocessedController()
    records = None
    match catalogtype:
        case CatalogType.AUTHOR:
            records = unprocessed_controller.list_authors_by_import(import_id)
        case CatalogType.WORK:
            records = unprocessed_controller.list_works_by_import(import_id)
        case CatalogType.EDITION:
            records = unprocessed_controller.list_editions_by_import(import_id)

    if records is None:
        raise HttpError(404, "import not found")

    return UnprocessedRecords(unprocessed_records=records)


@process_api.put("process/import/{import_id}", response=ProcessingStats)
def process_import(request, import_id: int):
    processor = Process()
    return processor.from_imp(import_id)


@process_api.put("process/import/all/type/{catalogtype}", response=ProcessingStats)
def process_all_of_type(request, catalogtype: CatalogType):
    processor = Process()
    return processor.from_type(catalogtype)


@process_api.put("process/import/{import_id}/type/{catalogtype}", response=ProcessingStats)
def process_type_from_import(request, import_id: int, catalogtype: CatalogType):
    processor = Process()
    return processor.from_type_from_import(import_id, catalogtype)


@process_api.put("process/{catalogtype}/{id}", response=ProcessingStats)
def process_single_record(request, catalogtype: CatalogType, id: int):
    processor = Process()
    return processor.from_single(catalogtype, id)
