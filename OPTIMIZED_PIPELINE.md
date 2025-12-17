# Optimized MCP Pipeline Architecture

## Overview

The pipeline is NOT linear - it's a **directed graph with conditional branches** based on task type. The optimization is knowing WHEN to call each tool, not just the order.

---

## Tool Inventory

### TIER 1 - Core (Always Available)

| Tool | Server | Key Functions | When to Use |
|------|--------|---------------|-------------|
| **unified-orchestrator** | unified-orchestrator | `session_restore`, `smart_remember`, `smart_recall`, `get_infrastructure`, `session_checkpoint` | Every session, every task |
| **ace** | ace | `ace_ask_start`, `ace_ask_complete`, `ace_code_retry_start/continue`, `ace_stats` | Task enhancement, code retry |
| **sequential-thinking** | sequential-thinking | `sequentialthinking` | Complex multi-step planning |
| **code-execution-mode** | code-execution-mode | `run_python`, `sandbox_help` | All code execution |

### TIER 2 - Conditional

| Tool | Server | Key Functions | When to Use |
|------|--------|---------------|-------------|
| **context7** | context7 | `resolve-library-id`, `get-library-docs` | Library/framework questions |
| **fast-port-checker** | fast-port-checker | `fast_check_port_available`, `fast_suggest_dev_port` | Before launching services |
| **memlayer** | memlayer | `remember`, `recall`, `get_all` | Low-level memory access |

### TIER 3 - Specialized

| Tool | Server | Key Functions | When to Use |
|------|--------|---------------|-------------|
| **flowlens** | flowlens | Flow analysis tools | Only with flow*.zip uploads |

---

## Pipeline Stages

```
═══════════════════════════════════════════════════════════════════
STAGE 1: SESSION INIT (Automatic - First Action)
═══════════════════════════════════════════════════════════════════

  ┌─────────────────────────────────────────────────────────────┐
  │  session_restore()                                          │
  │  └─→ Returns: infrastructure, tasks, preferences,           │
  │      templates, flows - ALL in ONE call                     │
  └─────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════
STAGE 2: TASK ENHANCEMENT (Per Task - Before Planning)
═══════════════════════════════════════════════════════════════════

  ┌─────────────────────────────────────────────────────────────┐
  │  PARALLEL:                                                  │
  │  ├─→ ace_ask_start(task)      # Enhance with strategies    │
  │  └─→ smart_recall("similar")  # Find related solutions     │
  └─────────────────────────────────────────────────────────────┘

  KEY INSIGHT: ACE enhances the task BEFORE planning,
  making the plan more effective!

═══════════════════════════════════════════════════════════════════
STAGE 3: CONTEXT LOADING (Conditional - Based on Task Type)
═══════════════════════════════════════════════════════════════════

  Task Type Detection:

  ┌─────────────┬─────────────────────────────────────────────────┐
  │ Task Type   │ Action                                          │
  ├─────────────┼─────────────────────────────────────────────────┤
  │ Library     │ context7.resolve-library-id → get-library-docs  │
  │ Server/DB   │ get_infrastructure(environment)                 │
  │ Services    │ fast_check_port_available / fast_suggest_dev    │
  │ Browser bug │ recall_flow_context() / debug_session_start()   │
  │ Other       │ Skip this stage                                 │
  └─────────────┴─────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════
STAGE 4: PLANNING (Complex Tasks Only)
═══════════════════════════════════════════════════════════════════

  ┌─────────────────────────────────────────────────────────────┐
  │  1. think_through(task)      # Structure approach           │
  │  2. sequentialthinking()     # Deep reasoning               │
  │  3. TodoWrite()              # Track implementation steps   │
  └─────────────────────────────────────────────────────────────┘

  Skip for simple tasks (single file edit, quick fix, etc.)

═══════════════════════════════════════════════════════════════════
STAGE 5: EXECUTION (The Work)
═══════════════════════════════════════════════════════════════════

  ┌─────────────────────────────────────────────────────────────┐
  │  Primary: run_python / sandbox_execute                      │
  │                                                             │
  │  On Failure:                                                │
  │  └─→ ace_code_retry_start(code, question)                  │
  │      └─→ ace_code_retry_continue(session_id, improved)     │
  │          └─→ Repeat until success or max_iterations        │
  └─────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════
STAGE 6: COMPLETION (After Every Task - MANDATORY)
═══════════════════════════════════════════════════════════════════

  ┌─────────────────────────────────────────────────────────────┐
  │  MANDATORY - NO EXCEPTIONS:                                 │
  │                                                             │
  │  1. smart_remember(event_type="task_completion", content={  │
  │       task, outcome, files_changed, learnings              │
  │     })                                                      │
  │                                                             │
  │  2. ace_ask_complete(session_id, response)                 │
  │     └─→ Learns strategies from the interaction             │
  │                                                             │
  │  3. update_task_progress() # If multi-session goal         │
  └─────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════
STAGE 7: SESSION END (Before Compaction/Exit)
═══════════════════════════════════════════════════════════════════

  ┌─────────────────────────────────────────────────────────────┐
  │  1. session_checkpoint(                                     │
  │       summary, achievements, pending_tasks, context        │
  │     )                                                       │
  │                                                             │
  │  2. set_current_task(goal, status, progress, next_steps)   │
  └─────────────────────────────────────────────────────────────┘
```

