# Copilot Coding Agent Configuration

# Repository Onboarding Instructions

# 1. Purpose
This repository is configured for optimal use with GitHub Copilot Coding Agent. The following settings and best practices are recommended for all contributors and Copilot agents working in this repository.

# 2. Coding Agent Instructions
- Always break down complex tasks into actionable todos and track progress.
- Use clear, concise commit messages and PR descriptions.
- Prefer using existing libraries and patterns in this codebase.
- When adding new files, follow the established directory structure and naming conventions.
- For multi-step changes, use a todo list and mark each as completed when done.
- Validate all code changes by running tests or linting before marking as complete.
- Reference this file for onboarding and best practices.

# 3. File/Directory Conventions
- Place new scripts in the root or appropriate subdirectory (e.g., `CursorDocsIndex/` for API/docs code).
- Add requirements to the relevant `requirements*.txt` file.
- Documentation should be added as Markdown files in the root or relevant subfolder.

# 4. Testing & Validation
- Run all relevant tests after making changes.
- Use `test-api.sh` for API validation in `CursorDocsIndex/`.
- Ensure no new errors are introduced (run linting if available).

# 5. Communication
- Use clear PR titles and descriptions.
- Document any non-obvious design decisions in the PR or in a Markdown file.

# 6. Security & Privacy
- Do not commit secrets or sensitive data.
- Review dependencies for security issues before adding.

# 7. Copilot Agent Best Practices
- Always check for existing implementations before creating new ones.
- Use semantic and grep search to find relevant code and documentation.
- When in doubt, ask for clarification or add a TODO for human review.

# 8. References
- [Best practices for Copilot coding agent in your repository](https://gh.io/copilot-coding-agent-tips)

# End of configuration
