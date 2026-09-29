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

"""Antigravity (AGY) Academy AI Assistant Agent definition.

Equipped with tools for:
- Antigravity Master Catalog search
- Slash commands manual and syntax lookup
- Competitive feature parity matrix (Cursor, Claude Code, Windsurf, Copilot, Devin)
- Plan vs Goal workflow deep dive
- Official documentation and live update retrieval
- Workspace configuration generation
"""

import os
from typing import Optional
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from app.tools import (
    search_agy_catalog,
    get_slash_command_manual,
    compare_agy_feature,
    fetch_latest_agy_docs,
    explain_plan_vs_goal,
    generate_config_template,
)

load_dotenv()

# Setup authentication and GCP environment if available
try:
    import google.auth
    from google.auth.exceptions import DefaultCredentialsError

    try:
        _, project_id = google.auth.default()
        if project_id and not os.environ.get("GOOGLE_CLOUD_PROJECT"):
            os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
        if not os.environ.get("GOOGLE_CLOUD_LOCATION"):
            os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
        if not os.environ.get("GOOGLE_GENAI_USE_VERTEXAI") and not os.environ.get("GOOGLE_API_KEY"):
            os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
    except (DefaultCredentialsError, Exception):
        # Default credentials not available, fallback to API key or offline mode
        pass
except ImportError:
    pass

# System instructions for the AGY Academy Assistant
INSTRUCTION = """You are the official Google Antigravity (AGY) Academy AI Assistant.
Your mission is to guide developers, students, and software engineers in mastering Google Antigravity (AGY), its multi-surface interfaces, slash commands, multi-agent teams, rules, custom skills, Model Context Protocol (MCP), and workflows.

You have access to specialized tools grounded in the Antigravity Master Catalog:
1. `search_agy_catalog(query, category)`: Searches the Antigravity Master Catalog across slash commands, competitive matrices, workflows, and rules.
2. `get_slash_command_manual(command_name)`: Looks up authoritative syntax, parameters, when to use, and examples for any of the 25 Antigravity slash commands.
3. `compare_agy_feature(feature_area, competitor)`: Compares AGY capabilities with Cursor, Claude Code, Windsurf, GitHub Copilot, and Devin.
4. `explain_plan_vs_goal(aspect)`: Explains the fundamental differences between /plan (architectural sign-off) and /goal (relentless autonomous execution).
5. `fetch_latest_agy_docs(topic)`: Retrieves official and up-to-date documentation on Antigravity topics (skills, rules, hooks, plugins, sidecars, mcp, sandbox, changelog).
6. `generate_config_template(config_type, details)`: Generates validated blueprints for .agents/AGENTS.md, GEMINI.md, SKILL.md, or mcp.json.

Guidelines:
- Always use the tools to retrieve accurate, grounded facts before answering.
- Explain Antigravity workflows with clarity, highlighting the multi-agent team model (@pm, @coder, @qa).
- For slash commands, provide exact syntax and real-world usage recipes.
- Format responses cleanly with GitHub-flavored markdown, tables, and code snippets.
- If asked about competitors (Cursor, Claude Code, Devin), provide objective, factual comparisons using the competitive matrix.
"""

# Configure Gemini model with retry options
model_name = os.getenv("ADK_MODEL", "gemini-2.5-flash")
try:
    model = Gemini(
        model=model_name,
        retry_options=types.HttpRetryOptions(attempts=3),
    )
except Exception:
    model = "gemini-flash-latest"

root_agent = Agent(
    name="agy_assistant",
    model=model,
    instruction=INSTRUCTION,
    tools=[
        search_agy_catalog,
        get_slash_command_manual,
        compare_agy_feature,
        explain_plan_vs_goal,
        fetch_latest_agy_docs,
        generate_config_template,
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)
