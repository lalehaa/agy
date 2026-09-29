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

"""Unit tests for ADK tools."""

import json
import pytest
from app.tools import (
    search_agy_catalog,
    get_slash_command_manual,
    compare_agy_feature,
    fetch_latest_agy_docs,
    explain_plan_vs_goal,
    generate_config_template,
)


def test_tool_search_catalog():
    res_str = search_agy_catalog("slash commands", category="slash")
    res = json.loads(res_str)
    assert "results" in res
    assert len(res["results"]) > 0


def test_tool_get_slash_command_manual():
    res_str = get_slash_command_manual("/goal")
    res = json.loads(res_str)
    assert res.get("command") == "/goal"
    assert "syntax" in res
    assert "when_to_use" in res


def test_tool_get_slash_command_manual_not_found():
    res_str = get_slash_command_manual("/xyz-unknown")
    res = json.loads(res_str)
    assert res.get("status") == "not_found"


def test_tool_compare_agy_feature():
    res_str = compare_agy_feature("cli", competitor="cursor")
    res = json.loads(res_str)
    assert "comparisons" in res
    assert len(res["comparisons"]) > 0


def test_tool_fetch_latest_agy_docs():
    res_str = fetch_latest_agy_docs("sandbox")
    res = json.loads(res_str)
    assert "content" in res
    assert "sandbox" in res["content"].lower()


def test_tool_explain_plan_vs_goal():
    res = explain_plan_vs_goal("all")
    assert "/plan" in res
    assert "/goal" in res


def test_tool_generate_config_template():
    res_str = generate_config_template("agents")
    res = json.loads(res_str)
    assert res.get("filename") == ".agents/AGENTS.md"
    assert "Product Manager" in res.get("template", "")
