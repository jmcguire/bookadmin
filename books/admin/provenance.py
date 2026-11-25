import json

from django.contrib import admin
from django.utils.html import format_html

from books.models import ProvenanceAuthor, ProvenanceEdition, ProvenanceImport, ProvenanceWork


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


@admin.register(ProvenanceAuthor)
class ProvenanceAuthorAdmin(admin.ModelAdmin):
    search_fields = ["external_id"]
    readonly_fields = [
        "external_id",
        "revision",
        "provenance_import",
        "pretty_data",
    ]
    exclude = ["unprocessed_data"]

    @admin.display(description="Unprocessed Data")
    def pretty_data(self, obj):
        return format_html(
            "<pre style='white-space: pre-wrap'>{}</pre>",
            json.dumps(obj.unprocessed_data, indent=2, ensure_ascii=False),
        )


@admin.register(ProvenanceWork)
class ProvenanceWorkAdmin(admin.ModelAdmin):
    search_fields = ["external_id"]
    readonly_fields = [
        "external_id",
        "revision",
        "provenance_import",
        "pretty_data",
    ]
    exclude = ["unprocessed_data"]

    @admin.display(description="Unprocessed Data")
    def pretty_data(self, obj):
        return format_html(
            "<pre style='white-space: pre-wrap'>{}</pre>",
            json.dumps(obj.unprocessed_data, indent=2, ensure_ascii=False),
        )


@admin.register(ProvenanceEdition)
class ProvenanceEditionAdmin(admin.ModelAdmin):
    search_fields = ["external_id"]
    readonly_fields = [
        "external_id",
        "revision",
        "provenance_import",
        "pretty_data",
    ]
    exclude = ["unprocessed_data"]

    @admin.display(description="Unprocessed Data")
    def pretty_data(self, obj):
        return format_html(
            "<pre style='white-space: pre-wrap'>{}</pre>",
            json.dumps(obj.unprocessed_data, indent=2, ensure_ascii=False),
        )
