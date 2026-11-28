from django.db import models

from .abstract_models import TimeStampedFieldsMixin

# editorial overrides and mapping decisions


class DecisionAndOverridesMixin(models.Model):
    overrides = models.JSONField(default=dict)
    decision = models.JSONField()

    class Meta:
        abstract = True


class DecisionEdition(TimeStampedFieldsMixin, DecisionAndOverridesMixin):  # pyright: ignore[reportIncompatibleVariableOverride]
    edition = models.OneToOneField(
        "books.CatalogEdition",
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="decision",
    )


class DecisionWork(TimeStampedFieldsMixin, DecisionAndOverridesMixin):  # pyright: ignore[reportIncompatibleVariableOverride]
    work = models.OneToOneField(
        "books.CatalogWork",
        on_delete=models.PROTECT,
        primary_key=True,
        related_name="decision",
    )


class DecisionEditionToWork(TimeStampedFieldsMixin):
    edition = models.ForeignKey("books.CatalogEdition", on_delete=models.PROTECT)
    # ? not sure about this one
    forced_work = models.ForeignKey("books.CatalogWork", on_delete=models.PROTECT)
    decision = models.JSONField()


class DecisionAuthor(TimeStampedFieldsMixin, DecisionAndOverridesMixin):  # pyright: ignore[reportIncompatibleVariableOverride]
    author = models.OneToOneField(
        "books.CatalogAuthor",
        on_delete=models.PROTECT,
        primary_key=True,
        related_name="decision",
    )
