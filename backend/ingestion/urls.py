from django.urls import path
<<<<<<< HEAD

from .views import ingest_data, upload_documents

urlpatterns = [
    path("run/", ingest_data, name="ingest-run"),
    path("upload/", upload_documents, name="upload-documents"),
=======
from .views import ingest_data

urlpatterns = [
    path("run/", ingest_data),
>>>>>>> 295313f9544a55975afdff91c3cab55d8a5a635a
]