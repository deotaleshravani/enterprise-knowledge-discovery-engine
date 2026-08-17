# Project Plan and Status

## Phase status summary

### Completed

- Environment repair for Python 3.11
- Dependency stabilization
- Django health validation
- Hybrid search and reranking
- Graph search
- Search explanation endpoint
- Export API
- Prompt engineering improvements
- Dashboard analytics endpoints
- Documentation and deployment scaffolding

### In progress / future

- React frontend for dashboard and chat
- Authentication and RBAC
- Upload pipeline for scanned and exported enterprise data
- More advanced analytics and search metrics
- Production deployment setup

## Roadmap mapping

### Step 6 — Graph Search
Status: implemented

- Relationship and entity lookup support is available in the graph search module.
- Example queries such as “Who worked with Neha?” are supported by the graph logic.

### Step 7 — Better Prompt Engineering
Status: implemented

- The active prompt includes role, instructions, context, rules, confidence policy, citation policy, and formatting guidance.

### Step 8 — Export APIs
Status: implemented

- JSON and CSV export endpoints are available.

### Step 9 — Documentation
Status: implemented in project docs

- README, architecture guide, API docs, database design, deployment guide, and sequence diagrams are included.

### Step 10 — Deployment
Status: scaffolded

- Dockerfile and docker-compose.yml were added for local container-based deployment.
- Cloud production steps are documented.

## Remaining enterprise-focused work

1. Full frontend dashboard with React
2. Authentication + RBAC roles
3. Real document upload interface
4. Better graph entity resolution
5. Advanced analytics pages and charts
6. Production deployment and reliability monitoring

## Recommended order

1. Finish RBAC and auth
2. Add upload pipeline
3. Add frontend dashboard
4. Add production deployment configuration
5. Add robust tests and smoke checks
