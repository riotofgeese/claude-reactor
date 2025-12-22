# Claude Code Workflow System - Complete Documentation (v2.0 - Code Execution Enhanced)

## Table of Contents
1. [System Overview](#system-overview)
2. [Core Principles](#core-principles)
3. [Workflow Phases](#workflow-phases)
4. [Skills System](#skills-system)
5. [MCP Integration](#mcp-integration)
6. [Memory Hierarchy](#memory-hierarchy)
7. [Tools & Components](#tools--components)
8. [Installation & Setup](#installation--setup)
9. [Usage Examples](#usage-examples)
10. [Integration with External Tools](#integration-with-external-tools)
11. [Troubleshooting](#troubleshooting)
12. [Best Practices](#best-practices)

## System Overview

The Claude Code Workflow System is a comprehensive development environment that combines structured thinking, intelligent tooling, and **sandboxed code execution**. It orchestrates specialized tools through a unified workflow where the model acts as an **architect and engineer**, writing executable scripts to interact with systems rather than making individual tool calls.

### Key Components
- **Workflow Engine**: 8-phase structured development process
- **Code Orchestration**: Model writes Python scripts to chain MCP tools (vs. chat-based tool calling)
- **Sandboxed Runtime**: Secure execution environment for logic and data processing
- **Memory System**: 4-tier persistent memory for context preservation
- **Protocol Enforcement**: DOING/EXPECTED/IF WRONG methodology

### The Token Reduction Principle
**v1.0 (Tool Calling)**: Each MCP call = separate tool invocation in chat context (~500-2000 tokens each)
**v2.0 (Code Execution)**: One script orchestrates N calls, only results returned (~98% reduction)

## Core Principles

### 1. The "Orchestrate, Don't Call" Principle
*Never manually call 5 tools when you can write 1 script to call them all. Logic belongs in code, not in the chat context.*

**Before (v1.0 - Token Heavy)**:
```
# 5 separate tool calls, each consuming context
mcp__stripe__get_customer(id="cus_123")  # ~800 tokens
mcp__postgres__query(sql="SELECT...")    # ~600 tokens
mcp__slack__send_message(...)            # ~500 tokens
# Total: ~2000+ tokens in context
```

**After (v2.0 - Token Efficient)**:
```python
# One script, results only
from mcp_client import stripe, postgres, slack

user = stripe.get_customer(id="cus_123")
usage = postgres.query("SELECT * FROM usage WHERE id=%s", (user.id,))
if usage['total'] > user['limit']:
    slack.send(f"Alert: {user.id} over limit")
print(f"Result: {'OVER' if usage['total'] > user['limit'] else 'OK'}")
# Total: ~200 tokens (result only)
```

### 2. Reality Gap Principle
*"Reality doesn't care about your model. The gap between model and reality is where all failures live."*

### 3. Data Triage Protocol
Intermediate data (e.g., full CSVs, API logs) **STAYS** in the sandbox. Only bring **Insights** back to the chat context.

| Data Type | Location | Bring to Chat? |
|-----------|----------|----------------|
| Raw API responses | Sandbox | NO |
| Full datasets | Sandbox | NO |
| Calculated results | Sandbox → Chat | YES (summary only) |
| Error messages | Sandbox → Chat | YES |
| Final insights | Sandbox → Chat | YES |

### 4. DOING Protocol (CRITICAL)
Before EVERY action:
```
DOING: [action]
EXPECT: [predicted outcome]
IF WRONG: [what that means]
```

### 5. Progressive Disclosure
Instead of loading 100+ tool schemas upfront, discover them on demand:
```bash
# Only load what you need
ls ~/mcp-servers/stripe/    # See available tools
cat ~/mcp-servers/stripe/tools.py  # Read specific interface
```

## Workflow Phases

### The Complete 8-Phase Workflow

#### Phase 0: AUTO-WORKFLOW (Default)
Invoke the `auto-workflow` skill FIRST:
```bash
auto-workflow skill
```

This automatically runs:
1. **Tool Discovery**: Scans `~/mcp-servers/` to find relevant tool definitions
2. **Context Search**: Checks negative-cache and project docs
3. **Planning**: Generates a sequential-thinking plan
4. **Roundtable Review**: codex + gemini validate approach

Skip to Phase 4 (SAFETY) after auto-workflow completes.

#### Phase 1: PREFLIGHT
Environment validation and preparation:
```bash
preflight-check skill
```
- Verify toolchain versions and git state
- **Launch Sandbox**: Ensure the Code Execution Environment is active
- Confirm dependencies installed

#### Phase 2: DISCOVERY (Progressive Disclosure)
Instead of loading 100+ tool schemas, discover them on demand:
```bash
# List available MCP server definitions
ls -R ~/mcp-servers/

# Read specific tool interfaces
cat ~/mcp-servers/github/tools.py
cat ~/mcp-servers/postgres/tools.py

# Or use the tool-explorer skill
tool-explorer skill "find database tools"
```

#### Phase 3: PLAN
Structured planning and validation:
```bash
# Complex tasks: Use structured reasoning
sequential-thinking MCP

# Plan the Orchestration Script
"I will write a script that:
 1. Fetches the user from Stripe (MCP)
 2. Checks their usage in Postgres (MCP)
 3. Calculates the difference using Pandas
 4. Returns only the variance."

# Review with AI
codex OR gemini → "Review this orchestration plan"
```

#### Phase 4: SAFETY
Risk mitigation before execution:
```bash
# Git snapshot for rollback
git-handbrake skill → SNAP=$(git stash create "handbrake-$(date +%s)")

# Dependency check
dependency-check skill
```

#### Phase 5: ORCHESTRATE & EXECUTE (The "Code Mode")
**Do not make individual tool calls. Write a script.**

The Pattern:
1. **Draft**: Write a Python script importing `mcp_client`
2. **Execute**: Run script in the sandbox
3. **Refine**: If it fails, read stderr, fix script, rerun

```python
# Example orchestration script
from mcp_client import stripe, postgres, memlayer

def check_user_status():
    """Orchestrate multiple MCP calls in one script."""
    # Step 1: Get user from Stripe
    user = stripe.get_customer(id="cus_123")

    # Step 2: Query usage from Postgres
    usage = postgres.query(
        "SELECT SUM(amount) as total FROM usage WHERE user_id = %s",
        (user['id'],)
    )

    # Step 3: Logic happens HERE, not in the LLM context
    variance = usage['total'] - user['limit']
    status = "OVER" if variance > 0 else "OK"

    # Step 4: Save insight to memory (also via MCP)
    if status == "OVER":
        memlayer.remember(
            content=f"User {user['id']} exceeded limit by {variance}",
            metadata={"type": "alert", "severity": "high"}
        )

    # Step 5: Return ONLY the insight, not raw data
    print(f"STATUS: {status}, VARIANCE: {variance}")

check_user_status()
```

**Key Benefits**:
- Raw API data never enters chat context
- Logic computed in sandbox, not by LLM
- Only final result returned (~50 tokens vs ~2000)

#### Phase 6: VERIFY
Quality assurance and testing:
```bash
# Lint gate
lint-gate skill

# Run tests via sandbox
run_python "pytest tests/test_auth.py"

# Security scan
secret-guard skill
```

#### Phase 7: RECOVERY (If Failed)
Error handling and rollback:
```bash
# Check typed recovery patterns
failure-playbooks skill

# Log failure to memory
negative-cache skill

# Rollback
git checkout -- . && git stash apply $SNAP
```

#### Phase 8: COMMIT
Success documentation and cleanup:
```bash
# Save to memory (Lessons Learned)
smart_remember → task_completion

# Add files individually (NEVER git add .)
git add FILE1 FILE2
```

## Skills System

Skills are composable tools that automate common workflow tasks.

### Core Skills Matrix

| Skill | Purpose | Integration | Token Impact |
|-------|---------|-------------|--------------|
| **auto-workflow** | Orchestrates Discovery→Plan→Review | **START HERE** | Reduces 5+ calls to 1 |
| **tool-explorer** | Navigate ~/mcp-servers to find tools | Sandbox | Avoids schema loading |
| preflight-check | Environment + sandbox validation | System checks | Early failure detection |
| git-handbrake | Snapshot for rollback | Git | Safety net |
| lint-gate | Pre-LLM linting filter | Linters | Prevents wasted iterations |
| tdd-enforcer | Write failing test first | Test frameworks | Focused development |
| negative-cache | Check past failures | Memlayer | Avoid repeated mistakes |
| dependency-check | Validate imports exist | Package managers | Early error detection |
| secret-guard | Scan for credentials | Security | Pre-commit safety |
| failure-playbooks | Typed error recovery | Error patterns | Fast resolution |

### Skill Implementation (v2.0 Pattern)
Skills now emphasize orchestration over individual calls:

```markdown
---
description: Tool discovery and interface lookup
---

<system-reminder>
INSTEAD of loading all tool schemas, progressively discover:

1. List servers: ls ~/mcp-servers/
2. Find relevant: grep -r "keyword" ~/mcp-servers/
3. Read interface: cat ~/mcp-servers/{server}/tools.py
4. Use in script: from mcp_client import {server}

This avoids 10,000+ tokens of schema loading.
</system-reminder>
```

## MCP Integration

### The Code Execution Architecture

The system uses a **Code Execution Server (Sandbox)** that wraps all other MCP servers.

```
┌─────────────────────────────────────────────────────────┐
│                    CHAT CONTEXT                         │
│  (Minimal: instructions, results, insights only)        │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│               CODE EXECUTION SANDBOX                    │
│  ┌─────────────────────────────────────────────────┐   │
│  │  from mcp_client import stripe, postgres, slack │   │
│  │                                                 │   │
│  │  # All logic runs HERE                          │   │
│  │  user = stripe.get_customer(...)                │   │
│  │  data = postgres.query(...)                     │   │
│  │  result = calculate(user, data)                 │   │
│  │  print(result)  # Only this goes to chat        │   │
│  └─────────────────────────────────────────────────┘   │
│                          │                              │
│              ┌───────────┼───────────┐                  │
│              ▼           ▼           ▼                  │
│         ┌────────┐ ┌──────────┐ ┌────────┐             │
│         │ Stripe │ │ Postgres │ │ Slack  │  ... MCPs   │
│         └────────┘ └──────────┘ └────────┘             │
└─────────────────────────────────────────────────────────┘
```

### 1. The Sandbox (Execution Environment)
- **Role**: A secure container where Python code runs
- **Capabilities**:
  - Full filesystem access (within sandbox)
  - pip installation for data analysis libs (pandas, numpy)
  - Network Access: Only to other MCP servers via the `mcp_client` bridge

### 2. The mcp_client Bridge
All MCP tools are exposed as Python libraries inside the sandbox.

**Syntax**: `from mcp_client import [server_name]`
**Usage**: `[server_name].[tool_name](args)`

```python
from mcp_client import unified_orchestrator, memlayer, context7, serena

# Memory operations
unified_orchestrator.smart_remember(
    event_type="task_completion",
    content={"task": "migration", "outcome": "success"}
)

# Documentation lookup
docs = context7.get_library_docs(
    library_id="/vercel/next.js",
    topic="app-router"
)

# Code navigation
symbols = serena.find_symbol(
    name_path_pattern="authenticate",
    relative_path="src/"
)
```

### 3. Core MCP Servers (Available via mcp_client)

| Server | Import | Key Methods |
|--------|--------|-------------|
| unified-orchestrator | `unified_orchestrator` | `smart_remember()`, `session_restore()`, `save_infrastructure()` |
| memlayer | `memlayer` | `remember()`, `recall()`, `get_stats()` |
| context7 | `context7` | `resolve_library_id()`, `get_library_docs()` |
| serena | `serena` | `find_symbol()`, `replace_symbol_body()`, `get_symbols_overview()` |
| ace | `ace` | `code_execute()`, `code_retry_start()`, `get_strategies()` |
| sequential-thinking | `sequential_thinking` | `think()` |
| codex | `codex` | `query()`, `reply()` |
| gemini | `gemini` | `query()`, `reply()` |
| deepseek | `deepseek` | `query()`, `reply()` |

## Memory Hierarchy

### Tier 1: Sandbox State (Ephemeral)
- **What**: Variables, temporary files, dataframes inside the running Python session
- **Policy**: **Aggressive Forgetting**. Do not dump this state to Chat.
- **Pattern**: Calculate results inside the sandbox and return only the answer

```python
# BAD: Dumps 10,000 rows to chat context
df = pandas.read_csv("huge_file.csv")
print(df)  # DON'T DO THIS

# GOOD: Process in sandbox, return insight only
df = pandas.read_csv("huge_file.csv")
anomalies = df[df['value'] > df['value'].mean() * 3]
print(f"Found {len(anomalies)} anomalies")  # Only this goes to chat
```

### Tier 2: Smart Memory (unified-orchestrator)
- **Persistence**: Session-to-session, project-scoped
- **Events**: task_completion, error_resolution, infrastructure, deployment
- **Access**: Via `mcp_client.unified_orchestrator`

### Tier 3: Semantic Memory (memlayer + claude-mem)
- **Persistence**: Permanent, cross-project
- **Purpose**: Long-term storage of insights, patterns, solutions
- **Access**: Via `mcp_client.memlayer`

### Tier 4: Tool Definitions (~/mcp-servers/)
- **Persistence**: Filesystem, version-controlled
- **Purpose**: Progressive disclosure of tool interfaces
- **Access**: `cat ~/mcp-servers/{server}/tools.py`

## Tools & Components

### mcp_client Bridge Implementation

The bridge translates Python calls to MCP protocol:

```python
# ~/mcp-servers/mcp_client/__init__.py
class MCPBridge:
    def __init__(self, server_name):
        self.server = server_name

    def __getattr__(self, tool_name):
        def call(**kwargs):
            return mcp_invoke(self.server, tool_name, kwargs)
        return call

# Auto-generate imports
stripe = MCPBridge("stripe")
postgres = MCPBridge("postgres")
unified_orchestrator = MCPBridge("unified-orchestrator")
memlayer = MCPBridge("memlayer")
# ... etc
```

### Progressive Tool Discovery

Instead of loading all schemas, discover on-demand:

```bash
# Structure
~/mcp-servers/
├── stripe/
│   ├── tools.py      # Interface definitions
│   └── examples.py   # Usage examples
├── postgres/
│   ├── tools.py
│   └── examples.py
├── unified-orchestrator/
│   ├── tools.py
│   └── examples.py
└── mcp_client/
    └── __init__.py   # The bridge
```

## Installation & Setup

### 1. Install v2.0 Enhanced Pipeline
```bash
# Run the enhanced installer
~/.claude/install-pipeline-v2.sh

# What it installs:
# - mcp_client bridge (~/mcp-servers/mcp_client/)
# - Tool definitions (~/mcp-servers/{server}/tools.py)
# - Updated skills with orchestration patterns
# - Sandbox verification in preflight-check
```

### 2. Verify Sandbox is Active
```bash
# preflight-check now includes:
python3 -c "from mcp_client import memlayer; print('Sandbox OK')"
```

### 3. Test Orchestration Pattern
```python
# Test script
from mcp_client import memlayer

# This should work in sandbox
result = memlayer.recall(query="test", limit=1)
print(f"Bridge working: {result is not None}")
```

## Usage Examples

### Example 1: Multi-MCP Orchestration (Token Efficient)

**Task**: Check if a user is over their usage limit, alert if so, log to memory.

**v1.0 Approach (Token Heavy)**:
```
# 4 separate tool calls in chat context
mcp__stripe__get_customer(...)     # ~800 tokens
mcp__postgres__query(...)          # ~600 tokens
mcp__slack__send_message(...)      # ~500 tokens
mcp__memlayer__remember(...)       # ~400 tokens
# Total context: ~2300 tokens
```

**v2.0 Approach (Token Efficient)**:
```python
# One script, one result
from mcp_client import stripe, postgres, slack, memlayer

def check_and_alert(user_id):
    user = stripe.get_customer(id=user_id)
    usage = postgres.query("SELECT SUM(amount) FROM usage WHERE user_id=%s", (user_id,))

    if usage['total'] > user['limit']:
        slack.send(channel="#alerts", text=f"User {user_id} over limit")
        memlayer.remember(content=f"Alert: {user_id} over by {usage['total'] - user['limit']}")
        return "ALERTED"
    return "OK"

print(check_and_alert("cus_123"))
# Total context: ~100 tokens (just "OK" or "ALERTED")
```

### Example 2: Data Analysis Without Context Bloat

**Task**: Analyze a CSV and find anomalies.

```python
from mcp_client import memlayer
import pandas as pd

def analyze_sales():
    # Data stays in sandbox
    df = pd.read_csv("/workspace/sales.csv")  # 50,000 rows

    # Analysis in sandbox
    anomalies = df[df['amount'] > df['amount'].mean() + 3 * df['amount'].std()]

    # Save insights to memory
    for _, row in anomalies.iterrows():
        memlayer.remember(
            content=f"Anomaly: Order {row['id']} amount {row['amount']}",
            metadata={"type": "anomaly", "severity": "high"}
        )

    # Return ONLY summary to chat
    print(f"Analyzed {len(df)} records. Found {len(anomalies)} anomalies.")

analyze_sales()
# Chat sees: "Analyzed 50000 records. Found 3 anomalies."
# NOT: 50,000 rows of data
```

### Example 3: Code Navigation + Modification

```python
from mcp_client import serena, memlayer

def refactor_auth():
    # Find the function
    results = serena.find_symbol(
        name_path_pattern="authenticateUser",
        relative_path="src/",
        include_body=True
    )

    if not results:
        print("ERROR: authenticateUser not found")
        return

    symbol = results[0]

    # Modify it
    new_body = symbol['body'].replace(
        "bcrypt.compare(",
        "await argon2.verify("
    )

    serena.replace_symbol_body(
        name_path=symbol['name_path'],
        relative_path=symbol['relative_path'],
        body=new_body
    )

    # Log the change
    memlayer.remember(
        content=f"Refactored {symbol['name_path']}: bcrypt → argon2",
        metadata={"type": "refactor", "file": symbol['relative_path']}
    )

    print(f"SUCCESS: Refactored {symbol['name_path']}")

refactor_auth()
```

## Troubleshooting

### 1. Sandbox Not Active
```bash
# Check if mcp_client is importable
python3 -c "from mcp_client import memlayer" 2>&1

# If fails, verify installation
ls ~/mcp-servers/mcp_client/__init__.py
```

### 2. MCP Bridge Errors
```python
# Debug mode
from mcp_client import _debug
_debug.enable()  # Shows raw MCP calls

from mcp_client import memlayer
memlayer.recall(query="test")  # Will show debug output
```

### 3. Data Accidentally in Context
If you see large data dumps in chat:
1. Check your `print()` statements
2. Ensure you're returning summaries, not raw data
3. Use the Data Triage Protocol

## Best Practices

### 1. Orchestrate, Don't Call
```python
# BAD: Multiple tool calls in chat
mcp__a__do_thing()
mcp__b__do_thing()
mcp__c__do_thing()

# GOOD: One script
from mcp_client import a, b, c
a.do_thing()
b.do_thing()
c.do_thing()
print("Done")
```

### 2. Data Stays in Sandbox
```python
# BAD: Dumps data to chat
data = api.get_all_records()
print(data)  # 10,000 records in chat context!

# GOOD: Process and summarize
data = api.get_all_records()
summary = f"Records: {len(data)}, Total: ${sum(r['amount'] for r in data)}"
print(summary)
```

### 3. Progressive Discovery
```bash
# BAD: Load all tool schemas upfront (10,000+ tokens)

# GOOD: Discover as needed
ls ~/mcp-servers/           # What servers exist?
cat ~/mcp-servers/stripe/tools.py  # What can stripe do?
```

### 4. Error Handling in Scripts
```python
from mcp_client import stripe, memlayer

def safe_operation():
    try:
        result = stripe.get_customer(id="cus_123")
        print(f"SUCCESS: {result['email']}")
    except Exception as e:
        memlayer.remember(
            content=f"stripe.get_customer failed: {e}",
            metadata={"type": "error", "service": "stripe"}
        )
        print(f"ERROR: {e}")

safe_operation()
```

### 5. Always Follow Protocol
```
DOING: Write orchestration script for user lookup
EXPECT: Script returns user status in <100 tokens
IF WRONG: May have data leak to context, check print statements
```

## Quick Reference

### Token Comparison

| Operation | v1.0 (Tool Calls) | v2.0 (Orchestration) | Savings |
|-----------|-------------------|----------------------|---------|
| 3 MCP calls | ~2,000 tokens | ~150 tokens | 92% |
| Data analysis | ~50,000 tokens | ~200 tokens | 99.6% |
| Code search + modify | ~3,000 tokens | ~300 tokens | 90% |

### Key Commands

```bash
# v2.0 Workflow
auto-workflow              # Includes tool discovery
preflight-check            # Verifies sandbox active
tool-explorer "keyword"    # Find relevant tools

# Orchestration Pattern
run_python "script.py"     # Execute in sandbox
```

### mcp_client Quick Reference

```python
from mcp_client import (
    unified_orchestrator,  # Memory, session, infra
    memlayer,              # Persistent storage
    context7,              # Documentation
    serena,                # Code navigation
    ace,                   # Code execution
    codex,                 # OpenAI consultation
    gemini,                # Google consultation
    deepseek,              # DeepSeek consultation
)
```

---

**Version**: 2.0 (Code Execution Enhanced)
**Principle**: Orchestrate, Don't Call
**Goal**: 98% token reduction through sandbox execution