---

## Decision Tree

```
                    ┌─────────────────────┐
                    │   Task Received     │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  STAGE 2: Enhance   │
                    │  ace_ask_start()    │
                    │  smart_recall()     │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
     ┌────────▼────────┐ ┌─────▼─────┐ ┌───────▼───────┐
     │ Library Work?   │ │Server/DB? │ │Start Service? │
     └────────┬────────┘ └─────┬─────┘ └───────┬───────┘
              │                │                │
     ┌────────▼────────┐ ┌─────▼─────┐ ┌───────▼───────┐
     │    context7     │ │get_infra()│ │ port_checker  │
     │ resolve → docs  │ │           │ │               │
     └────────┬────────┘ └─────┬─────┘ └───────┬───────┘
              │                │                │
              └────────────────┼────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Complex Task?      │
                    └──────────┬──────────┘
                          YES  │  NO
                    ┌──────────┴──────────┐
                    │                     │
           ┌────────▼────────┐   ┌────────▼────────┐
           │ STAGE 4: Plan   │   │ Skip to Stage 5 │
           │ think_through   │   │                 │
           │ sequentialthink │   │                 │
           │ TodoWrite       │   │                 │
           └────────┬────────┘   └────────┬────────┘
                    │                     │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  STAGE 5: Execute   │
                    │  run_python         │
                    └──────────┬──────────┘
                               │
                          FAILED?
                    ┌──────────┴──────────┐
                    │                     │
           ┌────────▼────────┐   ┌────────▼────────┐
           │ ace_code_retry  │   │ Continue...     │
           │ start/continue  │   │                 │
           └────────┬────────┘   └────────┬────────┘
                    │                     │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  STAGE 6: Complete  │
                    │  smart_remember()   │ ◄── MANDATORY
                    │  ace_ask_complete() │
                    └─────────────────────┘
```

---

## Unified-Orchestrator Tools Reference

### Session Management
| Tool | Purpose |
|------|---------|
| `session_restore()` | ONE-CLICK full context recovery |
| `session_checkpoint()` | Save state before compaction |
| `detect_project()` | Auto-detect project from cwd |

### Memory
| Tool | Purpose |
|------|---------|
| `smart_remember(event_type, content)` | Store with auto-categorization |
| `smart_recall(context)` | Context-aware retrieval |
| `get_memory_rules()` | Get save/recall rules |

### Infrastructure
| Tool | Purpose |
|------|---------|
| `save_infrastructure()` | Store server/DB connection details |
| `get_infrastructure()` | Retrieve stored infrastructure |
| `check_environment()` | Query running services |

### Task Management
| Tool | Purpose |
|------|---------|
| `set_current_task()` | Set multi-session goal |
| `get_current_task()` | Retrieve current task state |
| `update_task_progress()` | Quick progress update |

