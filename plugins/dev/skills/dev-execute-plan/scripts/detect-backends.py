#!/usr/bin/env python3
"""detect-backends.py — 探测本机可用的 dev-execute-plan 执行方式。

dev-execute-plan 在「选执行方式」那步跑它:根据机器实际装了哪些 agent CLI,
给出可选项,免得把任务委派给一个根本没装的后端。只读探测,不改任何东西。

执行方式:
  self    主 agent 自己实现 —— 默认。就是跑 dev-execute-plan 的这个 agent 直接动手,
          不依赖任何二进制,所以恒列为可用。
  其余    委派给外部 agent 子进程(见下方 KNOWN_BACKENDS 表),各需对应 CLI 在 PATH 上。

要支持一个新外部后端:往 KNOWN_BACKENDS 加一项(怎么探测),并在 dispatch.py 的
BACKENDS 里加一个 handler(怎么调用)即可 —— SKILL.md / backends.md 都不用动。

输出分两部分:给人看的清单 + 给 agent 解析的机器可读行(BACKENDS=... / DEFAULT=...)。
退出码恒为 0:探测结果是数据,不是成败。
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

HOME = Path.home()

# 已知外部后端表 —— 加新后端只改这里(探测)+ dispatch.py(调用)。
#   key        机器可读名(进 BACKENDS)
#   label      给人看的简述
#   bin        要在 PATH 上的可执行名
#   auth_files 任一存在即视为「已配置认证」
#   auth_envs  任一非空环境变量即视为「已配置认证」
KNOWN_BACKENDS = [
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
    print("dev-execute-plan 执行方式探测")
    print("==========================")
    print()

    available = ["self"]  # self 恒可用

    print(f"{OK} self     主 agent 自己实现  —— 始终可用,默认")

    for be in KNOWN_BACKENDS:
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
    print("BACKENDS=" + ",".join(available))
    print("DEFAULT=self")


if __name__ == "__main__":
    main()
