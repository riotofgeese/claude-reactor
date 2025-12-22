# MCP Integration

## Server List & Config
Claude Reactor uses a **filtered set of 16 MCP servers** (from install-pipeline-enhanced.sh) to maintain tool limits under 200.

### Core MCP Servers (Always Enabled)

#### 1. unified-orchestrator
- **Purpose**: Orchestrates sessions (restore context), memory (smart_recall/remember), infrastructure (save servers/DBs), workflows (think_through/sandbox_web_search).
- **Key Tools**: `session_restore`, `smart_remember`, `smart_recall`, `save_infrastructure`, `sandbox_execute`
- **Usage**: Auto-recalls on start; `mcp__unified-orchestrator__session_restore()` for compaction recovery.
- **Tokens**: ~25 tools; essential for persistence.

#### 2. memlayer
- **Purpose**: Project-isolated memory storage. Remembers tasks/errors/decisions; recalls by query.
- **Key Tools**: `remember`, `recall`, `get_all_memories`, `forget`
- **Usage**: `mcp__memlayer__remember(content="Task done")`; `/mem ID` for details.
- **Tokens**: ~8 tools; per-project isolation.

#### 3. ace
- **Purpose**: Sandbox code execution (Python) with learning (playbooks from runs/tests). Supports project isolation.
- **Key Tools**: `ace_code_execute`, `ace_code_retry_start`, `ace_ask`, `ace_get_strategies`
- **Usage**: `mcp__ace__ace_code_execute(code="...", question="...")`
- **Tokens**: ~20 tools; key for safe runs.

#### 4. code-execution-mode
- **Purpose**: Python sandbox with MCP integration. Primary execution environment for v2.0 protocol.
- **Key Tools**: `run_python`, `sandbox_help`
- **Usage**: `mcp__code-execution-mode__run_python(code="...", project_path="/path")`
- **Tokens**: ~3 tools; core for v2.0.

#### 5. sequential-thinking
- **Purpose**: Reflective planning for complex tasks. Thoughts chain with revisions/branches.
- **Key Tools**: `sequentialthinking`
- **Usage**: `{thought: "...", thought_number:1, total_thoughts:5, next_thought_needed: true}`
- **Tokens**: ~1 tool; for multi-step planning.

#### 6. code-reasoning
- **Purpose**: Alternative thinking tool with branch/revision support.
- **Key Tools**: `code-reasoning`
- **Usage**: Similar to sequential-thinking but with branch_id support.
- **Tokens**: ~1 tool.

#### 7. context7
- **Purpose**: Real-time library docs (resolve ID, get API/examples/guides).
- **Key Tools**: `resolve-library-id`, `get-library-docs`
- **Usage**: `mcp__context7__resolve-library-id(libraryName="react")` then `get-library-docs`
- **Tokens**: ~2 tools; up-to-date vs. cutoff knowledge.

### Browser & UI Debugging

#### 8. browser-tools
- **Purpose**: Browser automation and debugging. Console logs, network errors, screenshots.
- **Key Tools**: `getConsoleLogs`, `getNetworkErrors`, `takeScreenshot`, `runAccessibilityAudit`
- **Usage**: For UI debugging and accessibility checks.
- **Tokens**: ~15 tools.

#### 9. flowlens
- **Purpose**: Browser flow recording and analysis. Timeline events, screenshots, debugging.
- **Key Tools**: `get_flow_by_uuid`, `list_flow_timeline_events_within_range`, `take_flow_screenshot_at_second`
- **Usage**: For debugging browser-based issues with recorded flows.
- **Tokens**: ~10 tools.

### AI Model Integration

#### 10. gemini
- **Purpose**: Google Gemini AI integration for roundtable discussions.
- **Key Tools**: `gemini`, `gemini-reply`
- **Usage**: `mcp__gemini__gemini(prompt="Review this plan")`
- **Tokens**: ~2 tools.

#### 11. deepseek
- **Purpose**: DeepSeek AI integration for code review and planning.
- **Key Tools**: `deepseek`, `deepseek-reply`
- **Usage**: `mcp__deepseek__deepseek(prompt="...")`
- **Tokens**: ~2 tools.

#### 12. glm
- **Purpose**: GLM 4.6 AI integration.
- **Key Tools**: `glm`, `glm-reply`
- **Usage**: `mcp__glm__glm(prompt="...")`
- **Tokens**: ~2 tools.

### Infrastructure & Utilities

#### 13. fast-port-checker
- **Purpose**: Quick port availability checks before starting services.
- **Key Tools**: `fast_check_port_available`, `fast_suggest_dev_port`
- **Usage**: Always check ports before starting dev servers.
- **Tokens**: ~3 tools.

#### 14. omada-mcp-server
- **Purpose**: Network device management (Omada WiFi controller).
- **Key Tools**: `get_network_status`, `get_connected_clients`, `analyze_wifi_performance`
- **Usage**: For network infrastructure debugging.
- **Tokens**: ~20 tools.

#### 15. serena
- **Purpose**: Semantic coding tools with symbol-level operations.
- **Key Tools**: `find_symbol`, `replace_symbol_body`, `get_symbols_overview`, `search_for_pattern`
- **Usage**: For intelligent code navigation and refactoring.
- **Tokens**: ~30 tools.

### Disabled by Default (Available but Filtered)
These servers are in global config but disabled to save context:
- claude-code-mcp
- task-master-ai
- mcp-server-docker
- n8n-remote-script
- hf-mcp-server
- terminal-controller
- llamaswap
- Home Assistant
- perplexity-mcp
- pwmcp
- onepanel

## Setup & Management

### Installation
The pipeline installer (`install-pipeline-enhanced.sh`) automatically:
1. Filters MCP servers to only enabled ones
2. Creates `.mcp.json.filtered` with active servers
3. Symlinks `.mcp.json` to filtered version

### Manual Management
```bash
# Check current status
cat .mcp.json | jq '.mcpServers | keys'

# Enable a server (edit global config)
vim ~/.claude/mcp.json  # Set "enabled": true

# Reinstall to pick up changes
/home/crogers2287/.claude/install-pipeline-enhanced.sh $(pwd)
```

### Verification
```bash
# Count tools (should be <200)
claude "How many tools do you have access to?"

# List enabled servers
cat .mcp.json.filtered | jq '.mcpServers | keys'
```

## v2.0 Protocol Integration

In v2.0 mode (sandbox-first), MCP tools are called from within the sandbox:

```python
# Inside code-execution-mode sandbox
import mcp.runtime as runtime

# List available servers
servers = await runtime.list_servers()

# Use server proxies
result = await mcp_memlayer.remember(content="Task done")
```

This reduces token usage by ~90% compared to individual tool calls.

## Hooks Integration
- **SessionStart**: `session_restore` on unified-orchestrator
- **PreCompact**: `session_checkpoint` saves context
- **Stop**: `session-complete-memory.sh` logs session end

## Troubleshooting

### Tool Limit Error
If you see "Too many tools" errors:
1. Check filtered count: `cat .mcp.json.filtered | jq '.mcpServers | length'`
2. Disable additional servers in global config
3. Reinstall pipeline

### Server Not Responding
```bash
# Check if server is running
ps aux | grep mcp

# Restart specific server
pkill -f "server-name" && bun run start-server
```

License: MIT.
