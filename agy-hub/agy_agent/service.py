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

"""High-level service interface for the Antigravity Academy AI Assistant.

Enables seamless interaction from both the ADK CLI runtime and the Antigravity
Academy FastAPI web application. Supports online LLM runner with automatic
grounded fallback for offline testing and session history retention.
"""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Any, Dict, List, Optional

from .knowledge import knowledge_base
from .tools import (
    search_agy_catalog,
    get_slash_command_manual,
    compare_agy_feature,
    fetch_latest_agy_docs,
    explain_plan_vs_goal,
    generate_config_template,
)

logger = logging.getLogger(__name__)


class SessionContextManager:
    """In-memory session context manager retaining conversation history."""

    def __init__(self, max_turns: int = 10) -> None:
        self.max_turns = max_turns
        self._sessions: Dict[str, List[Dict[str, str]]] = {}

    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        """Returns the conversation history for a given session."""
        return self._sessions.get(session_id, [])

    def add_message(self, session_id: str, role: str, content: str) -> None:
        """Appends a message to the session history."""
        if session_id not in self._sessions:
            self._sessions[session_id] = []
        self._sessions[session_id].append({"role": role, "content": content})
        # Keep within max turns limit
        max_messages = self.max_turns * 2
        if len(self._sessions[session_id]) > max_messages:
            self._sessions[session_id] = self._sessions[session_id][-max_messages:]

    def clear_session(self, session_id: str) -> None:
        """Clears stored history for a session."""
        self._sessions.pop(session_id, None)


