from django.urls import path

from . import views
from .apis.imports import imports_api

app_name = "books"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("api/imports/", imports_api.urls),
]
