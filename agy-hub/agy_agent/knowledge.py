# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Knowledge indexing and retrieval engine for Google Antigravity (AGY).

Provides access to:
- The Antigravity Master Catalog (slash commands, competitive parity matrix, workflow deep dives)
- Built-in AGY guides (CLI, IDE, Desktop App 2.0, Python SDK)
- Configuration templates (AGENTS.md, GEMINI.md, SKILL.md, mcp.json)
- Up-to-date documentation topics and live doc retrieval
"""

from __future__ import annotations

import json
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
import urllib.request
import urllib.error

logger = logging.getLogger(__name__)

# Base paths
APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent
WORKSPACE_ROOT = PROJECT_ROOT.parent


def resolve_catalog_dir() -> Path:
    """Deterministically resolves the Antigravity Master Catalog directory."""
    if os.environ.get("CATALOG_DIR"):
        env_dir = Path(os.environ["CATALOG_DIR"]).resolve()
        if env_dir.exists():
            return env_dir

    candidates = [
        PROJECT_ROOT / "catalog",
        WORKSPACE_ROOT / "catalog",
        WORKSPACE_ROOT / "agy-hub" / "catalog",
        WORKSPACE_ROOT / "antigravity_academy" / "catalog",
        Path("/catalog"),
        Path("/app/catalog"),
    ]
    for c in candidates:
        if c.exists():
            return c.resolve()

    return (WORKSPACE_ROOT / "agy-hub" / "catalog").resolve()


CATALOG_DIR = resolve_catalog_dir()

# Built-in skills reference directory
BUILTIN_GUIDE_DIR = Path(
    "/Users/laleha/.gemini/antigravity-cli/builtin/skills/antigravity_guide"
)


class AGYKnowledgeBase:
    """In-memory index and search engine for Antigravity knowledge."""

    def __init__(self, catalog_dir: Optional[Path] = None) -> None:
        self.catalog_dir = catalog_dir or resolve_catalog_dir()
        self.slash_commands: Dict[str, Dict[str, Any]] = {}
        self.competitive_matrix: Dict[str, Any] = {}
        self.plan_vs_goal_doc: str = ""
        self.docs_cache: Dict[str, str] = {}
        self._load_knowledge()

    def _load_knowledge(self) -> None:
        """Loads and indexes knowledge files from disk."""
        # 1. Load slash commands
        slash_json = self.catalog_dir / "slash" / "slash_commands.json"
        if slash_json.exists():
            try:
                with open(slash_json, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for cmd in data.get("commands", []):
                        name = cmd.get("command", "").lower()
                        self.slash_commands[name] = cmd
                        for alias in cmd.get("aliases", []):
                            self.slash_commands[alias.lower()] = cmd
            except Exception as e:
                logger.warning("Error loading slash_commands.json: %s", e)

        # 2. Load competitive matrix
        comp_json = self.catalog_dir / "competitive" / "competitive_matrix.json"
        if comp_json.exists():
            try:
                with open(comp_json, "r", encoding="utf-8") as f:
                    self.competitive_matrix = json.load(f)
            except Exception as e:
                logger.warning("Error loading competitive_matrix.json: %s", e)

        # 3. Load plan vs goal deep dive
        pvg_md = self.catalog_dir / "slash" / "plan_vs_goal.md"
        if pvg_md.exists():
            try:
                with open(pvg_md, "r", encoding="utf-8") as f:
                    self.plan_vs_goal_doc = f.read()
            except Exception as e:
                logger.warning("Error loading plan_vs_goal.md: %s", e)

        # 4. Load builtin guide offline docs if present
        if BUILTIN_GUIDE_DIR.exists():
            ref_dir = BUILTIN_GUIDE_DIR / "references"
            if ref_dir.exists():
                for p in ref_dir.glob("*.md"):
                    try:
                        with open(p, "r", encoding="utf-8") as f:
                            self.docs_cache[p.stem.lower()] = f.read()
                    except Exception as e:
                        logger.warning("Error reading %s: %s", p, e)

        # 5. Populate curated knowledge topics
        self._populate_curated_docs()

    def _populate_curated_docs(self) -> None:
        """Populates curated, verified documentation for core Antigravity concepts."""
        self.docs_cache["skills"] = (
            "# Antigravity Custom Skills (`SKILL.md`)\n\n"
            "Skills extend Antigravity agent capabilities with specialized instructions, scripts, and references.\n"
            "Structure:\n"
            "- Located in `.agents/skills/<skill-name>/` or `~/.gemini/antigravity-cli/skills/`\n"
            "- Must contain `SKILL.md` with YAML frontmatter:\n"
            "  ```yaml\n"
            "  ---\n"
            "  name: skill-name\n"
            "  description: Clear description of when this skill should be activated.\n"
            "  ---\n"
            "  ```\n"
            "- Can include subdirectories: `scripts/`, `examples/`, `references/`, `resources/`."
        )

        self.docs_cache["rules"] = (
            "# Antigravity Rules & Development Teams\n\n"
            "Antigravity supports multi-persona agent teams and strict engineering constraints:\n"
            "- `.agents/AGENTS.md`: Defines role-based subagent personas (@pm, @coder, @qa).\n"
            "- `.agents/GEMINI.md`: Enforces mandatory repo-wide standards (e.g. environment isolation, typing, tests, black formatting).\n"
            "- `CLAUDE.md` / `.cursorrules`: Fully supported for cross-IDE compatibility."
        )

        self.docs_cache["subagents"] = (
            "# Subagents & Parallel Orchestration\n\n"
            "Antigravity provides hierarchical agent invocation:\n"
            "- `invoke_subagent`: Spawns subagents with isolated workspaces or shared trees.\n"
            "- `define_subagent`: Dynamically constructs new specialized subagent types during execution.\n"
            "- `manage_subagents`: Inspects live state, sends messages, or terminates background subagents.\n"
            "- Subagents run concurrently and notify the parent upon completion without busy polling."
        )

        self.docs_cache["sandbox"] = (
            "# Terminal Sandbox & Security Profiles\n\n"
            "Antigravity isolates terminal execution inside lightweight container sandboxes:\n"
            "- Sandboxing prevents accidental system corruption or unauthorized network access.\n"
            "- Granular permission tiers: read-only, workspace-scoped write, and human-confirmation gates.\n"
            "- Secret scrubbing: Automatic redaction of API keys and tokens in terminal output."
        )

        self.docs_cache["mcp"] = (
            "# Model Context Protocol (MCP) in AGY\n\n"
            "Antigravity natively implements the Model Context Protocol (MCP):\n"
            "- Supports both eager and lazily-loaded MCP servers.\n"
            "- Manifest configured in `~/.gemini/antigravity-cli/mcp/` or project configuration.\n"
            "- Tools include `call_mcp_tool`, `list_resources`, and `read_resource`."
        )

        self.docs_cache["sidecars"] = (
            "# Sidecars & Background Daemons\n\n"
            "Persistent sidecars run alongside the agent session:\n"
            "- Used for dev servers, file watchers, test runners, and proxy tunnels.\n"
            "- Managed via `manage_task` with action 'list', 'status', 'send_input', 'kill'."
        )

        self.docs_cache["hooks"] = (
            "# Lifecycle Hooks\n\n"
            "Lifecycle hooks intercept agent actions before and after execution:\n"
            "- Pre-tool hooks: Validate commands before execution (e.g. blocking dangerous commands).\n"
            "- Post-tool hooks: Trigger automated formatting (`black`) or lint checks (`ruff`).\n"
            "- Context hooks: Dynamically inject environmental context or token usage limits."
        )

        self.docs_cache["changelog"] = (
            "# Antigravity 2.0 & Recent Release Notes\n\n"
            "Highlights:\n"
            "- Antigravity 2.0 Desktop Canvas with Auxiliary Pane (Subagents, Background Tasks, Artifacts, Terminals).\n"
            "- Full ADK 2.0 and Agent Platform integration with A2A protocol.\n"
            "- Socratic design interview workflow via `/grill-me`.\n"
            "- Autonomous test-healing loops via `/goal`.\n"
            "- Multi-persona team collaboration via `@pm`, `@coder`, `@qa` personas."
        )

    def search_catalog(self, query: str, category: str = "all") -> Dict[str, Any]:
        """Performs a structured search across the catalog."""
        query_norm = query.lower().strip()
        words = re.findall(r"\w+", query_norm)
        matches: List[Dict[str, Any]] = []

        # 1. Search slash commands
        if category in ("all", "slash", "commands"):
            for cmd_name, cmd in self.slash_commands.items():
                score = 0
                searchable = (
                    f"{cmd.get('command', '')} {cmd.get('summary', '')} "
                    f"{cmd.get('description', '')} {cmd.get('when_to_use', '')} "
                    f"{cmd.get('example', '')} {cmd.get('category', '')}"
                ).lower()

                if query_norm in cmd_name:
                    score += 15
                for w in words:
                    if w in searchable:
                        score += 3

                if score > 0:
                    matches.append(
                        {
                            "type": "slash_command",
                            "title": cmd.get("command"),
                            "category": cmd.get("category"),
                            "summary": cmd.get("summary"),
                            "syntax": cmd.get("syntax"),
                            "when_to_use": cmd.get("when_to_use"),
                            "example": cmd.get("example"),
                            "score": score,
                            "source": "antigravity_academy/catalog/slash/slash_commands.json",
                        }
                    )

        # 2. Search competitive matrix
        if category in ("all", "competitive"):
            dimensions = self.competitive_matrix.get("dimensions", [])
            for dim in dimensions:
                cat_name = dim.get("category_name", "")
                for feat in dim.get("features", []):
                    feat_text = (
                        f"{cat_name} {feat.get('name', '')} {feat.get('antigravity_support', '')} "
                        f"{feat.get('notes', '')}"
                    ).lower()
                    score = 0
                    for w in words:
                        if w in feat_text:
                            score += 2
                    if score > 0:
                        matches.append(
                            {
                                "type": "competitive_feature",
                                "title": feat.get("name"),
                                "category": cat_name,
                                "antigravity_support": feat.get("antigravity_support"),
                                "ratings": feat.get("ratings", {}),
                                "notes": feat.get("notes"),
                                "score": score,
                                "source": "antigravity_academy/catalog/competitive/feature_parity_matrix.md",
                            }
                        )

        # 3. Search plan vs goal if relevant
        if category in ("all", "workflows"):
            pvg_lower = self.plan_vs_goal_doc.lower()
            score = 0
            if "plan" in query_norm or "goal" in query_norm or "workflow" in query_norm:
                score += 8
            for w in words:
                if w in pvg_lower:
                    score += 1
            if score >= 8:
                matches.append(
                    {
                        "type": "workflow_deep_dive",
                        "title": "/plan vs /goal Deep Dive",
                        "summary": "Architectural sign-off with /plan vs autonomous test-healing with /goal.",
                        "score": score,
                        "source": "antigravity_academy/catalog/slash/plan_vs_goal.md",
                    }
                )

        # Sort matches by relevance score
        matches.sort(key=lambda x: x.get("score", 0), reverse=True)
        return {
            "query": query,
            "category": category,
            "total_matches": len(matches),
            "results": matches[:6],
        }

    def get_command_details(self, command_name: str) -> Optional[Dict[str, Any]]:
        """Returns details for a specific slash command."""
        cmd = command_name.strip()
        if not cmd.startswith("/"):
            cmd = f"/{cmd}"
        return self.slash_commands.get(cmd.lower())

    def compare_feature(
        self, feature_area: str, competitor: str = "all"
    ) -> Dict[str, Any]:
        """Compares Antigravity capabilities against specified competitor(s)."""
        feature_norm = feature_area.lower().strip()
        words = re.findall(r"\w+", feature_norm)
        comp_norm = competitor.lower().strip()

        matched_features: List[Dict[str, Any]] = []
        dimensions = self.competitive_matrix.get("dimensions", [])

        for dim in dimensions:
            for feat in dim.get("features", []):
                searchable = (
                    f"{dim.get('category_name', '')} {feat.get('name', '')} {feat.get('notes', '')}"
                ).lower()
                if any(w in searchable for w in words) or feature_norm in searchable:
                    ratings = feat.get("ratings", {})
                    if comp_norm != "all" and comp_norm in ratings:
                        filtered_ratings = {comp_norm: ratings[comp_norm]}
                    else:
                        filtered_ratings = ratings

                    matched_features.append(
                        {
                            "feature": feat.get("name"),
                            "category": dim.get("category_name"),
                            "antigravity": feat.get("antigravity_support"),
                            "ratings": filtered_ratings,
                            "notes": feat.get("notes"),
                        }
                    )

        return {
            "feature_area": feature_area,
            "competitor": competitor,
            "total_matches": len(matched_features),
            "comparisons": matched_features[:5],
            "benchmark_targets": self.competitive_matrix.get("metadata", {}).get(
                "benchmark_targets", []
            ),
        }

    def fetch_docs(self, topic: str) -> Dict[str, Any]:
        """Retrieves official docs for a topic, with live URL fetch or offline cache."""
        clean_topic = topic.lower().strip().replace(" ", "-").replace("/", "")

        # Check local cache first
        content = self.docs_cache.get(clean_topic)
        if not content:
            # Fuzzy check in cache
            for k, v in self.docs_cache.items():
                if clean_topic in k or k in clean_topic:
                    content = v
                    clean_topic = k
                    break

        # Attempt online live fetch if it looks like a URL or official topic
        official_url = f"https://antigravity.google/docs/{clean_topic}"
        live_fetched = False

        if not content:
            try:
                req = urllib.request.Request(
                    official_url,
                    headers={"User-Agent": "AntigravityAcademyAgent/1.0"},
                )
                with urllib.request.urlopen(req, timeout=3) as resp:
                    if resp.status == 200:
                        raw_html = resp.read().decode("utf-8")
                        content = f"# Live Documentation from {official_url}\n\n{raw_html[:2000]}"
                        live_fetched = True
            except Exception:
                # Fallback to general overview if not found
                content = (
                    f"# Google Antigravity Documentation: {topic.title()}\n\n"
                    f"Official reference topic for '{topic}'. See official docs at {official_url}.\n"
                    "Google Antigravity provides native developer tooling, multi-agent workspaces, "
                    "terminal sandbox security, and deep ADK integration."
                )

        return {
            "topic": clean_topic,
            "url": official_url,
            "live_fetched": live_fetched,
            "content": content,
        }

    def generate_config(self, config_type: str, details: str = "") -> Dict[str, Any]:
        """Generates configuration files for Antigravity workspaces."""
        ctype = config_type.lower().strip()

        if "agents" in ctype or "persona" in ctype:
            template = (
                "# My AI Development Team\n\n"
                "## Product Manager (@pm)\n"
                "- Role: Translates user ideas into granular, flawless technical specifications.\n"
                "- Behavior: Strict and detail-oriented. Must verify requirements before code is written.\n\n"
                "## Engineer (@coder)\n"
                "- Role: Writes exceptionally clean, production-ready Python or TypeScript code.\n"
                "- Behavior: Strictly adheres to the spec generated by @pm. Does not add unrequested features.\n\n"
                "## Quality Assurance (@qa)\n"
                "- Role: Reviews generated code, writes test suites, and runs validation loops.\n"
                "- Behavior: Tries hard to break the code. Reports explicit error tracebacks back to @coder.\n"
            )
            filename = ".agents/AGENTS.md"
        elif "gemini" in ctype or "rule" in ctype:
            template = (
                "# Project Rules & Standards\n\n"
                "## Environment Isolation & Dependency Management\n"
                "- Always execute inside an isolated virtual environment (`.venv`).\n"
                "- Never install global packages or use `--break-system-packages`.\n\n"
                "## Code Style & Guardrails\n"
                "- All backend logic must be typed Python 3.11+.\n"
                "- Always run `black` formatting before declaring a task complete.\n"
                "- Write corresponding unit tests in `tests/` for all route changes.\n"
            )
            filename = ".agents/GEMINI.md"
        elif "skill" in ctype:
            skill_name = details.strip() or "custom-skill"
            template = (
                f"---\n"
                f"name: {skill_name}\n"
                f"description: Performs automated operations for {skill_name}.\n"
                f"---\n\n"
                f"# {skill_name.title()} Skill Instructions\n\n"
                f"## 1. Trigger Conditions\n"
                f"Activate when the user asks for {skill_name} tasks.\n\n"
                f"## 2. Execution Guidelines\n"
                f"- Read required references.\n"
                f"- Validate inputs before running operations.\n"
            )
            filename = f".agents/skills/{skill_name}/SKILL.md"
        elif "mcp" in ctype:
            template = json.dumps(
                {
                    "mcpServers": {
                        "postgresql": {
                            "command": "npx",
                            "args": [
                                "-y",
                                "@modelcontextprotocol/server-postgres",
                                "postgresql://localhost/mydb",
                            ],
                        }
                    }
                },
                indent=2,
            )
            filename = "mcp.json"
        else:
            template = (
                "# Antigravity Configuration Blueprint\n"
                f"# Generated for: {config_type}\n"
            )
            filename = "config.md"

        return {
            "config_type": config_type,
            "filename": filename,
            "template": template,
        }


# Global singleton instance
knowledge_base = AGYKnowledgeBase()
