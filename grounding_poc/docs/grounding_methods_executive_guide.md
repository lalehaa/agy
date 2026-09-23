# Google Gemini & Vertex AI Grounding Mechanisms

This document outlines the four primary grounding options available across Google Gemini APIs, Google Cloud Vertex AI, and the Gemini Enterprise Agent Platform.

---

## 1. Grounding Options Comparison

| Grounding Method | Target Scope | SDK Tool / Parameter | Key Value Proposition |
| :--- | :--- | :--- | :--- |
| **Standard Google Search Grounding** | Public Web | `Tool(google_search=GoogleSearch())` | Connects Gemini models to public Google Search for live web information and inline citations. |
| **Web Grounding Enterprise** | Public Web (Enterprise) | `Tool(enterprise_web_search=EnterpriseWebSearch())` | Backed by 99.9% SLA, enterprise Data Processing Addendum (no data training), and Cloud Audit Logging. |
| **Grounding with Vertex AI Search Services** | Private Data | `Tool(retrieval=Retrieval(vertex_ai_search=...))` | Private RAG over internal enterprise document repositories within Google Cloud IAM security boundaries. |
| **Grounding with Agent Search** | Private Agent Data | `Tool(retrieval=Retrieval(vertex_ai_search=...))` + `api_version="v1"` | Connects AI agents to enterprise knowledge engines using the Gemini Enterprise Agent Platform. |

---

## 2. Official Google Documentation

* **Standard Google Search Grounding**: https://ai.google.dev/gemini-api/docs/grounding
* **Web Grounding Enterprise**: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/grounding/web-grounding-enterprise
* **Grounding with Vertex AI Search Services**: https://cloud.google.com/vertex-ai/generative-ai/docs/grounding/ground-with-vertex-data
* **Grounding with Agent Search**: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/grounding/grounding-with-vertex-ai-search

---

## 3. Code Implementations

### Method 1: Standard Google Search Grounding

```python
from google import genai
from google.genai.types import GenerateContentConfig, GoogleSearch, Tool

client = genai.Client()
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What are the latest developments in artificial intelligence?",
    config=GenerateContentConfig(tools=[Tool(google_search=GoogleSearch())]),
)

print(response.text)
```

### Method 2: Web Grounding Enterprise

```python
from google import genai
from google.genai.types import (
    EnterpriseWebSearch,
    GenerateContentConfig,
    HttpOptions,
    Tool,
)

client = genai.Client(http_options=HttpOptions(api_version="v1"))
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="When is the next total solar eclipse in the United States?",
    config=GenerateContentConfig(
        tools=[Tool(enterprise_web_search=EnterpriseWebSearch())]
    ),
)

print(response.text)
```

### Method 3: Grounding with Vertex AI Search Services

```python
from google import genai
from google.genai.types import (
    GenerateContentConfig,
    Retrieval,
    Tool,
    VertexAISearch,
)

client = genai.Client(
    vertexai=True, project="PROJECT_ID", location="us-central1"
)
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Summarize internal company travel reimbursement policy",
    config=GenerateContentConfig(
        tools=[
            Tool(
                retrieval=Retrieval(
                    vertex_ai_search=VertexAISearch(
                        datastore="projects/PROJECT_ID/locations/LOCATION/collections/default_collection/dataStores/DATASTORE_ID"
                    )
                )
            )
        ]
    ),
)

print(response.text)
```

### Method 4: Grounding with Agent Search

```python
from google import genai
from google.genai.types import (
    GenerateContentConfig,
    HttpOptions,
    Retrieval,
    Tool,
    VertexAISearch,
)

client = genai.Client(http_options=HttpOptions(api_version="v1"))
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Summarize internal company guidelines",
    config=GenerateContentConfig(
        tools=[
            Tool(
                retrieval=Retrieval(
                    vertex_ai_search=VertexAISearch(
                        datastore="projects/PROJECT_ID/locations/LOCATION/collections/default_collection/dataStores/DATASTORE_ID"
                    )
                )
            )
        ]
    ),
)

print(response.text)
```

---

## 4. Grounding Method Breakdown

### Method 1: Standard Google Search Grounding (`google_search`)
* **Overview**: Dynamically queries Google Search during content generation to provide up-to-date web information and inline source links.
* **Target Audience**: Consumer-facing web applications, prototypes, and public tools.
* **Authentication**: Developer API Key.

### Method 2: Web Grounding Enterprise (`web_enterprise`)
* **Overview**: Provides enterprise-grade web search grounding on the Gemini Enterprise Agent Platform with strict data protection, audit logging, and SLA guarantees.
* **Target Audience**: Enterprise production systems subject to compliance, legal, and privacy regulations.
* **Authentication**: Google Cloud IAM / Service Accounts.

### Method 3: Grounding with Vertex AI Search Services (`vertex_search`)
* **Overview**: Grounds model responses on private enterprise data repositories (PDFs, Markdown, BigQuery) using Vertex AI Search Datastores.
* **Target Audience**: Enterprise knowledge portals, internal Q&A tools, and document analysis systems.
* **Authentication**: Vertex AI Context (`vertexai=True`) and Google Cloud IAM.

### Method 4: Grounding with Agent Search (`agent_search`)
* **Overview**: Connects AI agents to enterprise knowledge engines and search indices through the Gemini Enterprise Agent Platform.
* **Target Audience**: Enterprise multi-agent platforms and autonomous enterprise workflows.
* **Authentication**: Gemini Enterprise Agent Platform API (`api_version="v1"`).

---

## 5. API Testing Examples

### REST API Endpoint Query Example

```json
{
  "prompt": "What are the latest developments in artificial intelligence?",
  "mode": "google_search"
}
```

### REST API Endpoint Query for Private Datastore

```json
{
  "prompt": "Summarize internal company travel reimbursement policy",
  "mode": "vertex_search",
  "datastore_id": "hr-policy-datastore"
}
```
