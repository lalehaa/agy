# Google Antigravity (AGY) Feature Parity Matrix

Comprehensive feature parity comparison between **Google Antigravity (AGY)** and tier-1 AI coding assistants: **Cursor**, **Anthropic Claude Code**, **Windsurf (Codeium)**, **GitHub Copilot**, and **Cognition Devin**.

---

## 1. Master Feature Parity Table

### Legend
| Symbol | Meaning | Description |
| :---: | :--- | :--- |
| ✅ | **Full Support** | Native, first-class implementation |
| ⭐ | **Antigravity Edge** | Exclusive or significantly superior native capability |
| ⚠️ | **Partial Support** | Limited scope, manual workaround, or third-party plugin |
| ❌ | **Not Supported** | No native equivalent available |

### Comprehensive Parity Matrix

| Category | Feature / Capability | Google Antigravity | Cursor | Claude Code | Windsurf | GitHub Copilot | Cognition Devin |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Surfaces** | Headless Terminal CLI | ⭐ Native (`agy`) | ❌ No | ✅ Native (`claude`) | ❌ No | ⚠️ CLI extension | ❌ No |
| | Standalone AI-First IDE | ✅ Native IDE | ✅ VS Code Fork | ❌ No | ✅ VS Code Fork | ⚠️ Extension only | ⚠️ Cloud VS Code |
| | Desktop Canvas 2.0 (Dual-Pane) | ⭐ Native Canvas | ⚠️ Composer Dock | ❌ No | ⚠️ Cascade Dock | ❌ No | ⚠️ Web Dashboard |
| | Programmatic Python SDK | ⭐ Native SDK | ❌ No | ❌ No | ❌ No | ❌ No | ⚠️ Custom API |
| | Local Execution & Privacy | ✅ 100% Local | ✅ Local | ✅ Local | ✅ Local | ⚠️ Cloud Relay | ❌ Remote Cloud VM |
| **Workflows** | Relentless Goal Execution | ⭐ `/goal` (Loop + Test-heal) | ✅ Agent Mode | ✅ CLI Tool Loop | ⚠️ Cascade Agent | ❌ Assistive only | ✅ Cloud Run Loop |
| | Architectural Sign-Off Gate | ⭐ `/plan` (Blueprint Gate) | ⚠️ Checkpoints | ❌ No | ⚠️ Task steps | ⚠️ Workspace PR | ⚠️ Web Checklist |
| | Socratic Requirements Modal | ⭐ `/grill-me` (`ask_question`) | ❌ No | ⚠️ CLI stdin prompt | ❌ No | ❌ No | ❌ No |
| | Continuous Rule Learning | ⭐ `/learn` (Auto-persist) | ⚠️ Manual Notepad | ✅ Memory Bank | ⚠️ Memory bank | ❌ No | ⚠️ Knowledge Base |
| | Background Cron & Staged Timers | ⭐ `/schedule` (Cron & Timers) | ❌ No | ❌ No | ❌ No | ❌ No | ⚠️ Webhook queue |
| **Multi-Agent** | Dynamic Subagent Spawning | ⭐ `invoke_subagent` (Trees) | ❌ Single Agent | ⚠️ Sequential Tools | ❌ Single Agent | ❌ No | ⚠️ Cloud Worker |
| | Git Worktree Isolation | ⭐ `Workspace: 'branch'` | ❌ In-place edits | ❌ In-place edits | ❌ In-place edits | ⚠️ Cloud branch | ✅ Cloud Docker VM |
| | Team Personas (@pm, @coder, @qa)| ⭐ `.agents/AGENTS.md` | ❌ Flat prompt | ⚠️ `CLAUDE.md` text | ❌ No | ⚠️ Workspace tags | ❌ Single Persona |
| | Reactive Wakeups (No Polling) | ⭐ Native Event Wakeups | ❌ Polling loop | ⚠️ Terminal blocking | ❌ Polling loop | ⚠️ Polling | ⚠️ Polling |
| **Customization** | Progressive Disclosure Skills | ⭐ Modular `SKILL.md` | ❌ Monolithic rules | ⚠️ Flat prompt files| ❌ Flat rules | ❌ Flat prompts | ❌ API Tools |
| | Model Context Protocol (MCP) | ✅ Eager & Lazy Tools | ✅ Native Client | ✅ Native Client | ✅ Native Client | ❌ Closed platform | ⚠️ Selected APIs |
| | Lazy MCP Schema Loading | ⭐ On-demand (Saves context) | ❌ Eager only | ❌ Eager only | ❌ Eager only | ❌ No | ❌ No |
| | Lifecycle Event Hooks | ⭐ Native (`/hooks`) | ❌ No | ⚠️ Shell scripts | ❌ No | ❌ No | ⚠️ Webhooks |
| **Dev Experience**| Auxiliary Workspace Pane | ⭐ Subagents/Tasks/Artifacts | ❌ Standard Sidebar | ❌ Terminal only | ❌ Standard Sidebar | ❌ Standard Sidebar | ⚠️ Web Panels |
| | Rendered Mermaid & Artifacts | ⭐ Native Mermaid / HTML | ⚠️ Plain Markdown | ❌ ANSI text only | ⚠️ Plain Markdown | ⚠️ In-PR Markdown | ⚠️ Web HTML View |
| | Interactive Selection Modals | ⭐ Native Buttons / Checkboxes | ❌ Plain text only | ❌ Plain text only | ❌ Plain text only | ❌ Plain text only | ❌ Web chat text |
| | Inline Code Lenses & Diffs | ✅ Native Diff Reviewer | ⭐ Inline `Cmd+K` | ⚠️ CLI Patch View | ✅ Inline Cascade | ⚠️ GitHub PR Diff | ⚠️ Web Diff View |

