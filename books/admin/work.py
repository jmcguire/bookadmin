from django.contrib import admin

from books.models import Work


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
