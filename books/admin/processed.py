import json

from django.contrib import admin
from django.utils.html import format_html

from books.models import (
    ProcessedAuthor,
    ProcessedEdition,
    ProcessedEditionToWorkMapping,
    ProcessedWork,
)


@admin.register(ProcessedAuthor)
class ProcessedAuthorAdmin(admin.ModelAdmin):
    readonly_fields = ["provenance_author", "record_title", "pretty_data"]
    exclude = ["data"]

    @admin.display(description="Processed Data")
    def pretty_data(self, obj):
        return format_html(
            "<pre style='white-space: pre-wrap'>{}</pre>",
            json.dumps(obj.data, indent=2, ensure_ascii=False),
        )


@admin.register(ProcessedEdition)
class ProcessedEditionAdmin(admin.ModelAdmin):
    readonly_fields = ["provenance_edition", "record_title", "pretty_data"]
    exclude = ["data"]

    @admin.display(description="Processed Data")
    def pretty_data(self, obj):
        return format_html(
            "<pre style='white-space: pre-wrap'>{}</pre>",
            json.dumps(obj.data, indent=2, ensure_ascii=False),
        )


@admin.register(ProcessedWork)
class ProcessedWorkAdmin(admin.ModelAdmin):
    readonly_fields = ["provenance_work", "record_title", "pretty_data"]
    exclude = ["data"]

    @admin.display(description="Processed Data")
    def pretty_data(self, obj):
        return format_html(
            "<pre style='white-space: pre-wrap'>{}</pre>",
            json.dumps(obj.data, indent=2, ensure_ascii=False),
        )


@admin.register(ProcessedEditionToWorkMapping)
class ProcessedEditionToWorkMappingAdmin(admin.ModelAdmin):
    readonly_fields = [
        "provenance_edition_external_id",
        "provenance_work_external_id",
        "processed_edition",
        "processed_work",
    ]
