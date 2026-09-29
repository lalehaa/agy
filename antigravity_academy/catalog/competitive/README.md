# Antigravity Competitive Intelligence Catalog

This directory houses comparative benchmarks, feature parity matrices, and strategic evaluations comparing **Google Antigravity (AGY)** with peer tier-1 AI development platforms and agentic coding tools.

## Contents

| Document | Format | Description |
| :--- | :---: | :--- |
| **[feature_parity_matrix.md](feature_parity_matrix.md)** | Markdown Tables | Comprehensive executive scorecard, head-to-head competitor comparison tables, and migration guide. |
| **[competitive_matrix.json](competitive_matrix.json)** | JSON Schema | Machine-readable dataset containing structured benchmark ratings, dimensions, and competitor summaries. |

## Evaluated Competitor Landscape

| Competitor | Primary Archetype | Primary Surface | Primary Focus |
| :--- | :--- | :--- | :--- |
| **Cursor** | AI-First IDE Fork | VS Code Fork | Inline editing (`Ctrl+K`), fast codebase indexing, Composer Agent |
| **Anthropic Claude Code** | Terminal-First CLI Agent | Terminal CLI | Low-latency terminal REPL, bash tool execution, Claude 3.7 Sonnet |
| **Windsurf (Codeium)** | Context-Aware IDE | VS Code Fork | Cascade flow tracking, editor tab/cursor awareness, Supercomplete |
| **GitHub Copilot** | Ecosystem Assistive Tool | IDE Extension + Web | Inline autocomplete, GitHub PR summaries, Copilot Workspace |
| **Cognition Devin** | Autonomous Cloud Engineer | Cloud VM / Web | Asynchronous cloud VM execution, headless browser, Jira ticket resolution |

## Key Strategic Takeaways

| Strategic Differentiator | Antigravity Native Advantage | Competitor Landscape Comparison |
| :--- | :--- | :--- |
| **Multi-Surface Unification** | Unified backend across CLI (`agy`), Desktop Canvas 2.0, IDE, and Python SDK | Competitors force a choice between IDE-only (Cursor, Windsurf) or terminal-only (Claude Code). |
| **Subagent Worktree Isolation** | Dynamic subagents with isolated git worktrees (`Workspace: 'branch'`) | Competitors modify files directly in-place, risking merge conflicts and context pollution. |
| **Dual Execution Philosophy** | Decoupled high-trust planning (`/plan`) and relentless autonomous execution (`/goal`) | Competitors either jump straight into bash or lack autonomous test-healing loops. |
| **Token Window Economics** | Modular `SKILL.md` with progressive disclosure and lazy-loaded MCP schemas | Competitors use flat rule files that consume prompt tokens on every interaction turn. |
