#!/usr/bin/env python3
"""dispatch.py — 把一份 prompt 文件派发给指定外部后端,在「当前分支」改代码 + 提交。

固定参数(yolo / 工作目录 / 输出格式)都封装在这里;主 agent 只需:
  1) 把拼好的派发 prompt 写进一个文件
  2) 跑 dispatch.py <后端名> <仓库根> <prompt文件> [模型]
不用记各后端各自的 flag。

prompt 以 argv 列表传给后端进程(不经过 shell),所以再长、带引号或换行都安全。

输出契约(与后端无关):
  stdout = 后端最终消息(报告,仅供参考;真正的依据是主 agent 的 git diff)
  stderr = 全过程日志
  退出码 = 后端退出码;参数错误 / 后端没装 / 未知后端 → 2 并在 stderr 说明。

要支持一个新后端:在 BACKENDS 里加一个 handler(怎么调用),并在
detect-backends.py 的 KNOWN_BACKENDS 里加一项(怎么探测)即可。
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def die(msg):
    print(f"dispatch.py: {msg}", file=sys.stderr)
    sys.exit(2)


def run_codex(repo, prompt, model):
    """codex exec:必须无沙箱(yolo)—— 否则 -s workspace-write 会禁写 .git,执行者能改
    代码但 git add 报 Operation not permitted、拿不到提交。工作目录=仓库根;最终消息写
    临时文件再读到 stdout;过程日志(含 codex 自己的 stdout)全导到 stderr,不污染
    当报告用的 stdout。"""
    if not shutil.which("codex"):
        die("codex 未安装(PATH 上没有 codex)")
    fd, out_path = tempfile.mkstemp(suffix=".txt")
    os.close(fd)
    cmd = ["codex", "exec", prompt, "-C", repo,
           "--dangerously-bypass-approvals-and-sandbox"]
    if model:
        cmd += ["-m", model]
    cmd += ["--output-last-message", out_path]
    rc = subprocess.run(cmd, stdout=sys.stderr).returncode
    try:
        sys.stdout.write(Path(out_path).read_text(encoding="utf-8"))
    except OSError:
        pass
    finally:
        Path(out_path).unlink(missing_ok=True)
    return rc


def run_cursor(repo, prompt, model):
    """cursor-agent:--yolo(=--force,Run Everything)放开 write/shell 才能改+提交;
    --output-format text 时 stdout 即最终消息,直接继承;不传 -w/--worktree(那会跑到
    隔离 worktree)。"""
    if not shutil.which("cursor-agent"):
        die("cursor-agent 未安装(PATH 上没有 cursor-agent)")
    cmd = ["cursor-agent", "-p", prompt, "--workspace", repo]
    if model:
        cmd += ["-m", model]
    cmd += ["--output-format", "text", "--yolo"]
    return subprocess.run(cmd).returncode


# 后端名 → handler。加新后端在这里加一项(并在 detect-backends.py 加探测)。
BACKENDS = {
    "codex": run_codex,
    "cursor": run_cursor,
}


def main(argv):
    if len(argv) < 3:
        die("用法: dispatch.py <后端名> <仓库根> <prompt文件> [模型]")
    backend, repo, pf = argv[0], argv[1], argv[2]
    model = argv[3] if len(argv) > 3 else ""

    if not Path(repo).is_dir():
        die(f"仓库目录不存在: {repo}")
    if not Path(pf).is_file():
        die(f"prompt 文件不存在: {pf}")

    handler = BACKENDS.get(backend)
    if handler is None:
        die(f"未知后端: {backend}(支持: {', '.join(BACKENDS)})")

    prompt = Path(pf).read_text(encoding="utf-8")
    sys.exit(handler(repo, prompt, model))


if __name__ == "__main__":
    main(sys.argv[1:])
