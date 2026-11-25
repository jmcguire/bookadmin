# todo when is __init__ to big?
from ninja import ModelSchema, Schema

from books.models import ProvenanceImport


class FileImportStats(Schema):
    size: int
    lines: int
    success: int
    failed: int

    # eventually have detailed results: a success file and a failure file, that says precisely what succeeded and what failed and why


class FileImportResults(Schema):
    import_id: int
    file_stats: FileImportStats
    import_stats: dict


class FileList(Schema):
    files: list


class ImportsList(Schema):
    imports: list[ProvenanceImportOut]


class ProvenanceImportOut(ModelSchema):
    stats: dict

    class Meta:
        model = ProvenanceImport
        fields = ["id", "provider", "uri", "imported_on", "filename", "results"]

    @staticmethod
    def resolve_stats(obj):
        return obj.stats()
