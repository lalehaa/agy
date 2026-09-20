# Antigravity Academy

An interactive web application and developer playground designed to educate developers on how to set up, configure, and master all functionalities of **Google Antigravity (AGY)**.

## Features
- **8 Guided Curriculum Labs**: Step-by-step interactive walkthroughs covering setup, slash commands, rules, custom skills, MCP servers, subagents, hooks, and terminal sandbox.
- **Config Generators**: Interactive forms to visually construct `.agents/AGENTS.md`, `GEMINI.md`, `SKILL.md`, and `mcp.json`.
- **Live Validators**: Real-time syntax and schema checkers for Antigravity rules, skill frontmatter, and MCP manifests.
- **Progress Tracking**: Lab progress saved directly in file-based JSON storage.

## Quick Start

1. **Activate Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run Server**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

3. **Access App**: Open `http://localhost:8000` in your web browser.

