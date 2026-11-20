from django.contrib import admin

from books.models import ProvenanceAuthor


@admin.register(ProvenanceAuthor)
class ProvenanceAuthorAdmin(admin.ModelAdmin):
    search_fields = ["external_id"]
    readonly_fields = ["external_id", "revision", "data", "provenance_import"]
