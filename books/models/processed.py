from django.db import models

# processed data
# data from provenance is processed into the fields we understand and need
# record title is a denormalized piece of data, just to give a human-readable title for our admin page


class ProcessedEdition(models.Model):
    provenance_edition = models.OneToOneField(
        "books.ProvenanceEdition",
        primary_key=True,
        on_delete=models.PROTECT,
        related_name="processed",
    )
    data = models.JSONField()
    record_title = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.provenance_edition_id} {self.record_title}"


class ProcessedWork(models.Model):
    provenance_work = models.OneToOneField(
        "books.ProvenanceWork", primary_key=True, on_delete=models.PROTECT, related_name="processed"
    )
    data = models.JSONField()
    record_title = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.provenance_work_id} {self.record_title}"


class ProcessedAuthor(models.Model):
    provenance_author = models.OneToOneField(
        "books.ProvenanceAuthor",
        primary_key=True,
        on_delete=models.PROTECT,
        related_name="processed",
    )
    data = models.JSONField()
    record_title = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.provenance_author_id} {self.record_title}"


class ProcessedEditionToWorkMapping(models.Model):
    provenance_edition_external_id = models.CharField(max_length=100)
    provenance_work_external_id = models.CharField(max_length=100)

    processed_edition = models.ForeignKey(
        "books.ProcessedEdition", on_delete=models.PROTECT, null=True, blank=True
    )
    processed_work = models.ForeignKey(
        "books.ProcessedWork", on_delete=models.PROTECT, null=True, blank=True
    )
