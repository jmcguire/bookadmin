from django.contrib import admin

from books.models import CatalogEdition


@admin.register(CatalogEdition)
class EditionAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]
    empty_value_display = "(not generated yet)"
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "work",
                    "year_published",
                )
            },
        ),
        (
            "Optional",
            {
                "fields": (
                    "description",
                    "translator",
                    "introduction_by",
                    "default_cover",
                    "publisher",
                    "pages",
                    "language",
                )
            },
        ),
        (
            "Timestamp Metadata",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )
