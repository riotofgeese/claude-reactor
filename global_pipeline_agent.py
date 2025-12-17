#!/usr/bin/env python3
"""
Global Pipeline Agent: Extremely knowledgeable about our /p pipeline workflow.
Called at beginning of every session and text entry to orchestrate the system.

This agent knows:
1. Our enhanced pipeline installer (skills priority, filtered MCPs)
2. The 8-phase workflow from CLAUDE.md
3. All skills and when to use them
4. Auto-Serena integration for magic code navigation
5. Memory system with smart_remember after every task
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import subprocess

REPO_ROOT = Path(__file__).resolve().parent
OUTPUT_PATH = Path("/tmp/global_pipeline_agent_context.json")
COMPACT_CONTEXT = os.environ.get("GLOBAL_AGENT_COMPACT", "1") != "0"
MAX_GUIDANCE_LINES = 3

class GlobalPipelineAgent:
    """Global agent with deep knowledge of our pipeline workflow."""

    def __init__(self):
        self.project = os.environ.get("PROJECT_NAME") or os.path.basename(os.getcwd()) or "sandbox"
        self.pipeline_knowledge = self._load_pipeline_knowledge()

    def _load_pipeline_knowledge(self) -> Dict[str, Any]:
        """Load deep knowledge about our pipeline."""
        return {
            "pipeline_name": "Enhanced /p Pipeline with Skills Priority",
            "created_date": "2025-12-15",
            "key_features": [
                "Skills prioritized over MCPs",
                "Filtered MCP config (enabled servers only)",
                "Auto-Serena magic code navigation",
                "8-phase workflow enforcement",
                "Memory system with smart_remember"
            ],
            "installer_details": {
                "script": "/home/crogers2287/.claude/install-pipeline-enhanced.sh",
                "phases": [
                    "PHASE 1: INSTALLING SKILLS (Priority)",
                    "PHASE 2: CREATING FILTERED MCP CONFIG",
                    "PHASE 3: INSTALLING ESSENTIAL FILES"
                ],
                "skills_count": self._count_skills(),
                "mcp_servers_enabled": self._count_enabled_mcps()
            },
            "workflow_phases": {
                "1. PREFLIGHT": "preflight-check (environment validation)",
                "2. CONTEXT": "docs-first + negative-cache + context7",
                "3. PLAN": "sequential-thinking + codex/gemini review",
                "4. SAFETY": "git-handbrake + dependency-check",
                "5. EXECUTE": "Write code (ACE or run_python)",
                "6. VERIFY": "lint-gate + tests + secret-guard",
                "7. RECOVERY": "failure-playbooks (if errors)",
                "8. COMMIT": "smart_remember (always)"
            },
            "skills_reference": self._load_skills_reference(),
            "mcp_requirements": [
                "unified-orchestrator (session state, memory)",
                "memlayer (persistent storage)",
                "ace (code execution with learning)",
                "context7 (library docs)",
                "sequential-thinking (step reasoning)"
            ],
            "auto_serena_integration": {
                "hook": "/home/crogers2287/.claude/hooks/auto-serena-hook.py",
                "skill": "/home/crogers2287/.claude/skills/auto-serena.md",
                "patterns": [
                    "find where X is defined",
                    "add Y to function Z",
                    "update X to do Y",
                    "navigate to the X class"
                ],
                "action_types": ["find", "navigate", "insert", "update", "refactor"]
            },
            "memory_system": {
                "rule": "After EVERY task: smart_remember",
                "event_types": ["task_completion", "error_resolution", "session_checkpoint"],
                "mandatory": True
            },
            "quick_commands": {
                "check_port": "lsof -i :3000",
                "find_available_port": "for p in $(seq 3000 3100); do ! lsof -i :$p >/dev/null 2>&1 && echo $p && break; done",
                "git_handbrake": 'SNAP=$(git stash create "handbrake-$(date +%s)") && echo "Snapshot: ${SNAP:-HEAD}"',
                "quick_lint": '[ -f package.json ] && npx tsc --noEmit || ruff check . 2>&1 | head -20'
            },
            "donts": [
                "Guess API params — check context7/dependency-check first",
                "Silently retry failures — surface them, log to negative-cache",
                "Touch code you can't explain (Chesterton's Fence)",
                "Skip git-handbrake before risky edits",
                "Commit without secret-guard scan",
                "Review with codex/gemini before lint-gate passes",
                "Batch memory saves — save immediately",
                "git add . — add files individually"
            ]
        }

    def _count_skills(self) -> int:
        """Count available skills."""
        skills_dir = Path("/home/crogers2287/.claude/skills")
        if skills_dir.exists():
            return len(list(skills_dir.glob("*.md")))
        return 0

    def _count_enabled_mcps(self) -> int:
        """Count enabled MCP servers in filtered config."""
        filtered_path = Path("/home/crogers2287/.claude/mcp.json.filtered")
        if not filtered_path.exists():
            # Try to count from global config
            global_path = Path("/home/crogers2287/.claude/mcp.json")
            if global_path.exists():
                try:
                    with open(global_path, 'r') as f:
                        data = json.load(f)
                    servers = data.get("mcpServers", {})
                    # Count enabled servers
                    enabled = [s for s, config in servers.items() if config.get("enabled") == True]
                    return len(enabled)
                except:
                    pass
            return 0

        try:
            with open(filtered_path, 'r') as f:
                data = json.load(f)
            return len(data.get("mcpServers", {}))
        except:
            return 0

    def _load_skills_reference(self) -> List[Dict[str, str]]:
        """Load skills reference from memory."""
        return [
            {"skill": "auto-workflow", "purpose": "MAGIC: Context→Plan→Review", "when": "START HERE"},
            {"skill": "preflight-check", "purpose": "Environment validation", "when": "Start of task"},
            {"skill": "docs-first", "purpose": "Read project docs", "when": "Before planning"},
            {"skill": "negative-cache", "purpose": "Check past failures", "when": "Before planning"},
            {"skill": "local-context", "purpose": "Semantic code search", "when": "Before planning (auto)"},
            {"skill": "dependency-check", "purpose": "Validate imports", "when": "Before coding"},
            {"skill": "git-handbrake", "purpose": "Snapshot for rollback", "when": "Before edits"},
            {"skill": "lint-gate", "purpose": "Pre-LLM filter", "when": "After code, before review"},
            {"skill": "tdd-enforcer", "purpose": "Write failing test first", "when": "Bug fixes"},
            {"skill": "secret-guard", "purpose": "Scan for credentials", "when": "Before commit"},
            {"skill": "failure-playbooks", "purpose": "Typed error recovery", "when": "When errors occur"},
            {"skill": "dev-browser", "purpose": "Headless Playwright", "when": "UI testing"},
            {"skill": "context7", "purpose": "Library docs", "when": "Need API info"},
            {"skill": "codex", "purpose": "OpenAI review", "when": "Plan review"},
            {"skill": "gemini", "purpose": "Google review", "when": "Plan review"},
            {"skill": "sequential-thinking", "purpose": "Step reasoning", "when": "Complex planning"},
            {"skill": "serena", "purpose": "Semantic code retrieval & editing", "when": "Code navigation/editing"},
            {"skill": "auto-serena", "purpose": "Magic code navigation", "when": "Automatic (via hooks)"}
        ]

    def analyze_user_prompt(self, prompt: str) -> Dict[str, Any]:
        """Analyze user prompt and provide pipeline guidance."""
        prompt_lower = prompt.lower()

        analysis = {
            "prompt": prompt,
            "detected_intent": "general",
            "recommended_phase": "CONTEXT",
            "recommended_skills": [],
            "recommended_mcps": [],
            "auto_serena_detected": False,
            "workflow_guidance": []
        }

        # Detect intent
        if any(word in prompt_lower for word in ["find", "where is", "show me", "navigate", "go to"]):
            analysis["detected_intent"] = "code_navigation"
            analysis["recommended_phase"] = "CONTEXT"
            analysis["auto_serena_detected"] = True
            analysis["workflow_guidance"].append("Auto-Serena will automatically help with code navigation")

        if any(word in prompt_lower for word in ["add", "insert", "update", "modify", "edit"]):
            analysis["detected_intent"] = "code_modification"
            analysis["recommended_phase"] = "SAFETY"
            analysis["recommended_skills"].append("git-handbrake")
            analysis["workflow_guidance"].append("Run git-handbrake before making changes")

        if any(word in prompt_lower for word in ["bug", "fix", "error", "issue", "problem"]):
            analysis["detected_intent"] = "bug_fix"
            analysis["recommended_phase"] = "PLAN"
            analysis["recommended_skills"].append("tdd-enforcer")
            analysis["workflow_guidance"].append("Use tdd-enforcer: write failing test first")

        if any(word in prompt_lower for word in ["new feature", "implement", "create", "build"]):
            analysis["detected_intent"] = "feature_implementation"
            analysis["recommended_phase"] = "CONTEXT"
            analysis["recommended_skills"].append("auto-workflow")
            analysis["workflow_guidance"].append("START HERE: Use auto-workflow skill")

        # Recommend skills based on intent
        if analysis["detected_intent"] in ["feature_implementation", "code_modification"]:
            analysis["recommended_skills"].extend(["docs-first", "negative-cache"])
            analysis["recommended_mcps"].append("context7")

        if analysis["detected_intent"] in ["bug_fix", "code_modification"]:
            analysis["recommended_mcps"].append("sequential-thinking")

        # Always recommend memory commit
        analysis["workflow_guidance"].append("After task: mcp__unified-orchestrator__smart_remember")

        return analysis

    def generate_session_guidance(self) -> Dict[str, Any]:
        """Generate comprehensive session guidance."""
        return {
            "session_start_time": self._get_timestamp(),
            "project": self.project,
            "agent_type": "Global Pipeline Agent",
            "pipeline_status": self._check_pipeline_status(),
            "guidance": {
                "before_every_action": "DOING: [action]\\nEXPECT: [predicted outcome]\\nIF WRONG: [what that means]",
                "checkpoints": "Max 3 actions before verifying reality matches your model",
                "workflow_reminder": "Follow the 8-phase workflow in order",
                "memory_rule": "After EVERY task: smart_remember with event_type='task_completion'"
            },
            "quick_reference": {
                "phases": list(self.pipeline_knowledge["workflow_phases"].keys()),
                "key_skills": [s["skill"] for s in self.pipeline_knowledge["skills_reference"][:5]],
                "essential_mcps": self.pipeline_knowledge["mcp_requirements"][:3]
            },
            "current_state": {
                "skills_available": self.pipeline_knowledge["installer_details"]["skills_count"],
                "mcp_servers_enabled": self.pipeline_knowledge["installer_details"]["mcp_servers_enabled"],
                "auto_serena_active": True,
                "memory_system_active": True
            }
        }

    def _check_pipeline_status(self) -> Dict[str, Any]:
        """Check if pipeline is properly installed."""
        status = {
            "skills_directory": os.path.exists(".claude/skills"),
            "mcp_config": os.path.exists(".mcp.json") or os.path.exists(".mcp.json.filtered"),
            "claude_md": os.path.exists(".claude/CLAUDE.md"),
            "commands_directory": os.path.exists(".claude/commands")
        }

        status["overall"] = all(status.values())
        status["missing_components"] = [k for k, v in status.items() if not v and k != "overall"]

        return status

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()

    def _build_context_payload(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """Build a compact payload for downstream consumers."""
        prompt = output.get("prompt_analysis", {})
        guidance = prompt.get("workflow_guidance") or []

        return {
            "pipeline": output.get("pipeline_name"),
            "project": output.get("session_guidance", {}).get("project"),
            "status": output.get("session_guidance", {}).get("pipeline_status"),
            "prompt": {
                "text": prompt.get("prompt"),
                "intent": prompt.get("detected_intent"),
                "phase": prompt.get("recommended_phase"),
                "skills": prompt.get("recommended_skills"),
                "mcps": prompt.get("recommended_mcps"),
                "auto_serena": prompt.get("auto_serena_detected"),
                "guidance": guidance[:MAX_GUIDANCE_LINES],
            },
        }

    def _write_context(self, payload: Dict[str, Any]):
        """Persist context with minimal whitespace to save tokens."""
        try:
            OUTPUT_PATH.write_text(json.dumps(payload, separators=(",", ":")))
        except Exception as e:
            print(f"⚠️  Failed to write context file: {e}", file=sys.stderr)

    def run(self, user_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Run the global pipeline agent."""
        session_guidance = self.generate_session_guidance()

        if user_prompt:
            prompt_analysis = self.analyze_user_prompt(user_prompt)
        else:
            prompt_analysis = {"prompt": None, "detected_intent": "session_start"}

        output = {
            **self.pipeline_knowledge,
            "session_guidance": session_guidance,
            "prompt_analysis": prompt_analysis,
            "agent_instructions": [
                "I am the Global Pipeline Agent, deeply knowledgeable about our /p pipeline workflow.",
                "I guide users through our 8-phase workflow with skills priority.",
                "I ensure Auto-Serena magic code navigation works seamlessly.",
                "I enforce memory system usage with smart_remember after every task.",
                "I help users follow our pipeline best practices and avoid common mistakes."
            ],
            "next_actions": [
                "1. Review session guidance above",
                "2. Follow the 8-phase workflow for your task",
                "3. Use recommended skills and MCPs",
                "4. Remember to smart_remember after task completion"
            ]
        }

        # Save compact file for other tools to use
        payload = self._build_context_payload(output) if COMPACT_CONTEXT else output
        self._write_context(payload)

        return output


def main():
    """Main entry point."""
    agent = GlobalPipelineAgent()

    # Get user prompt from command line or environment
    user_prompt = None
    if len(sys.argv) > 1:
        user_prompt = " ".join(sys.argv[1:])
    elif "USER_PROMPT" in os.environ:
        user_prompt = os.environ["USER_PROMPT"]

    result = agent.run(user_prompt)

    # Print summary
    print("=" * 60)
    print("🌐 GLOBAL PIPELINE AGENT ACTIVATED")
    print("=" * 60)
    print(f"Project: {result['session_guidance']['project']}")
    print(f"Pipeline: {result['pipeline_name']}")
    print(f"Skills available: {result['installer_details']['skills_count']}")
    print(f"MCP servers enabled: {result['installer_details']['mcp_servers_enabled']}")
    print()

        if result['prompt_analysis']['prompt']:
            print("📝 Prompt Analysis:")
            print(f"  Intent: {result['prompt_analysis']['detected_intent']}")
            print(f"  Recommended phase: {result['prompt_analysis']['recommended_phase']}")
            if result['prompt_analysis']['recommended_skills']:
                print(f"  Recommended skills: {', '.join(result['prompt_analysis']['recommended_skills'])}")
            if result['prompt_analysis']['workflow_guidance']:
                print("  Guidance:")
                for guidance in result['prompt_analysis']['workflow_guidance'][:MAX_GUIDANCE_LINES]:
                    print(f"    • {guidance}")
            print()

    print("🚀 Quick Start:")
    print("  1. Review the 8-phase workflow")
    print("  2. Use skills priority over MCPs")
    print("  3. Auto-Serena handles code navigation")
    print("  4. smart_remember after EVERY task")
    print()
    print("💾 Context saved to:", OUTPUT_PATH)
    print("=" * 60)


if __name__ == "__main__":
    main()
