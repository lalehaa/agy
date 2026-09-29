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

"""Unit tests for AGY knowledge indexing and retrieval engine."""

import pytest
from app.knowledge import knowledge_base, AGYKnowledgeBase


def test_knowledge_base_initialization():
    kb = AGYKnowledgeBase()
    assert kb.slash_commands, "Expected slash commands to be loaded"
    assert "/plan" in kb.slash_commands
    assert "/goal" in kb.slash_commands
    assert "/grill-me" in kb.slash_commands
    assert "/schedule" in kb.slash_commands
    assert len(kb.slash_commands) >= 25


def test_search_catalog_slash_command():
    result = knowledge_base.search_catalog("goal", category="slash")
    assert result["total_matches"] > 0
    top = result["results"][0]
    assert "/goal" in top["title"]
    assert top["type"] == "slash_command"


def test_search_catalog_competitive():
    result = knowledge_base.search_catalog("cursor", category="competitive")
    assert result["total_matches"] > 0
    assert any("competitive_feature" == r["type"] for r in result["results"])


def test_get_command_details():
    cmd = knowledge_base.get_command_details("/plan")
    assert cmd is not None
    assert cmd["command"] == "/plan"
    assert "syntax" in cmd
    assert "summary" in cmd
    assert "when_to_use" in cmd


def test_get_command_details_without_slash():
    cmd = knowledge_base.get_command_details("goal")
    assert cmd is not None
    assert cmd["command"] == "/goal"


def test_get_command_details_not_found():
    cmd = knowledge_base.get_command_details("/nonexistent-command-xyz")
    assert cmd is None


def test_compare_feature_all_competitors():
    comp = knowledge_base.compare_feature("cli", competitor="all")
    assert comp["total_matches"] > 0
    first = comp["comparisons"][0]
    assert "ratings" in first
    assert "cursor" in first["ratings"]
    assert "claude_code" in first["ratings"]


def test_compare_feature_specific_competitor():
    comp = knowledge_base.compare_feature("subagent", competitor="cursor")
    assert comp["total_matches"] > 0
    for c in comp["comparisons"]:
        assert "cursor" in c["ratings"]


def test_plan_vs_goal_deep_dive_loaded():
    assert knowledge_base.plan_vs_goal_doc
    assert "/plan" in knowledge_base.plan_vs_goal_doc
    assert "/goal" in knowledge_base.plan_vs_goal_doc


def test_fetch_docs_cached_topic():
    docs = knowledge_base.fetch_docs("skills")
    assert docs["topic"] == "skills"
    assert "SKILL.md" in docs["content"]


def test_fetch_docs_rules():
    docs = knowledge_base.fetch_docs("rules")
    assert "AGENTS.md" in docs["content"]
    assert "GEMINI.md" in docs["content"]


def test_generate_config_agents():
    cfg = knowledge_base.generate_config("agents")
    assert cfg["filename"] == ".agents/AGENTS.md"
    assert "Product Manager (@pm)" in cfg["template"]
    assert "Engineer (@coder)" in cfg["template"]
    assert "Quality Assurance (@qa)" in cfg["template"]


def test_generate_config_gemini():
    cfg = knowledge_base.generate_config("gemini")
    assert cfg["filename"] == ".agents/GEMINI.md"
    assert ".venv" in cfg["template"]
    assert "black" in cfg["template"]


def test_generate_config_skill():
    cfg = knowledge_base.generate_config("skill", details="test-runner")
    assert "test-runner" in cfg["filename"]
    assert "name: test-runner" in cfg["template"]
