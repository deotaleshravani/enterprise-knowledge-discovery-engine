from documents.models import Document
from search.models import Chunk
from search.formatter.formatter import format_document
from search.chunking.text_chunker import chunk_text
from search.chunking.document_formatter import (
    build_searchable_text
)

def run_chunking():

    created_count = 0

    documents = Document.objects.all()

    for document in documents:

        formatted_text = build_searchable_text(
            document
        )

        chunks = chunk_text(
            formatted_text
        )

        for index, chunk in enumerate(chunks):

            Chunk.objects.update_or_create(
                document=document,
                chunk_index=index,
                defaults={
                    "text": chunk
                }
            )

            created_count += 1

    print(f"Created/Updated {created_count} chunks")

    return created_count