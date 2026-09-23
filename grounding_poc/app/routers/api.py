from fastapi import APIRouter, HTTPException, status

from app.models import (
    GroundingQueryRequest,
    GroundingResult,
    ComparisonResponse,
    ConfigRequest,
    ConfigResponse,
)
from app.grounding_service import GroundingService

router = APIRouter(prefix="/api", tags=["grounding"])
service = GroundingService()


@router.post("/ground", response_model=GroundingResult)
def execute_grounding(request: GroundingQueryRequest) -> GroundingResult:
    if not request.prompt or not request.prompt.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prompt text cannot be empty.",
        )
    return service.execute_grounding(request)


@router.post("/compare", response_model=ComparisonResponse)
def compare_grounding_modes(request: GroundingQueryRequest) -> ComparisonResponse:
    if not request.prompt or not request.prompt.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prompt text cannot be empty.",
        )
    return service.compare_all(request.prompt, model_name=request.model_name)


@router.get("/config", response_model=ConfigResponse)
def get_config() -> ConfigResponse:
    cfg = service.get_config()
    return ConfigResponse(**cfg)


@router.post("/config", response_model=ConfigResponse)
def update_config(req: ConfigRequest) -> ConfigResponse:
    service.update_config(
        project_id=req.project_id,
        location=req.location,
        datastore_id=req.datastore_id,
        model_name=req.model_name,
    )
    cfg = service.get_config()
    return ConfigResponse(**cfg)
