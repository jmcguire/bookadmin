from django.contrib import admin

from books.models import ProvenanceImport


@admin.register(ProvenanceImport)
class ProvenanceImportAdmin(admin.ModelAdmin):
    search_fields = ["provider", "uri"]
    readonly_fields = ["provider", "uri", "imported_on", "results"]
