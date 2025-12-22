# Agentic Pipeline Playbook (Codex) - MCP Orchestrated

This is the MCP-orchestrated end-to-end pipeline for Codex sessions. It uses direct MCP calls (no OmniMCP gateway) to orchestrate: MemLayer recall → Acontext enhancement → Sequential thinking → Code execution → MemLayer commit.

**Architecture:**
- ❌ No OmniMCP gateway required (direct MCP calls)
- ✅ unified-orchestrator MCP (MemLayer smart_recall/smart_remember)
- ✅ Acontext HTTP service (prompt enhancement at localhost:3010)
- ✅ sequential-thinking MCP (planning with enhanced context)
- ✅ code-execution-mode MCP (Python execution)
- ✅ Full MCP orchestration, lightweight, no gateway dependency

## Quickstart
- First tool call auto‑boots the pipeline (PreToolUse → `ensure-agentic-pipeline.sh` → orchestrator).
- Manual bootstrap: `/p` in chat also runs the same init and unlocks tools; `/p status` reports readiness/log tail; `/clear` resets markers/logs.
- Session context is saved to `/tmp/agentic_pipeline_context.json`.
- Work loop:
  1) Read context file to prime the prompt.
  2) Run sequential thinking; pull docs via Context7 if needed.
  3) Execute code in sandbox (`code-execution-mode.run_python` with `project_path=/home/crogers2287/sandbox`).
  4) Log the fix (`~/.claude/hooks/commit-task.sh "description"`). Stop hook also auto‑commits on exit.

## Files and Hooks
- PreToolUse: `.claude/settings.json` → `ensure-agentic-pipeline.sh`
- Bootstrap: `~/.claude/hooks/automatic-pipeline-trigger-fixed.sh` (kept for legacy steps)
- Orchestrator: `~/.claude/hooks/agentic-orchestrator.sh` → `sandbox/agentic_orchestrator.py`
- Context output: `/tmp/agentic_pipeline_context.json`
- Ready markers: `/tmp/.agentic_pipeline_ready_${USER}`, `/tmp/.agentic_orchestrator_ran_${USER}`
- Logs: `/tmp/agentic_pipeline.log`

## What the Orchestrator Does (5-Step MCP Orchestration)

The orchestrator prepares a context file with a 5-step MCP orchestration sequence:

1. **Recall** - MemLayer context retrieval (direct SQLite access, project-scoped)
   - Already executed by orchestrator → loads recent project memories

2. **Enhance** - Acontext prompt enhancement (HTTP service at localhost:3010)
   - Enhances context with task complexity analysis and optimization suggestions

3. **Plan** - Sequential thinking with enhanced context
   - Status: Pending → Use `mcp__sequential-thinking__sequentialthinking`

4. **Execute** - Code execution via MCP
   - Status: Pending → Use `mcp__code-execution-mode__run_python`

5. **Commit** - Save results to MemLayer
   - Status: Pending → Use `mcp__unified-orchestrator__smart_remember`

**Output:** `/tmp/agentic_pipeline_context.json` with:
- `workflow: "mcp_orchestrated"`
- `orchestration_sequence[]` - Full 5-step workflow with status tracking
- `mcp_services[]` - List of required MCP tools
- `acontext_enhancement{}` - Enhanced context from Acontext service

## Recommended Flow (per task)

### Automatic Bootstrap (Steps 1-2)
- PreToolUse hook → `ensure-agentic-pipeline.sh` → orchestrator
- ✓ Step 1: MemLayer recall (completed automatically)
- ✓ Step 2: Acontext enhancement (completed automatically)

### Manual Orchestration (Steps 3-5)
Follow the orchestration sequence in the context file:

**Step 3: Plan**
```
mcp__sequential-thinking__sequentialthinking(
    thought="Review enhanced context and plan implementation",
    thoughtNumber=1,
    totalThoughts=3,
    nextThoughtNeeded=true
)
```

**Step 4: Execute**
```
mcp__code-execution-mode__run_python(
    code="<your implementation>",
    project_path="/home/crogers2287/sandbox"
)
```

**Step 5: Commit**
```
mcp__unified-orchestrator__smart_remember(
    event_type="task_completion",
    content={
        "task": "<what was done>",
        "outcome": "<results>",
        "files_changed": ["<files>"]
    }
)
```

Alternatively, use the Stop hook which auto-commits via `session-complete-memory.sh`

