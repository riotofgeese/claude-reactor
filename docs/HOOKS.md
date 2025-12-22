# Hooks Configuration

## Overview

Claude Reactor uses a **lite hooks** configuration for optimal token efficiency. Hooks are shell scripts that execute at specific lifecycle events in Claude Code sessions.

## Current Hook Configuration

Located in `~/.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(grep:*)",
      "Bash(journalctl:*)",
      "Bash(last:*)",
      "Bash(ln:*)",
      "Bash(tree:*)",
      "mcp__unified-orchestrator__session_restore"
    ]
  },
  "enableAllProjectMcpServers": true,
  "hooks": {
    "PostToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"continue\": true}'"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/home/crogers2287/.claude/hooks/session-complete-memory.sh",
            "timeout": 10000
          }
        ]
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

## Hook Types

### PostToolUse
Runs after every tool execution. The lite config just outputs `{"continue": true}` to allow continuation.

### Stop
Runs when a session ends. Calls `session-complete-memory.sh` to log session completion.

### PreToolUse (Optional)
For DOING protocol enforcement. Installed in project `.claude/hooks/`:

```bash
# pre-tool-use-protocol.sh
# Enforces DOING/EXPECTED/IF WRONG pattern
```

### PreCompact (Optional)
Saves context before compaction:

```bash
# pre-compact-save.sh
# Saves session state to memlayer before context compaction
```

### PostCompact (Optional)
Restores context after compaction:

```bash
# post-compaction-restore.sh
# Restores session state from memlayer after compaction
```

## Critical Hook Rules

### 1. JSON Output Required
All hooks MUST output valid JSON to STDOUT:

```json
{"continue": true}
```

or

```json
{"continue": false, "message": "Blocked because..."}
```

If a hook outputs nothing or invalid JSON, Claude Code will **stop** execution.

### 2. Exit Codes
- Exit 0: Success
- Exit 1: Failure (but not necessarily blocking)
- The JSON output determines blocking, not exit code

### 3. Timeout
Default timeout is 60000ms (1 minute). Set custom timeouts for long-running hooks:

```json
{
  "type": "command",
  "command": "/path/to/hook.sh",
  "timeout": 10000
}
```

## Project-Specific Hooks

Project hooks are installed to `.claude/hooks/` by `install-pipeline-enhanced.sh`:

```
.claude/hooks/
├── pre-tool-use-protocol.sh   # DOING protocol enforcement
├── post-compaction-restore.sh # Context recovery
└── pre-compact-save.sh        # Context preservation
```

These are copied (not symlinked) to ensure isolation.

## Available Global Hooks

Located in `~/.claude/hooks/`:

| Hook | Purpose |
|------|---------|
| `session-complete-memory.sh` | Log session end to memlayer |
| `pre-tool-use-protocol.sh` | DOING/EXPECTED/IF WRONG enforcement |
| `post-compaction-restore.sh` | Context recovery after compaction |
| `pre-compact-save.sh` | Save context before compaction |
| `auto-error-recovery.sh` | Automatic error pattern detection |
| `pipeline-gate.sh` | Gate complex prompts through planning |

## Troubleshooting

### Hook Not Running
1. Check `hooksEnabled` in settings.json (should not be `false`)
2. Verify hook path exists and is executable
3. Check permissions: `chmod +x ~/.claude/hooks/hook-name.sh`

### Hook Blocking Execution
1. Check hook output: `bash ~/.claude/hooks/hook-name.sh`
2. Ensure JSON output: `{"continue": true}`
3. Check for syntax errors in hook script

### Hook Output Not Visible
1. Use STDOUT for JSON output (not STDERR)
2. Redirect logging to file, not console
3. Use `<system-reminder>` tags for Claude-visible output

## Creating Custom Hooks

### Template

```bash
#!/bin/bash
# hook-name.sh - Description of what this hook does

# Get tool context from environment
TOOL_NAME="${CLAUDE_TOOL_NAME:-unknown}"
TOOL_INPUT="${CLAUDE_TOOL_INPUT:-}"

# Your logic here
if [[ "$TOOL_NAME" == "Bash" ]]; then
    # Do something for Bash commands
    :
fi

# Required: Output JSON
echo '{"continue": true}'
exit 0
```

### Installation

1. Create hook in `~/.claude/hooks/`
2. Make executable: `chmod +x ~/.claude/hooks/hook-name.sh`
3. Add to settings.json hooks section
4. Restart Claude Code

## Lite vs Full Hooks

### Lite (Current - Recommended)
- Minimal overhead
- ~90% token reduction
- Only essential hooks (PostToolUse continuation, Stop logging)
- Use for most projects

### Full (Available)
- Complete protocol enforcement
- DOING pattern validation
- Automatic error recovery
- Use for complex projects requiring strict guardrails

To switch to full hooks:
```bash
cp ~/.claude/hooks/master-pre-tool.sh ~/.claude/hooks/active-pre-tool.sh
# Then add to settings.json PreToolUse section
```

## Plugin Integration

Enabled plugins provide hook-like functionality:

- **feature-dev**: Guided feature development workflow
- **hookify**: Create hooks from conversation analysis
- **code-review**: Automated code review on changes

These are enabled via `enabledPlugins` in settings.json.
