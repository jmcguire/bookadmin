import json

from django.contrib import admin
from django.utils.html import format_html

from books.models import ProvenanceAuthor


@admin.register(ProvenanceAuthor)
class ProvenanceAuthorAdmin(admin.ModelAdmin):
    search_fields = ["external_id"]
    readonly_fields = [
        "external_id",
        "revision",
        "provenance_import",
        "pretty_data",
        "unprocessed_data",
    ]

    exclude = ["data"]

    @admin.display(description="Data")
    def pretty_data(self, obj):
        return format_html(
            "<pre style='white-space: pre-wrap'>{}</pre>",
            json.dumps(obj.data, indent=2, ensure_ascii=False),
        )