### Planning
| Tool | Purpose |
|------|---------|
| `think_through(task)` | Structure sequential thinking |
| `discover_tools(query)` | Find MCP tools |

### Sandbox
| Tool | Purpose |
|------|---------|
| `sandbox_execute()` | Execute Python with project isolation |
| `verify_project_path()` | Verify project path before operations |

---

## ACE Tools Reference

### Prompt Enhancement
| Tool | Purpose |
|------|---------|
| `ace_ask_start(question, agent)` | Enhance task with learned strategies |
| `ace_ask_complete(session_id, response)` | Complete and learn from interaction |
| `ace_ask_oneshot(question, response, agent)` | One-shot enhance + learn |

### Code Execution with Learning
| Tool | Purpose |
|------|---------|
| `ace_code_execute(code, question)` | Execute and learn from results |
| `ace_code_retry_start(code, question)` | Start auto-retry loop |
| `ace_code_retry_continue(session_id, improved)` | Continue retry |

### Analytics
| Tool | Purpose |
|------|---------|
| `ace_stats(agent)` | Dashboard statistics |
| `list_playbooks()` | List all agent playbooks |
| `get_strategies(agent)` | Get learned strategies |

---

## Auto-Triggers

| Trigger | Action |
|---------|--------|
| Session start | `session_restore()` |
| Task received | `ace_ask_start()` + `smart_recall()` |
| Library keyword | `context7.resolve-library-id` |
| Server/DB keyword | `get_infrastructure()` |
| Code failure | `ace_code_retry_start()` |
| Task complete | `smart_remember()` + `ace_ask_complete()` |
| Pre-compaction | `session_checkpoint()` |

---

## Key Optimizations

1. **ACE First**: `ace_ask_start()` BEFORE planning - enhances task understanding
2. **Parallel Loading**: `ace_ask_start()` + `smart_recall()` run together
3. **Conditional Context**: Only load what's needed (context7, infrastructure, ports)
4. **Unified Hub**: Use `unified-orchestrator` for memory, not raw `memlayer`
5. **Auto-Retry**: Let ACE handle code failures with intelligent improvement
6. **Mandatory Completion**: ALWAYS `smart_remember()` after every task

---

## Memory Architecture (smart_remember → MemLayer)

### Dual-Write Mechanism

`smart_remember()` writes to MemLayer with automatic fallback:

```
┌─────────────────────────────────────────────────────────────────┐
│  smart_remember(event_type, content)                            │
│                                                                 │
│  1. Format content with metadata (timestamp, project, tags)     │
│  2. Try HTTP endpoint (memlayer-service:8082) - PRIMARY         │
│     └─→ If success: Return result                               │
│     └─→ If fail: Continue to fallback                           │
│  3. Direct SQLite write - FALLBACK                              │
│     └─→ Write to project_{project_name}.db                      │
│     └─→ Same schema as HTTP service                             │
└─────────────────────────────────────────────────────────────────┘
```

### Storage Format

Both methods use identical schema:
```sql
CREATE TABLE memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,        -- Formatted task summary
    metadata TEXT,                -- JSON: event_type, project, tags, timestamp
    project_id TEXT,              -- Project identifier
    created_at TIMESTAMP          -- ISO format timestamp
)
```

### Content Formatting

smart_remember automatically formats content:
```
Task Name (YYYY-MM-DD)

WHAT WAS DONE:
<outcome>

FILES CHANGED:
- file1.py
- file2.js

KEY LEARNINGS:
<learnings>

Project: project_name (on hostname)
Tags: event_type, project_name
```

### Database Location

- **HTTP Service**: Uses Docker volume at `/home/crogers2287/mcp-server-memlayer/memlayer-storage/`
- **Fallback**: Writes directly to `project_{detected_project}.db`
- **Project Detection**: Auto-detects from `os.getcwd()` basename

### When to Use Which

| Use Case | Tool |
|----------|------|
| After completing tasks | `smart_remember(event_type="task_completion")` |
| Storing patterns/solutions | `smart_remember(event_type="learning")` |
| Low-level memory access | Direct `memlayer.remember()` |
| Retrieving memories | `smart_recall()` or `memlayer.recall()`
