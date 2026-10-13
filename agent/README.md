# Workspace Agent

A small command-line agent on the Claude API. Claude picks the tools, the SDK tool runner executes them and loops until the job is done. File access is locked to `agent/workspace/`.

## Run it

```bash
pip install -r agent/requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...   # or: ant auth login
python agent/agent.py
```

Try: `make a file called plan.md with a 3 step plan for launching a workshop, then read it back to me`.

## Tools

| Tool | What it does |
| --- | --- |
| `list_files` | Lists files in the workspace |
| `read_file` | Reads a workspace file |
| `write_file` | Creates or overwrites a workspace file |
| `current_datetime` | Returns local date and time |

Add a tool by writing a function with `@beta_tool`, a docstring and typed arguments, then adding it to `TOOLS`. The docstring is what Claude reads to decide when to use it, so write it carefully.

## Settings

Model `claude-opus-5-5` at effort `medium`. Server-side refusal fallback is on (`fallbacks="default"`), so a declined request is retried on a suitable model instead of just failing; remove those two lines in `run_turn` to turn it off.
