"""A small command-line AI agent built on the Claude API tool runner.

Claude decides which tools to call; the SDK runs them and loops until the
task is done. File tools are confined to the ./workspace folder.
"""

import datetime
import pathlib
import sys

import anthropic
from anthropic import beta_tool

MODEL = "claude-opus-5-5"
WORKSPACE = (pathlib.Path(__file__).parent / "workspace").resolve()
WORKSPACE.mkdir(exist_ok=True)

SYSTEM = (
    "You are a practical assistant working inside a local workspace folder. "
    "Use the tools to inspect and create files when the task calls for it, "
    "and answer directly when it does not. Keep replies short and concrete."
)


def _safe_path(relative: str) -> pathlib.Path:
    path = (WORKSPACE / relative).resolve()
    if not path.is_relative_to(WORKSPACE):
        raise ValueError(f"{relative!r} is outside the workspace")
    return path


@beta_tool
def list_files() -> str:
    """List every file in the workspace, with sizes in bytes."""
    files = [p for p in WORKSPACE.rglob("*") if p.is_file()]
    if not files:
        return "The workspace is empty."
    return "\n".join(f"{p.relative_to(WORKSPACE)} ({p.stat().st_size} bytes)" for p in files)


@beta_tool
def read_file(path: str) -> str:
    """Read a text file from the workspace.

    Args:
        path: File path relative to the workspace, e.g. notes/todo.md.
    """
    try:
        return _safe_path(path).read_text(encoding="utf-8")
    except (OSError, ValueError) as e:
        return f"Error: {e}"


@beta_tool
def write_file(path: str, content: str) -> str:
    """Create or overwrite a text file in the workspace.

    Args:
        path: File path relative to the workspace, e.g. reports/summary.md.
        content: The full text to write.
    """
    try:
        target = _safe_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"Wrote {len(content)} characters to {path}"
    except (OSError, ValueError) as e:
        return f"Error: {e}"


@beta_tool
def current_datetime() -> str:
    """Return the current local date and time in ISO format."""
    return datetime.datetime.now().isoformat(timespec="seconds")


TOOLS = [list_files, read_file, write_file, current_datetime]


def run_turn(client: anthropic.Anthropic, messages: list) -> None:
    """Run one user turn to completion, appending everything to `messages`."""
    runner = client.beta.messages.tool_runner(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM,
        tools=TOOLS,
        messages=messages,
        output_config={"effort": "medium"},
        # If a safety classifier declines, retry on a suitable fallback model.
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    )
    for message in runner:
        messages.append({"role": "assistant", "content": message.content})
        for block in message.content:
            if block.type == "text" and block.text.strip():
                print(f"\nClaude: {block.text}")
            elif block.type == "tool_use":
                print(f"  [tool] {block.name}({block.input})")
        tool_response = runner.generate_tool_call_response()
        if tool_response is not None:
            messages.append(tool_response)
        if message.stop_reason == "refusal":
            print("\nClaude declined this request.")


def main() -> None:
    client = anthropic.Anthropic()
    messages: list = []
    print(f"Agent ready. Workspace: {WORKSPACE}\nType 'exit' to quit.")
    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if user_input.lower() in {"exit", "quit"}:
            break
        if not user_input:
            continue
        checkpoint = len(messages)
        messages.append({"role": "user", "content": user_input})
        try:
            run_turn(client, messages)
        except anthropic.AuthenticationError:
            sys.exit("No valid API key. Set ANTHROPIC_API_KEY or run `ant auth login`.")
        except anthropic.RateLimitError:
            print("Rate limited, wait a moment and try again.")
            del messages[checkpoint:]
        except anthropic.APIStatusError as e:
            print(f"API error {e.status_code}: {e.message}")
            del messages[checkpoint:]
        except anthropic.APIConnectionError:
            print("Could not reach the API, check your connection.")
            del messages[checkpoint:]


if __name__ == "__main__":
    main()
