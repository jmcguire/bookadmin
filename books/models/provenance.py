from django.db import models

# incoming data from various services
# this is flat data import with no translation or understanding from our side
# (that part happens in the convert models)


class ProvenanceQuerySet(models.QuerySet):
    def unprocessed_external_ids(self) -> list[str]:
        return list(self.filter(processed__isnull=True).values_list("external_id", flat=True))

    def ids_by_import(self, import_id: int) -> list[str]:
        return list(self.filter(provenance_import_id=import_id).values_list("id", flat=True))

    def ids(self) -> list[str]:
        return list(self.values_list("id", flat=True))


class ProvenanceFieldsMixin(models.Model):
    external_id = models.CharField(max_length=200)
    revision = models.CharField(max_length=200)
    unprocessed_data = models.JSONField()

    objects = ProvenanceQuerySet.as_manager()

    class Meta:
        abstract = True


class ProvenanceEdition(ProvenanceFieldsMixin):
    provenance_import = models.ForeignKey(
        "ProvenanceImport", on_delete=models.PROTECT, related_name="editions"
    )

    def __str__(self):
        return f"{self.id} {self.external_id} {self.revision}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["external_id", "revision"],
                name="unique_provenance_edition_external_id_and_revision",
            )
        ]


class ProvenanceWork(ProvenanceFieldsMixin):
    provenance_import = models.ForeignKey(
        "ProvenanceImport", on_delete=models.PROTECT, related_name="works"
    )

    def __str__(self):
        return f"{self.id} {self.external_id} {self.revision}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["external_id", "revision"],
                name="unique_provenance_work_external_id_and_revision",
            )
        ]


class ProvenanceAuthor(ProvenanceFieldsMixin):
    provenance_import = models.ForeignKey(
        "ProvenanceImport", on_delete=models.PROTECT, related_name="authors"
    )

    def __str__(self):
        return f"{self.id} {self.external_id} {self.revision}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["external_id", "revision"],
                name="unique_provenance_author_external_id_and_revision",
            )
        ]


# often a bunch of import records come from a single batch
class ProvenanceImport(models.Model):
    provider = models.CharField(max_length=200)
    uri = models.CharField(max_length=200, null=True)  # some globally unique identifier?
    imported_on = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=200)  # replace with FileField or FilePathField?
    results = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.id} {self.provider} {self.filename} {self.imported_on.strftime('%Y-%m-%d %H:%M:%S')}"

    def stats(self):
        # todo return an object instead
        return {
            "editions": self.editions.count(),
            "works": self.works.count(),
            "authors": self.authors.count(),
        }
