---
description: Takes an app idea, generates a spec, writes the code, and passes it to QA.
---

# Multi-Agent Factory Workflow

### Step 1: Requirements Architecture
Call @pm to analyze the user's input idea. Generate a comprehensive `technical_spec.md` file in the root folder. Stop and wait for user approval.

### Step 2: Full-Stack Generation
Once the user types "Approved", pass `technical_spec.md` to @coder. Instruct @coder to write the application files inside an `app/` directory.

### Step 3: Execution and Verification
Pass the generated `app/` folder to @qa. Instruct @qa to run a verification check and generate an implementation walkthrough report.