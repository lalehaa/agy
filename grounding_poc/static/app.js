document.addEventListener('alpine:init', () => {
    Alpine.data('groundingApp', () => ({
        activeTab: 'compare',
        promptInput: 'What are the key benefits and security features of Vertex AI Grounding?',
        selectedModel: 'gemini-2.0-flash',
        singleMode: 'google_search',
        isLoading: false,
        toastMessage: '',
        showToast: false,

        // Comparison Results State
        comparisonData: null,
        singleResult: null,

        // Config State
        config: {
            project_id: 'my-gcp-project',
            location: 'us-central1',
            datastore_id: 'my-enterprise-datastore',
            model_name: 'gemini-2.0-flash'
        },

        async init() {
            await this.fetchConfig();
            await this.runComparison();
        },

        triggerToast(msg) {
            this.toastMessage = msg;
            this.showToast = true;
            setTimeout(() => { this.showToast = false; }, 3000);
        },

        async fetchConfig() {
            try {
                const res = await fetch('/api/config');
                if (res.ok) {
                    this.config = await res.json();
                    this.selectedModel = this.config.model_name || 'gemini-2.0-flash';
                }
            } catch (err) {
                console.error('Failed to fetch config:', err);
            }
        },

        async saveConfig() {
            try {
                const res = await fetch('/api/config', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(this.config)
                });
                if (res.ok) {
                    this.config = await res.json();
                    this.triggerToast('Configuration updated!');
                }
            } catch (err) {
                console.error('Failed to save config:', err);
            }
        },

        async runComparison() {
            if (!this.promptInput.trim()) {
                this.triggerToast('Please enter a prompt.');
                return;
            }
            this.isLoading = true;
            try {
                const res = await fetch('/api/compare', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        prompt: this.promptInput,
                        model_name: this.selectedModel,
                        project_id: this.config.project_id,
                        location: this.config.location,
                        datastore_id: this.config.datastore_id
                    })
                });
                if (res.ok) {
                    this.comparisonData = await res.json();
                } else {
                    const err = await res.json();
                    this.triggerToast(err.detail || 'Error executing grounding comparison.');
                }
            } catch (err) {
                console.error('Comparison error:', err);
                this.triggerToast('Network error while fetching grounding comparison.');
            } finally {
                this.isLoading = false;
            }
        },

        async runSingleMode() {
            if (!this.promptInput.trim()) {
                this.triggerToast('Please enter a prompt.');
                return;
            }
            this.isLoading = true;
            try {
                const res = await fetch('/api/ground', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        prompt: this.promptInput,
                        mode: this.singleMode,
                        model_name: this.selectedModel,
                        project_id: this.config.project_id,
                        location: this.config.location,
                        datastore_id: this.config.datastore_id
                    })
                });
                if (res.ok) {
                    this.singleResult = await res.json();
                } else {
                    const err = await res.json();
                    this.triggerToast(err.detail || 'Error running grounding query.');
                }
            } catch (err) {
                console.error('Single query error:', err);
                this.triggerToast('Network error while running grounding query.');
            } finally {
                this.isLoading = false;
            }
        },

        copyToClipboard(text) {
            navigator.clipboard.writeText(text);
            this.triggerToast('Copied to clipboard!');
        }
    }));
});

