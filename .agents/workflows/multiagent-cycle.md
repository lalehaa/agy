---
description: akes an app idea in multiagent process generates a spec, writes the code, and passes it to QA.
---

# Multi-Agent Factory Workflow

### Step 1: Ideation & Architecture
Trigger **@pm** to run the `draft-spec` skill based on the user's app description.

### Step 2: Implementation
Once the user confirms, route the generated file path to **@coder** to execute the `generate-code` skill.

### Step 3: Assurance
Pass the workspace updates to **@qa** to trigger the `audit-code` loop.