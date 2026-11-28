import json

from django.contrib import admin
from django.contrib.admin import ActionLocation
from django.utils.html import format_html

from books.models import ProvenanceAuthor, ProvenanceEdition, ProvenanceImport, ProvenanceWork
from books.services.processing.process_controller import Process


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
        "processed",
        "pretty_data",
    ]
    exclude = ["unprocessed_data"]

    @admin.display(description="Unprocessed Data")
    def pretty_data(self, obj):
        return format_html(
            "<pre style='white-space: pre-wrap'>{}</pre>",
            json.dumps(obj.unprocessed_data, indent=2, ensure_ascii=False),
        )

    @admin.display(description="Processed Record")
    def processed(self, obj):
        return getattr(obj, "processed", None)

    actions = ["process_record"]

    @admin.action(
        location=ActionLocation.CHANGE_FORM,
        description="Process Record",
    )
    def process_record(self, request, queryset):
        record = queryset.get()
        process = Process()
        if process._process_author(record.id):
            self.message_user(request, "Processing succeeded.")
        else:
            self.message_user(request, "Processing failed.")


@admin.register(ProvenanceWork)
class ProvenanceWorkAdmin(admin.ModelAdmin):
    search_fields = ["external_id"]
    readonly_fields = [
        "external_id",
        "revision",
        "provenance_import",
        "processed",
        "pretty_data",
    ]
    exclude = ["unprocessed_data"]

    @admin.display(description="Unprocessed Data")
    def pretty_data(self, obj):
        return format_html(
            "<pre style='white-space: pre-wrap'>{}</pre>",
            json.dumps(obj.unprocessed_data, indent=2, ensure_ascii=False),
        )

    @admin.display(description="Processed Record")
    def processed(self, obj):
        return getattr(obj, "processed", None)

    actions = ["process_record"]

    @admin.action(
        location=ActionLocation.CHANGE_FORM,
        description="Process Record",
    )
    def process_record(self, request, queryset):
        record = queryset.get()
        process = Process()
        if process._process_work(record.id):
            self.message_user(request, "Processing succeeded.")
        else:
            self.message_user(request, "Processing failed.")


@admin.register(ProvenanceEdition)
class ProvenanceEditionAdmin(admin.ModelAdmin):
    search_fields = ["external_id"]
    readonly_fields = [
        "external_id",
        "revision",
        "provenance_import",
        "processed",
        "pretty_data",
    ]
    exclude = ["unprocessed_data"]

    @admin.display(description="Unprocessed Data")
    def pretty_data(self, obj):
        return format_html(
            "<pre style='white-space: pre-wrap'>{}</pre>",
            json.dumps(obj.unprocessed_data, indent=2, ensure_ascii=False),
        )

    @admin.display(description="Processed Record")
    def processed(self, obj):
        return getattr(obj, "processed", None)

    actions = ["process_record"]

    @admin.action(
        location=ActionLocation.CHANGE_FORM,
        description="Process Record",
    )
    def process_record(self, request, queryset):
        record = queryset.get()
        process = Process()
        if process._process_edition(record.id):
            self.message_user(request, "Processing succeeded.")
        else:
            self.message_user(request, "Processing failed.")
