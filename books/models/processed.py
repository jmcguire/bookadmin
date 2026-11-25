from django.db import models

# processed data
# data from provenance is processed into the fields we understand and need


class ProcessedEdition(models.Model):
    provenance_edition = models.ForeignKey(
        "books.ProvenanceEdition", on_delete=models.PROTECT, related_name="processed"
    )
    data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.external_id} {self.revision}"


class ProcessedWork(models.Model):
    provenance_work = models.ForeignKey(
        "books.ProvenanceWork", on_delete=models.PROTECT, related_name="processed"
    )
    data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.external_id} {self.revision}"


class ProcessedAuthor(models.Model):
    provenance_author = models.ForeignKey(
        "books.ProvenanceAuthor", on_delete=models.PROTECT, related_name="processed"
    )
    data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.external_id} {self.revision}"


class ProcessedEditionToWorkMapping(models.Model):
    provenance_edition_external_id = models.CharField(max_length=100)
    provenance_work_external_id = models.CharField(max_length=100)

    processed_edition = models.ForeignKey(
        "books.ProcessedEdition", on_delete=models.PROTECT, null=True, blank=True
    )
    processed_work = models.ForeignKey(
        "books.ProcessedWork", on_delete=models.PROTECT, null=True, blank=True
    )
