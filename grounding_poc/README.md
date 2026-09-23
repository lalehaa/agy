# Vertex AI & Gemini Grounding PoC

A production-ready Proof of Concept (PoC) application benchmarking and comparing the 3 primary Google Vertex AI and Gemini Grounding mechanisms:
1. **Web Grounding Enterprise** (Enterprise Web Search tool)
2. **Grounding with Google Search** (Standard Google Search Grounding via `google-genai` / Vertex AI SDK)
3. **Grounding with Vertex AI Search Services** (Enterprise Unstructured & Structured Datastores)

## Features
- **Side-by-Side Comparison Matrix**: Run prompts simultaneously across all 3 grounding modes.
- **Citation & Source Inspector**: Render grounding web search queries, grounding chunks, title links, confidence scores, and raw JSON metadata.
- **Config & Environment Panel**: Configure GCP Project ID, Location, Model (`gemini-2.5-flash`, `gemini-2.0-flash`), and Datastore IDs in real-time.
- **Mock Fallback**: Automatic mock grounding fallback for local development when GCP credentials are not active.

## Quick Start

1. **Activate Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run Server**:
   ```bash
   uvicorn app.main:app --port 8001 --reload
   ```

3. **Open Dashboard**: Visit `http://localhost:8001` in your browser.

