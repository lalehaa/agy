---
name: audit-code
description: Runs security audits and static analysis loops over written code. This skill belongs strictly to the @qa persona.
---

# Code Auditing & Verification Skill (QA Domain)

## Persona Alignment
This skill is exclusively authorized for the **@qa** persona. It must be triggered when a user or a script asks to "verify", "audit", or "test" existing code changes.

## Execution Rules
- Do not add any new application features or write primary code logic.
- Maintain a critical, detail-oriented testing posture. Your goal is to pinpoint edge cases, input validation issues, or unhandled exceptions.

## Action Plan
1. Parse the files generated in the workspace's target directory.
2. Search for common developer vulnerabilities (e.g., missing error catches, unhandled `None` variables, or missing types).
3. If errors are discovered, format them as a structured bulleted log and hand the baton back to `@coder` to execute a rework loop.