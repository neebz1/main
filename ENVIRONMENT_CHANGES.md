# Environment Variable Changes in VS Code Workspace

This document collects environment variable changes made by VS Code extensions in the current workspace. These variables are set automatically to enable features and integrations for development.

---

## Terminal Environment Changes

### Extension: GitHub.codespaces

- `CODESPACE_VSCODE_FOLDER=/workspaces/main`

### Extension: vscode.git

Enables the following features: git auth provider

- `GIT_ASKPASS=/vscode/bin/linux-x64/03c265b1adee71ac88f833e065f7bb956b60550a/extensions/git/dist/askpass.sh`
- `VSCODE_GIT_ASKPASS_NODE=/vscode/bin/linux-x64/03c265b1adee71ac88f833e065f7bb956b60550a/node`
- `VSCODE_GIT_ASKPASS_EXTRA_ARGS=`
- `VSCODE_GIT_ASKPASS_MAIN=/vscode/bin/linux-x64/03c265b1adee71ac88f833e065f7bb956b60550a/extensions/git/dist/askpass-main.js`
- `VSCODE_GIT_IPC_HANDLE=/tmp/vscode-git-9eddb6ad54.sock`

---

**Summary:**
These environment variables are managed by VS Code and its extensions to support development workflows, authentication, and integration with remote environments. Manual changes are not recommended unless you understand their impact.
