#!/usr/bin/env python3
"""detect-agents.py — 探测本机可委派的 agent CLI。

dev-execute-plan 在「选执行方式」那步跑它:根据机器实际装了哪些 agent CLI,
给出可委派选项,免得把任务委派给一个根本没装的 agent。只读探测,不改任何东西。

执行方式:
  主 agent 自己实现是 dev-execute-plan 的默认行为,不需要探测,也不在本脚本输出里表示。
  AGENTS 只列可委派的 agent CLI(见下方 KNOWN_AGENTS 表),各需对应 CLI 在 PATH 上。

要支持一个新的可委派 agent:往 KNOWN_AGENTS 加一项(怎么探测),并在 dispatch.py 的
AGENTS 里加一个 handler(怎么调用)即可 —— SKILL.md / delegation.md 都不用动。

输出分两部分:给人看的清单 + 给 agent 解析的机器可读行(AGENTS=...)。
AGENTS 只包含可委派 agent;自己实现由 dev-execute-plan 流程默认处理。
退出码恒为 0:探测结果是数据,不是成败。
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

HOME = Path.home()

# 已知可委派 agent 表 —— 加新 agent 只改这里(探测)+ dispatch.py(调用)。
#   key        机器可读名(进 AGENTS)
#   label      给人看的简述
#   bin        要在 PATH 上的可执行名
#   auth_files 任一存在即视为「已配置认证」
#   auth_envs  任一非空环境变量即视为「已配置认证」
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


def version_line(binary):
    """尽量拿一行版本号,拿不到就空串。"""
    try:
        out = subprocess.run(
            [binary, "--version"],
            capture_output=True, text=True, timeout=10,
        ).stdout
        return out.splitlines()[0].strip() if out and out.strip() else ""
    except Exception:
        return ""


def has_auth(be):
    if any(p.exists() for p in be["auth_files"]):
        return True
    return any(os.environ.get(e) for e in be["auth_envs"])


def main():
    print("dev-execute-plan 可委派 agent 探测")
    print("================================")
    print()

    available = []

    for be in KNOWN_AGENTS:
        path = shutil.which(be["bin"])
        if not path:
            print(f"{NO} {be['key']:<8} {be['label']:<13} —— 未安装(PATH 上没有 {be['bin']})")
            continue
        ver = version_line(be["bin"])
        ver_str = f"  ({ver})" if ver else ""
        if has_auth(be):
            print(f"{OK} {be['key']:<8} {be['label']:<13} —— {path}{ver_str}  已配置认证")
        else:
            print(f"{WARN} {be['key']:<8} {be['label']:<13} —— {path}{ver_str}  但未见登录态,可能需先登录")
        available.append(be["key"])

    print()
    print("AGENTS=" + ",".join(available))


if __name__ == "__main__":
    main()
