# Architecture Overview

## System Architecture

Claude Reactor is built on a layered architecture that transforms Claude Code into a production-ready development environment.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACE LAYER                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Claude CLI  │  │   /slash    │  │   Hooks     │  │   Skills    │        │
│  │  Terminal   │  │  Commands   │  │   System    │  │   System    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────────────────────┤
│                           ORCHESTRATION LAYER                                │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         8-Phase Pipeline                               │  │
│  │  DISCOVER → CONTEXT → PLAN → SAFETY → EXECUTE → VERIFY → REVIEW → COMMIT │
│  └───────────────────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐  │
│  │   Protocol Engine   │  │   Memory Manager    │  │   Context Router    │  │
│  │   (DOING/EXPECT)    │  │   (L1-L4 Hierarchy) │  │   (Project Detect)  │  │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────────────────────┤
│                              MCP SERVER LAYER                                │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │unified- │ │memlayer │ │  code-  │ │   ace   │ │sequen-  │ │context7 │   │
│  │orchestr │ │         │ │  exec   │ │         │ │  tial   │ │         │   │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘   │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │browser- │ │flowlens │ │ gemini  │ │deepseek │ │  glm    │ │ serena  │   │
│  │  tools  │ │         │ │         │ │         │ │         │ │         │   │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘   │
├─────────────────────────────────────────────────────────────────────────────┤
│                            PERSISTENCE LAYER                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐  │
│  │   Project Memory    │  │   Infrastructure    │  │   Global Facts      │  │
│  │   (memlayer DB)     │  │   (unified-orch)    │  │   (~/.claude/)      │  │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────────────────────┤
│                            EXECUTION LAYER                                   │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                    code-execution-mode Sandbox                          ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    ││
│  │  │   Python    │  │    File     │  │    Shell    │  │     MCP     │    ││
│  │  │   Runtime   │  │   System    │  │   Commands  │  │   Proxies   │    ││
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    ││
│  └─────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Component Deep Dive

### 1. User Interface Layer

#### Claude CLI Terminal
- Primary interaction point
- Receives user prompts
- Displays responses and progress
- Handles input/output streaming

#### Slash Commands (`/command`)
- 27 registered commands
- Defined in `~/.claude/commands/*.md`
- Markdown-based with frontmatter config
- Support arguments and tool restrictions

```markdown
---
description: Initialize pipeline
allowed-tools: Bash(ls:*), Read, Glob
---

# Command content here...
```

#### Hooks System
- Event-driven execution
- 5 hook types (PreToolUse, PostToolUse, Stop, PreCompact, PostCompact)
- JSON output required
- Configurable timeouts

#### Skills System
- 53 reusable modules
- Dynamic loading based on project type
- Stored in `~/.claude/skills/`
- Support for project-specific overrides

---

### 2. Orchestration Layer

#### 8-Phase Pipeline

```
┌──────────────────────────────────────────────────────────────────────┐
│                         PIPELINE FLOW                                 │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐          │
│   │DISCOVER │───▶│ CONTEXT │───▶│  PLAN   │───▶│ SAFETY  │          │
│   │  ~5s    │    │  ~10s   │    │ 10-30s  │    │  ~3s    │          │
│   └─────────┘    └─────────┘    └─────────┘    └─────────┘          │
│        │                                            │                │
│        │         ┌──────────────────────────────────┘                │
│        │         │                                                   │
│        │         ▼                                                   │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐          │
│   │ COMMIT  │◀───│ REVIEW  │◀───│ VERIFY  │◀───│ EXECUTE │          │
│   │  ~5s    │    │  ~15s   │    │  ~20s   │    │variable │          │
│   └─────────┘    └─────────┘    └─────────┘    └─────────┘          │
│        │                                                             │
│        ▼                                                             │
│   ┌─────────┐                                                        │
│   │ MEMORY  │  ←── Persistent storage of results                     │
│   └─────────┘                                                        │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

#### Protocol Engine (DOING/EXPECT/IF WRONG)

Every action is wrapped in a verification protocol:

```
DOING: [Precise description of action]
EXPECT: [Measurable expected outcome]
IF WRONG: [Diagnostic path if outcome differs]
```

This enables:
- **Auditability**: Every action is logged with intent
- **Rollback**: Clear expectations enable automatic recovery
- **Debugging**: IF WRONG provides immediate diagnostic direction

#### Memory Manager

Four-tier hierarchy for context persistence:

| Level | Name | Scope | Persistence | Use Case |
|-------|------|-------|-------------|----------|
| L1 | Session | Conversation | Until close | Working memory |
| L2 | Project | Project folder | Permanent | Task history |
| L3 | Infrastructure | Environment | Permanent | Server configs |
| L4 | Global | User account | Permanent | Preferences |

#### Context Router

Automatically detects project type and loads appropriate resources:

```python
# Detection logic (simplified)
if 'package.json' in files or 'tsconfig.json' in files:
    project_type = 'frontend'
    load_skills(['dev-browser', 'lint-gate', 'sequential-thinking'])
