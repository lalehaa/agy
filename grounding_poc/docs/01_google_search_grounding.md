# Grounding Method 1: Google Search Grounding (`google_search`)

> **Customer Demo Summary**: Connect Gemini models to live, public web search data using standard `GoogleSearch()`.

---

## 1. What is Google Search Grounding?

**Google Search Grounding** connects Gemini models to the public Google Search engine using the standard `GoogleSearch()` tool in the Google GenAI SDK. It allows developers to quickly build applications that need real-time web facts, breaking news, or public documentation citations.

### Key Characteristics
* **Tool Object**: Uses `Tool(google_search=GoogleSearch())`.
* **API Target**: Standard Gemini Developer API / Vertex AI.
* **Ideal For**: Prototypes, web applications, and consumer-facing features.

---

## 2. Official Google Documentation

* 📖 **Gemini API Grounding Guide**: [Google GenAI API Grounding Reference](https://ai.google.dev/gemini-api/docs/grounding)
* 📖 **Vertex AI Grounding Overview**: [Google Cloud Grounding Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/grounding/overview)

---

## 3. Code Example (Standard Google Search Tool)

Notice that Method 1 uses **`Tool(google_search=GoogleSearch())`**:

```python
from google import genai
from google.genai.types import GoogleSearch, GenerateContentConfig, Tool

# 1. Initialize client
client = genai.Client()

# 2. Call Gemini with standard Google Search tool enabled
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What are the latest developments in AI?",
    config=GenerateContentConfig(
        tools=[
            # Standard Google Search tool
            Tool(google_search=GoogleSearch())
        ]
    ),
)

# 3. Print grounded answer & public web citations
print(response.text)
```

---

## 4. Code Side-by-Side Comparison: Method 1 vs. Method 2

```python
# -------------------------------------------------------------
# METHOD 1: Standard Google Search Grounding (google_search)
# -------------------------------------------------------------
from google.genai.types import GoogleSearch, Tool

config = GenerateContentConfig(
    tools=[
        Tool(google_search=GoogleSearch())  # <--- Standard Google Search Tool
    ]
)

# -------------------------------------------------------------
# METHOD 2: Web Grounding Enterprise (enterprise_web_search)
# -------------------------------------------------------------
from google.genai.types import EnterpriseWebSearch, Tool

config = GenerateContentConfig(
    tools=[
        Tool(
            enterprise_web_search=EnterpriseWebSearch()
        )  # <--- Gemini Enterprise Agent Platform Tool
    ]
)
```

---

## 5. How to Test & Demo

### Option A: HTTP REST API (`curl`)

```bash
curl -X POST "http://127.0.0.1:8000/api/ground" \
     -H "Content-Type: application/json" \
     -d '{
           "prompt": "What are the latest developments in AI?",
           "mode": "google_search"
         }'
```

### Option B: Quick Test via `pytest`

```bash
PYTHONPATH=. pytest tests/test_grounding.py -k test_single_grounding_google_search
```
