from django.db import models

from .abstract_models import TimeStampedFieldsMixin

# core tables that make up our book catalog


# a single published volume
class Edition(TimeStampedFieldsMixin):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    default_cover = models.ForeignKey(
        "books.Cover", on_delete=models.PROTECT, null=True, blank=True
    )
    translator = models.ForeignKey(
        "books.Author",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="translations",
    )
    introduction_by = models.ForeignKey(
        "books.Author",
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
    work = models.ForeignKey("books.Work", on_delete=models.PROTECT)
    language = models.ForeignKey(
        "books.Language", on_delete=models.PROTECT, null=True, blank=True
    )


# a piece of intellectual property
class Work(TimeStampedFieldsMixin):
    title = models.CharField(max_length=200)
    author = models.ForeignKey("books.Author", on_delete=models.PROTECT)
    description = models.CharField(max_length=200)
    year_first_published = models.SmallIntegerField(null=True, blank=True)
    language = models.ForeignKey(
        "books.Language", on_delete=models.PROTECT, null=True, blank=True
    )
    default_cover = models.ForeignKey(
        "books.Cover", on_delete=models.PROTECT, null=True, blank=True
    )


class Author(TimeStampedFieldsMixin):
    given_name = models.CharField(max_length=200)
    family_name = models.CharField(max_length=200)
    sort_name = models.CharField(max_length=200)
    print_name = models.CharField(max_length=200)
    nationality = models.ForeignKey(
        "books.Nationality", on_delete=models.PROTECT, null=True, blank=True
    )
    language = models.ForeignKey(
        "books.Language", on_delete=models.PROTECT, null=True, blank=True
    )
    birth = models.DateField(null=True, blank=True)
    death = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=200)

    def save(self, **kwargs):
        # or use GeneratedField?
        self.print_name = self.given_name + " " + self.family_name
        self.sort_name = self.family_name + " " + self.given_name
        super().save(**kwargs)