elif 'requirements.txt' in files or 'pyproject.toml' in files:
    project_type = 'backend'
    load_skills(['debugging-playbook', 'tdd-enforcer'])
elif 'Dockerfile' in files:
    project_type = 'devops'
    load_skills(['portmon', 'pipeline-health-check'])
```

---

### 3. MCP Server Layer

#### Server Categories

```
┌─────────────────────────────────────────────────────────────────────┐
│                        MCP SERVER TOPOLOGY                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  CORE INFRASTRUCTURE          THINKING & PLANNING                    │
│  ┌─────────────────────┐     ┌─────────────────────┐                │
│  │ unified-orchestrator│     │ sequential-thinking │                │
│  │ (25 tools)          │     │ (1 tool)            │                │
│  ├─────────────────────┤     ├─────────────────────┤                │
│  │ memlayer           │     │ code-reasoning      │                │
│  │ (8 tools)          │     │ (1 tool)            │                │
│  ├─────────────────────┤     └─────────────────────┘                │
│  │ code-execution-mode │                                            │
│  │ (3 tools) PRIMARY   │     CONTEXT & DOCS                         │
│  ├─────────────────────┤     ┌─────────────────────┐                │
│  │ ace                │     │ context7            │                │
│  │ (20 tools)         │     │ (2 tools)           │                │
│  └─────────────────────┘     └─────────────────────┘                │
│                                                                      │
│  BROWSER & TESTING            AI MODELS                              │
│  ┌─────────────────────┐     ┌─────────────────────┐                │
│  │ browser-tools      │     │ gemini              │                │
│  │ (15 tools)         │     │ (2 tools)           │                │
│  ├─────────────────────┤     ├─────────────────────┤                │
│  │ flowlens           │     │ deepseek            │                │
│  │ (7 tools)          │     │ (2 tools)           │                │
│  └─────────────────────┘     ├─────────────────────┤                │
│                               │ glm                │                │
│  DEV TOOLS                    │ (2 tools)          │                │
│  ┌─────────────────────┐     └─────────────────────┘                │
│  │ serena (10 tools)  │                                            │
│  │ codex (2 tools)    │                                            │
│  │ fast-port (3 tools)│                                            │
│  │ omada (15 tools)   │                                            │
│  └─────────────────────┘                                            │
│                                                                      │
│  TOTAL: ~150 tools (under 200 provider limit)                       │
└─────────────────────────────────────────────────────────────────────┘
```

#### Server Communication

```
┌──────────────┐     JSON-RPC      ┌──────────────┐
│  Claude CLI  │◀────────────────▶│  MCP Server  │
└──────────────┘                   └──────────────┘
       │                                  │
       │ Tool Call                        │ Execute
       ▼                                  ▼
┌──────────────┐                   ┌──────────────┐
│ Tool Schema  │                   │   Handler    │
│  Validation  │                   │   Function   │
└──────────────┘                   └──────────────┘
```

---

### 4. Persistence Layer

#### Project Memory (memlayer)

```sql
-- Conceptual schema
memories (
  id INTEGER PRIMARY KEY,
  project_id TEXT,
  content TEXT,
  metadata JSON,
  created_at TIMESTAMP,
  embedding VECTOR  -- For semantic search
)
```

#### Infrastructure Storage

```json
{
  "servers": {
    "prod-api": {
      "host": "api.example.com",
      "port": 443,
      "ssh_user": "deploy",
      "deploy_cmd": "git pull && pm2 restart all"
    }
  },
  "databases": {
    "main-postgres": {
      "host": "db.example.com",
      "port": 5432,
      "name": "production"
    }
  }
}
```

#### Global Configuration

```
~/.claude/
├── CLAUDE.md           # Global instructions
├── settings.json       # Permissions, hooks, plugins
├── skills.json         # Skill manifest
├── mcp.json           # MCP server definitions
└── projects/          # Per-project configs
    ├── my-app/
    └── another-project/
