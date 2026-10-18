# Security

This is a personal, public knowledge base. It holds no credentials, personal data or private material by design:
a private blocklist of terms that must never be published is checked locally and in CI on every change (ADR 012).

**Reporting a problem:** please use GitHub's private vulnerability reporting (the **Security** tab → "Report a
vulnerability"). That covers a leaked secret, a workflow that could be abused, or anything published here that should
not be. Please do not open a public issue with the details.

**What is in scope:** the workflows in `.github/`, the tools in `tools/`, and the published content in `wiki/`.
Secrets live only in GitHub Actions secrets and are never printed; the blocklist checker never prints a matched term.
