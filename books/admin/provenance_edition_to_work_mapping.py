from django.contrib import admin

from books.models import ProvenanceEditionToWorkMapping


@admin.register(ProvenanceEditionToWorkMapping)
class ProvenanceEditionToWorkMappingAdmin(admin.ModelAdmin):
    readonly_fields = [
        "provenance_edition_external_id",
        "provenance_work_external_id",
        "provenance_edition",
        "provenance_work",
        "provenance_import",
    ]
