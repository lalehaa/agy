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
    res = client.post("/api/validate", json={"config_type": "agents", "content": valid_content})
    assert res.status_code == 200
    assert res.json()["valid"] is True

    invalid_content = "Just plain text without headers"
    res_inv = client.post("/api/validate", json={"config_type": "agents", "content": invalid_content})
    assert res_inv.status_code == 200
    assert res_inv.json()["valid"] is False


def test_validate_skill_config():
    valid_skill = "---\nname: my-skill\ndescription: Test skill\n---\n# Instructions\nDo something."
    res = client.post("/api/validate", json={"config_type": "skill", "content": valid_skill})
    assert res.status_code == 200
    assert res.json()["valid"] is True

    invalid_skill = "Missing frontmatter"
    res_inv = client.post("/api/validate", json={"config_type": "skill", "content": invalid_skill})
    assert res_inv.status_code == 200
    assert res_inv.json()["valid"] is False


def test_validate_mcp_config():
    valid_mcp = '{"mcpServers": {"srv": {"command": "node"}}}'
    res = client.post("/api/validate", json={"config_type": "mcp", "content": valid_mcp})
    assert res.status_code == 200
    assert res.json()["valid"] is True

    invalid_mcp = "{ invalid json }"
    res_inv = client.post("/api/validate", json={"config_type": "mcp", "content": invalid_mcp})
    assert res_inv.status_code == 200
    assert res_inv.json()["valid"] is False

