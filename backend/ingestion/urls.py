from django.urls import path
from .views import ingest_data

urlpatterns = [
    path("run/", ingest_data),
]