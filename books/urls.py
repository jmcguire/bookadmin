from django.urls import path

from . import views
from .services.identitymapping.api import identitymapping_api
from .services.importing.api import import_api
from .services.processing.api import process_api

app_name = "books"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("api/imports/", import_api.urls),
    path("api/process/", process_api.urls),
    path("api/identitymapping/", identitymapping_api.urls),
]
