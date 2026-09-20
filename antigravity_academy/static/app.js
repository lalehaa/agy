document.addEventListener('alpine:init', () => {
    Alpine.data('academyApp', () => ({
        activeTab: 'curriculum',
        modules: [],
        activeModule: null,
        userProgress: {}, // { "mod-1": ["mod-1-lab-1"] }
        toastMessage: '',
        showToast: false,

        // Generator State
        genType: 'agents',
        // Agents Form
        agentsForm: {
            pm_name: '@pm',
            pm_role: 'Translates user ideas into granular, flawless technical specifications.',
            coder_name: '@coder',
            coder_role: 'Writes exceptionally clean, production-ready Python or JavaScript code.',
            qa_name: '@qa',
            qa_role: 'Reviews generated code, writes test suites, and runs validation loops.',
            custom_rules: ['Always check .venv before running python scripts', 'Format files with black']
        },
        newRuleText: '',
        // Skill Form
        skillForm: {
            name: 'code-auditor',
            description: 'Runs security and linting checks over modified codebase files.',
            instructions: '1. Inspect files using view_file.\n2. Search for missing try/except blocks or credentials.\n3. Report detailed tracebacks.',
            allowed_tools: ['view_file', 'run_command']
        },
        newToolText: '',
        // MCP Form
        mcpForm: {
            server_name: 'alloydb-postgresql',
            command: 'python3',
            args: ['-m', 'mcp_server_alloydb'],
            env_vars: [
                { key: 'DB_HOST', value: 'localhost' },
                { key: 'DB_PORT', value: '5432' }
            ]
        },
        newEnvKey: '',
        newEnvVal: '',
        generatedResult: {
            filename: 'AGENTS.md',
            content: '# Generating...'
        },

        // Validator State
        valType: 'agents',
        valContent: `# My AI Development Team\n\n## Product Manager (@pm)\n- Role: Technical specs\n\n## Engineer (@coder)\n- Role: Writes code\n\n## QA (@qa)\n- Role: Tests code`,
        valResult: null,

        async init() {
            await this.loadCurriculum();
            await this.loadProgress();
            this.generateConfig();
        },

        triggerToast(msg) {
            this.toastMessage = msg;
            this.showToast = true;
            setTimeout(() => { this.showToast = false; }, 3000);
        },

        async loadCurriculum() {
            try {
                const res = await fetch('/api/curriculum');
                if (res.ok) {
                    this.modules = await res.json();
                    if (this.modules.length > 0) {
                        this.activeModule = this.modules[0];
                    }
                }
            } catch (err) {
                console.error('Failed to load curriculum:', err);
            }
        },

        async loadProgress() {
            try {
                const res = await fetch('/api/progress');
                if (res.ok) {
                    const data = await res.json();
                    this.userProgress = data.progress || {};
                }
            } catch (err) {
                console.error('Failed to load progress:', err);
            }
        },

        isLabCompleted(moduleId, labId) {
            const completedList = this.userProgress[moduleId] || [];
            return completedList.includes(labId);
        },

        async toggleLab(moduleId, labId) {
            let completedList = [...(this.userProgress[moduleId] || [])];
            if (completedList.includes(labId)) {
                completedList = completedList.filter(id => id !== labId);
            } else {
                completedList.push(labId);
            }
            this.userProgress[moduleId] = completedList;

            try {
                await fetch('/api/progress', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        module_id: moduleId,
                        completed_labs: completedList
                    })
                });
                this.triggerToast('Progress saved!');
            } catch (err) {
                console.error('Failed to save progress:', err);
            }
        },

        getModuleProgressPercent(module) {
            if (!module || !module.labs || module.labs.length === 0) return 0;
            const completed = (this.userProgress[module.id] || []).length;
            return Math.round((completed / module.labs.length) * 100);
        },

        // Generator Actions
        addCustomRule() {
            if (this.newRuleText.trim()) {
                this.agentsForm.custom_rules.push(this.newRuleText.trim());
                this.newRuleText = '';
                this.generateConfig();
            }
        },
        removeCustomRule(idx) {
            this.agentsForm.custom_rules.splice(idx, 1);
            this.generateConfig();
        },

        addSkillTool() {
            if (this.newToolText.trim()) {
                this.skillForm.allowed_tools.push(this.newToolText.trim());
                this.newToolText = '';
                this.generateConfig();
            }
        },
        removeSkillTool(idx) {
            this.skillForm.allowed_tools.splice(idx, 1);
            this.generateConfig();
        },

        addMcpEnv() {
            if (this.newEnvKey.trim()) {
                this.mcpForm.env_vars.push({
                    key: this.newEnvKey.trim(),
                    value: this.newEnvVal.trim()
                });
                this.newEnvKey = '';
                this.newEnvVal = '';
                this.generateConfig();
            }
        },
        removeMcpEnv(idx) {
            this.mcpForm.env_vars.splice(idx, 1);
            this.generateConfig();
        },

        async generateConfig() {
            let endpoint = '/api/generate/agents';
            let payload = {};

            if (this.genType === 'agents') {
                endpoint = '/api/generate/agents';
                payload = this.agentsForm;
            } else if (this.genType === 'skill') {
                endpoint = '/api/generate/skill';
                payload = this.skillForm;
            } else if (this.genType === 'mcp') {
                endpoint = '/api/generate/mcp';
                const envObj = {};
                this.mcpForm.env_vars.forEach(item => {
                    if (item.key) envObj[item.key] = item.value;
                });
                payload = {
                    server_name: this.mcpForm.server_name,
                    command: this.mcpForm.command,
                    args: this.mcpForm.args,
                    env_vars: envObj
                };
            }

            try {
                const res = await fetch(endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                if (res.ok) {
                    this.generatedResult = await res.json();
                }
            } catch (err) {
                console.error('Failed to generate config:', err);
            }
        },

        copyToClipboard(text) {
            navigator.clipboard.writeText(text);
            this.triggerToast('Copied to clipboard!');
        },

        downloadConfig() {
            const blob = new Blob([this.generatedResult.content], { type: 'text/plain' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = this.generatedResult.filename || 'config.txt';
            a.click();
            window.URL.revokeObjectURL(url);
            this.triggerToast(`Downloaded ${a.download}`);
        },

        // Validator Actions
        async validateContent() {
            try {
                const res = await fetch('/api/validate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        config_type: this.valType,
                        content: this.valContent
                    })
                });
                if (res.ok) {
                    this.valResult = await res.json();
                }
            } catch (err) {
                console.error('Validation error:', err);
            }
        }
    }));
});

