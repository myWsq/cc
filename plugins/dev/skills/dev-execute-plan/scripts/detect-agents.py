#!/usr/bin/env python3
"""Detect agent CLIs that dev-execute-plan can delegate to.

Self-execution is the default dev-execute-plan behavior and is not reported here.
The machine-readable output is:

    AGENTS=codex,cursor,claude

Only detected agent CLIs are included.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

HOME = Path.home()

KNOWN_AGENTS = [
    {
        "key": "codex",
        "label": "codex exec",
        "bin": "codex",
        "auth_files": [HOME / ".codex" / "auth.json"],
        "auth_envs": [],
    },
    {
        "key": "cursor",
        "label": "cursor-agent",
        "bin": "cursor-agent",
        "auth_files": [HOME / ".cursor" / "cli-config.json"],
        "auth_envs": ["CURSOR_API_KEY"],
    },
    {
        "key": "claude",
        "label": "claude headless",
        "bin": "claude",
        "auth_files": [HOME / ".claude.json", HOME / ".claude" / ".credentials.json"],
        "auth_envs": ["ANTHROPIC_API_KEY"],
    },
]

OK, NO, WARN = "[ok]", "[no]", "[!]"


def version_line(binary: str) -> str:
    try:
        out = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        ).stdout
        return out.splitlines()[0].strip() if out and out.strip() else ""
    except Exception:
        return ""


def has_auth(agent: dict) -> bool:
    if any(path.exists() for path in agent["auth_files"]):
        return True
    return any(os.environ.get(name) for name in agent["auth_envs"])


def main() -> None:
    print("dev-execute-plan delegated agent detection")
    print("==========================================")
    print()

    available: list[str] = []

    for agent in KNOWN_AGENTS:
        path = shutil.which(agent["bin"])
        if not path:
            print(f"{NO} {agent['key']:<8} {agent['label']:<15} not installed")
            continue

        version = version_line(agent["bin"])
        version_suffix = f" ({version})" if version else ""
        auth = "authenticated" if has_auth(agent) else "auth not detected"
        marker = OK if has_auth(agent) else WARN
        print(f"{marker} {agent['key']:<8} {agent['label']:<15} {path}{version_suffix} {auth}")
        available.append(agent["key"])

    print()
    print("AGENTS=" + ",".join(available))


if __name__ == "__main__":
    main()
