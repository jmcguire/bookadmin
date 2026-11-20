from django.contrib import admin

from books.models import ProvenanceWork


@admin.register(ProvenanceWork)
class ProvenanceWorkAdmin(admin.ModelAdmin):
    search_fields = ["external_id"]
    readonly_fields = ["external_id", "revision", "data", "provenance_import"]
