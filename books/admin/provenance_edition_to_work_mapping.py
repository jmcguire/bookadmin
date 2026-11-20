from django.contrib import admin

from books.models import ProvenanceEditionToWorkMapping


@admin.register(ProvenanceEditionToWorkMapping)
class ProvenanceEditionToWorkMappingAdmin(admin.ModelAdmin):
    readonly_fields = [
        "provenance_edition",
        "provenance_work",
        "provenance_import",
        "revision",
    ]
