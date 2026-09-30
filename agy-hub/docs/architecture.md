# Antigravity Academy Architecture: agy-hub & agy-agent

![System Architecture Diagram](agy_architecture_diagram.png)

## High-Level System Architecture

```mermaid
flowchart TB
    subgraph Clients["Surfaces & Clients"]
        WebUser["🧑‍💻 Web Browser<br/>(Antigravity Academy UI)"]
        DevUser["🛠️ Developer / Tester<br/>(ADK Dev-UI / Terminal CLI)"]
    end

    subgraph Hub["agy-hub (Academy Web Application :8000)"]
        direction TB
        Frontend["Single Page App<br/>(Alpine.js + Tailwind CSS)"]
        
        subgraph HubBackend["FastAPI Backend (app/main.py)"]
            APIRouter["API Router (app/routers/api.py)"]
            CurriculumService["Curriculum Engine<br/>(app/curriculum.py)"]
            ConfigValidator["Config Validator<br/>(app/validator.py)"]
        end
        
        DataStore[("User Progress<br/>data/user_progress.json")]
    end

    subgraph Agent["agy-agent (Google ADK Agent Service :8081)"]
        direction TB
        ADKServer["ADK Web Server / Dev-UI<br/>(google.adk.cli.web)"]
        
        subgraph AgentCore["Agent Core (app/agent.py)"]
            AppRunner["App & Runner Instance"]
            RootAgent["Root Agent: agy_assistant<br/>(Instruction + Persona)"]
            Plugins["Plugins & Middlewares<br/>(BasePlugin Hooks)"]
        end

        subgraph ToolSuite["ADK Tool Suite (app/tools.py)"]
            T1["get_slash_command_manual"]
            T2["explain_plan_vs_goal"]
            T3["compare_agy_feature"]
            T4["fetch_latest_agy_docs"]
            T5["generate_config_template"]
            T6["search_agy_catalog"]
        end

        subgraph ServiceLayer["Service & Memory (app/service.py)"]
            AssistantService["AGYAssistantService<br/>(Hybrid Online/Offline)"]
            SessionMemory["SessionContextManager<br/>(Multi-Turn Memory)"]
        end
    end

    subgraph SharedCatalog["Antigravity Master Catalog (catalog/)"]
        SlashCatalog["Slash Commands<br/>(slash_commands.json)"]
        MatrixCatalog["Feature Parity Matrix<br/>(feature_parity_matrix.md)"]
        RulesCatalog["Templates & Rules<br/>(AGENTS.md, GEMINI.md)"]
    end

    subgraph Cloud["External AI & Cloud Services"]
        Gemini["✨ Google Gemini 2.5 Flash<br/>(Vertex AI / Gemini API)"]
        MCPServers["🔌 MCP Servers<br/>(AlloyDB, PostgreSQL, etc.)"]
    end

    %% Interactions
    WebUser -->|"HTTP / REST (:8000)"| Frontend
    Frontend -->|"JSON API Calls"| APIRouter
    APIRouter --> CurriculumService
    APIRouter --> ConfigValidator
    CurriculumService <--> DataStore

    %% Hub to Agent Bridge
    APIRouter -->|"Direct Python Import / Bridge"| AssistantService

    %% Dev User to ADK
    DevUser -->|"HTTP /dev-ui/ (:8081)"| ADKServer
    ADKServer --> AppRunner

    %% Agent Core Flow
    AppRunner --> RootAgent
    RootAgent --> Plugins
    RootAgent --> ToolSuite
    AssistantService --> SessionMemory
    AssistantService --> ToolSuite

    %% Tools to Catalog
    ToolSuite -->|"Grounded Lookup"| SharedCatalog

    %% Agent to Cloud
    RootAgent <-->|"GenAI SDK"| Gemini
    RootAgent <-->|"Model Context Protocol"| MCPServers
```

---

## Component Breakdown

### 1. `agy-hub` (Frontend & Academy Platform)
- **Role**: Interactive browser-based training portal for Google Antigravity.
- **Components**:
  - **Single Page Interface**: Alpine.js + Tailwind UI featuring 5 tabs (Curriculum, Config Generator, Real-time Validator, Interactive Cheatsheet, AI Assistant).
  - **Curriculum Engine**: 7 structured learning modules with interactive coding tasks and progress tracking.
  - **Syntax & Schema Validator**: Validates `.agents/AGENTS.md`, `GEMINI.md`, `SKILL.md`, and `mcp.json`.
  - **Direct Assistant Bridge**: Connects `/api/assistant/chat` directly to `AGYAssistantService` with session history.

### 2. `agy-agent` (Google ADK Autonomous Agent)
- **Role**: Grounded conversational AI assistant built on Google Agent Development Kit (ADK) v2.
- **Components**:
  - **`app/agent.py`**: Configures the `root_agent` with instructions, retry options, and tools.
  - **`app/tools.py`**: 6 specialized tools that query the Antigravity Master Catalog.
  - **`app/service.py`**: High-level service providing `SessionContextManager` and dual online/offline fallback engine.
  - **`app/knowledge.py`**: Deterministic catalog resolution across local workspace and container mounts.

### 3. Shared Catalog (`catalog/`)
- Single source of truth for:
  - 25 Antigravity slash commands.
  - Architectural comparisons (`/plan` vs `/goal`).
  - Competitive matrix (Cursor, Claude Code, Windsurf, Copilot, Devin).
  - Multi-agent blueprints and security policies.
