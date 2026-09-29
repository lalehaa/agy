# Google Antigravity (AGY) Slash Command Catalog

Welcome to the **Antigravity Slash Command Catalog**. This catalog provides a complete, structured reference for all slash commands available across the Antigravity ecosystem (including the Antigravity Desktop App, Antigravity CLI `agy`, and Antigravity IDE).

Slash commands are user-facing shortcuts executed in the chat or terminal interface (by typing `/`) that trigger specialized agent behaviors, launch autonomous workflows, manage session state, configure models, and manage permissions.

---

## Quick Navigation & Overview Matrix

| Command | Category | Purpose | Typical Use Case |
| :--- | :--- | :--- | :--- |
| [`/goal`](#1-goal) | Workflow | Relentless autonomous execution | Overnight tasks, 100% test coverage, complex refactoring |
| [`/plan`](#2-plan) | Workflow | Step-by-step architectural blueprint | Complex multi-layer features requiring human sign-off |
| [`/grill-me`](#3-grill-me) | Workflow | Socratic design & requirements interview | Brainstorming APIs, clarifying edge cases and tradeoffs |
| [`/learn`](#4-learn) | Workflow | Persist habits & conventions to memory | Memorizing project conventions or user preferences |
| [`/schedule`](#5-schedule) | Workflow | Background cron & timer triggers | Health check polling, staged reminders, scheduled reports |
| [`/diff`](#6-diff) | Session & Context | Interactive visual diff reviewer | Inspecting and approving agent code modifications |
| [`/compact`](#7-compact) | Session & Context | Token & history context compression | Freeing context window space in long sessions |
| [`/clear`](#8-clear-reset) | Session & Context | Context reset & fresh conversation | Starting a completely new task or feature |
| [`/fork`](#9-fork) | Session & Context | Branch trajectory at current point | Exploring alternative architectures without losing context |
| [`/rename`](#10-rename) | Session & Context | Rename active conversation session | Organizing conversation history and logs |
| [`/statusline`](#11-statusline) | Session & Context | Toggle status line in CLI / TUI | Checking model info, token count, and git status |
| [`/exit`](#12-exit-quit) | Session & Context | Exit CLI or TUI session | Quitting interactive session cleanly |
| [`/model`](#13-model) | Model & Reasoning | Switch active LLM or inspect models | Selecting Gemini 3.8 Flash, Gemini 3 Pro, etc. |
| [`/effort`](#14-effort) | Model & Reasoning | Adjust reasoning / thinking effort | Setting `low`, `medium`, `high`, or `max` reasoning |
| [`/usage`](#15-usage-quota) | Model & Reasoning | View quota & token consumption | Monitoring rate limits and context window usage |
| [`/credits`](#16-credits) | Model & Reasoning | Inspect G1 credits & tier status | Checking remaining compute credits |
| [`/skills`](#17-skills) | Customizations | Inspect & list discovered skills | Checking active workspace & built-in skills |
| [`/agents`](#18-agents) | Customizations | Manage personas (@pm, @coder, @qa) | Switching between defined team personas |
| [`/permissions`](#19-permissions) | Security & Tools | Configure tool permissions & sandbox | Managing command allowlists, denylists, and bash approvals |
| [`/hooks`](#20-hooks) | Security & Tools | Manage lifecycle event hooks | Pre-tool command auditing and post-run checks |
| [`/config`](#21-config-settings) | Configuration | Full configuration & settings panel | Modifying workspace policies and editor preferences |
| [`/mcp`](#22-mcp) | Integrations | Model Context Protocol servers | Connecting AlloyDB, PostgreSQL, BigQuery, or custom tools |
| [`/remote-control`](#23-remote-control) | Utilities | Toggle remote control daemon | Connecting remote sessions or microphone bridging |
| [`/changelog`](#24-changelog) | Utilities | View release notes & latest updates | Reading newly introduced Antigravity features |
| [`/help`](#25-help) | Utilities | Help manual & keybinding cheatsheet | Displaying built-in command syntax and keymaps |

---

## 1. Autonomous & Goal-Driven Workflows

### 1. `/goal`
- **Description**: Triggers autonomous, long-running goal execution mode. Instructs Antigravity to be extra thorough and relentlessly iterate, execute terminal commands, run test suites, catch and fix errors, and not stop until the goal is fully achieved.
- **When to Use**:
  - Running multi-hour or overnight tasks.
  - Generating complete test suites targeting 100% test coverage.
  - Complex multi-file refactoring where every step must pass build and verification gates.
- **Syntax**:
  ```text
  /goal <objective>
  ```
- **Example**:
  ```text
  /goal Refactor the database repository layer to async SQLAlchemy 2.0, update all routers, and ensure all tests in tests/ pass with 0 warnings.
  ```

---

### 2. `/plan`
- **Description**: Directs the agent to perform careful, phased step-by-step architectural planning before generating or modifying any code. It generates actionable milestones, lists dependencies, identifies risks, and asks for approval.
- **When to Use**:
  - Starting major architectural overhauls.
  - Building features touching frontend, backend, and external databases.
  - Working in critical production systems where code changes must be verified in advance.
- **Syntax**:
  ```text
  /plan <task description>
  ```
- **Example**:
  ```text
  /plan Add OAuth2 social login (Google and GitHub) to the FastAPI backend, including user database migration and session handling.
  ```

---

### 3. `/grill-me`
- **Description**: Initiates an interactive Socratic design interview with the agent. The agent questions your assumptions, explores architectural tradeoffs, clarifies ambiguities, and probes edge cases before generating specifications or code.
- **When to Use**:
  - Unclear or ambiguous feature requests.
  - Choosing between database architectures, API contracts, or library stacks.
  - Pre-flight alignment between engineering and product requirements.
- **Syntax**:
  ```text
  /grill-me [optional topic or prompt]
  ```
- **Example**:
  ```text
  /grill-me We want to add real-time multiplayer cursor sharing and canvas synchronization to our web app.
  ```

---

### 4. `/learn`
- **Description**: Directs the agent to persist a behavior, rule, pattern, or correction into its long-term project memory (`.agents/` or user guidelines) so that it follows this rule across all future tasks and sessions.
- **When to Use**:
  - Whenever you correct the agent on code style, library versions, or testing conventions.
  - When you solve a tricky environment setup or build issue that should not be repeated.
- **Syntax**:
  ```text
  /learn <rule, pattern, or guideline>
  ```
- **Example**:
  ```text
  /learn In this repository, always run `black` formatting before completing a task and never use global pip installs.
  ```

---

### 5. `/schedule`
- **Description**: Sets up background cron jobs or delayed one-shot timers that trigger agent notifications or monitor ongoing background operations without blocking the chat.
- **When to Use**:
  - Polling deployment status or health check endpoints.
  - Setting up reminders to review pull requests or batch runs.
  - Recurring scheduled monitoring of logs or metrics.
- **Syntax**:
  ```text
  /schedule Cron="<5-field-cron>" Prompt="<prompt>" [IsDaemon=true|false]
  /schedule DurationSeconds=<seconds> Prompt="<prompt>" [TimerCondition="never"|"any"]
  ```
- **Examples**:
  ```text
  /schedule Cron="*/15 * * * *" Prompt="Check staging server health at http://localhost:8000/health and log errors"
  /schedule DurationSeconds=600 Prompt="Remind me to check on the database migration progress"
  ```

---

## 2. Session, History & Trajectory Management

### 6. `/diff`
- **Description**: Opens the interactive visual diff viewer, displaying all modified files, side-by-side git hunks, and allowing in-place reviews, approvals, or rejections.
- **Syntax**:
  ```text
  /diff
  ```

---

### 7. `/compact`
- **Description**: Condenses earlier conversation turns into a high-density summary, drastically freeing up context window capacity while maintaining awareness of current code state, files, and objectives.
- **Syntax**:
  ```text
  /compact
  ```

---

### 8. `/clear` (or `/reset`)
- **Description**: Clears the conversation history and resets the session to a clean slate while preserving your active workspace and git files.
- **Syntax**:
  ```text
  /clear
  /reset
  ```

---

### 9. `/fork`
- **Description**: Branches the current conversation trajectory into a new fork. Allows exploring alternative technical approaches or experiments without polluting or losing the original conversation trajectory.
- **Syntax**:
  ```text
  /fork
  ```

---

### 10. `/rename`
- **Description**: Renames the active conversation session to a clear, descriptive title for easier retrieval in your conversation history.
- **Syntax**:
  ```text
  /rename <new session title>
  ```
- **Example**:
  ```text
  /rename mcp-server-setup
  ```

---

### 11. `/statusline`
- **Description**: Controls the visibility of the interactive status line at the bottom of the CLI / TUI interface.
- **Syntax**:
  ```text
  /statusline on        # Enable statusline
  /statusline off       # Disable statusline
  ```

---

### 12. `/exit` (or `/quit`)
- **Description**: Gracefully terminates the active CLI session. Can also be triggered with `Ctrl+D Ctrl+D`.
- **Syntax**:
  ```text
  /exit
  /quit
  ```

---

## 3. Model Selection & Reasoning Configuration

### 13. `/model`
- **Description**: Displays the active model, lists available Gemini models, or switches models for the current session or a single prompt.
- **Supported Models**:
  - `Gemini 3.8 Flash`: High speed, balanced reasoning, responsive pair programming.
  - `Gemini 3 Pro`: Deep reasoning, complex architectural design, heavy refactoring.
  - `Gemini 2.5 Flash Lite`: Ultra-fast, lightweight for quick searches and lookups.
- **Syntax**:
  ```text
  /model                           # Opens interactive model selection
  /model <model_name>              # Switch to specified model
  /model <model_name> <prompt>     # Run single prompt on specified model
  ```
- **Example**:
  ```text
  /model gemini-3.8-flash
  ```

---

### 14. `/effort`
- **Description**: Configures the reasoning effort / thinking budget allocated to the model. Higher effort enables deep step-by-step thinking for tricky problems; lower effort provides instant turnaround.
- **Options**: `low`, `medium`, `high`, `max`
- **Syntax**:
  ```text
  /effort <low|medium|high|max>
  ```
- **Example**:
  ```text
  /effort high
  ```

---

### 15. `/usage` (alias `/quota`)
- **Description**: Renders real-time statistics regarding context window usage (input tokens, cached tokens, output tokens), request rate limits, and model quotas.
- **Syntax**:
  ```text
  /usage
  /quota
  ```

---

### 16. `/credits`
- **Description**: Checks remaining Google Cloud / G1 subscription credits, tier status, and billing renewal info.
- **Syntax**:
  ```text
  /credits
  ```

---

## 4. Customizations, Personas & Extensions

### 17. `/skills`
- **Description**: Displays all discovered skills in your workspace (`.agents/skills/`), global configuration (`~/.gemini/config/skills/`), and built-in system skills. Shows activation triggers, descriptions, and capabilities.
- **Syntax**:
  ```text
  /skills
  ```

---

### 18. `/agents`
- **Description**: Lists all active and configured subagent personas and definitions (e.g., `@pm`, `@coder`, `@qa` defined in `.agents/AGENTS.md`, or built-in subagents like `research`).
- **Syntax**:
  ```text
  /agents
  ```

---

### 19. `/permissions`
- **Description**: Opens the interactive Tool Permission Editor. Configure which shell commands, file directories, and web domains require manual user confirmation versus running automatically or in the sandbox.
- **Syntax**:
  ```text
  /permissions
  ```

---

### 20. `/hooks`
- **Description**: Inspects and manages lifecycle event hooks defined in `hooks.json` (such as pre-tool security interceptors, automatic linters, and post-execution audit loggers).
- **Syntax**:
  ```text
  /hooks
  ```

---

### 21. `/config` (alias `/settings`)
- **Description**: Launches the interactive settings panel to configure workspace policies, auto-execution mode, terminal sandbox, and theme preferences.
- **Syntax**:
  ```text
  /config
  /settings
  ```

---

### 22. `/mcp`
- **Description**: Manages Model Context Protocol (MCP) server integrations. Allows listing connected servers (e.g. AlloyDB, GitHub, Brave Search), adding new servers, and inspecting available tools.
- **Syntax**:
  ```text
  /mcp
  ```

---

### 23. `/remote-control`
- **Description**: Manages the remote-control background daemon, enabling remote pairing, external host connections, or browser audio routing.
- **Syntax**:
  ```text
  /remote-control on
  /remote-control off
  /remote-control status
  ```

---

### 24. `/changelog`
- **Description**: Displays release notes, new capabilities, and feature updates for Google Antigravity.
- **Syntax**:
  ```text
  /changelog
  ```

---

### 25. `/help`
- **Description**: Prints the interactive help manual, detailing available commands, syntax, and keyboard shortcuts.
- **Syntax**:
  ```text
  /help
  ```

---

## Recommended Daily Workflow Combos

### Combo A: Feature Kickoff & Architecture Alignment
```text
1. /grill-me I want to build a real-time event streaming pipeline using Redis Streams.
2. [Answer agent questions and align on technical decisions]
3. /plan
4. [Review plan and proceed]
```

### Combo B: Relentless Autonomous Implementation
```text
1. /goal Build unit tests for app/validator.py with 100% branch coverage and format using black.
2. [Agent iterates, runs pytest, fixes failures, formats code, and reports completion]
3. /diff
```

### Combo C: Teaching Your Agent Team Rules
```text
1. /learn Always use strict typed Python 3.11+ and place all application code inside scoped subdirectories.
2. /skills
```
