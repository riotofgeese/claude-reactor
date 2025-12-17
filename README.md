# Claude Reactor

## Overview

Claude Reactor is a comprehensive pipeline system for Claude Code that integrates multiple MCP (Model Context Protocol) servers, skills, and workflow automation. It provides an 8-phase development workflow with memory persistence, code execution sandboxing, and multi-model consultation (Gemini, Codex, DeepSeek).

The project focuses on easy installation and setup, making it simple for developers to leverage a powerful agentic coding workflow with Claude Code.

## Key Features
- **8-Phase Workflow**: PREFLIGHT → CONTEXT → PLAN → SAFETY → EXECUTE → VERIFY → RECOVERY → COMMIT
- **Multi-Model Consultation**: Gemini, Codex, and DeepSeek MCP servers for plan review
- **Memory Persistence**: MemLayer and unified-orchestrator for cross-session context
- **Code Execution**: ACE sandbox for safe Python execution with learning
- **Skills System**: 15+ skills (auto-workflow, git-handbrake, lint-gate, tdd-enforcer, etc.)
- **Git Hooks**: Automated memory recall on session start, save on stop
- **Pipeline Installer**: `/p-install` command for one-click project setup
- **Context7 Integration**: Library documentation lookup

## Repo Structure
- `.claude/`: Symlinks to global Claude config (CLAUDE.md, skills, commands, mcp.json)
- `/hooks/`: Git hooks for pre-commit checks
- `/mcp/`: MCP server configurations (reactor.toml)
- `/docs/`: Documentation including [INSTALL.md](docs/INSTALL.md)
- `global_pipeline_agent.py`: Session orchestration agent
- `CLAUDE_CODE_WORKFLOW_SYSTEM.md`: Workflow documentation
- `OPTIMIZED_PIPELINE.md`: Pipeline optimization guide

## Installation

Quick install for any project:
```bash
/p-install /path/to/your/project
```

This creates symlinks to global config and enables all MCP servers.

## Usage

### Start with the workflow
```bash
claude                    # Start Claude Code
/p                        # Initialize pipeline
```

### Consult multiple models
```bash
# In Claude Code, use MCP tools:
mcp__gemini__gemini "Review my architecture"
mcp__codex__codex "Analyze this code"
mcp__deepseek__deepseek "Help debug this"
```

### Memory persistence
```bash
# Save task completion (automatic via hooks)
mcp__unified-orchestrator__smart_remember

# Recall context at session start
mcp__unified-orchestrator__session_restore
```

## Requirements
- Claude Code CLI
- Python 3.8+
- Git

## MCP Servers Included
| Server | Purpose |
|--------|---------|
| unified-orchestrator | Session state, memory, infrastructure |
| memlayer | Persistent cross-session storage |
| ace | Code execution sandbox with learning |
| gemini | Google Gemini consultation |
| codex | OpenAI Codex consultation |
| deepseek | DeepSeek consultation |
| context7 | Library documentation |
| sequential-thinking | Step-by-step reasoning |
| flowlens | Browser debugging |
| serena | Semantic code navigation |

## License
MIT License - see [LICENSE](LICENSE) for details.

## Contributing
Fork the repo, create a feature branch, and submit a pull request.
