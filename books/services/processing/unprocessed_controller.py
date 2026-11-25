from books.models import (
    ProcessedAuthor,
    ProcessedEdition,
    ProcessedWork,
    ProvenanceAuthor,
    ProvenanceEdition,
    ProvenanceImport,
    ProvenanceWork,
)

from .results import (
    UnprocessedFromImport,
    UnprocessedStats,
)


class UnprocessedController:
    def __init__(self):
        pass

    def stats(self) -> UnprocessedStats:
        stats = UnprocessedStats()

        stats.provenance_authors_count = ProvenanceAuthor.objects.count()
        stats.processed_authors_count = ProcessedAuthor.objects.count()
        stats.provenance_works_count = ProvenanceWork.objects.count()
        stats.processed_works_count = ProcessedWork.objects.count()
        stats.provenance_editions_count = ProvenanceEdition.objects.count()
        stats.processed_editions_count = ProcessedEdition.objects.count()

        return stats

    def list_authors(self, import_id: int) -> list | None:
        if import_id:
            imp = ProvenanceImport.objects.get(pk=import_id)
            if not imp:
                return None
            return list(imp.authors.unprocessed_external_ids())
        else:
            return list(ProvenanceAuthor.objects.unprocessed_external_ids())

    def list_editions(self, import_id: int) -> list | None:
        if import_id:
            imp = ProvenanceImport.objects.get(pk=import_id)
            if not imp:
                return None
            return list(imp.editions.unprocessed_external_ids())
        else:
            return list(ProvenanceEdition.objects.unprocessed_external_ids())

    def list_works(self, import_id: int) -> list | None:
        if import_id:
            imp = ProvenanceImport.objects.get(pk=import_id)
            if not imp:
                return None
            return list(imp.works.unprocessed_external_ids())
        else:
            return list(ProvenanceWork.objects.unprocessed_external_ids())

    def list_from_import(self, import_id: int) -> UnprocessedFromImport | None:
        imp = ProvenanceImport.objects.get(pk=import_id)
        if not imp:
            return None

        unconverted_from_import = UnprocessedFromImport()

        unconverted_from_import.authors = list(imp.authors.unprocessed_external_ids())
        unconverted_from_import.editions = list(imp.editions.unprocessed_external_ids())
        unconverted_from_import.works = list(imp.works.unprocessed_external_ids())

        return unconverted_from_import
