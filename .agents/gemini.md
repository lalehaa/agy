# Project Rules & Standards

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