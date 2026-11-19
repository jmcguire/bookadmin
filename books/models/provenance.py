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
    provenance_edition = models.BigAutoField(primary_key=True)
    provenance_import = models.ForeignKey(
        "ProvenanceImport", null=True, on_delete=models.PROTECT
    )

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        constraints = [  # noqa: RUF012
            models.UniqueConstraint(
                fields=[
                    "provenance_edition",
                    "provenance_import",
                ],
                name="unique_import_edition",
            ),
        ]


class ProvenanceWork(ProvenanceFieldsMixin):
    provenance_work = models.BigAutoField(primary_key=True)
    provenance_import = models.ForeignKey("ProvenanceImport", on_delete=models.PROTECT)
    external_id = models.CharField(max_length=200)
    revision = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )
    data = models.JSONField()

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        constraints = [  # noqa: RUF012
            models.UniqueConstraint(
                fields=[
                    "provenance_work",
                    "provenance_import",
                ],
                name="unique_import_work",
            ),
        ]


class ProvenanceEditionToWorkMapping(models.Model):
    provenance_edition = models.ForeignKey(
        "ProvenanceEdition", on_delete=models.PROTECT
    )
    provenance_work = models.ForeignKey("ProvenanceWork", on_delete=models.PROTECT)
    provenance_import = models.ForeignKey("ProvenanceImport", on_delete=models.PROTECT)
    revision = models.CharField(max_length=200)

    class Meta:
        constraints = [  # noqa: RUF012
            models.UniqueConstraint(
                fields=[
                    "provenance_edition",
                    "provenance_work",
                    "provenance_import",
                ],
                name="unique_import_edition_work",
            ),
        ]


class ProvenanceAuthor(ProvenanceFieldsMixin):
    provenance_author = models.BigAutoField(primary_key=True)
    provenance_import_id = models.ForeignKey(
        "ProvenanceImport", on_delete=models.PROTECT
    )


# often a bunch of import records come from a single batch
class ProvenanceImport(models.Model):
    provenance_import = models.BigAutoField(primary_key=True)
    provider = models.CharField(max_length=200)
    uri = models.CharField(max_length=200)  # some globally true identifier?
    imported = models.DateTimeField(auto_now_add=True)
