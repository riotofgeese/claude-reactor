# Installation Guide for Gemini MCP Project

This guide provides step-by-step instructions to install and set up the Gemini MCP integration in your Claude Code environment. The focus is on simplicity and quick enabling of features like MCP servers, git hooks, and aliases.

## Prerequisites
- Git installed
- Claude Code CLI available
- Bash shell (for aliases and scripts)
- VSCode (optional, for settings.json configuration)
- Node.js (if using any npm-based tools) or Python (for configs)

## Step 1: Clone or Initialize the Repository
If cloning from GitHub (once pushed):
```bash
git clone https://github.com/yourusername/gemini-mcp.git
cd gemini-mcp
```

Or initialize in your working directory:
```bash
git init
# Copy files or use run.sh for init
```

## Step 2: Run the Initialization Script
The project includes `run.sh` for quick setup. Make it executable and run:
```bash
chmod +x run.sh
./run.sh
```

This script will:
- Ensure directories are created (hooks, mcp, docs)
- Set up git hooks (symlink to .git/hooks)
- Load MCP configurations (e.g., copy mcp configs to ~/.claude or appropriate dir)
- Install any dependencies (npm install if package.json exists)
- Verify setup

**Note**: Customize `run.sh` if needed for your environment.

## Step 3: Add Bash Aliases
Add the following snippet to your `~/.bashrc` (or `~/.zshrc` for zsh) for quick access to Gemini commands:

```bash
# Gemini MCP Aliases
alias gemini-session='claude-code gemini'  # Start a new Gemini session
alias gemini-continue='claude-code gemini-reply'  # Continue an existing session
alias gemini-config='cd /path/to/gemini-mcp && ./run.sh --config'  # Reload configs
alias gemini-review='gemini-session "Review: "'  # Quick code review start

# Reload bash to apply
source ~/.bashrc
```

After adding, reload your shell:
```bash
source ~/.bashrc
```

Now you can use `gemini-review "my code"` to start reviews easily.

## Step 4: Configure settings.json (VSCode/Claude Code)
Create or update `.vscode/settings.json` in your project root to enable MCP servers and hooks. This integrates with Claude Code and VSCode extensions.

```json
{
  "claude.code.mcpServers": [
    "gemini",
    "unified-orchestrator",
    "ace"
  ],
  "claude.code.hooksEnabled": true,
  "claude.code.sandboxMode": "workspace-write",
  "extensions.autoUpdate": true,
  "git.enableSmartCommit": true,
  "terminal.integrated.defaultProfile.linux": "bash"
}
```

- `claude.code.mcpServers`: List of MCP servers to load (add 'gemini' for integration)
- `claude.code.hooksEnabled`: Enables git hooks from /hooks/
- `claude.code.sandboxMode`: Sets default sandbox access for Gemini sessions

If using Claude Code CLI without VSCode, export these as environment variables:
```bash
export CLAUDE_MCP_SERVERS="gemini,unified-orchestrator"
export CLAUDE_HOOKS_ENABLED=true
export CLAUDE_SANDBOX_MODE="workspace-write"
```

Add to `~/.bashrc` for persistence.

## Step 5: Enable Git Hooks
The `/hooks/` directory contains sample hooks. To enable:
```bash
# Symlink hooks to .git/hooks (run.sh does this automatically)
ln -s ../../hooks/pre-commit .git/hooks/pre-commit
ln -s ../../hooks/post-merge .git/hooks/post-merge

# Make executable
chmod +x .git/hooks/*
```

Hooks included:
- `pre-commit`: Runs linting and secret scans before commits
- `post-merge`: Updates MCP configs after pulls

## Step 6: Verify Installation
Test the setup:
```bash
# Check git hooks
git hook list  # Should show pre-commit, post-merge

# Test alias
gemini-session --help  # Should show Gemini MCP tool help

# Start a test session
gemini-session "Hello, Gemini!"
```

Run `run.sh --verify` for a full check.

## Troubleshooting
- **Hooks not running**: Ensure symlinks are correct and files are executable.
- **MCP not loading**: Check `claude.code.mcpServers` in settings or env vars.
- **Aliases not found**: Reload shell with `source ~/.bashrc`.
- **Dependencies missing**: Run `npm install` if Node.js tools are used.

For issues, see the [README](../README.md) or open an issue on GitHub.

## Next Steps
- Explore `/mcp/` for custom configurations (e.g., model overrides)
- Use Gemini for code reviews: `gemini-review "Analyze performance"`
- Contribute: Add more hooks or configs to `/hooks/` and `/mcp/`