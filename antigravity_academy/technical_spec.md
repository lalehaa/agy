# Antigravity Academy Technical Specification

## Overview
Antigravity Academy is built with Python 3.11+, FastAPI, Pydantic v2, Jinja2 templates, Tailwind CSS, and Alpine.js.

## Directory Structure
```
antigravity_academy/
├── .venv/                   # Isolated Virtual Environment
├── app/
│   ├── main.py              # FastAPI Application Entrypoint
│   ├── models.py            # Pydantic Schemas & Data Types
│   ├── curriculum.py        # Curriculum Data & Lab Instructions
│   ├── validator.py         # Config Schema & Syntax Validators
│   ├── routers/
│   │   └── api.py           # REST API Endpoints
│   └── templates/
│       └── index.html       # Single Page Application Dashboard
├── static/
│   └── app.js               # Alpine.js Client State & Reactivity
├── data/                    # JSON file persistence for lab progress
├── tests/
│   └── test_api.py          # Pytest API and Unit Test Suite
├── requirements.txt
├── README.md
└── technical_spec.md
```

## API Specifications

- `GET /api/curriculum`: Returns all 8 modules and lab details.
- `GET /api/progress`: Returns user completion status across modules.
- `POST /api/progress`: Saves module lab completion status.
- `POST /api/generate/agents`: Generates formatted `.agents/AGENTS.md` content from form input.
- `POST /api/generate/skill`: Generates formatted `SKILL.md` (YAML frontmatter + markdown) from form input.
- `POST /api/generate/mcp`: Generates formatted `mcp.json` configuration from form input.
- `POST /api/validate/config`: Validates string content against schema rules (`agents`, `skill`, `mcp`).

