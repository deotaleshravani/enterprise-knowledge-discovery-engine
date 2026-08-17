from django.urls import path

from .views import ingest_data, upload_documents

urlpatterns = [
    path("run/", ingest_data, name="ingest-run"),
    path("upload/", upload_documents, name="upload-documents"),
]