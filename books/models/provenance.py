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


class ProvenanceWork(ProvenanceFieldsMixin):
    provenance_import = models.ForeignKey(
        "ProvenanceImport", on_delete=models.PROTECT, related_name="works"
    )


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


# often a bunch of import records come from a single batch
class ProvenanceImport(models.Model):
    provider = models.CharField(max_length=200)
    uri = models.CharField(
        max_length=200, null=True
    )  # some globally unique identifier?
    imported = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(
        max_length=200
    )  # replace with FileField or FilePathField?

    def stats(self):
        return {
            "editions": self.editions.count(),
            "works": self.works.count(),
            "authors": self.authors.count(),
            "mappings": self.mappings.count(),
        }
