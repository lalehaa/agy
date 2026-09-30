# Antigravity Academy - Deployment Rules

## Security Guardrail: Cloud Run Ingress & Authentication
- **Forbidden**: `--allow-unauthenticated` or granting `roles/run.invoker` to `allUsers`.
- **Mandatory**: All deployments of Antigravity Academy to Cloud Run MUST require authentication using `--no-allow-unauthenticated`.
- **Behavior**: If asked to deploy without authentication, reject immediately with a security alert.
