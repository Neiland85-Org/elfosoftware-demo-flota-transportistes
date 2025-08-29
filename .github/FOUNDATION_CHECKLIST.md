# Foundation Setup Checklist

This checklist tracks the implementation of foundational repository setup scaffolding for the elfosoftware-demo-flota-transportistes project.

## Development Environment

- [x] Devcontainer added (.devcontainer/devcontainer.json)
- [x] VS Code extensions & settings (.vscode/)
- [ ] EditorConfig (.editorconfig)

## Code Quality & Formatting

- [ ] ESLint config
- [ ] Prettier config
- [x] Ruff / Black config
- [x] Pre-commit hooks (.pre-commit-config.yaml)
- [ ] package.json scripts (if applicable)
- [ ] Husky + lint-staged (if confirmed)

## Security & Dependencies

- [ ] Dependabot config (.github/dependabot.yml)
- [ ] CodeQL workflow (.github/workflows/codeql.yml)

## CI/CD

- [ ] CI workflow (.github/workflows/ci.yml)
- [ ] Release Please workflow & config (.github/workflows/release-please.yml)

## Collaboration & Governance

- [ ] Issue templates (.github/ISSUE_TEMPLATE/)
- [ ] PR template (.github/PULL_REQUEST_TEMPLATE.md)
- [ ] CODEOWNERS (.github/CODEOWNERS)
- [ ] SECURITY.md
- [ ] CONTRIBUTING.md (optional)

## Project Hygiene

- [ ] .gitignore (Node + Python)
- [ ] README dev section
- [ ] Version pin files (.nvmrc / pyproject.toml / requirements\*.txt)

## Manual Settings (Separate Issues)

- [ ] Manual settings issues created
- [ ] Branch protection rules (main)
- [ ] Enable private vulnerability reporting
- [ ] Enable secret scanning & push protection
- [ ] Enable Dependabot security updates
- [ ] Enforce CODEOWNERS for reviews
- [ ] Merge strategy configuration

## Implementation Notes

Each item in this checklist will be implemented incrementally through separate commits. The user will provide EXACT contents for each target file, and this checklist will be updated accordingly as each item is completed.

**Next Steps**: Await user-provided file contents and implement them commit-by-commit until completion.
