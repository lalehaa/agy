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

"""ADK Tools for the Antigravity (AGY) Academy AI Assistant.

These tool functions provide structured information from:
- The Antigravity Master Catalog
- Slash command manuals and combo recipes
- Competitive feature parity matrix (Cursor, Claude Code, Windsurf, Copilot, Devin)
- Plan vs Goal workflow deep dive
- Built-in guides and live official documentation
- Antigravity workspace configuration generation
"""

from __future__ import annotations

import json
from typing import Any, Dict

from .knowledge import knowledge_base


def search_agy_catalog(query: str, category: str = "all") -> str:
    """Searches the Antigravity Master Catalog for information on AGY features.

    Use this tool when the user asks questions about Antigravity capabilities,
    slash commands, architecture, rules, workflows, or comparisons.

    Args:
        query: The search keywords or question (e.g. 'subagents', '/goal', 'sandbox').
        category: Filter by category: 'all', 'slash', 'competitive', 'workflows', or 'rules'.

    Returns:
        JSON string containing relevant catalog entries with source citations and relevance scores.
    """
    results = knowledge_base.search_catalog(query=query, category=category)
    return json.dumps(results, indent=2)


def get_slash_command_manual(command_name: str) -> str:
    """Retrieves authoritative syntax, parameters, when to use, and examples for a slash command.

    Args:
        command_name: The slash command to look up (e.g. '/plan', '/goal', '/grill-me', '/schedule', '/learn').

    Returns:
        JSON string with command syntax, aliases, category, description, and usage examples.
    """
    details = knowledge_base.get_command_details(command_name)
    if not details:
        return json.dumps(
            {
                "status": "not_found",
                "message": f"Command '{command_name}' not found in the Antigravity catalog.",
                "available_commands": list(knowledge_base.slash_commands.keys()),
            },
            indent=2,
        )
    return json.dumps(details, indent=2)


def compare_agy_feature(feature_area: str, competitor: str = "all") -> str:
    """Compares Antigravity against AI coding competitors (Cursor, Claude Code, Windsurf, Copilot, Devin).

    Args:
        feature_area: Feature or capability to compare (e.g. 'cli', 'subagents', 'sandbox', 'autonomy', 'rules').
        competitor: Optional specific competitor ('cursor', 'claude_code', 'windsurf', 'github_copilot', 'devin', or 'all').

    Returns:
        JSON string with comparative ratings, native support details, and analytical notes.
    """
    comparison = knowledge_base.compare_feature(
        feature_area=feature_area, competitor=competitor
    )
    return json.dumps(comparison, indent=2)


def fetch_latest_agy_docs(topic: str) -> str:
    """Retrieves official documentation and updates on an Antigravity topic or concept.

    Args:
        topic: The topic name (e.g. 'skills', 'rules', 'hooks', 'plugins', 'sidecars', 'mcp', 'sandbox', 'changelog').

    Returns:
        JSON string containing the topic documentation, source URL, and content.
    """
    docs = knowledge_base.fetch_docs(topic=topic)
    return json.dumps(docs, indent=2)


def explain_plan_vs_goal(aspect: str = "all") -> str:
    """Provides a detailed architectural breakdown comparing the /plan and /goal slash commands.

    Args:
        aspect: The focus area: 'all', 'matrix', 'plan', 'goal', or 'combos'.

    Returns:
        Markdown string explaining when to use /plan vs /goal, the quick comparison matrix, and combo workflows.
    """
    doc = knowledge_base.plan_vs_goal_doc
    if not doc:
        return (
            "### /plan vs /goal Quick Summary\n\n"
            "- **/plan**: High gatekeeping, architectural blueprinting, risk assessment, human review before code is modified.\n"
            "- **/goal**: Autonomous test-healing execution loop, iterates through terminal commands and test failures until acceptance criteria pass 100%."
        )
    return doc


def generate_config_template(config_type: str, details: str = "") -> str:
    """Generates ready-to-use Antigravity configuration files.

    Args:
        config_type: Type of configuration ('agents', 'gemini', 'skill', 'mcp').
        details: Additional details (e.g., custom skill name or rules).

    Returns:
        JSON string containing the suggested filename and template contents.
    """
    config = knowledge_base.generate_config(config_type=config_type, details=details)
    return json.dumps(config, indent=2)
