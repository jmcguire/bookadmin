from ninja import Schema


class UnprocessedFromImport(Schema):
    authors: list[str] = []
    editions: list[str] = []
    works: list[str] = []


class UnprocessedStats(Schema):
    provenance_authors_count: int = 0
    processed_authors_count: int = 0
    provenance_works_count: int = 0
    processed_works_count: int = 0
    provenance_editions_count: int = 0
    processed_editions_count: int = 0


class UnprocessedRecords(Schema):
    unprocessed_records: list[str] = []


class ProcessingStats(Schema):
    success: int = 0
    failure: int = 0
