from django.db import models

from .abstract_models import TimeStampedFieldsMixin

# editorial overrides and mapping decisions


class DecisionAndOverrides(models.Model):
    overrides = models.JSONField(default=dict)
    decision = models.JSONField()

    class Meta:
        abstract = True


class DecisionEdition(TimeStampedFieldsMixin, DecisionAndOverrides):  # pyright: ignore[reportIncompatibleVariableOverride]
    edition = models.OneToOneField(
        "books.Edition",
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="decision",
    )


class DecisionWork(TimeStampedFieldsMixin, DecisionAndOverrides):  # pyright: ignore[reportIncompatibleVariableOverride]
    work = models.OneToOneField(
        "books.Work",
        on_delete=models.PROTECT,
        primary_key=True,
        related_name="decision",
    )


class DecisionEditionToWork(TimeStampedFieldsMixin):
    edition = models.ForeignKey("books.Edition", on_delete=models.PROTECT)
    # ? not sure about this one
    forced_work = models.ForeignKey("books.Work", on_delete=models.PROTECT)
    decision = models.JSONField()


class DecisionAuthor(TimeStampedFieldsMixin, DecisionAndOverrides):  # pyright: ignore[reportIncompatibleVariableOverride]
    author = models.OneToOneField(
        "books.Author",
        on_delete=models.PROTECT,
        primary_key=True,
        related_name="decision",
    )
