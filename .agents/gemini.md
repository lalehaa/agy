# Project Rules & Standards



## Environment Isolation & Dependency Management
- **CRITICAL**: You are strictly forbidden from installing global python packages or using the `--break-system-packages` flag.
- **Enforcement Rule**: Do not simply write instructions telling the user to create or activate an environment. You must actively execute the bash terminal tools yourself to provision the environment.
- **Execution Checklist**:
  1. Check if `.venv` exists in the application subfolder. If missing, immediately execute `python3 -m venv .venv` using your terminal tool.
  2. Always prefix any python-based execution or installation command with the activation snippet: `source .venv/bin/activate && ...`
  3. Ensure all packages (`uvicorn`, `fastapi`, etc.) are fully installed into this local virtual environment before finalizing the workflow step.


## Code Style & Guardrails
- **Language**: All backend logic must be written in strict, typed Python 3.11+.
- **Formatting**: Always run `black` formatting on files before declaring a task complete.
- **Testing Requirement**: Never modify a core routing file without either updating or writing a corresponding unit test in the `tests/` directory.

## Strict Constraints
- DO NOT use deprecated legacy endpoints.
- DO NOT hardcode API credentials or environment secrets. Use `os.getenv()` exclusively.
- If an operation requires a database migration, you must explicitly flag it to the user and wait for human confirmation before running the script.

## Workspace Architecture & Project Creation
- **New Applications Only**: Whenever you are instructed to create a completely new application (as opposed to editing or refactoring an existing application layout), you must immediately generate a dedicated root folder for it inside the current workspace directory.
- **Isolation Requirement**: Absolutely no loose development files or application source files should ever be written directly to the project's global root directory. Everything belongs inside the scoped application directory.
- **Technical Specification Storage**: All architecture blueprints, technical markdown files (`README.md`, `technical_spec.md`, design docs, etc.) created for this new application must be stored neatly inside that newly created application folder, keeping the main repository workspace clean and structured.