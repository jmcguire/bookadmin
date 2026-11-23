import json

from django.contrib import admin
from django.utils.html import format_html

from books.models import ProvenanceImport


@admin.register(ProvenanceImport)
class ProvenanceImportAdmin(admin.ModelAdmin):
    search_fields = ["provider", "uri"]
    readonly_fields = ["provider", "uri", "imported_on", "pretty_results"]
    exclude = ["results"]

    @admin.display(description="Results")
    def pretty_results(self, obj):
        return format_html(
            "<pre style='white-space: pre-wrap'>{}</pre>",
            json.dumps(obj.results, indent=2, ensure_ascii=False),
        )
