from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from app.routers.api import router as api_router

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Antigravity Academy",
    description="Interactive educational dashboard and developer playground for Google Antigravity.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = BASE_DIR.parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Templates
templates_dir = BASE_DIR / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# Include routers
app.include_router(api_router)


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