### One-shot runner (auto-logs)
Use `python3 agentic_pipeline_runner.py --summary "<task>" [--command "<cmd>"] [--notes "..."]`
- Runs orchestrator (recall + optional Acontext) via `ensure-agentic-pipeline.sh`
- Optionally executes the command (shell)
- Automatically writes a structured memory to MemLayer (project detected from PWD)
- Memory includes `workflow: "simplified"` and `mcp_backend: "code-execution-mode"` metadata

#### Global convenience command
Run from any directory:
```
run-agentic-pipeline "Short summary" "optional command" "optional notes"
```
This symlink points to `sandbox/run_agentic_pipeline.sh`, which calls the runner and still uses your current working directory for project detection and command execution.

## Notes and Constraints
- **Acontext service** runs at localhost:3010 (Node.js HTTP service, not MCP)
- **No OmniMCP gateway** - all MCP calls are direct to individual servers
- **MemLayer recall** uses direct SQLite access (fast, no MCP overhead)
- **MemLayer commit** uses unified-orchestrator MCP (smart_remember tool)
- **Code execution** via code-execution-mode MCP (Python sandbox with /workspace mount)
- **Hooks are non-blocking** - failures won't stop tool use; check `/tmp/agentic_pipeline.log`

### MCP Servers Required
Ensure these are enabled in `~/.claude/mcp.json`:
- `unified-orchestrator` (line 171-177)
- `sequential-thinking` (line 178-185)
- `code-execution-mode` (line 186-190)

### Acontext Service
Start with: `cd ~/.claude/acontext-service && PORT=3010 node index.js`
Or use the background starter: `~/.claude/scripts/start-acontext.sh`

## Verification Commands
- Quick status: `/p status` (runs `pipeline-status.sh` and shows markers/log tail)
- Context file exists: `ls -l /tmp/agentic_pipeline_context.json`
- Log tail: `tail -n 40 /tmp/agentic_pipeline.log`
- Markers: `cat /tmp/.agentic_pipeline_ready_${USER}` and `cat /tmp/.agentic_orchestrator_ran_${USER}`
- Check workflow: `cat /tmp/agentic_pipeline_context.json | jq '.workflow, .mcp_backend'`

## MCP Orchestration Benefits

**Architecture:**
```
┌─────────────┐
│ PreToolUse  │ (Hook triggers on first tool call)
│    Hook     │
└──────┬──────┘
       │
       v
┌─────────────────────────────────────────┐
│   Agentic Orchestrator                  │
│   (Python script)                       │
├─────────────────────────────────────────┤
│ Step 1: MemLayer Recall (SQLite)        │ ✓ Direct access
│ Step 2: Acontext Enhance (HTTP)         │ ✓ localhost:3010
└──────┬──────────────────────────────────┘
       │ Writes context file
       v
┌─────────────────────────────────────────┐
│   /tmp/agentic_pipeline_context.json    │
│   - Enhanced context                    │
│   - Orchestration sequence              │
│   - Next steps (3-5)                    │
└──────┬──────────────────────────────────┘
       │
       v
┌─────────────────────────────────────────┐
│   Manual MCP Orchestration              │
├─────────────────────────────────────────┤
│ Step 3: sequential-thinking (MCP)       │
│ Step 4: code-execution-mode (MCP)       │
│ Step 5: unified-orchestrator (MCP)      │
└─────────────────────────────────────────┘
```

**Key Features:**
- ✅ **No OmniMCP gateway** - Direct MCP calls to each server
- ✅ **Acontext enhancement** - HTTP service for prompt optimization
- ✅ **Sequential thinking** - Structured planning before execution
- ✅ **Full MCP integration** - unified-orchestrator for memory management
- ✅ **Automatic bootstrap** - Steps 1-2 run on first tool call
- ✅ **Manual orchestration** - Steps 3-5 follow clear sequence

**What's Different:**
- **vs. Simplified**: Adds Acontext enhancement + sequential thinking
- **vs. OmniMCP**: No gateway dependency, direct MCP calls only
- **vs. Original**: Removes Context7, keeps core MCP orchestration

**Workflow State:**
- Steps 1-2: Automatic (hook-driven)
- Steps 3-5: Manual (MCP tool calls)
- Memory: Persistent across sessions via unified-orchestrator

This MCP-orchestrated pipeline provides structured, multi-step workflows with enhanced context while maintaining direct MCP access and avoiding gateway dependencies.
