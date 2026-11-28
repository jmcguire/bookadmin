from django.db import models

from .abstract_models import TimeStampedFieldsMixin

# core tables that make up our book catalog


# a single published volume
class CatalogEdition(TimeStampedFieldsMixin):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    default_cover = models.ForeignKey(
        "books.Cover", on_delete=models.PROTECT, null=True, blank=True
    )
    translator = models.ForeignKey(
        "books.CatalogAuthor",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="translations",
    )
    introduction_by = models.ForeignKey(
        "books.CatalogAuthor",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="introductions",
    )
    year_published = models.SmallIntegerField(null=True, blank=True)
    publisher = models.ForeignKey(
        "books.Publisher", on_delete=models.PROTECT, null=True, blank=True
    )
    pages = models.PositiveSmallIntegerField(null=True, blank=True)
    work = models.ForeignKey("books.CatalogWork", on_delete=models.PROTECT)
    language = models.ForeignKey("books.Language", on_delete=models.PROTECT, null=True, blank=True)


# a piece of intellectual property
class CatalogWork(TimeStampedFieldsMixin):
    title = models.CharField(max_length=200)
    author = models.ForeignKey("books.CatalogAuthor", on_delete=models.PROTECT)
    description = models.CharField(max_length=200)
    year_first_published = models.SmallIntegerField(null=True, blank=True)
    language = models.ForeignKey("books.Language", on_delete=models.PROTECT, null=True, blank=True)
    default_cover = models.ForeignKey(
        "books.Cover", on_delete=models.PROTECT, null=True, blank=True
    )
    # todo what about anthologies with multiple authors and an editor?


class CatalogAuthor(TimeStampedFieldsMixin):
    given_name = models.CharField(max_length=200)  # first name
    family_name = models.CharField(max_length=200)  # last name
    sort_name = models.CharField(max_length=200)
    print_name = models.CharField(max_length=200)
    nationality = models.ForeignKey(
        "books.Nationality", on_delete=models.PROTECT, null=True, blank=True
    )
    language = models.ForeignKey("books.Language", on_delete=models.PROTECT, null=True, blank=True)

    birthday = models.DateField(null=True, blank=True)
    birthyear = models.SmallIntegerField(null=True, blank=True)
    deathday = models.DateField(null=True, blank=True)
    deathyear = models.SmallIntegerField(null=True, blank=True)
    century_active = models.CharField(max_length=10, null=True, blank=True)
    # year identifier is when the birth and death is just not knowable
    # but we have something
    # so we store a string like "5c bce"

    bio_short = models.CharField(
        max_length=80
    )  # one sentence, has an implicit "{name} " before it. e.g. " is a celebrated childrens author."
    bio = models.CharField(max_length=500)  # one paragraph
    source_ids = models.JSONField(
        null=True, blank=True
    )  # for e.g. openlibrary, wikidata, lc_naf, etc

    def save(self, **kwargs):
        # or use GeneratedField?
        self.print_name = self.given_name + " " + self.family_name
        self.sort_name = self.family_name + " " + self.given_name
        super().save(**kwargs)
