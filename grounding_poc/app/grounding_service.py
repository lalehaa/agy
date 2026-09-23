import json
import os
import time
from typing import Dict, List, Optional

from app.models import (
    GroundingQueryRequest,
    GroundingResult,
    GroundingMetadata,
    CitationSource,
    GroundingChunk,
    ComparisonResponse,
)


class GroundingService:
    def __init__(self):
        self.project_id = os.getenv("GCP_PROJECT_ID", "demo-gcp-project")
        self.location = os.getenv("GCP_LOCATION", "us-central1")
        self.datastore_id = os.getenv(
            "VERTEX_SEARCH_DATASTORE_ID", "demo-enterprise-datastore"
        )
        self.datastore_location = os.getenv("VERTEX_SEARCH_LOCATION", "global")
        self.default_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    def update_config(
        self,
        project_id: Optional[str] = None,
        location: Optional[str] = None,
        datastore_id: Optional[str] = None,
        model_name: Optional[str] = None,
    ):
        if project_id:
            self.project_id = project_id
        if location:
            self.location = location
        if datastore_id:
            self.datastore_id = datastore_id
        if model_name:
            self.default_model = model_name

    def get_config(self) -> Dict[str, str]:
        return {
            "project_id": self.project_id,
            "location": self.location,
            "datastore_id": self.datastore_id,
            "model_name": self.default_model,
        }

    def _execute_google_search_grounding(
        self, prompt: str, model_name: str
    ) -> GroundingResult:
        start_time = time.time()

        # Try live SDK invocation if credentials exist
        has_credentials = bool(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or os.getenv("GEMINI_API_KEY")
        )
        if has_credentials:
            try:
                from google import genai
                from google.genai import types

                client = genai.Client()
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        tools=[types.Tool(google_search=types.GoogleSearch())]
                    ),
                )
                elapsed = (time.time() - start_time) * 1000

                # Extract grounding metadata from live SDK response
                meta = GroundingMetadata()
                candidates = getattr(response, "candidates", [])
                if candidates:
                    cand = candidates[0]
                    gm = getattr(cand, "grounding_metadata", None)
                    if gm:
                        queries = getattr(gm, "web_search_queries", [])
                        meta.web_search_queries = [str(q) for q in queries]

                        chunks = getattr(gm, "grounding_chunks", [])
                        for c in chunks:
                            web = getattr(c, "web", None)
                            if web:
                                meta.citations.append(
                                    CitationSource(
                                        title=getattr(web, "title", "Web Result"),
                                        url=getattr(web, "uri", "#"),
                                    )
                                )

                return GroundingResult(
                    mode="google_search",
                    mode_title="Grounding with Google Search",
                    response_text=response.text or "No response text.",
                    metadata=meta,
                    latency_ms=round(elapsed, 2),
                    is_mock=False,
                    raw_response_json=json.dumps({"status": "live", "prompt": prompt}),
                )
            except Exception as e:
                # Fallback to mock on SDK exception
                pass

        # Mock / Demo Grounding Response
        elapsed = (time.time() - start_time) * 1000 + 320.0
        meta = GroundingMetadata(
            web_search_queries=[
                f"{prompt} official documentation",
                f"{prompt} Google Cloud release notes",
            ],
            citations=[
                CitationSource(
                    title="Google Cloud Documentation - Vertex AI Grounding",
                    url="https://cloud.google.com/vertex-ai/generative-ai/docs/grounding/overview",
                    snippet="Grounding with Google Search connects Gemini models to public web search results.",
                    confidence_score=0.96,
                ),
                CitationSource(
                    title="Gemini API Grounding Reference",
                    url="https://ai.google.dev/gemini-api/docs/grounding",
                    snippet="Enable real-time search grounding by attaching GoogleSearch tool to content generation requests.",
                    confidence_score=0.92,
                ),
            ],
            chunks=[
                GroundingChunk(
                    text=f"Grounding with Google Search allows Gemini models to fetch live, up-to-date web information for queries like '{prompt}'.",
                    source_indices=[0, 1],
                )
            ],
            search_entry_point_html='<div class="google-search-chip">Search: <strong>'
            + prompt
            + "</strong></div>",
        )

        response_text = (
            f"Based on real-time Google Search grounding, here are key insights for '{prompt}':\n\n"
            "1. **Live Web Connectivity**: Grounding with Google Search verifies model statements using fresh web indices.\n"
            "2. **Inline Citations**: Facts are tied directly to web search result sources with confidence metrics.\n"
            "3. **Recency & Accuracy**: Reduces hallucinations by injecting search result snippets into the model prompt context."
        )

        return GroundingResult(
            mode="google_search",
            mode_title="Grounding with Google Search",
            response_text=response_text,
            metadata=meta,
            latency_ms=round(elapsed, 2),
            is_mock=True,
            raw_response_json=json.dumps(
                {
                    "mode": "google_search",
                    "search_queries": meta.web_search_queries,
                    "citations_count": len(meta.citations),
                },
                indent=2,
            ),
        )

    def _execute_web_enterprise_grounding(
        self, prompt: str, model_name: str
    ) -> GroundingResult:
        start_time = time.time()
        elapsed = (time.time() - start_time) * 1000 + 410.0

        meta = GroundingMetadata(
            web_search_queries=[
                f"enterprise {prompt} policy",
                f"GCP enterprise web grounding compliance {prompt}",
            ],
            citations=[
                CitationSource(
                    title="GCP Web Grounding Enterprise Docs",
                    url="https://cloud.google.com/vertex-ai/docs/enterprise-grounding",
                    snippet="Enterprise Web Grounding provides SLA-backed web search grounding with data governance and audit logs.",
                    confidence_score=0.98,
                ),
                CitationSource(
                    title="Vertex AI Enterprise Search Security Matrix",
                    url="https://cloud.google.com/vertex-ai/docs/security/grounding-compliance",
                    snippet="Enterprise Search Grounding guarantees customer data isolation and strict region residency.",
                    confidence_score=0.95,
                ),
            ],
            chunks=[
                GroundingChunk(
                    text=f"GCP Web Grounding Enterprise applies enterprise compliance and audit tracking when grounding '{prompt}'.",
                    source_indices=[0, 1],
                )
            ],
            search_entry_point_html='<div class="enterprise-chip"><i class="fa-solid fa-building-shield"></i> GCP Web Grounding Enterprise</div>',
        )

        response_text = (
            f"**GCP Web Grounding Enterprise Report** for '{prompt}':\n\n"
            "• **Enterprise Governance**: Operates under strict Google Cloud enterprise data processing agreements (DPA).\n"
            "• **Audit Logging**: All grounding queries, retrieved sources, and model responses are logged to Cloud Logging.\n"
            "• **High Reliability**: Backed by Google Cloud production SLAs and dedicated throughput limits."
        )

        return GroundingResult(
            mode="web_enterprise",
            mode_title="GCP Web Grounding Enterprise",
            response_text=response_text,
            metadata=meta,
            latency_ms=round(elapsed, 2),
            is_mock=True,
            raw_response_json=json.dumps(
                {
                    "mode": "web_enterprise",
                    "project_id": self.project_id,
                    "location": self.location,
                    "enterprise_sla": "99.9%",
                },
                indent=2,
            ),
        )

    def _execute_vertex_search_grounding(
        self, prompt: str, model_name: str, datastore_id: Optional[str] = None
    ) -> GroundingResult:
        start_time = time.time()
        ds_id = datastore_id or self.datastore_id
        elapsed = (time.time() - start_time) * 1000 + 290.0

        meta = GroundingMetadata(
            web_search_queries=[f"datastore:{ds_id} search '{prompt}'"],
            citations=[
                CitationSource(
                    title=f"Internal Document - {ds_id}/doc_architecture.pdf",
                    url=f"gs://{self.project_id}-knowledge-base/docs/doc_architecture.pdf",
                    snippet=f"Internal reference doc for '{prompt}' stored in Vertex AI Search datastore {ds_id}.",
                    confidence_score=0.99,
                ),
                CitationSource(
                    title=f"Enterprise Knowledge Base - {ds_id}/api_guidelines.md",
                    url=f"gs://{self.project_id}-knowledge-base/docs/api_guidelines.md",
                    snippet=f"Standard operating procedures matching '{prompt}'.",
                    confidence_score=0.94,
                ),
            ],
            chunks=[
                GroundingChunk(
                    text=f"Vertex AI Search retrieved 2 internal documents from Datastore '{ds_id}' relevant to '{prompt}'.",
                    source_indices=[0, 1],
                )
            ],
            search_entry_point_html=f'<div class="vertex-search-chip"><i class="fa-solid fa-database"></i> Datastore: <strong>{ds_id}</strong></div>',
        )

        response_text = (
            f"**Vertex AI Search Services Grounded Result** for '{prompt}' (Datastore: `{ds_id}`):\n\n"
            "1. **Private Datastore Access**: Grounded exclusively against internal enterprise documents stored in Vertex AI Search.\n"
            "2. **Semantic Vector Search**: Combines keyword and hybrid vector retrieval over PDF, HTML, and BigQuery data stores.\n"
            "3. **Zero Data Leakage**: Search indices remain strictly within your Google Cloud IAM boundary."
        )

        return GroundingResult(
            mode="vertex_search",
            mode_title="Grounding with Vertex AI Search Services",
            response_text=response_text,
            metadata=meta,
            latency_ms=round(elapsed, 2),
            is_mock=True,
            raw_response_json=json.dumps(
                {
                    "mode": "vertex_search",
                    "project_id": self.project_id,
                    "datastore_id": ds_id,
                    "datastore_location": self.datastore_location,
                },
                indent=2,
            ),
        )

    def execute_grounding(self, request: GroundingQueryRequest) -> GroundingResult:
        model = request.model_name or self.default_model
        mode = request.mode or "google_search"

        if mode == "web_enterprise":
            return self._execute_web_enterprise_grounding(request.prompt, model)
        elif mode == "vertex_search":
            return self._execute_vertex_search_grounding(
                request.prompt, model, datastore_id=request.datastore_id
            )
        else:
            return self._execute_google_search_grounding(request.prompt, model)

    def compare_all(
        self, prompt: str, model_name: Optional[str] = None
    ) -> ComparisonResponse:
        model = model_name or self.default_model

        req_search = GroundingQueryRequest(
            prompt=prompt, mode="google_search", model_name=model
        )
        req_enterprise = GroundingQueryRequest(
            prompt=prompt, mode="web_enterprise", model_name=model
        )
        req_vertex = GroundingQueryRequest(
            prompt=prompt, mode="vertex_search", model_name=model
        )

        res_search = self.execute_grounding(req_search)
        res_enterprise = self.execute_grounding(req_enterprise)
        res_vertex = self.execute_grounding(req_vertex)

        return ComparisonResponse(
            prompt=prompt,
            results={
                "web_enterprise": res_enterprise,
                "google_search": res_search,
                "vertex_search": res_vertex,
            },
        )
