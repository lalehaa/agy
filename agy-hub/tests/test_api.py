import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Antigravity Academy" in response.text


def test_get_curriculum():
    response = client.get("/api/curriculum")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 8
    assert data[0]["id"] == "mod-1"
    assert "Antigravity Overview" in data[0]["title"]


def test_progress_flow():
    # Update progress for mod-1
    payload = {"module_id": "mod-1", "completed_labs": ["mod-1-lab-1"]}
    response = client.post("/api/progress", json=payload)
    assert response.status_code == 200
    progress_data = response.json()["progress"]
    assert "mod-1" in progress_data
    assert "mod-1-lab-1" in progress_data["mod-1"]

    # Retrieve progress
    get_res = client.get("/api/progress")
    assert get_res.status_code == 200
    assert get_res.json()["progress"]["mod-1"] == ["mod-1-lab-1"]


def test_generate_agents_config():
    payload = {
        "pm_name": "@pm",
        "pm_role": "Specs role",
        "coder_name": "@coder",
        "coder_role": "Code role",
        "qa_name": "@qa",
        "qa_role": "QA role",
        "custom_rules": ["Always use black formatter"],
    }
    response = client.post("/api/generate/agents", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "AGENTS.md"
    assert "Product Manager (@pm)" in data["content"]
    assert "Always use black formatter" in data["content"]


def test_generate_skill_config():
    payload = {
        "name": "code-auditor",
        "description": "Audits Python code",
        "instructions": "1. Inspect files\n2. Report bugs",
        "allowed_tools": ["view_file"],
    }
    response = client.post("/api/generate/skill", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "code-auditor/SKILL.md"
    assert "name: code-auditor" in data["content"]
    assert "description: Audits Python code" in data["content"]


def test_generate_mcp_config():
    payload = {
        "server_name": "test-server",
        "command": "python3",
        "args": ["-m", "test"],
        "env_vars": {"KEY": "VAL"},
    }
    response = client.post("/api/generate/mcp", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "mcp.json"
    assert '"test-server"' in data["content"]


def test_validate_agents_config():
    valid_content = "# Team Config\n\n## Product Manager (@pm)\n- Role: Specs\n## Engineer (@coder)\n- Role: Code\n## QA (@qa)\n- Role: Testing"
    res = client.post(
        "/api/validate", json={"config_type": "agents", "content": valid_content}
    )
    assert res.status_code == 200
    assert res.json()["valid"] is True

    invalid_content = "Just plain text without headers"
    res_inv = client.post(
        "/api/validate", json={"config_type": "agents", "content": invalid_content}
    )
    assert res_inv.status_code == 200
    assert res_inv.json()["valid"] is False


def test_validate_skill_config():
    valid_skill = "---\nname: my-skill\ndescription: Test skill\n---\n# Instructions\nDo something."
    res = client.post(
        "/api/validate", json={"config_type": "skill", "content": valid_skill}
    )
    assert res.status_code == 200
    assert res.json()["valid"] is True

    invalid_skill = "Missing frontmatter"
    res_inv = client.post(
        "/api/validate", json={"config_type": "skill", "content": invalid_skill}
    )
    assert res_inv.status_code == 200
    assert res_inv.json()["valid"] is False


def test_validate_mcp_config():
    valid_mcp = '{"mcpServers": {"srv": {"command": "node"}}}'
    res = client.post(
        "/api/validate", json={"config_type": "mcp", "content": valid_mcp}
    )
    assert res.status_code == 200
    assert res.json()["valid"] is True

    invalid_mcp = "{ invalid json }"
    res_inv = client.post(
        "/api/validate", json={"config_type": "mcp", "content": invalid_mcp}
    )
    assert res_inv.status_code == 200
    assert res_inv.json()["valid"] is False


def test_assistant_suggestions():
    response = client.get("/api/assistant/suggestions")
    assert response.status_code == 200
    suggestions = response.json()
    assert isinstance(suggestions, list)
    assert len(suggestions) > 0
    assert any("goal" in s.lower() for s in suggestions)


def test_assistant_chat_slash_command():
    payload = {"message": "/plan"}
    response = client.post("/api/assistant/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "/plan" in data["response"]
    assert data["tool_used"] == "get_slash_command_manual"


def test_assistant_chat_plan_vs_goal():
    payload = {"message": "How does /plan differ from /goal?"}
    response = client.post("/api/assistant/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "plan" in data["response"].lower()
    assert "goal" in data["response"].lower()
    assert data["tool_used"] == "explain_plan_vs_goal"


def test_assistant_chat_competitor():
    payload = {"message": "Compare Antigravity with Cursor"}
    response = client.post("/api/assistant/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "cursor" in data["response"].lower()
    assert data["tool_used"] == "compare_agy_feature"


def test_assistant_chat_empty_validation():
    payload = {"message": "   "}
    response = client.post("/api/assistant/chat", json=payload)
    assert response.status_code == 400


def test_assistant_service_loaded():
    from app.routers.api import assistant_service

    assert assistant_service is not None


def test_assistant_chat_session_history():
    session_id = "test-session-123"
    # Turn 1
    res1 = client.post(
        "/api/assistant/chat",
        json={"message": "/plan", "session_id": session_id},
    )
    assert res1.status_code == 200
    data1 = res1.json()
    assert data1["session_id"] == session_id

    # Turn 2: Follow-up query in same session
    res2 = client.post(
        "/api/assistant/chat",
        json={"message": "Can you give me an example?", "session_id": session_id},
    )
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["session_id"] == session_id

    from app.routers.api import assistant_service

    history = assistant_service.sessions.get_history(session_id)
    assert len(history) >= 4  # 2 user messages + 2 assistant responses


def test_assistant_chat_config_generation():
    payload = {"message": "Generate AGENTS.md configuration blueprint for team"}
    response = client.post("/api/assistant/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "AGENTS.md" in data["response"]
    assert data["tool_used"] == "generate_config_template"


def test_assistant_chat_docs():
    payload = {"message": "Tell me about lifecycle hooks in AGY"}
    response = client.post("/api/assistant/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "hook" in data["response"].lower()
    assert data["tool_used"] == "fetch_latest_agy_docs"
