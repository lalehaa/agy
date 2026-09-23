# Grounding Method 2: GCP Web Grounding Enterprise (`web_enterprise`)

> **Customer Demo Summary**: Enterprise web grounding using Gemini Enterprise Agent Platform's dedicated `EnterpriseWebSearch` tool, featuring SLA guarantees (99.9%), enterprise data governance (DPA), and audit logging.

---

## 1. What is Web Grounding Enterprise?

**Web Grounding Enterprise** connects Gemini models to live web search using the **Gemini Enterprise Agent Platform** and the dedicated `EnterpriseWebSearch` tool. Designed for enterprise production environments, it enforces Google Cloud enterprise security, data privacy (no data used for model training), Cloud Audit Logging, and high-availability SLAs.

### Key Characteristics
* **Dedicated Enterprise Tool**: Uses `Tool(enterprise_web_search=EnterpriseWebSearch())`.
* **Data Privacy Guarantee (DPA)**: Covered under Google Cloud DPA—prompts and search queries are **never** logged or used for public model training.
* **Audit & Compliance**: Integrates directly with Google Cloud Audit Logs.
* **Production SLA (99.9%)**: Backed by Google Cloud production availability and dedicated throughput limits.

---

## 2. Official Google Documentation

* 📖 **Gemini Enterprise Agent Platform - Web Grounding Enterprise**: [Google Cloud Gemini Enterprise Web Grounding Docs](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/grounding/web-grounding-enterprise)

---

## 3. Code Example (Gemini Enterprise Agent Platform)

Notice that Method 2 explicitly imports and attaches `EnterpriseWebSearch()`:

```python
from google import genai
from google.genai.types import (
    EnterpriseWebSearch,
    GenerateContentConfig,
    HttpOptions,
    Tool,
)

# 1. Initialize client configured for Gemini Enterprise Agent Platform API (v1)
client = genai.Client(http_options=HttpOptions(api_version="v1"))

# 2. Call Gemini using the Enterprise Web Search tool
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="When is the next total solar eclipse in the United States?",
    config=GenerateContentConfig(
        tools=[
            # Use Enterprise Web Search Tool
            Tool(enterprise_web_search=EnterpriseWebSearch())
        ],
    ),
)

# 3. Print enterprise-grounded response
print(response.text)
```

---

## 4. Code Side-by-Side Comparison: Method 1 vs. Method 2

```python
# -------------------------------------------------------------
# METHOD 1: Standard Google Search Grounding (Consumer / Developer API)
# -------------------------------------------------------------
from google.genai.types import GoogleSearch, Tool

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="...",
    config=GenerateContentConfig(
        tools=[
            # Standard Google Search tool
            Tool(google_search=GoogleSearch())
        ]
    ),
)

# -------------------------------------------------------------
# METHOD 2: Web Grounding Enterprise (Gemini Enterprise Agent Platform)
# -------------------------------------------------------------
from google.genai.types import EnterpriseWebSearch, Tool

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="...",
    config=GenerateContentConfig(
        tools=[
            # Dedicated Enterprise Web Search tool
            Tool(enterprise_web_search=EnterpriseWebSearch())
        ]
    ),
)
```

### Key Differences Summary:
* **Tool Object**: Method 1 uses `google_search=GoogleSearch()`, whereas Method 2 uses `enterprise_web_search=EnterpriseWebSearch()`.
* **Infrastructure Target**: Method 2 routes requests through Gemini Enterprise Agent Platform with enterprise DPA and audit logging.

---

## 5. How to Test & Demo

### Option A: HTTP REST API (`curl`)

```bash
curl -X POST "http://127.0.0.1:8000/api/ground" \
     -H "Content-Type: application/json" \
     -d '{
           "prompt": "When is the next total solar eclipse in the United States?",
           "mode": "web_enterprise"
         }'
```

### Option B: Quick Test via `pytest`

```bash
PYTHONPATH=. pytest tests/test_grounding.py -k test_single_grounding_web_enterprise
```
