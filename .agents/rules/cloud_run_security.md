# Cloud Run Security Guardrail

## Cloud Run Deployment Authentication Requirement
- **CRITICAL**: Under NO circumstances should any Cloud Run service be deployed with unauthenticated access.
- **Forbidden Flags**: You are strictly forbidden from executing or generating deployment commands containing `--allow-unauthenticated`.
- **Mandatory Flag**: All Cloud Run deployments must explicitly enforce authentication using `--no-allow-unauthenticated`.
- **Enforcement Action**: If a deployment request or script does not enforce authentication or attempts to deploy with `--allow-unauthenticated`, you must immediately reject the deployment, warn the user about the security violation, and refuse to proceed unless `--no-allow-unauthenticated` is enforced.
