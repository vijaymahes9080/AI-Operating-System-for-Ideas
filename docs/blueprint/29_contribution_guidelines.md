# Contribution Guidelines

Thank you for choosing to contribute to IdeasOS! This document outlines coding standards, environment setup, and the Pull Request (PR) lifecycle.

---

## 1. Fast Track: Developer Setup

To set up a local development environment:

```bash
# 1. Clone the repository
git clone https://github.com/ideas-os/ideas-os.git
cd ideas-os

# 2. Run the bootstrap setup script
# (Ensures node modules, uv python env, and SQLite databases are configured)
./scripts/setup.sh

# 3. Start the hot-reloading development server
./scripts/dev.sh
```

---

## 2. Coding Style & Linting Rules

We enforce strict formatting rules to maintain code cleanliness across the monorepo:

### Python (Backend & Agents)
- **Tooling**: We use **Ruff** for linting and code formatting (replaces black, flake8, and isort).
- **Standards**:
  - Run linting check: `ruff check backend/app/`
  - Auto-format files: `ruff format backend/app/`
  - Function definitions must include type hints: `def run_analysis(idea: str) -> dict:`

### TypeScript & React (Frontend)
- **Tooling**: We use **Prettier** for formatting and **ESLint** for code analysis.
- **Standards**:
  - Run formatting: `npm run format` (inside `frontend/`)
  - Run static tests: `npm run lint` (inside `frontend/`)
  - Component imports must be grouped: react core -> components/ui -> hooks -> stores.

---

## 3. Git Commit Convention

We follow the **Conventional Commits** specification. Commit messages must be structured as follows:

```
<type>(<scope>): <description>

[Optional Body]
[Optional Footer / Issue Reference]
```

### Types
- `feat`: A new feature (e.g., `feat(agent): add security critique loop`).
- `fix`: A bug fix (e.g., `fix(db): resolve SQLite WAL locking concurrency`).
- `docs`: Documentation updates.
- `style`: Changes that do not affect code logic (formatting, spaces).
- `refactor`: Code changes that neither fix a bug nor add a feature.
- `test`: Adding or correcting tests.

---

## 4. Pull Request Lifecycle

1. **Create Branch**: Branch off `main` using descriptive naming conventions: `feature/agent-debate` or `bugfix/inbox-pdf-crash`.
2. **Implement & Test**: Write code and ensure local tests pass via `pytest` and `vitest`.
3. **Open Pull Request**: Target the `main` branch. Provide a summary of changes, screenshot evidence for UI modifications, and reference associated issues (e.g. `Closes #142`).
4. **CI Verification**: GitHub Actions automatically runs Ruff, ESLint, Bandit security scans, and Playwright E2E tests on every commit push.
5. **Peer Review**: At least one core maintainer must approve the PR changes before merge.
