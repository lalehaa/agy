# Grounding PoC Technical Specification

## Overview
Grounding PoC demonstrates and evaluates Google Cloud Vertex AI & Gemini Grounding capabilities across three distinct modes.

## Architecture & Directory Structure
```
grounding_poc/
├── .venv/                      # Python 3.11+ Virtual Environment
├── app/
│   ├── main.py                 # FastAPI Application Entrypoint
│   ├── models.py               # Pydantic Schemas for Requests & Responses
│   ├── grounding_service.py    # Service implementing 3 Grounding Strategies
│   ├── routers/
│   │   └── api.py              # REST API Endpoints for Single & Side-by-Side Queries
│   └── templates/
│       └── index.html          # Comparison Dashboard Template
├── static/
│   ├── app.js                  # Alpine.js Client Store
│   └── vendor/
│       ├── alpine.min.js       # Bundled Alpine.js
│       └── tailwind.min.js     # Bundled Tailwind CSS
├── tests/
│   └── test_grounding.py       # Pytest Integration & Unit Test Suite
├── requirements.txt
├── README.md
└── technical_spec.md
```

## Grounding Modes Specification

1. **Web Grounding Enterprise** (`web_enterprise`):
   - Uses `google-genai` / `google-cloud-aiplatform` with Enterprise Web Search parameters (`enterprise_web_search`).
   - Retrieves real-time web content with enterprise SLA and audit logging.

2. **Grounding with Google Search** (`google_search`):
   - Uses Gemini Search Grounding (`Tool(google_search=GoogleSearch())`).
   - Extracts web search queries, web source titles, URLs, and grounding metadata.

3. **Grounding with Vertex AI Search Services** (`vertex_search`):
   - Uses Vertex AI Search datastore retrieval (`Tool(retrieval=Retrieval(vertex_ai_search=...))`).
   - Queries custom GCP Datastores (documents, internal knowledge bases, enterprise search indexes).

## Environment Variables
- `GCP_PROJECT_ID` (e.g., `my-gcp-project`)
- `GCP_LOCATION` (default `us-central1`)
- `VERTEX_SEARCH_DATASTORE_ID` (e.g., `my-datastore-id`)
- `VERTEX_SEARCH_LOCATION` (default `global`)

