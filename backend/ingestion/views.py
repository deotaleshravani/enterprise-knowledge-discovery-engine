from django.http import JsonResponse
from ingestion.pipeline.ingest_pipeline import run_ingestion

def ingest_data(request):
    count = run_ingestion()
    return JsonResponse({"message": "Ingestion complete", "documents": count})