# Enterprise Knowledge Discovery Engine (EKDE)

EKDE is an enterprise search and RAG system designed to answer internal knowledge questions using documents, tickets, meetings, Slack messages, and structured knowledge graph data.

## What this project does

- Search company knowledge across multiple data sources
- Rerank and explain why results were retrieved
- Build a graph of people, projects, technologies, and tickets
- Chat with an LLM using only retrieved context
- Export search analytics as JSON or CSV
- Show dashboard statistics for documents, chunks, sessions, and graph structure

## Architecture summary

- Backend: Django + Django REST Framework
- Search: FAISS + BM25 + reranker
- Graph: NetworkX-based relationship graph
- LLM: Ollama-compatible local model access
- Embeddings: SentenceTransformers / BGE model
- Data sources: Jira, PDF, meetings, Slack

## Stack

- Python 3.11
- Django 5.2.17
- Django REST Framework 3.17.1
- FAISS
- Sentence Transformers
- Rank-BM25
- NetworkX
- Ollama

## Project layout

```text
backend/
  admin_api/
  chatbot/
  documents/
  ekde/
  ingestion/
  search/
  users/
  manage.py

datasets/
  jira/
  meetings/
  pdfs/
  slack/

docs/
  architecture.md
  project_plan.md
  database_design.md
  api_reference.md
  deployment_guide.md
  sequence_diagrams.md

requirements.txt
Dockerfile
docker-compose.yml
```

## Local setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cd backend
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## Key API endpoints

### Chat

- POST /api/chat/
- GET /api/chat/sessions/
- GET /api/chat/history/<session_id>/

### Search

- GET /api/search/explain/?q=postgresql
- GET /api/graph/search/?q=postgresql
- GET /api/graph/
- GET /api/graph/stats/
- GET /api/export/json/
- GET /api/export/csv/

### Admin dashboard

- GET /api/admin/dashboard/
- GET /api/admin/analytics/
- GET /api/admin/documents/
- GET /api/admin/chunks/
- GET /api/admin/sessions/
- GET /api/admin/graph/

## What is completed in this repo

### Completed

- Dependency repair for Python 3.11
- Django startup validation
- Search explanation API
- Graph search API
- Export API
- Better prompt structure
- Dashboard analytics endpoints
- Full project documentation set
- Docker deployment scaffolding

### Not fully completed

- Full React frontend
- Authentication and RBAC
- Admin upload pipeline
- Production deployment to cloud
- Large-scale testing and integration coverage

## Roadmap status

This project is in a strong backend-ready state, but the full enterprise product stack still needs additional work for:

- user login and role-based access control
- document upload automation
- frontend dashboard and chat UI
- production deployment and observability

## Deployment notes

The project includes Docker examples for local containerized runs.
For production, use:

- Backend: Render or Railway
- Frontend: Vercel
- LLM: Ollama self-hosted or a hosted API
- Database: PostgreSQL via Supabase / Render

## License

This project is intended for educational and internal enterprise demonstration use.
