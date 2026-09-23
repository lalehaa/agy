from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class GroundingMode(str, Enum):
    WEB_ENTERPRISE = "web_enterprise"
    GOOGLE_SEARCH = "google_search"
    VERTEX_SEARCH = "vertex_search"


class CitationSource(BaseModel):
    title: str
    url: str
    snippet: Optional[str] = None
    confidence_score: Optional[float] = None


class GroundingChunk(BaseModel):
    text: str
    source_indices: List[int] = Field(default_factory=list)


class GroundingMetadata(BaseModel):
    web_search_queries: List[str] = Field(default_factory=list)
    citations: List[CitationSource] = Field(default_factory=list)
    chunks: List[GroundingChunk] = Field(default_factory=list)
    search_entry_point_html: Optional[str] = None


class GroundingQueryRequest(BaseModel):
    prompt: str = Field(
        ..., example="What are the latest developments in Vertex AI Grounding?"
    )
    mode: Optional[str] = Field(default="google_search")
    model_name: str = Field(default="gemini-2.0-flash")
    project_id: Optional[str] = None
    location: Optional[str] = None
    datastore_id: Optional[str] = None


class GroundingResult(BaseModel):
    mode: str
    mode_title: str
    response_text: str
    metadata: GroundingMetadata
    latency_ms: float
    is_mock: bool = False
    raw_response_json: Optional[str] = None


class ComparisonResponse(BaseModel):
    prompt: str
    results: Dict[str, GroundingResult]


class ConfigRequest(BaseModel):
    project_id: Optional[str] = None
    location: Optional[str] = None
    datastore_id: Optional[str] = None
    model_name: Optional[str] = None


class ConfigResponse(BaseModel):
    project_id: str
    location: str
    datastore_id: str
    model_name: str