```

---

### 5. Execution Layer

#### code-execution-mode Sandbox

The primary execution environment for v2.0:

```
┌─────────────────────────────────────────────────────────────────────┐
│                     SANDBOX ENVIRONMENT                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  /workspace (mounted from project_path)                              │
│  ├── Full read/write access                                         │
│  ├── Persistent changes                                             │
│  └── Git operations supported                                       │
│                                                                      │
│  Python Runtime                                                      │
│  ├── Standard library                                               │
│  ├── pathlib, subprocess, json                                      │
│  ├── MCP client proxies (mcp_memlayer, mcp_context7, etc.)         │
│  └── Custom modules via pip                                         │
│                                                                      │
│  Shell Access                                                        │
│  ├── subprocess.run() for commands                                  │
│  ├── Git operations                                                 │
│  └── Build tools (npm, cargo, etc.)                                 │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

#### Token Efficiency Comparison

```
┌────────────────────────────────────────────────────────────────────┐
│                    TOKEN USAGE COMPARISON                           │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  v1.0 Approach (5 tool calls)                                      │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │ Read(file)           → 500 tokens (file content)        │       │
│  │ Grep(pattern)        → 300 tokens (matches)             │       │
│  │ Edit(file, old, new) → 700 tokens (confirmation)        │       │
│  │ Bash(git status)     → 200 tokens (output)              │       │
│  │ Bash(git commit)     → 300 tokens (output)              │       │
│  │                                                         │       │
│  │ TOTAL: ~2,000-3,000 tokens                              │       │
│  └─────────────────────────────────────────────────────────┘       │
│                                                                     │
│  v2.0 Approach (1 sandbox call)                                    │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │ run_python(code='''                                     │       │
│  │   content = Path("/workspace/file").read_text()         │       │
│  │   # Process in sandbox (no token cost)                  │       │
│  │   modified = content.replace(old, new)                  │       │
│  │   Path("/workspace/file").write_text(modified)          │       │
│  │   subprocess.run(["git", "commit", "-m", "msg"])        │       │
│  │   print(json.dumps({"status": "done"}))                 │       │
│  │ ''')                                                    │       │
│  │                                                         │       │
│  │ TOTAL: ~200-400 tokens (summary only)                   │       │
│  └─────────────────────────────────────────────────────────┘       │
│                                                                     │
│  SAVINGS: 70-90% token reduction                                   │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### Request Processing

```
User Prompt
     │
     ▼
┌────────────────┐
│  Parse Intent  │
└────────────────┘
     │
     ▼
┌────────────────┐     ┌────────────────┐
│ Check Hooks    │────▶│ PreToolUse     │
│ (PreToolUse)   │     │ Hook Scripts   │
└────────────────┘     └────────────────┘
     │
     ▼
┌────────────────┐
│ Load Skills    │
│ (Project Type) │
└────────────────┘
     │
     ▼
┌────────────────┐     ┌────────────────┐
│ Recall Memory  │────▶│ memlayer       │
│ (Context)      │     │ MCP Server     │
└────────────────┘     └────────────────┘
     │
     ▼
┌────────────────┐     ┌────────────────┐
│ Execute Plan   │────▶│ code-execution │
│ (8 Phases)     │     │ -mode Sandbox  │
└────────────────┘     └────────────────┘
     │
     ▼
┌────────────────┐     ┌────────────────┐
│ Check Hooks    │────▶│ PostToolUse    │
│ (PostToolUse)  │     │ Hook Scripts   │
└────────────────┘     └────────────────┘
     │
     ▼
┌────────────────┐     ┌────────────────┐
│ Save Memory    │────▶│ memlayer       │
│ (Results)      │     │ MCP Server     │
└────────────────┘     └────────────────┘
     │
     ▼
