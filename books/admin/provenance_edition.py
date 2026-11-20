from django.contrib import admin

from books.models import ProvenanceEdition


@admin.register(ProvenanceEdition)
class ProvenanceEditionAdmin(admin.ModelAdmin):
    search_fields = ["external_id"]
    readonly_fields = ["external_id", "revision", "data", "provenance_import"]
