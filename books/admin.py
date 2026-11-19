from django.contrib import admin

from .models import Author, Edition, Work


@admin.register(Author)
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


@admin.register(Edition)
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


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
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
                    "author",
                    "description",
                    "language",
                    "year_first_published",
                    "default_cover",
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
