#!/usr/bin/env bash
#
# dispatch.sh — 把一份 prompt 文件派发给指定外部后端(codex / cursor)。
#
# 固定参数(yolo / 工作目录 / 输出格式)都封装在这里;主 agent 只需:
#   1) 把拼好的派发 prompt 写进一个文件
#   2) 调 dispatch.sh <backend> <repo-root> <prompt-file> [model]
# 不用记 codex/cursor 各自的 flag。脚本让后端在「当前分支」改代码 + 提交,
# 跑完把后端的最终消息(报告)打到 stdout(仅供参考,真正的依据是主 agent 的 git diff)。
#
# 用法:
#   dispatch.sh codex  <仓库根绝对路径> <prompt文件> [模型]
#   dispatch.sh cursor <仓库根绝对路径> <prompt文件> [模型]
#
# stdout = 后端最终消息(报告);stderr = 全过程日志。
# 退出码 = 后端退出码;参数错误 / 后端没装 → 2 并在 stderr 说明。

set -u

backend="${1:-}"
repo="${2:-}"
pf="${3:-}"
model="${4:-}"

die() { echo "dispatch.sh: $*" >&2; exit 2; }

[ -n "$backend" ] && [ -n "$repo" ] && [ -n "$pf" ] || \
  die "用法: dispatch.sh <codex|cursor> <仓库根> <prompt文件> [模型]"
[ -d "$repo" ] || die "仓库目录不存在: $repo"
[ -f "$pf" ]   || die "prompt 文件不存在: $pf"

prompt="$(cat "$pf")"

case "$backend" in
  codex)
    command -v codex >/dev/null 2>&1 || die "codex 未安装(command -v codex 无结果)"
    out="$(mktemp)"
    # 固定:无沙箱(yolo)——否则 workspace-write 禁写 .git,执行者能改代码但 git add
    #       会 Operation not permitted、拿不到提交;工作目录=仓库根;最终消息写 out。
    #       全过程日志(含 codex 自己的 stdout)走 stderr,不污染当报告用的 stdout。
    if [ -n "$model" ]; then
      codex exec "$prompt" -C "$repo" --dangerously-bypass-approvals-and-sandbox \
        -m "$model" --output-last-message "$out" >&2
    else
      codex exec "$prompt" -C "$repo" --dangerously-bypass-approvals-and-sandbox \
        --output-last-message "$out" >&2
    fi
    rc=$?
    cat "$out"
    rm -f "$out"
    exit "$rc"
    ;;
  cursor)
    command -v cursor-agent >/dev/null 2>&1 || die "cursor-agent 未安装(command -v cursor-agent 无结果)"
    # 固定:--yolo(=--force,放开 write/shell 才能改+提交);workspace=仓库根;
    #       text 输出即最终消息;不传 -w/--worktree(那会跑到隔离 worktree)。
    if [ -n "$model" ]; then
      cursor-agent -p "$prompt" --workspace "$repo" -m "$model" --output-format text --yolo
    else
      cursor-agent -p "$prompt" --workspace "$repo" --output-format text --yolo
    fi
    exit "$?"
    ;;
  *)
    die "未知后端: $backend(只支持 codex / cursor)"
    ;;
esac
