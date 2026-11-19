from django.db import models

# the edition data can come from one or more provenance records
# many-to-one of provenance-to-edition
# this will probably be explicit in the provence data, but we want to map it to our keys


class IdentityMappingProvenanceEditionToOurEdition(models.Model):
    provenance_edition = models.OneToOneField(
        "books.ProvenanceEdition", on_delete=models.CASCADE, primary_key=True
    )
    edition = models.ForeignKey("books.Edition", on_delete=models.PROTECT)


class IdentityMappingProvenanceWorkToOurWork(models.Model):
    provenance_work = models.OneToOneField(
        "books.ProvenanceWork", on_delete=models.CASCADE, primary_key=True
    )
    work = models.ForeignKey("books.Work", on_delete=models.PROTECT)


class IdentityMappingProvenanceAuthorToOurAuthor(models.Model):
    provenance_author = models.OneToOneField(
        "books.ProvenanceAuthor", on_delete=models.CASCADE, primary_key=True
    )
    author = models.ForeignKey("books.Author", on_delete=models.PROTECT)