---

## 2. Competitor Archetype & Positioning Table

| Platform | Primary Archetype | Primary Surface | Major Strength | Critical Vulnerability |
| :--- | :--- | :--- | :--- | :--- |
| **Google Antigravity** | Multi-Surface Autonomous Suite | CLI + Desktop 2.0 + IDE + SDK | Dynamic subagent trees, worktree isolation, dual `/plan` & `/goal` | Rapidly growing ecosystem |
| **Cursor** | AI-First IDE Fork | VS Code Fork | Polished inline `Cmd+K` editing, fast embedding codebase indexing | Single-agent context limit, in-place edits only, IDE lock-in |
| **Claude Code** | Terminal-First CLI Agent | Terminal CLI | Fast terminal REPL, low latency, strong Claude 3.7 Sonnet reasoning | No visual UI, no artifacts, sequential execution only |
| **Windsurf** | Context-Aware IDE | VS Code Fork | Cascade flow tracking cursor and active editor tabs | Proprietary ecosystem, no open SDK, single-agent context |
| **GitHub Copilot** | Ecosystem Assistive Tool | IDE Extension + Web | Native GitHub PR integration, enterprise compliance | Assistive only; lacks autonomous test-healing loops & MCP |
| **Cognition Devin** | Autonomous Cloud Engineer | Cloud VM / Web | End-to-end cloud VM container, headless browser, remote queue | High SaaS cost, cloud latency, lacks local pair programming |

---

## 3. Competitor Head-to-Head Comparison Table

| Evaluation Area | Google Antigravity | Cursor | Claude Code | Windsurf | GitHub Copilot | Cognition Devin |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Execution Loop** | `/goal` test-healing loop | Agent loop | CLI tool loop | Cascade flow | Assistive autocomplete | Autonomous cloud VM |
| **Human Review Gate**| `/plan` interactive gate | Snapshot checkpoints | Terminal prompt | Step list | PR review | Web dashboard modal |
| **Requirements Gathering** | Interactive `/grill-me` | Chat back-and-forth | Terminal text prompts | Chat back-and-forth | Issue comments | Chat back-and-forth |
| **Filesystem Safety** | Isolated git worktrees | In-place file edits | In-place file edits | In-place file edits | Cloud branch | Cloud Docker container |
| **Agent Scaling** | Dynamic subagent trees | Single-agent chat | Sequential tools | Single-agent chat | Single thread | Asynchronous workers |
| **Configuration Format**| `AGENTS.md` + `SKILL.md` | `.cursorrules` | `CLAUDE.md` | `.windsurfrules` | Prompt settings | Custom cloud playbooks |
| **Model Protocol** | Eager & Lazy MCP | Eager MCP | Eager MCP | Eager MCP | Closed APIs | Cloud integrations |
| **Visual Outputs** | Rendered Mermaid & Artifacts| Chat Markdown | ANSI text | Chat Markdown | Web PR diff | Web VM stream |

---

## 4. Migration Cheat Sheet Table

| Migrating From | Original Format | Antigravity Native Replacement | Direct Technical Advantage |
| :--- | :--- | :--- | :--- |
| **Cursor** | `.cursorrules` (monolithic) | `.agents/AGENTS.md` + `GEMINI.md` | Divides instructions across @pm, @coder, and @qa personas |
| **Claude Code** | `CLAUDE.md` (flat instructions) | Modular Skills (`.agents/skills/*/SKILL.md`) | Progressive disclosure saves 70%+ prompt context tokens |
| **Windsurf** | Cascade Flows | Workflows (`/goal` + `/schedule`) | Relentless autonomous verification loops until all tests pass |
| **GitHub Copilot** | Copilot Instructions | Workspace Architecture Policies | Enforces strict folder isolation, virtualenvs, and automated formatting |
| **Cognition Devin** | Custom Cloud Playbooks | Antigravity Python SDK (`agy` scripts) | Runs autonomous agents locally in CI/CD without SaaS VM fees |
