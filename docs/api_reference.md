# API Reference

## Chat

### POST /api/chat/

Request body:

```json
{
  "question": "What is the failure mode for the payment API?",
  "session_id": "optional-session-id"
}
```

Response:

```json
{
  "answer": "The payment API was failing due to a timeout in the database connection pool.",
  "citations": [
    {"title": "Production Runbook", "source": "pdf"}
  ],
  "confidence": 88,
  "session_id": "abc123"
}
```

## Search explanation

### GET /api/search/explain/?q=postgresql

Returns metadata-based explanation of retrieval.

## Graph search

### GET /api/graph/search/?q=postgresql

Returns graph-based related entities.

## Graph endpoints

- GET /api/graph/
- GET /api/graph/stats/

## Export endpoints

- GET /api/export/json/
- GET /api/export/csv/

## Admin dashboard

- GET /api/admin/dashboard/
- GET /api/admin/analytics/
- GET /api/admin/documents/
- GET /api/admin/chunks/
- GET /api/admin/sessions/
- GET /api/admin/graph/

## Notes

- Most APIs are JSON-based and designed for backend dashboard and chatbot use.
- CSV export is intended for spreadsheet analysis and quick report generation.
