from django.db import models

# the edition data can come from one or more processed records
# many-to-one of processed-to-edition
# this will probably be explicit in the processed data, but we want to map it to our keys


class IdentityMappingEditionProcessedToCatalog(models.Model):
    processed_edition = models.OneToOneField(
        "books.ProcessedEdition", on_delete=models.CASCADE, primary_key=True
    )
    catalog_edition = models.ForeignKey("books.CatalogEdition", on_delete=models.PROTECT)
    manual_override = models.BooleanField(default=False)


class IdentityMappingWorkProcessedToCatalog(models.Model):
    processed_work = models.OneToOneField(
        "books.ProcessedWork", on_delete=models.CASCADE, primary_key=True
    )
    catalog_work = models.ForeignKey("books.CatalogWork", on_delete=models.PROTECT)
    manual_override = models.BooleanField(default=False)


class IdentityMappingAuthorProcessedToCatalog(models.Model):
    processed_author = models.OneToOneField(
        "books.ProcessedAuthor", on_delete=models.CASCADE, primary_key=True
    )
    catalog_author = models.ForeignKey("books.CatalogAuthor", on_delete=models.PROTECT)
    manual_override = models.BooleanField(default=False)


class ISBN(models.Model):
    # maybe later change this to allow different identifier types
    # like "type" and "value"
    # too complicated for our first pass
    isbn13 = models.CharField(primary_key=True)
    edition = models.ForeignKey("books.CatalogEdition", on_delete=models.PROTECT)
