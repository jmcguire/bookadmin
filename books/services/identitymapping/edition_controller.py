from ninja import Schema

from books.models import ProcessedEdition


class ISBNFoundMissing(Schema):
    found: int = 0
    missing: int = 0


class EditionController:
    def __init__(self):
        pass

    def fill_in_isbn_table(self) -> ISBNFoundMissing:
        editions = ProcessedEdition.objects.all()
        isbn = []
        results = ISBNFoundMissing()
        for edition in editions:
            ids = []
            try:
                ids = edition.data["identifiers"]["isbn_13"]
            except ValueError:
                results.missing += 1
                continue
            results.found += 1
            isbn.extend(ids)

        return results
