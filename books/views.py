from typing import Any

from django.db.models.query import QuerySet
from django.views import generic


class IndexView(generic.ListView):
    template_name = "books/index.html"

    def get_queryset(self) -> QuerySet[Any, Any]:
        return []
