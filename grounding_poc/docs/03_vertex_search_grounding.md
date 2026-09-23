# Grounding Method 3: Grounding with Vertex AI Search Services (`vertex_search`)

> **Customer Demo Summary**: Ground Gemini models on your private internal company data (PDFs, docs, intranet, BigQuery) without exposing data to the public internet.

---

## 1. What is Vertex AI Search Grounding?

**Grounding with Vertex AI Search** connects Gemini to internal enterprise datastores using private Retrieval-Augmented Generation (RAG). Instead of searching the web, Gemini searches your company's private documents (e.g., policy manuals, architecture specs, customer tickets, BigQuery data) to answer questions with exact internal references.

### Why Use It? (Business Value)
* **Private RAG over Company Knowledge**: Turn internal docs (PDFs, Markdown, Word, HTML) into an intelligent Q&A system.
* **Zero Data Leakage**: Operations remain strictly inside your private Google Cloud IAM security perimeter.
* **Hybrid Semantic Vector Search**: Combines keyword matching with semantic vector retrieval for accurate document discovery.
* **Datastore Scoping**: Point queries to specific datastores tailored for sales, engineering, HR, or support.

---

## 2. Official Google Documentation

* 📖 **Ground with Vertex AI Search**: [Ground Gemini with Private Data Docs](https://cloud.google.com/vertex-ai/generative-ai/docs/grounding/ground-with-vertex-data)
* 📖 **Vertex AI Search Overview**: [Vertex AI Search & Conversation Guide](https://cloud.google.com/generative-ai-app-builder/docs/introduction)

---

## 3. Simple Code Example (How Easy It Is)

Attach a `VertexAISearch` retrieval tool referencing your private datastore ID:

```python
from google import genai
from google.genai import types

# 1. Initialize Client under Vertex AI Enterprise mode
client = genai.Client(
    vertexai=True, project="your-gcp-project-id", location="us-central1"
)

# 2. Query Gemini grounded on internal Vertex AI Search Datastore
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Summarize internal company travel reimbursement policy",
    config=types.GenerateContentConfig(
        tools=[
            types.Tool(
                retrieval=types.Retrieval(
                    vertex_ai_search=types.VertexAISearch(
                        datastore="projects/your-gcp-project-id/locations/global/collections/default_collection/dataStores/hr-policy-datastore"
                    )
                )
            )
        ]
    ),
)

# 3. Print answer grounded in internal enterprise docs
print(response.text)
```

---

## 4. How to Test & Demo

### Option A: Using HTTP REST API (`curl`)

```bash
curl -X POST "http://127.0.0.1:8000/api/ground" \
     -H "Content-Type: application/json" \
     -d '{
           "prompt": "Internal architecture guidelines",
           "mode": "vertex_search",
           "datastore_id": "engineering-docs-ds"
         }'
```

### Option B: Side-by-Side Comparison Endpoint (`/api/compare`)

Run all 3 grounding modes simultaneously to show the customer the difference:

```bash
curl -X POST "http://127.0.0.1:8000/api/compare" \
     -H "Content-Type: application/json" \
     -d '{
           "prompt": "Compare internal policies vs public industry standards"
         }'
```

### Option C: Quick Test via `pytest`

```bash
PYTHONPATH=. pytest tests/test_grounding.py -k test_single_grounding_vertex_search
```
