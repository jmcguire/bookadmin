from django.db import models

# incoming data from various services
# this is flat data with no translation or understanding from our side


class ProvenanceFieldsMixin(models.Model):
    external_id = models.CharField(max_length=200)
    revision = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )
    data = models.JSONField()

    class Meta:
        abstract = True


class ProvenanceEdition(ProvenanceFieldsMixin):
    provenance_import = models.ForeignKey(
        "ProvenanceImport", on_delete=models.PROTECT, related_name="editions"
    )

    def __str__(self):
        return f"{self.external_id} {self.revision}"


class ProvenanceWork(ProvenanceFieldsMixin):
    provenance_import = models.ForeignKey(
        "ProvenanceImport", on_delete=models.PROTECT, related_name="works"
    )

    def __str__(self):
        return f"{self.external_id} {self.revision}"


class ProvenanceEditionToWorkMapping(models.Model):
    provenance_edition = models.ForeignKey(
        "ProvenanceEdition", on_delete=models.PROTECT
    )
    provenance_work = models.ForeignKey("ProvenanceWork", on_delete=models.PROTECT)
    provenance_import = models.ForeignKey(
        "ProvenanceImport", on_delete=models.PROTECT, related_name="mappings"
    )
    revision = models.CharField(max_length=200)


class ProvenanceAuthor(ProvenanceFieldsMixin):
    provenance_import = models.ForeignKey(
        "ProvenanceImport", on_delete=models.PROTECT, related_name="authors"
    )

    def __str__(self):
        return f"{self.external_id} {self.revision}"


# often a bunch of import records come from a single batch
class ProvenanceImport(models.Model):
    provider = models.CharField(max_length=200)
    uri = models.CharField(
        max_length=200, null=True
    )  # some globally unique identifier?
    imported_on = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(
        max_length=200
    )  # replace with FileField or FilePathField?
    results = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.provider} {self.filename} {self.imported_on.strftime('%Y-%m-%d %H:%M:%S')}"

    def stats(self):
        # todo return an object instead
        return {
            "editions": self.editions.count(),
            "works": self.works.count(),
            "authors": self.authors.count(),
            "mappings": self.mappings.count(),
        }
