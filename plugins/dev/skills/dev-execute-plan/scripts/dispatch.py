#!/usr/bin/env python3
"""dispatch.py — 把一份 prompt 文件派发给指定 agent CLI,在「当前分支」改代码 + 提交。

固定参数(yolo / 跳权限 / 工作目录)都封装在这里;主 agent 只需:
  1) 把拼好的派发 prompt 写进一个文件
  2) 跑 dispatch.py <agent名> <仓库根> <prompt文件> [模型]
不用记各 agent CLI 各自的 flag。

prompt 以 argv 列表传给 agent 进程(不经过 shell),所以再长、带引号或换行都安全。

输出契约(与 agent 无关):
  stdout = agent 的普通(人类可读)输出 —— 后台盯盘看这里掌握进度,但只是参考
  stderr = agent 自身诊断 / 噪音日志(如 token 刷新报错)
  退出码 = agent 退出码;参数错误 / agent 没装 / 未知 agent → 2 并在 stderr 说明。

为什么不阻塞死等:配合后台运行盯盘。主 agent 用后台方式启动本脚本(如 Claude Code 的
run_in_background),周期性读 stdout 掌握进度、方向跑偏/卡死就直接 kill 早停。但要记牢:
agent 的 stdout 只是参考,真相源永远是 `git diff <基线>..HEAD`——评审依据它,不是这段文字。
脚本只管把 agent 输出如实透传(继承 stdout/stderr),不阻塞、不解析、不抢 stdout。

要支持一个新的可委派 agent:在 AGENTS 里加一个 handler(怎么调用),并在 detect-agents.py 的
KNOWN_AGENTS 里加一项(怎么探测)即可。
"""

import shutil
import subprocess
import sys
from pathlib import Path


def die(msg):
    print(f"dispatch.py: {msg}", file=sys.stderr)
    sys.exit(2)


def run_codex(repo, prompt, model):
    """codex exec:必须无沙箱(yolo)—— 否则 -s workspace-write 会禁写 .git,执行者改了代码
    却 git add 报 Operation not permitted、拿不到提交。不开 --json,用默认人类可读输出:执行
    过程直接打到 stdout(后台盯盘即见进度),codex 自身诊断噪音走 stderr。工作目录=仓库根。
    subprocess 继承本进程 stdout/stderr。"""
    if not shutil.which("codex"):
        die("codex 未安装(PATH 上没有 codex)")
    cmd = ["codex", "exec", prompt, "-C", repo,
           "--dangerously-bypass-approvals-and-sandbox"]
    if model:
        cmd += ["-m", model]
    return subprocess.run(cmd).returncode


def run_cursor(repo, prompt, model):
    """cursor-agent:--yolo(=--force,Run Everything)放开 write/shell 才能改+提交;
    --output-format text 用默认人类可读输出(stdout 即 agent 文字,后台盯盘看进度与结果);
    不传 -w/--worktree(那会跑到隔离 worktree,我们要当前分支)。"""
    if not shutil.which("cursor-agent"):
        die("cursor-agent 未安装(PATH 上没有 cursor-agent)")
    cmd = ["cursor-agent", "-p", prompt, "--workspace", repo]
    if model:
        cmd += ["-m", model]
    cmd += ["--output-format", "text", "--yolo"]
    return subprocess.run(cmd).returncode


def run_claude(repo, prompt, model):
    """claude(Claude Code 自身的 headless 模式)委派给另一个 claude 实例:-p/--print 跑
    headless;--dangerously-skip-permissions 放开权限(等价 yolo)才能改+提交,否则会卡在权限
    询问。用默认人类可读输出(不开 stream-json),agent 文字直接到 stdout。claude 没有「设工作
    目录」flag,直接用 subprocess 的 cwd=仓库根。"""
    if not shutil.which("claude"):
        die("claude 未安装(PATH 上没有 claude)")
    cmd = ["claude", "-p", prompt, "--dangerously-skip-permissions"]
    if model:
        cmd += ["--model", model]
    return subprocess.run(cmd, cwd=repo).returncode


# agent 名 → handler。加新 agent 在这里加一项(并在 detect-agents.py 加探测)。
AGENTS = {
    "codex": run_codex,
    "cursor": run_cursor,
    "claude": run_claude,
}


def main(argv):
    if len(argv) < 3:
        die("用法: dispatch.py <agent名> <仓库根> <prompt文件> [模型]")
    agent, repo, pf = argv[0], argv[1], argv[2]
    model = argv[3] if len(argv) > 3 else ""

    if not Path(repo).is_dir():
        die(f"仓库目录不存在: {repo}")
    if not Path(pf).is_file():
        die(f"prompt 文件不存在: {pf}")

    handler = AGENTS.get(agent)
    if handler is None:
        die(f"未知 agent: {agent}(支持: {', '.join(AGENTS)})")

    prompt = Path(pf).read_text(encoding="utf-8")
    sys.exit(handler(repo, prompt, model))


if __name__ == "__main__":
    main(sys.argv[1:])
