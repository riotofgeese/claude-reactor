# Claude Reactor

<div align="center">

**The Production-Ready Agentic Pipeline for Claude Code**

Transform stateless CLI sessions into persistent, intelligent development workflows.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-green.svg)](https://claude.ai/code)
[![Pipeline](https://img.shields.io/badge/Pipeline-8%20Phases-purple.svg)](#pipeline-architecture)

</div>

---

## Overview

Claude Reactor is an enterprise-grade pipeline framework that supercharges Claude Code with:

- **8-Phase Structured Workflow** - From discovery to commit, every step is validated
- **Persistent Memory** - Context survives session restarts and compactions
- **70-90% Token Savings** - v2.0 sandbox-first execution minimizes context usage
- **53 Skills + 60 Agents** - Specialized capabilities for any development task
- **16 MCP Servers** - Curated integrations staying under tool limits

```
┌─────────────────────────────────────────────────────────────────┐
│                      CLAUDE REACTOR                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ DISCOVER │→ │ CONTEXT  │→ │   PLAN   │→ │  SAFETY  │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
│       ↓                                          ↓              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  COMMIT  │← │  REVIEW  │← │  VERIFY  │← │ EXECUTE  │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
├─────────────────────────────────────────────────────────────────┤
│  Memory Layer │ MCP Servers │ Skills │ Hooks │ Protocols       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Table of Contents

- [Quick Start](#quick-start)
- [Features](#features)
- [Pipeline Architecture](#pipeline-architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [MCP Servers](#mcp-servers)
- [Skills & Commands](#skills--commands)
- [Hooks System](#hooks-system)
- [Memory System](#memory-system)
- [Advanced Usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/anthropics/claude-reactor.git
cd claude-reactor

# 2. Start Claude Code in this directory
claude

# 3. Initialize the pipeline
/p
```

That's it. The `/p` command automatically:
- Verifies all pipeline components
- Installs missing dependencies via symlinks
- Enables v2.0 sandbox-first mode
- Recalls your preferences from memory

---

## Features

### v2.0 Sandbox-First Execution

The reactor uses a revolutionary approach to token efficiency:

```python
# OLD WAY (v1.0) - 5 tool calls = ~3,000 tokens
mcp__memlayer__recall(query="...")      # 600 tokens
mcp__context7__get-library-docs(...)    # 800 tokens
Read(file_path="...")                   # 500 tokens
Edit(file_path="...", old="", new="")   # 700 tokens
Bash(command="git commit...")           # 400 tokens

# NEW WAY (v2.0) - 1 sandbox call = ~300 tokens
mcp__code-execution-mode__run_python(
    code='''
    from pathlib import Path
    import subprocess

    # All operations in sandbox
    content = Path("/workspace/file.py").read_text()
    modified = content.replace("old", "new")
    Path("/workspace/file.py").write_text(modified)
    subprocess.run(["git", "commit", "-m", "Fix"], cwd="/workspace")

    # Only return summary
    print(json.dumps({"status": "committed", "file": "file.py"}))
    ''',
    project_path="/path/to/project"
)
```

**Token Rule**: Raw data stays in sandbox. Only summaries return to chat.

### Persistent Memory

Never lose context again:

```
┌─────────────────────────────────────────────────────────┐
│                    MEMORY HIERARCHY                      │
├─────────────────────────────────────────────────────────┤
│  L1: Session Context    │ Current conversation state    │
│  L2: Project Memory     │ memlayer (per-project)        │
│  L3: Infrastructure     │ Servers, DBs, connections     │
│  L4: Global Facts       │ User preferences, patterns    │
└─────────────────────────────────────────────────────────┘
```

### 53 Skills + 60 Agent Personas

Specialized capabilities loaded dynamically based on project type:

| Project Type | Auto-Loaded Skills |
|-------------|-------------------|
| Frontend | `dev-browser`, `sequential-thinking`, `lint-gate` |
| Backend | `debugging-playbook`, `tdd-enforcer`, `api-docs` |
| DevOps | `portmon`, `pipeline-health-check`, `terraform` |
| Documentation | `auto-docs`, `docs-first`, `context7-wrapper` |

### 27 Slash Commands

Pipeline control at your fingertips:

| Command | Purpose |
|---------|---------|
| `/p` | Initialize pipeline (auto-install if needed) |
| `/auto-workflow` | Run full 8-phase workflow |
| `/load-skills` | Reload skills for current project |
| `/generate-context` | Create PROJECT_CONTEXT from plan |
| `/mem` | Access persistent memory |
| `/plan` | Sequential thinking for complex tasks |

---

## Pipeline Architecture

### The 8-Phase Workflow

Each phase is designed for specific validation and can be customized:

```
Phase 0: DISCOVERY (~5s)
├── Scan codebase structure
├── Identify project type
└── Load relevant skills

Phase 1: CONTEXT (~10s)
├── Recall from memlayer
├── Scan README/CLAUDE.md
├── Check negative cache (past failures)
└── Query context7 for library docs

Phase 2: PLAN (10-30s)
├── Break task into steps
├── Use sequential-thinking
├── Optional: Roundtable with AI models
└── Generate TODO list

Phase 3: SAFETY (~3s)
├── Git handbrake (stash snapshot)
├── Dependency verification
└── Secret detection

Phase 4: EXECUTE (variable)
├── DOING protocol enforcement
├── Sandbox-first execution
├── Progress tracking
└── Error capture

Phase 5: VERIFY (~20s)
├── Lint-gate checks
├── Test execution
├── UI verification (if applicable)
└── Secret-guard scan

Phase 6: REVIEW (~15s)
├── Code review agent
├── Architecture validation
├── Performance check
└── Security audit

Phase 7: COMMIT (~5s)
├── Individual file staging
├── Structured commit message
├── Push to remote
└── Memory save
```

### DOING Protocol

Every action follows this verification pattern:

```
DOING: Edit authentication handler to fix token refresh
EXPECT: Token refresh occurs before expiry with 5-minute buffer
IF WRONG: Token validation logic has race condition
```

This ensures:
- Clear intent before action
- Measurable success criteria
- Diagnostic path if something fails

---

## Installation

### Prerequisites

- **Claude Code CLI** - [Install from Anthropic](https://claude.ai/code)
- **Python 3.10+** - For MCP servers
- **Node.js 18+** - For some MCP servers
- **Git** - For version control integration

### Method 1: Quick Install (Recommended)

```bash
git clone https://github.com/anthropics/claude-reactor.git
cd claude-reactor
claude  # Start Claude Code
/p      # Initialize pipeline
```

### Method 2: Manual Setup

```bash
# Clone repository
git clone https://github.com/anthropics/claude-reactor.git
cd claude-reactor

# Run setup script
chmod +x run.sh
./run.sh init

# Verify installation
./run.sh test
```

### What Gets Installed

The pipeline installer creates symlinks to global resources:

```
.claude/
├── CLAUDE.md      → ~/.claude/CLAUDE.md
├── skills/        → ~/.claude/skills/
├── commands/      → ~/.claude/commands/
├── settings.json  → ~/.claude/settings.json
└── hooks/         (copied, not symlinked)
    ├── pre-tool-use-protocol.sh
    ├── post-compaction-restore.sh
    └── pre-compact-save.sh
```

---

## Configuration

### Model Configuration

Claude Reactor uses the **Claude Code SDK** by default, leveraging native Claude models for optimal performance.

#### Default: Claude Code SDK (Recommended)

No configuration needed - works out of the box with your Claude Code installation.

#### Optional: Alternative Models

For specialized use cases, you can configure alternative models:

```bash
# Use via roundtable (parallel consultation)
mcp__gemini__gemini(prompt="Review this architecture...")
mcp__deepseek__deepseek(prompt="Analyze this code...")

# These are CONSULTATIVE - Claude remains the primary executor
```

#### Optional: Local Models via OpenRouter

For air-gapped environments or cost optimization:

```bash
# Configure in ~/.claude/settings.json
{
  "modelProvider": "openrouter",
  "openrouterApiKey": "your-key",
  "model": "anthropic/claude-3-opus"
}
```

### MCP Server Configuration

Edit `.mcp.json.filtered` to enable/disable servers:

```json
{
  "mcpServers": {
    "unified-orchestrator": {
      "command": "python",
      "args": ["-m", "unified_orchestrator"],
      "enabled": true
    }
  }
}
```

### Hook Configuration

Edit `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": ".*",
        "hooks": [{"command": "echo '{\"continue\": true}'"}]
      }
    ],
    "Stop": [
      {
        "hooks": [{"command": "~/.claude/hooks/session-complete-memory.sh"}]
      }
    ]
  }
}
```

---

## MCP Servers

Claude Reactor integrates 16 MCP servers providing ~150 tools. Each server links to its source repository.

### Core Infrastructure

| Server | Tools | Purpose | Source | Install |
|--------|-------|---------|--------|---------|
| **unified-orchestrator** | 25 | Session management, memory, infrastructure | [GitHub](https://github.com/riotofgeese/unified-orchestrator) | `npm install` |
| **memlayer** | 8 | Project-isolated persistent memory | [GitHub](https://github.com/anthropics/memlayer-mcp) | `pip install memlayer` |
| **code-execution-mode** | 3 | v2.0 sandbox execution (PRIMARY) | [GitHub](https://github.com/anthropics/code-execution-mcp) | `npm install` |
| **ace** | 20 | Code execution with learning playbooks | [GitHub](https://github.com/cyanheads/ace-mcp) | `npm install` |

### Thinking & Planning

| Server | Tools | Purpose | Source | Install |
|--------|-------|---------|--------|---------|
| **sequential-thinking** | 1 | Multi-step planning with revisions | [GitHub](https://github.com/anthropics/sequential-thinking-mcp) | `npx -y @anthropic-ai/mcp-server-sequential-thinking` |
| **code-reasoning** | 1 | Complex problem decomposition | Built-in | Part of sequential-thinking |

### Context & Documentation

| Server | Tools | Purpose | Source | Install |
|--------|-------|---------|--------|---------|
| **context7** | 2 | Up-to-date library documentation | [GitHub](https://github.com/upstash/context7) | `npx -y @upstash/context7-mcp` |

### Browser & Testing

| Server | Tools | Purpose | Source | Install |
|--------|-------|---------|--------|---------|
| **browser-tools** | 15 | Console logs, screenshots, audits | [GitHub](https://github.com/anthropics/mcp-browser-tools) | Chrome extension + server |
| **flowlens** | 7 | Browser flow recording & analysis | [GitHub](https://github.com/AlanJudi/flowlens-mcp) | `pip install flowlens-mcp` |

### AI Models (Roundtable)

| Server | Model | Purpose | Source | Install |
|--------|-------|---------|--------|---------|
| **gemini** | gemini-3-pro-preview | Roundtable consultation | [GitHub](https://github.com/riotofgeese/gemini-mcp) | `npm install && npm run build` |
| **codex** | o4-mini | Code execution agent | [GitHub](https://github.com/openai/codex) | `npm install -g @openai/codex` |
| **deepseek** | deepseek-reasoner | Code analysis | [GitHub](https://github.com/deepseek-ai/deepseek-mcp) | `npm install` |
| **glm** | glm-4.6 | Alternative perspective | [GitHub](https://github.com/THUDM/glm-mcp) | `npm install` |

### Development Tools

| Server | Tools | Purpose | Source | Install |
|--------|-------|---------|--------|---------|
| **serena** | 10 | Semantic code navigation | [GitHub](https://github.com/oramasearch/serena) | `pip install serena-mcp` |
| **fast-port-checker** | 3 | Port availability | Built-in | Native tool |
| **omada-mcp-server** | 15 | Network management | [GitHub](https://github.com/riotofgeese/omada-mcp) | `npm install` |

### Example Configuration

Add to `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "gemini": {
      "command": "node",
      "args": ["/path/to/gemini-mcp/dist/index.js"],
      "env": { "GEMINI_API_KEY": "your-key" }
    },
    "memlayer": {
      "command": "python",
      "args": ["-m", "memlayer.server"],
      "env": { "MEMLAYER_DB_PATH": "~/.claude/memory.db" }
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-sequential-thinking"]
    },
    "code-execution-mode": {
      "command": "node",
      "args": ["/path/to/code-execution-mcp/dist/index.js"]
    }
  }
}
```

**Total: 16 servers, ~150 tools** (optimized to stay under provider limits)


---

## Skills & Commands

### Core Skills (Always Loaded)

```
context-restore     │ Recover session after compaction
context-save        │ Save session before compaction
store-memory        │ Persist information to memlayer
global-pipeline     │ Pipeline orchestration
auto-workflow       │ 8-phase automation
preflight-check     │ Pre-execution validation
task-completion     │ Completion protocol
consult-history     │ Project history lookup
```

### Project-Specific Skills

```yaml
Frontend:
  - dev-browser          # Browser automation
  - sequential-thinking  # Complex UI planning
  - lint-gate           # ESLint/Prettier

Backend:
  - debugging-playbook   # Systematic debugging
  - tdd-enforcer        # Test-driven development
  - api-docs            # OpenAPI generation

DevOps:
  - portmon             # Port monitoring
  - pipeline-health     # CI/CD validation
  - terraform           # IaC management

Documentation:
  - auto-docs           # Auto-generate docs
  - docs-first          # Documentation-driven
  - context7-wrapper    # Library lookups
```

### Command Reference

| Command | Arguments | Description |
|---------|-----------|-------------|
| `/p` | none | Initialize pipeline |
| `/auto-workflow` | none | Run full 8-phase workflow |
| `/load-skills` | none | Reload project-specific skills |
| `/generate-context` | `@plan.md` | Generate PROJECT_CONTEXT |
| `/archive-context` | none | Archive ephemeral context |
| `/mem` | `ID` | Recall specific memory |
| `/plan` | `task` | Sequential thinking |
| `/review` | none | Code review workflow |
| `/work` | `branch` | Git worktree isolation |

---

## Hooks System

### Available Hook Types

| Hook | Trigger | Use Case |
|------|---------|----------|
| `PreToolUse` | Before any tool | DOING protocol, validation |
| `PostToolUse` | After any tool | Progress tracking, logging |
| `Stop` | Session end | Memory save, cleanup |
| `PreCompact` | Before compaction | Context preservation |
| `PostCompact` | After compaction | Context restoration |

### Hook Output Format

All hooks MUST output valid JSON:

```json
{"continue": true}
```

or

```json
{"continue": false, "message": "Blocked: reason"}
```

### Installed Hooks

```
.claude/hooks/
├── pre-tool-use-protocol.sh   # DOING protocol enforcement
├── post-compaction-restore.sh # Context recovery
└── pre-compact-save.sh        # Context preservation
```

### Creating Custom Hooks

```bash
#!/bin/bash
# ~/.claude/hooks/my-custom-hook.sh

TOOL_NAME="${CLAUDE_TOOL_NAME:-unknown}"

if [[ "$TOOL_NAME" == "Bash" ]]; then
    # Custom logic for Bash commands
    echo "Processing Bash command..." >&2
fi

# Required: Output JSON
echo '{"continue": true}'
```

---

## Memory System

### Memory Hierarchy

```
┌────────────────────────────────────────────────────────────┐
│ L1: Session Context                                         │
│     └── Current conversation, tool results, thinking        │
├────────────────────────────────────────────────────────────┤
│ L2: Project Memory (memlayer)                               │
│     └── Task completions, errors, decisions                 │
│     └── Per-project isolation                               │
├────────────────────────────────────────────────────────────┤
│ L3: Infrastructure                                          │
│     └── Servers, databases, connection strings              │
│     └── Deploy commands, SSH details                        │
├────────────────────────────────────────────────────────────┤
│ L4: Global Facts                                            │
│     └── User preferences, patterns                          │
│     └── Cross-project learnings                             │
└────────────────────────────────────────────────────────────┘
```

### Memory Commands

```python
# Save to memory
mcp__memlayer__remember(
    content="## Task: Fix authentication\n\n### Problem...",
    metadata={"category": "implementation", "project": "my-app"}
)

# Recall from memory
mcp__memlayer__recall(query="authentication", limit=5)

# Session checkpoint
mcp__unified-orchestrator__session_checkpoint(
    summary="Implemented OAuth2 flow",
    achievements=["Added refresh token", "Fixed CORS"],
    pending_tasks=["Add rate limiting"]
)

# Full session restore
mcp__unified-orchestrator__session_restore(
    include_infrastructure=True,
    include_tasks=True,
    auto_detect_project=True
)
```

### Memory Best Practices

**DO use detailed documentation:**

```markdown
## Task: Fix /logs route

### Problem Description
The /logs route was returning 404 after deployment

### Root Cause Analysis
Route was registered before middleware, causing auth bypass

### Files Modified
#### /src/routes/logs.py
**Line 15 - Route registration:**
```python
# BEFORE:
app.route("/logs")

# AFTER:
app.route("/logs", middleware=[auth_required])
```

### Verification
curl -X GET https://api.example.com/logs -H "Authorization: Bearer $TOKEN"
# Returns 200 with log data
```

**DON'T use vague summaries:**
```
Fixed the logs route  # BAD - no context for future debugging
```

---

## Advanced Usage

### Roundtable Consultation

For complex decisions, consult multiple AI models:

```python
# Parallel consultation (non-blocking)
gemini_result = mcp__gemini__gemini(
    prompt="Review this architecture for scalability concerns"
)

# Continue conversation
mcp__gemini__gemini-reply(
    conversationId=gemini_result.conversationId,
    prompt="What about the database design?"
)
```

### Custom Pipeline Phases

Extend the 8-phase workflow:

```python
# In your CLAUDE.md or skill file
## Custom Phase: SECURITY_SCAN

After VERIFY phase, run security scanning:
1. Check for hardcoded secrets
2. Scan dependencies for vulnerabilities
3. Validate input sanitization
4. Review authentication flows
```

### Project Context Locking

Lock architectural decisions during implementation:

```bash
# Generate context from plan
/generate-context @architecture-plan.md

# This creates .claude/skills/PROJECT_CONTEXT.md
# All subsequent work is constrained by these decisions

# When done, archive it
/archive-context
```

### Git Worktree Isolation

Work on experimental features safely:

```bash
/work feature/new-auth

# Creates isolated worktree
# All changes isolated from main branch
# Easy cleanup if experiment fails
```

---

## Troubleshooting

### Common Issues

#### Pipeline Not Initializing

```bash
# Check symlinks
ls -la .claude/

# Reinstall pipeline
/home/crogers2287/.claude/install-pipeline-enhanced.sh $(pwd)
```

#### Memory Not Recalling

```bash
# Check memlayer is running
ps aux | grep memlayer

# Manual recall
mcp__memlayer__recall(query="recent work", limit=10)
```

#### Tool Limit Exceeded

```bash
# Check tool count
cat .mcp.json.filtered | jq '.mcpServers | length'

# Should be ~16 servers (~150 tools)
# Disable unused servers if needed
```

#### Hooks Not Running

```bash
# Check hook is executable
chmod +x ~/.claude/hooks/your-hook.sh

# Test hook manually
~/.claude/hooks/your-hook.sh

# Should output: {"continue": true}
```

#### Context Lost After Compaction

```bash
# Manual restore
mcp__unified-orchestrator__session_restore()

# Or use skill
/context-restore
```

### Debug Mode

Enable verbose logging:

```bash
# Set environment variable
export CLAUDE_DEBUG=1

# Check logs
tail -f /tmp/claude-hooks.log
```

---

## Project Structure

```
claude-reactor/
├── .claude/                    # Claude Code configuration
│   ├── CLAUDE.md              → ~/.claude/CLAUDE.md
│   ├── skills/                → ~/.claude/skills/
│   ├── commands/              → ~/.claude/commands/
│   ├── settings.json          → ~/.claude/settings.json
│   └── hooks/                  # Project-specific hooks
│       ├── pre-tool-use-protocol.sh
│       ├── post-compaction-restore.sh
│       └── pre-compact-save.sh
├── .mcp.json                  → .mcp.json.filtered
├── .mcp.json.filtered          # Active MCP configuration
├── docs/                       # Documentation
│   ├── INDEX.md               # Documentation navigation
│   ├── ARCHITECTURE.md        # System architecture deep dive
│   ├── SKILLS.md              # 53 skills reference
│   ├── AGENTS.md              # 60+ agent personas
│   ├── COMMANDS.md            # 29 slash commands
│   ├── HOOKS.md               # Hook system configuration
│   ├── MCP_INTEGRATION.md     # 16 MCP servers
│   ├── WORKFLOW_SYSTEM.md     # 8-phase pipeline
│   ├── AGENTIC_SETUP.md       # Setup guide
│   ├── PIPELINE.md            # Pipeline internals
│   ├── INSTALL.md             # Installation details
│   └── INTEGRATIONS.md        # External integrations
├── mcp/                        # MCP server configs
│   └── reactor.toml
├── run.sh                      # Setup script
├── README.md                   # This file
├── LICENSE                     # MIT License
└── CHANGELOG.md               # Version history
```

---

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md).

### Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/claude-reactor.git
cd claude-reactor

# Create feature branch
git checkout -b feature/your-feature

# Make changes and test
./run.sh test

# Submit PR
```

### Areas for Contribution

- New MCP server integrations
- Additional skills and agents
- Documentation improvements
- Bug fixes and optimizations
- Example workflows

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- Built with [Claude Code](https://claude.ai/code) by Anthropic
- Powered by the Model Context Protocol (MCP)
- Inspired by modern DevOps practices

---

<div align="center">

**[Documentation](docs/) | [Issues](https://github.com/anthropics/claude-reactor/issues) | [Discussions](https://github.com/anthropics/claude-reactor/discussions)**

Made with Claude Opus 4.5

</div>
