from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class LabTask(BaseModel):
    id: str
    title: str
    instruction: str
    code_template: str
    explanation: str


class CurriculumModule(BaseModel):
    id: str
    title: str
    description: str
    icon: str
    estimated_time: str
    labs: List[LabTask]


class ProgressUpdate(BaseModel):
    module_id: str
    completed_labs: List[str] = Field(default_factory=list)


class UserProgressResponse(BaseModel):
    progress: Dict[str, List[str]] = Field(default_factory=dict)


class AgentsConfigInput(BaseModel):
    pm_name: str = "@pm"
    pm_role: str = "Translates user ideas into granular, flawless technical specifications."
    coder_name: str = "@coder"
    coder_role: str = "Writes exceptionally clean, production-ready Python or JavaScript code."
    qa_name: str = "@qa"
    qa_role: str = "Reviews generated code, writes test suites, and runs validation loops."
    custom_rules: List[str] = Field(default_factory=list)


class SkillConfigInput(BaseModel):
    name: str
    description: str
    instructions: str
    allowed_tools: List[str] = Field(default_factory=list)


class MCPConfigInput(BaseModel):
    server_name: str
    command: str
    args: List[str] = Field(default_factory=list)
    env_vars: Dict[str, str] = Field(default_factory=dict)


class ConfigGenerationResponse(BaseModel):
    filename: str
    content: str


class ValidationRequest(BaseModel):
    config_type: str  # "agents", "skill", "mcp"
    content: str


class ValidationResult(BaseModel):
    valid: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

