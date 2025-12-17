#!/bin/bash

# Gemini MCP Project Initialization Script
# Usage: ./run.sh [init|config|verify]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Gemini MCP Initialization Script"

case "${1:-init}" in
  init)
    echo "Initializing project structure..."

    # Create directories if they don't exist
    mkdir -p hooks mcp docs .vscode

    # Create sample pre-commit hook
    if [ ! -f "$SCRIPT_DIR/hooks/pre-commit" ]; then
      cat > "$SCRIPT_DIR/hooks/pre-commit" << 'EOF'
#!/bin/sh
# Pre-commit hook for Gemini MCP Project
# Run linting, secret scans, etc.

echo "Running pre-commit checks for Gemini MCP..."
# Example: npm run lint --if-present
# Example: git secrets --scan

# Exit with error if checks fail (add your checks here)
exit 0
EOF
      chmod +x "$SCRIPT_DIR/hooks/pre-commit"
      echo "Created sample pre-commit hook."
    fi

    # Create sample MCP config for Gemini
    if [ ! -f "$SCRIPT_DIR/mcp/gemini.toml" ]; then
      mkdir -p "$SCRIPT_DIR/mcp"
      cat > "$SCRIPT_DIR/mcp/gemini.toml" << 'EOF'
# Gemini MCP Configuration
# Default model: gemini-3-pro-preview
# Sandbox mode: read-only (change to workspace-write for file access)

[prompt]
base_instructions = "You are a helpful AI assistant integrated with Claude Code for code review and analysis."

[session]
model = "gemini-3-pro-preview"
sandbox = "read-only"
cwd = "/path/to/your/project"

[developer]
instructions = "Focus on code quality, scalability, and best practices."
EOF
      echo "Created sample MCP config: mcp/gemini.toml"
    fi

    # Symlink git hooks if .git exists
    if [ -d "$SCRIPT_DIR/.git" ] || [ -d "$SCRIPT_DIR/../.git" ]; then
      HOOKS_DIR="$SCRIPT_DIR/.git/hooks"
      [ ! -d "$HOOKS_DIR" ] && HOOKS_DIR="$SCRIPT_DIR/../.git/hooks"

      if [ -d "$HOOKS_DIR" ]; then
        ln -sf "$SCRIPT_DIR/hooks/pre-commit" "$HOOKS_DIR/pre-commit"
        echo "Symlinked pre-commit hook to .git/hooks/"
      fi
    else
      echo "Git repository not found. Run 'git init' first."
    fi

    # Install dependencies if package.json exists
    if [ -f "$SCRIPT_DIR/package.json" ]; then
      echo "Installing Node.js dependencies..."
      npm install
    fi

    echo "Initialization complete! See docs/INSTALL.md for next steps."
    ;;

  config)
    echo "Reloading configurations..."
    # Reload MCP configs or env vars here
    # Example: source ~/.bashrc if aliases are set
    echo "Configurations reloaded. Restart Claude Code if necessary."
    ;;

  verify)
    echo "Verifying setup..."
    if [ -f "$SCRIPT_DIR/.git" ] || git rev-parse --git-dir > /dev/null 2>&1; then
      echo "✓ Git repository detected."
    else
      echo "✗ Git not initialized. Run 'git init'."
    fi

    if [ -d "$SCRIPT_DIR/hooks" ] && [ -f "$SCRIPT_DIR/hooks/pre-commit" ]; then
      echo "✓ Hooks directory and sample pre-commit exist."
    else
      echo "✗ Hooks not set up. Run './run.sh init'."
    fi

    if [ -f "$SCRIPT_DIR/mcp/gemini.toml" ]; then
      echo "✓ MCP config exists."
    else
      echo "✗ MCP config missing. Run './run.sh init'."
    fi

    if [ -L "$SCRIPT_DIR/.git/hooks/pre-commit" ] || [ -f "$SCRIPT_DIR/.git/hooks/pre-commit" ]; then
      echo "✓ Pre-commit hook linked."
    else
      echo "✗ Pre-commit hook not linked."
    fi

    echo "Verification complete."
    ;;

  *)
    echo "Usage: $0 {init|config|verify}"
    exit 1
    ;;
esac