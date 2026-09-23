# Grounding Method 4: Grounding with Agent Search (`agent_search`)

> **Customer Demo Summary**: Ground Gemini models on private enterprise data and agent engines using Gemini Enterprise Agent Platform's **Grounding with Agent Search**.

---

## 1. What is Grounding with Agent Search?

**Grounding with Agent Search** connects Gemini models to enterprise agent knowledge engines and search indices through the **Gemini Enterprise Agent Platform**. It enables autonomous AI agents and enterprise applications to perform accurate, factual Retrieval-Augmented Generation (RAG) over corporate document stores, enterprise databases, and internal APIs with strict data privacy, enterprise access controls, and zero data leakage.

### Key Value Propositions
* **Enterprise Agent Engine Connectivity**: Connects AI agents directly to organization knowledge stores (PDFs, docs, intranet, BigQuery, enterprise search).
* **Zero External Data Leakage**: Prompts, queries, and retrieved contexts remain strictly within your Google Cloud IAM security perimeter.
* **Gemini Enterprise Agent Platform Integration**: Uses standard `HttpOptions(api_version="v1")` and enterprise retrieval tools.
* **Hybrid Semantic & Vector Retrieval**: Combines keyword precision with dense vector embeddings for high-accuracy agent decision making.

---

## 2. Official Google Documentation

* 📖 **Gemini Enterprise Agent Platform - Grounding with Agent Search**: [Grounding with Agent Search Documentation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/grounding/grounding-with-vertex-ai-search)

---

## 3. Code Example (Gemini Enterprise Agent Platform)

Notice that Method 4 uses `HttpOptions(api_version="v1")` with the `VertexAISearch` / Agent Search retrieval tool:

```python
from google import genai
from google.genai.types import (
    GenerateContentConfig,
    HttpOptions,
    Retrieval,
    Tool,
    VertexAISearch,
)

# 1. Initialize client configured for Gemini Enterprise Agent Platform API (v1)
client = genai.Client(http_options=HttpOptions(api_version="v1"))

# 2. Call Gemini using Grounding with Agent Search
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Summarize internal company guidelines",
    config=GenerateContentConfig(
        tools=[
            # Use Grounding with Agent Search Tool for enterprise knowledge
            Tool(
                retrieval=Retrieval(
                    vertex_ai_search=VertexAISearch(
                        datastore="projects/YOUR_PROJECT_ID/locations/global/collections/default_collection/dataStores/YOUR_DATASTORE_ID"
                    )
                )
            )
        ],
    ),
)

# 3. Print grounded answer derived from enterprise agent search
print(response.text)
```

---

## 4. Complete Code Comparison (All Grounding Methods)

```python
# -------------------------------------------------------------
# METHOD 1: Standard Google Search Grounding (Consumer / Developer API)
# -------------------------------------------------------------
Tool(google_search=GoogleSearch())

# -------------------------------------------------------------
# METHOD 2: Web Grounding Enterprise (Gemini Enterprise Agent Platform)
# -------------------------------------------------------------
Tool(enterprise_web_search=EnterpriseWebSearch())

# -------------------------------------------------------------
# METHOD 3: Grounding with Vertex AI Search Services (Vertex AI SDK)
# -------------------------------------------------------------
Tool(
    retrieval=Retrieval(
        vertex_ai_search=VertexAISearch(
            datastore="projects/PROJECT_ID/locations/LOCATION/collections/default_collection/dataStores/DATASTORE_ID"
        )
    )
)

# -------------------------------------------------------------
# METHOD 4: Grounding with Agent Search (Gemini Enterprise Agent Platform)
# -------------------------------------------------------------
# Client: genai.Client(http_options=HttpOptions(api_version="v1"))
Tool(
    retrieval=Retrieval(
        vertex_ai_search=VertexAISearch(
            datastore="projects/PROJECT_ID/locations/LOCATION/collections/default_collection/dataStores/DATASTORE_ID"
        )
    )
)
```

---

## 5. How to Test & Demo

### Option A: HTTP REST API (`curl`)

```bash
curl -X POST "http://127.0.0.1:8000/api/ground" \
     -H "Content-Type: application/json" \
     -d '{
           "prompt": "Summarize internal company guidelines",
           "mode": "vertex_search",
           "datastore_id": "hr-policy-datastore"
         }'
```

### Option B: Quick Test via `pytest`

```bash
PYTHONPATH=. pytest tests/test_grounding.py -k test_single_grounding_vertex_search
```
