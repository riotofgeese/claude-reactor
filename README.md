# Gemini MCP Project

## Overview

This repository implements an MCP (Modular Component Platform) integration for Google Gemini AI models within the Claude Code environment. It provides tools for starting Gemini sessions, continuing conversations, and configuring the integration for code review, planning, and analysis tasks.

The project focuses on easy installation and setup, making it simple for developers to leverage Gemini's capabilities alongside Claude Code.

## Key Features
- Dedicated MCP tools: `gemini` for starting sessions and `gemini-reply` for continuing conversations
- Git hooks in `/hooks/` for automating workflows (e.g., pre-commit checks, post-merge setups)
- MCP configuration files in `/mcp/` for server setup and tool loading
- Comprehensive documentation in `/docs/` including installation guides
- Support for sandbox modes (read-only, workspace-write, danger-full-access)
- Easy configuration via `settings.json` for VSCode/Claude Code integration
- Initialization script `run.sh` for quick project setup

## Repo Structure
- `/hooks/`: Git hooks for pre-commit, post-merge, and other lifecycle events
- `/mcp/`: Configuration files for MCP servers (e.g., gemini config.toml, prompts)
- `/docs/`: Documentation including [INSTALL.md](docs/INSTALL.md) for setup instructions
- `.gitignore`: Defaults for Node.js/Python projects (node_modules, __pycache__, .env, etc.)
- `settings.json`: Configuration for enabling MCP servers and hooks in editors
- `run.sh`: Shell script for initializing the project (git init, npm install if applicable, MCP setup)
- `README.md`: This file
- `LICENSE`: MIT License

## Installation
See [docs/INSTALL.md](docs/INSTALL.md) for step-by-step instructions.

Key highlights:
- Add bashrc aliases for quick gemini session starts
- Configure `settings.json` to load MCP and enable hooks
- Run `run.sh` to initialize the project environment

## Usage
Once installed:
1. Start a Gemini session:
   ```
   gemini "Review this code architecture for scalability"
   ```
   Parameters: prompt (required), cwd, sandbox, base-instructions, etc.

2. Continue a session:
   ```
   gemini-reply <conversationId> "Provide more details on the review"
   ```

Configure via MCP tools for custom models (default: gemini-3-pro-preview).

## Requirements
- Claude Code CLI
- Node.js (for potential scripts) or Python (for MCP configs)
- Git

## License
MIT License - see [LICENSE](LICENSE) for details.

## Contributing
Fork the repo, create a feature branch, and submit a pull request. See CONTRIBUTING.md (to be added) for guidelines.

## Support
For issues, open a GitHub issue or use the gemini tools for analysis.
