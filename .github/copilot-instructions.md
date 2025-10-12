# Repository Onboarding Instructions

## 1. Purpose
This repository is configured for optimal use with GitHub Copilot Coding Agent. The following settings and best practices are recommended for all contributors and Copilot agents working in this repository.

## 2. Coding Agent Instructions
- Always break down complex tasks into actionable todos and track progress.
- Use clear, concise commit messages and PR descriptions.
- Prefer using existing libraries and patterns in this codebase.
- When adding new files, follow the established directory structure and naming conventions.
- For multi-step changes, use a todo list and mark each as completed when done.
- Validate all code changes by running tests or linting before marking as complete.
- Reference this file for onboarding and best practices.

## 3. File/Directory Conventions

### Project Structure
```
/home/runner/work/main/main/
├── CursorDocsIndex/          # Documentation indexing and semantic search system
│   ├── docs_agent/           # Core module for doc ingestion and search
│   ├── docs_cli.py           # Command-line interface
│   ├── api_server.py         # REST API server
│   ├── install.sh            # Installation script
│   ├── test-api.sh           # API testing script
│   └── requirements.txt      # Python dependencies for docs module
├── sound_packs/              # Audio samples (drums, loops, vocals, one_shots)
├── *.py                      # Main Python scripts (AI tools, mixing, etc.)
├── *.sh                      # Shell scripts for starting services
└── requirements*.txt         # Python dependencies for different modules
```

### Naming Conventions
- **Python scripts**: Use snake_case (e.g., `ai_mixing_engineer.py`, `logic_copilot_lite.py`)
- **Shell scripts**: Use kebab-case with descriptive names (e.g., `start-music-ai.sh`, `setup-chatgpt-training.sh`)
- **Documentation**: Use UPPERCASE or Title-Case for guide files (e.g., `README.md`, `QUICK-START.md`)
- **Requirements files**: Use pattern `requirements*.txt` with descriptive suffixes (e.g., `requirements_mixing.txt`, `requirements_lite.txt`)

### Where to Place New Files
- **New Python scripts**: Place in repository root
- **Documentation**: Place in root or relevant subdirectory (use existing patterns)
- **CursorDocsIndex code**: Place in `CursorDocsIndex/` directory
  - API/docs-related Python code: `CursorDocsIndex/docs_agent/`
  - CLI scripts: `CursorDocsIndex/`
- **Test scripts**: Place in relevant directory (e.g., `CursorDocsIndex/test-api.sh`)
- **Sound packs**: Place in appropriate `sound_packs/` subdirectory (drums, loops, vocals, one_shots)

### Requirements Files
- Add dependencies to the relevant `requirements*.txt` file based on the module:
  - `requirements.txt` - Main/general dependencies
  - `requirements_mixing.txt` - AI mixing engineer dependencies
  - `requirements_lite.txt` - Lite/basic dependencies
  - `requirements_live_ai.txt` - Live AI assistant dependencies
  - `requirements_plugin.txt` - Plugin dependencies
  - `requirements_chatgpt_training.txt` - ChatGPT training dependencies
  - `CursorDocsIndex/requirements.txt` - Documentation agent dependencies

## 4. Testing & Validation

### General Testing
- Run all relevant tests after making changes
- Ensure no new errors are introduced
- Test scripts before committing (e.g., run shell scripts with `bash -n script.sh` for syntax check)

### Module-Specific Testing
- **CursorDocsIndex**: Use `CursorDocsIndex/test-api.sh` for API validation
- **AI Tools**: Test each tool by running its respective `start-*.sh` script
- **Python modules**: Run the Python script directly to verify functionality

### Validation Checklist
- [ ] Code follows existing naming conventions
- [ ] Dependencies added to correct requirements file
- [ ] Scripts are executable (chmod +x for .sh files)
- [ ] Documentation updated if functionality changed
- [ ] No secrets or API keys committed
- [ ] .gitignore rules respected (no audio files, __pycache__, .env, etc.)

## 5. Communication
- Use clear PR titles and descriptions
- Document any non-obvious design decisions in the PR or in a Markdown file
- For complex features, create a guide file (e.g., `*-GUIDE.md` pattern)
- Use emoji in documentation for better readability (✅, 📁, 🚀, etc.) - matches existing style

## 6. Security & Privacy
- Do not commit secrets or sensitive data
- Keep API keys in `.env` file (already gitignored)
- Review dependencies for security issues before adding
- Do not commit large audio files (already handled by .gitignore)

## 7. Copilot Agent Best Practices
- Always check for existing implementations before creating new ones
- Use semantic and grep search to find relevant code and documentation
- When in doubt, ask for clarification or add a TODO for human review
- Follow the pattern of existing documentation files (emoji, structure, tone)
- Check README.md and related guides before making major changes

## 8. Module-Specific Guidelines

### CursorDocsIndex
- This is a semantic documentation indexing system
- Follow the patterns in `CursorDocsIndex/README.md` and `QUICK-START.md`
- When modifying, ensure backward compatibility with CLI commands
- Test with `./install.sh` and `./test-api.sh` before committing
- Core logic is in `docs_agent/` module (ingestion.py, search.py, core.py, models.py)

### AI Tools (Music Production)
- Main entry points are `start-*.sh` scripts
- Python scripts use various AI APIs (configured in .env)
- Test by running the start script and verifying the service launches
- Keep in mind Logic Pro integration and macOS-specific features

### Sound Packs
- Only placeholder .txt files are committed
- Actual audio files (.wav, .mp3, .aif, etc.) are gitignored
- Keep the directory structure for user organization

## 9. Common Patterns in This Repository
- **Guides**: Comprehensive markdown files with emoji, clear sections, and code examples
- **Start scripts**: Shell scripts that activate venv and launch Python services
- **Requirements**: Modular dependencies for different features
- **CLI tools**: Use typer and rich for terminal UI (see `CursorDocsIndex/docs_cli.py`)

## 10. References
- [Best practices for Copilot coding agent in your repository](https://gh.io/copilot-coding-agent-tips)
- Repository README.md for overview
- Individual module README files for specific details

## 11. Key Repository Details
- **Owner**: neebz1/main
- **Primary Purpose**: AI-powered coding and music production environment
- **Main Technologies**: Python, Shell scripting, AI APIs
- **Target User**: Developer working with AI tools, Cursor IDE, and Logic Pro

---

**End of configuration**

*Last updated: October 2025*