Response to User
```

### Memory Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      MEMORY LIFECYCLE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Session Start                                                   │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────┐                                            │
│  │ session_restore │  ←── Restore from L2/L3/L4                 │
│  └─────────────────┘                                            │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────┐                                            │
│  │  Work Session   │  ←── L1 accumulates context                │
│  └─────────────────┘                                            │
│       │                                                          │
│       ├─────────────────────────┐                               │
│       │                         │                               │
│       ▼                         ▼                               │
│  ┌─────────────────┐     ┌─────────────────┐                   │
│  │ Task Complete   │     │  Compaction     │                   │
│  │ save to L2      │     │  save to L2     │                   │
│  └─────────────────┘     └─────────────────┘                   │
│       │                         │                               │
│       ▼                         ▼                               │
│  ┌─────────────────┐     ┌─────────────────┐                   │
│  │  Continue or    │     │   L1 cleared    │                   │
│  │  Session End    │     │   L2-L4 intact  │                   │
│  └─────────────────┘     └─────────────────┘                   │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────┐                                            │
│  │ session_complete│  ←── Final L2 save                         │
│  └─────────────────┘                                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Configuration Files

### .mcp.json.filtered

```json
{
  "mcpServers": {
    "unified-orchestrator": {
      "command": "python",
      "args": ["-m", "unified_orchestrator"],
      "env": {"PROJECT_PATH": "."},
      "enabled": true
    },
    "memlayer": {
      "command": "bun",
      "args": ["run", "start-server"],
      "cwd": "/path/to/memlayer",
      "enabled": true
    }
    // ... 14 more servers
  }
}
```

### settings.json

```json
{
  "permissions": {
    "allow": [
      "Bash(grep:*)",
      "Bash(ln:*)",
      "mcp__unified-orchestrator__session_restore"
    ],
    "deny": []
  },
  "enableAllProjectMcpServers": true,
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
  },
  "enabledPlugins": {
    "feature-dev@claude-plugins-official": true,
    "hookify@claude-plugins-official": true,
    "code-review@claude-plugins-official": true
  }
}
```

### skills.json

```json
{
  "_meta": {
    "version": "1.0.0",
    "last_updated": "2025-12-21"
  },
  "skills": {
    "context-restore": {
      "tags": ["core", "context"],
      "priority": "critical",
      "always_load": true
    }
    // ... 45+ more skills
  },
  "project_detection": {
    "frontend": {
      "files": ["package.json", "tsconfig.json"],
      "load_skills": ["dev-browser", "lint-gate"]
    }
    // ... more project types
  }
}
```

---

## Security Model

### Permission Boundaries

```
┌─────────────────────────────────────────────────────────────────┐
│                    PERMISSION HIERARCHY                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  USER LEVEL (settings.json)                                     │
│  ├── Allow: Specific tool patterns                              │
│  ├── Deny: Blocked operations                                   │
│  └── Ask: Require confirmation                                  │
│                                                                  │
│  PROJECT LEVEL (.claude/settings.local.json)                    │
│  ├── Override user permissions                                  │
│  └── Project-specific restrictions                              │
│                                                                  │
│  HOOK LEVEL (hook scripts)                                      │
│  ├── Validate operations pre-execution                          │
│  └── Block dangerous patterns                                   │
│                                                                  │
│  SANDBOX LEVEL (code-execution-mode)                            │
│  ├── Isolated execution environment                             │
│  ├── Controlled filesystem access (/workspace)                  │
│  └── Network restrictions (if configured)                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Secret Protection

- **secret-guard skill**: Scans for credentials before commit
- **Pre-commit hooks**: Block files with detected secrets
- **Environment isolation**: Secrets in env vars, not code

---

## Performance Considerations

### Token Optimization

| Strategy | Savings | Implementation |
|----------|---------|----------------|
| v2.0 Sandbox | 70-90% | All operations in single call |
| Skill Loading | ~84% | Only load relevant skills |
| MCP Filtering | ~50% | 16 vs 50+ servers |
| Memory Summaries | ~60% | Store summaries, not raw data |

### Latency Optimization

| Phase | Target | Strategy |
|-------|--------|----------|
| DISCOVER | <5s | Cached project detection |
| CONTEXT | <10s | Parallel memory/doc fetch |
| EXECUTE | Variable | Sandbox batching |
| COMMIT | <5s | Streamlined git ops |

---

## Extensibility

### Adding New Skills

```markdown
# ~/.claude/skills/my-skill.md
---
name: my-skill
description: What this skill does
---

# Skill Name

## When to Use
- Trigger conditions

## Process
1. Step one
2. Step two

## Example
\`\`\`python
# Code example
\`\`\`
```

### Adding New Commands

```markdown
# ~/.claude/commands/my-command.md
---
description: Short description
allowed-tools: Read, Write, Bash(git:*)
---

# /my-command

## Usage
/my-command [arg]

## Behavior
What the command does...
```

### Adding New Hooks

```bash
#!/bin/bash
# ~/.claude/hooks/my-hook.sh

# Your logic here

# Required output
echo '{"continue": true}'
```

---

## Deployment Patterns

### Single Developer

```
Local Machine
├── Claude Code CLI
├── ~/.claude/ (global config)
└── ~/projects/
    ├── project-a/ (.claude/ symlinks)
    └── project-b/ (.claude/ symlinks)
```

### Team Deployment

```
Shared Config (git repo)
├── .claude/
│   ├── skills/ (team skills)
│   ├── commands/ (team commands)
│   └── CLAUDE.md (team standards)
└── Each developer clones & symlinks
```

### CI/CD Integration

```yaml
# .github/workflows/claude-review.yml
- name: Claude Code Review
  run: |
    claude --prompt "Review this PR for issues"
    # Uses pipeline phases for validation
```
