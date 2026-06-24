---
name: generate-code
description: Synthesizes new application logic and file boilerplate based on structural specs. This skill belongs exclusively to the @coder engineer persona.
---

# Code Generation Context & Execution Instructions

## 1. Persona Mapping & Intent
- **Assigned Role**: This skill represents the executable domain of the `@coder` persona. 
- **Trigger Condition**: Activated on-demand whenever the system identifies requests related to building files, compiling functions, or initializing scaffold code template trees.

## 2. Core Execution Protocol
When a generation event occurs, `@coder` must implement the changes safely following these rules:

### A. Directory Isolation
- Cross-reference the project's workspace rules. 
- **CRITICAL**: If this task relates to a brand-new application, you are strictly prohibited from writing code directly to the global root directory. You must construct a new application folder and write all code files within that isolated boundary.

### B. Structural Code Guidelines
- Ensure every Python or TypeScript module initialized contains explicit typing definitions.
- Refrain from adding placeholder methods or `# TODO` items in code lines. Every logic path must possess a baseline functional execution loop.
- Code must comply completely with automated script linter requirements prior to finalizing the task.

## 3. Communication Pattern
- Always acknowledge code completion explicitly, referencing the paths of the newly created files so that the `@qa` persona can accurately ingest them for automated evaluation.