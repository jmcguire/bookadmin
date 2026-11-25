from django.contrib import admin

from books.models import CatalogAuthor


@admin.register(CatalogAuthor)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ["given_name", "family_name"]
    readonly_fields = [
        "sort_name",
        "print_name",
        "created_at",
        "updated_at",
    ]
    empty_value_display = "(not generated yet)"
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "given_name",
                    "family_name",
                    "language",
                    "nationality",
                    "description",
                    "birth",
                    "death",
                )
            },
        ),
        (
            "Resolved Names",
            {
                "fields": ("sort_name", "print_name"),
                "description": "Generated from given and family names",
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
