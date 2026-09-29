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

        // AI Assistant State
        chatInput: '',
        chatLoading: false,
        chatSuggestions: [],
        chatMessages: [
            {
                role: 'assistant',
                content: 'Hello! I am your Google Antigravity (AGY) Academy AI Assistant powered by Google ADK. Ask me anything about slash commands (/plan, /goal, /grill-me, /schedule), multi-agent teams (@pm, @coder, @qa), competitive comparisons with Cursor and Claude Code, custom skills, or sandbox permissions!',
                tool_used: 'search_agy_catalog',
                source: 'Antigravity Master Catalog'
            }
        ],

        async init() {
            await this.loadCurriculum();
            await this.loadProgress();
            await this.loadChatSuggestions();
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
        },

        // Assistant Actions
        async loadChatSuggestions() {
            try {
                const res = await fetch('/api/assistant/suggestions');
                if (res.ok) {
                    this.chatSuggestions = await res.json();
                }
            } catch (err) {
                console.error('Failed to load chat suggestions:', err);
            }
        },

        async sendChatMessage(msgOverride = null) {
            const text = (msgOverride || this.chatInput).trim();
            if (!text || this.chatLoading) return;

            this.chatMessages.push({
                role: 'user',
                content: text
            });
            this.chatInput = '';
            this.chatLoading = true;

            this.$nextTick(() => {
                const container = document.getElementById('chat-scroll-container');
                if (container) container.scrollTop = container.scrollHeight;
            });

            try {
                const res = await fetch('/api/assistant/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                if (res.ok) {
                    const data = await res.json();
                    this.chatMessages.push({
                        role: 'assistant',
                        content: data.response,
                        tool_used: data.tool_used,
                        source: data.source
                    });
                } else {
                    this.chatMessages.push({
                        role: 'assistant',
                        content: 'Sorry, I encountered an error answering your question. Please try again.',
                        source: 'Error Handler'
                    });
                }
            } catch (err) {
                this.chatMessages.push({
                    role: 'assistant',
                    content: 'Network connection failed while reaching the agent service.',
                    source: 'Network Error'
                });
            } finally {
                this.chatLoading = false;
                this.$nextTick(() => {
                    const container = document.getElementById('chat-scroll-container');
                    if (container) container.scrollTop = container.scrollHeight;
                });
            }
        },

        useSuggestion(suggestion) {
            this.sendChatMessage(suggestion);
        },

        formatMarkdown(content) {
            if (!content) return '';
            // Basic secure markdown rendering for chat
            let html = content
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;');
            
            // Code blocks
            html = html.replace(/```([a-zA-Z]*)\n([\s\S]*?)```/g, (match, lang, code) => {
                return `<pre class="bg-slate-950 p-3 rounded-lg border border-slate-800 my-2 overflow-x-auto text-xs font-mono text-cyan-300"><code>${code.trim()}</code></pre>`;
            });

            // Inline code
            html = html.replace(/`([^`]+)`/g, '<code class="bg-slate-800 text-cyan-300 px-1.5 py-0.5 rounded text-xs font-mono">$1</code>');

            // Headers
            html = html.replace(/^### (.*$)/gim, '<h4 class="font-bold text-slate-100 text-sm mt-3 mb-1">$1</h4>');
            html = html.replace(/^## (.*$)/gim, '<h3 class="font-bold text-cyan-400 text-base mt-3 mb-1.5">$1</h3>');
            html = html.replace(/^# (.*$)/gim, '<h2 class="font-bold text-cyan-300 text-lg mt-4 mb-2">$1</h2>');

            // Bold
            html = html.replace(/\*\*([^*]+)\*\*/g, '<strong class="font-semibold text-slate-100">$1</strong>');

            // Lists
            html = html.replace(/^\- (.*$)/gim, '<li class="ml-4 list-disc text-slate-300">$1</li>');

            // Line breaks
            html = html.replace(/\n\n/g, '<br><br>');
            return html;
        }
    }));
});

