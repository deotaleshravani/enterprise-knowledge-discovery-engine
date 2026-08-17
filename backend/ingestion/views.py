<<<<<<< HEAD
import json

from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from documents.models import Document
from ingestion.pipeline.ingest_pipeline import run_ingestion
from ingestion.services.normalizer import normalize
from search.chunking.chunk_pipeline import run_chunking
from search.embeddings.embedding_pipeline import run_embedding_pipeline
from search.knowledge_graph.graph_builder import build_graph


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ingest_data(request):
    source = request.data.get("source") or request.data.get("type") or "manual"
    payload = request.data.get("payload") or request.data.get("data") or request.data.get("records")

    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            payload = {"text": payload}

    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict):
        records = [payload]
    else:
        records = []

    created_documents = []
    for record in records:
        normalized = normalize(record, source)
        if not normalized.get("id"):
            continue
        document, _ = Document.objects.update_or_create(
            id=normalized["id"],
            defaults={
                "source": normalized["source"],
                "text": normalized["text"],
                "author": normalized["author"],
                "date": normalized.get("date"),
                "metadata": normalized["metadata"],
            },
        )
        created_documents.append(document.id)

    run_chunking()
    run_embedding_pipeline()
    build_graph()

    return JsonResponse({
        "message": "Ingestion complete",
        "source": source,
        "documents": len(created_documents),
        "document_ids": created_documents,
    }, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_documents(request):
    records = request.data.get("records") or []
    source = request.data.get("source") or "manual"

    if not records:
        return JsonResponse({"error": "No records supplied"}, status=400)

    return ingest_data(request)
=======
from django.http import JsonResponse
from ingestion.pipeline.ingest_pipeline import run_ingestion

def ingest_data(request):
    count = run_ingestion()
    return JsonResponse({"message": "Ingestion complete", "documents": count})
>>>>>>> 295313f9544a55975afdff91c3cab55d8a5a635a