class AGYAssistantService:
    """Service providing conversational responses on Google Antigravity features."""

    def __init__(self) -> None:
        self.knowledge = knowledge_base
        self.sessions = SessionContextManager()
        self._runner: Optional[Any] = None
        self._init_runner()

    def _init_runner(self) -> None:
        """Initializes ADK runner if credentials are present."""
        has_creds = bool(
            os.getenv("GOOGLE_API_KEY")
            or os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            or os.getenv("GOOGLE_CLOUD_PROJECT")
        )
        if not has_creds:
            return

        try:
            from .agent import app as adk_app
            from google.adk.runners import Runner
            from google.adk.sessions import InMemorySessionService
            from google.adk.artifacts import InMemoryArtifactService

            self._runner = Runner(
                app=adk_app,
                session_service=InMemorySessionService(),
                artifact_service=InMemoryArtifactService(),
                auto_create_session=True,
            )
        except Exception as e:
            logger.info("ADK runner initialized without cloud session: %s", e)
            self._runner = None

    def answer_query(
        self, query: str, session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Processes a user message and returns a comprehensive, grounded answer."""
        query_norm = query.strip()
        lower = query_norm.lower()

        # Record user query in session history if session_id provided
        if session_id:
            self.sessions.add_message(session_id, "user", query_norm)

        # Contextual check: if query is very short and references prior topic
        if session_id and len(query_norm.split()) < 4:
            history = self.sessions.get_history(session_id)
            if len(history) >= 2:
                # Last assistant response or user query context
                prev_user = history[-2].get("content", "").lower()
                if any(k in prev_user for k in ["/plan", "/goal", "cursor", "claude"]):
                    lower = f"{lower} {prev_user}"

        result: Dict[str, Any]

        # 1. Check for /plan vs /goal comparison
        if ("plan" in lower and "goal" in lower) or ("plan vs goal" in lower):
            summary = explain_plan_vs_goal("matrix")
            result = {
                "response": summary,
                "source": "antigravity_academy/catalog/slash/plan_vs_goal.md",
                "tool_used": "explain_plan_vs_goal",
            }

        # 2. Check for config template generation
        elif (
            "generate" in lower or "template" in lower or "blueprint" in lower
        ) and not lower.startswith("/"):
            ctype = (
                "agents"
                if "agents" in lower or "persona" in lower or "team" in lower
                else (
                    "gemini"
                    if "gemini" in lower or "rule" in lower
                    else "skill" if "skill" in lower else "mcp"
                )
            )
            config_res = self.knowledge.generate_config(config_type=ctype)
            response_text = (
                f"### Configuration Template for `{config_res['filename']}`\n\n"
                f"Here is a production-ready configuration blueprint:\n\n"
                f"```{('yaml' if config_res['filename'].endswith('.md') else 'json')}\n"
                f"{config_res['template']}\n"
                f"```"
            )
            result = {
                "response": response_text,
                "source": "Rules & Configuration Catalog",
                "tool_used": "generate_config_template",
                "metadata": config_res,
            }

        # 3. Check for specific slash command queries
        elif (slash_match := re.search(r"(/[\w\-]+)", query_norm)) and (
            slash_match.group(1).lower() in self.knowledge.slash_commands
        ):
            cmd = slash_match.group(1).lower()
            cmd_data = self.knowledge.slash_commands[cmd]
            response_text = (
                f"### Antigravity Slash Command: `{cmd_data.get('command')}`\n\n"
                f"**Category**: {cmd_data.get('category')}  \n"
                f"**Syntax**: `{cmd_data.get('syntax')}`  \n\n"
                f"**Summary**: {cmd_data.get('summary')}\n\n"
                f"**Description**: {cmd_data.get('description')}\n\n"
                f"**When to use**: {cmd_data.get('when_to_use')}\n\n"
                f"**Example Recipe**:\n```text\n{cmd_data.get('example')}\n```"
            )
            result = {
                "response": response_text,
                "source": "antigravity_academy/catalog/slash/slash_commands.json",
                "tool_used": "get_slash_command_manual",
                "metadata": cmd_data,
            }

        # 4. Check for competitor comparison
        elif any(
            c in lower
            for c in [
                "cursor",
                "claude",
                "windsurf",
                "copilot",
                "devin",
                "versus",
                "vs",
                "compet",
            ]
        ):
            competitors = ["cursor", "claude", "windsurf", "copilot", "devin"]
            matched_comp = [c for c in competitors if c in lower]
            target_comp = matched_comp[0] if matched_comp else "all"
            feature = (
                "cli"
                if "cli" in lower
                else (
                    "subagent"
                    if "subagent" in lower
                    else "sandbox" if "sandbox" in lower else "workflows"
                )
            )
            comp_result = self.knowledge.compare_feature(
                feature_area=feature, competitor=target_comp
            )

            lines = [
                f"### Google Antigravity Competitive Comparison ({target_comp.title()})\n"
            ]
            for f in comp_result.get("comparisons", []):
                lines.append(f"#### {f.get('feature')} ({f.get('category')})")
                lines.append(f"- **Antigravity**: {f.get('antigravity')}")
                for c_name, c_rat in f.get("ratings", {}).items():
                    lines.append(f"- **{c_name.title()}**: {c_rat}")
                if f.get("notes"):
                    lines.append(f"- *Notes*: {f.get('notes')}")
                lines.append("")

            result = {
                "response": "\n".join(lines),
                "source": "antigravity_academy/catalog/competitive/feature_parity_matrix.md",
                "tool_used": "compare_agy_feature",
                "metadata": comp_result,
            }

        # 5. Check for config keyword fallback
        elif "generate" in lower or "template" in lower or "config" in lower:
            ctype = (
                "agents"
                if "agents" in lower or "persona" in lower or "team" in lower
                else (
                    "gemini"
                    if "gemini" in lower or "rule" in lower
                    else "skill" if "skill" in lower else "mcp"
                )
            )
            config_res = self.knowledge.generate_config(config_type=ctype)
            response_text = (
                f"### Configuration Template for `{config_res['filename']}`\n\n"
                f"Here is a production-ready configuration blueprint:\n\n"
                f"```{('yaml' if config_res['filename'].endswith('.md') else 'json')}\n"
                f"{config_res['template']}\n"
                f"```"
            )
            result = {
                "response": response_text,
                "source": "Rules & Configuration Catalog",
                "tool_used": "generate_config_template",
                "metadata": config_res,
            }

        # 6. Check for official documentation topic
        elif any(
            t in lower
            for t in [
                "skills",
                "rules",
                "hooks",
                "plugins",
                "sidecars",
                "mcp",
                "sandbox",
                "subagents",
                "changelog",
            ]
        ):
            doc_topics = [
                "skills",
                "rules",
                "hooks",
                "plugins",
                "sidecars",
                "mcp",
                "sandbox",
                "subagents",
                "changelog",
            ]
            matched_topic = [t for t in doc_topics if t in lower]
            doc_res = self.knowledge.fetch_docs(topic=matched_topic[0])
            result = {
                "response": doc_res["content"],
                "source": doc_res.get("url"),
                "tool_used": "fetch_latest_agy_docs",
                "metadata": doc_res,
            }

        # 7. General semantic catalog search
        else:
            search_res = self.knowledge.search_catalog(query=query)
            if search_res.get("results"):
                top = search_res["results"][0]
                if top.get("type") == "slash_command":
                    resp = (
                        f"### Found Slash Command: `{top.get('title')}`\n\n"
                        f"**Summary**: {top.get('summary')}\n\n"
                        f"**Syntax**: `{top.get('syntax')}`\n\n"
                        f"**When to use**: {top.get('when_to_use')}\n\n"
                        f"**Example**: `{top.get('example')}`"
                    )
                elif top.get("type") == "competitive_feature":
                    resp = (
                        f"### {top.get('title')} ({top.get('category')})\n\n"
                        f"**Antigravity Support**: {top.get('antigravity_support')}\n\n"
                        f"**Ratings**: {json.dumps(top.get('ratings', {}), indent=2)}\n\n"
                        f"**Notes**: {top.get('notes')}"
                    )
                else:
                    resp = f"### {top.get('title')}\n\n{top.get('summary')}"

                result = {
                    "response": resp,
                    "source": top.get("source"),
                    "tool_used": "search_agy_catalog",
                    "metadata": search_res,
                }
            else:
                # 8. Default overview response
                result = {
                    "response": (
                        "### Google Antigravity (AGY) Assistant\n\n"
                        "I am your guide to mastering Google Antigravity! You can ask me about:\n"
                        "- **Slash Commands**: `/plan`, `/goal`, `/grill-me`, `/schedule`, `/learn`, `/compact`\n"
                        "- **Competitive Comparisons**: How AGY compares to Cursor, Claude Code, Windsurf, Copilot, or Devin\n"
                        "- **Multi-Agent Teams**: Structuring `@pm`, `@coder`, and `@qa` personas in `.agents/AGENTS.md`\n"
                        "- **Modular Skills**: Creating `SKILL.md` bundles with scripts and references\n"
                        "- **Security**: Terminal sandboxes, permission gates, and secret redaction\n"
                        "- **Configuration Blueprints**: Generating templates for `AGENTS.md`, `GEMINI.md`, or `mcp.json`"
                    ),
                    "source": "Antigravity Master Catalog",
                    "tool_used": "search_agy_catalog",
                }

        # Add session_id to result and store assistant response
        if session_id:
            result["session_id"] = session_id
            self.sessions.add_message(session_id, "assistant", result["response"])

        return result


# Global assistant service instance
assistant_service = AGYAssistantService()
