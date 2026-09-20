import json
import re
import yaml
from typing import Dict, Any
from app.models import ValidationResult


def validate_agents_config(content: str) -> ValidationResult:
    errors = []
    warnings = []

    if not content or not content.strip():
        return ValidationResult(valid=False, errors=["Content is empty."])

    # Check for personas
    personas = ["@pm", "@coder", "@qa"]
    found_personas = [p for p in personas if p in content]

    for p in personas:
        if p not in found_personas:
            warnings.append(f"Persona '{p}' is not defined in the AGENTS.md document.")

    if not any(header in content for header in ["# ", "## "]):
        errors.append("Document missing Markdown headers (# or ##).")

    if "Role:" not in content and "role:" not in content and "- Role" not in content:
        warnings.append("Consider explicitly adding 'Role:' bullet points for each persona.")

    valid = len(errors) == 0
    return ValidationResult(valid=valid, errors=errors, warnings=warnings)


def validate_skill_config(content: str) -> ValidationResult:
    errors = []
    warnings = []

    if not content or not content.strip():
        return ValidationResult(valid=False, errors=["Content is empty."])

    # Check for YAML frontmatter block --- ... ---
    pattern = r"^---\s*\n(.*?)\n---\s*\n?(.*)"
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        errors.append("Skill file missing YAML frontmatter enclosed in '---' headers.")
        return ValidationResult(valid=False, errors=errors, warnings=warnings)

    frontmatter_str = match.group(1)
    body_str = match.group(2)

    try:
        frontmatter = yaml.safe_load(frontmatter_str)
        if not isinstance(frontmatter, dict):
            errors.append("YAML frontmatter must be a key-value dictionary.")
            return ValidationResult(valid=False, errors=errors, warnings=warnings)

        if "name" not in frontmatter or not str(frontmatter["name"]).strip():
            errors.append("Frontmatter missing required field 'name'.")
        elif not re.match(r"^[a-zA-Z0-9_-]+$", str(frontmatter["name"])):
            errors.append("Skill 'name' should contain only alphanumeric characters, underscores, or hyphens.")

        if "description" not in frontmatter or not str(frontmatter["description"]).strip():
            warnings.append("Frontmatter missing recommended field 'description'.")

    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML frontmatter syntax: {str(e)}")

    if not body_str or not body_str.strip():
        warnings.append("Skill markdown instructions body is empty.")

    valid = len(errors) == 0
    return ValidationResult(valid=valid, errors=errors, warnings=warnings)


def validate_mcp_config(content: str) -> ValidationResult:
    errors = []
    warnings = []

    if not content or not content.strip():
        return ValidationResult(valid=False, errors=["Content is empty."])

    try:
        data = json.loads(content)
        if not isinstance(data, dict):
            errors.append("Root MCP JSON must be an object.")
            return ValidationResult(valid=False, errors=errors, warnings=warnings)

        if "mcpServers" not in data or not isinstance(data["mcpServers"], dict):
            errors.append("MCP config missing top-level 'mcpServers' object.")
            return ValidationResult(valid=False, errors=errors, warnings=warnings)

        servers = data["mcpServers"]
        if len(servers) == 0:
            warnings.append("'mcpServers' object is empty. No servers defined.")

        for server_name, server_cfg in servers.items():
            if not isinstance(server_cfg, dict):
                errors.append(f"Server config for '{server_name}' must be an object.")
                continue

            if "command" not in server_cfg or not str(server_cfg["command"]).strip():
                errors.append(f"Server '{server_name}' missing required 'command' string.")

            if "args" in server_cfg and not isinstance(server_cfg["args"], list):
                warnings.append(f"Server '{server_name}' field 'args' should be an array of strings.")

            if "env" in server_cfg and not isinstance(server_cfg["env"], dict):
                warnings.append(f"Server '{server_name}' field 'env' should be an object/dictionary.")

    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON format: {str(e)}")

    valid = len(errors) == 0
    return ValidationResult(valid=valid, errors=errors, warnings=warnings)


def validate_config(config_type: str, content: str) -> ValidationResult:
    if config_type == "agents":
        return validate_agents_config(content)
    elif config_type == "skill":
        return validate_skill_config(content)
    elif config_type == "mcp":
        return validate_mcp_config(content)
    else:
        return ValidationResult(
            valid=False,
            errors=[f"Unsupported config type '{config_type}'. Expected 'agents', 'skill', or 'mcp'."],
        )

