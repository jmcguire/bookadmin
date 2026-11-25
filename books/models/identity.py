from django.db import models

# the edition data can come from one or more processed records
# many-to-one of processed-to-edition
# this will probably be explicit in the processed data, but we want to map it to our keys


class IdentityMappingProcessedEditionToOurEdition(models.Model):
    provenance_edition = models.OneToOneField(
        "books.ProcessedEdition", on_delete=models.CASCADE, primary_key=True
    )
    edition = models.ForeignKey("books.CatalogEdition", on_delete=models.PROTECT)


class IdentityMappingProcessedWorkToOurWork(models.Model):
    provenance_work = models.OneToOneField(
        "books.ProcessedWork", on_delete=models.CASCADE, primary_key=True
    )
    work = models.ForeignKey("books.CatalogWork", on_delete=models.PROTECT)


class IdentityMappingProcessedAuthorToOurAuthor(models.Model):
    provenance_author = models.OneToOneField(
        "books.ProcessedAuthor", on_delete=models.CASCADE, primary_key=True
    )
    author = models.ForeignKey("books.CatalogAuthor", on_delete=models.PROTECT)
