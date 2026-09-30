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

"""Integration tests for AGYAssistantService."""

import pytest
from app.service import assistant_service


def test_service_slash_command_lookup():
    result = assistant_service.answer_query("/grill-me")
    assert "/grill-me" in result["response"]
    assert result["tool_used"] == "get_slash_command_manual"


def test_service_plan_vs_goal_query():
    result = assistant_service.answer_query(
        "Can you explain how /plan is different from /goal?"
    )
    assert "plan" in result["response"].lower()
    assert "goal" in result["response"].lower()
    assert result["tool_used"] == "explain_plan_vs_goal"


def test_service_competitive_query():
    result = assistant_service.answer_query("How does Antigravity compare to Devin?")
    assert "devin" in result["response"].lower()
    assert result["tool_used"] == "compare_agy_feature"


def test_service_generate_config_query():
    result = assistant_service.answer_query(
        "Please generate AGENTS.md config template for my team"
    )
    assert "AGENTS.md" in result["response"]
    assert result["tool_used"] == "generate_config_template"


def test_service_docs_query():
    result = assistant_service.answer_query("Tell me about lifecycle hooks in AGY")
    assert "hook" in result["response"].lower()
    assert result["tool_used"] == "fetch_latest_agy_docs"


def test_service_session_history():
    sid = "agent-unit-session-001"
    res1 = assistant_service.answer_query("/plan", session_id=sid)
    assert res1["session_id"] == sid
    res2 = assistant_service.answer_query("Explain syntax", session_id=sid)
    assert res2["session_id"] == sid
    history = assistant_service.sessions.get_history(sid)
    assert len(history) == 4
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "/plan"
    assert history[1]["role"] == "assistant"
