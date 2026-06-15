#!/usr/bin/env bash
#
# detect-backends.sh — 探测本机可用的 dev-implement 执行方式。
#
# dev-implement 在「选执行方式」那步跑它:根据机器实际装了哪些 agent CLI,
# 给出可选项,免得把任务委派给一个根本没装的后端。只读探测,不改任何东西。
#
# 三种执行方式:
#   self    主 agent 自己实现 —— 默认。就是跑 dev-implement 的这个 Claude 直接动手,
#           不依赖任何二进制,所以恒列为可用。
#   codex   codex exec        —— 委派给外部子进程,需要 `codex` 在 PATH 上。
#   cursor  cursor-agent      —— 委派给外部子进程,需要 `cursor-agent` 在 PATH 上。
#
# 输出分两部分:给人看的清单 + 给 agent 解析的机器可读行(BACKENDS=... / DEFAULT=...)。
# 退出码恒为 0:探测结果是数据,不是成败。

set -u

# ── 小工具 ────────────────────────────────────────────────────────────
mark_ok="[✓]"
mark_no="[✗]"
mark_warn="[!]"

# first_version_line CMD —— 尽量拿一行版本号,拿不到就空串
first_version_line() {
  "$1" --version 2>/dev/null | head -n1 || true
}

available=("self") # self 恒可用

echo "dev-implement 执行方式探测"
echo "=========================="
echo

# ── self(主 agent 自己实现) ─────────────────────────────────────────
echo "$mark_ok self     主 agent 自己实现                    —— 始终可用,默认"

# ── codex ────────────────────────────────────────────────────────────
if codex_path="$(command -v codex 2>/dev/null)"; then
  codex_ver="$(first_version_line codex)"
  if [ -f "$HOME/.codex/auth.json" ]; then
    echo "$mark_ok codex    codex exec    —— $codex_path${codex_ver:+  ($codex_ver)}  已配置认证"
    available+=("codex")
  else
    echo "$mark_warn codex    codex exec    —— $codex_path${codex_ver:+  ($codex_ver)}  但未见 ~/.codex/auth.json,可能需先登录"
    available+=("codex")
  fi
else
  echo "$mark_no codex    codex exec    —— 未安装(command -v codex 无结果)"
fi

# ── cursor ───────────────────────────────────────────────────────────
if cursor_path="$(command -v cursor-agent 2>/dev/null)"; then
  cursor_ver="$(first_version_line cursor-agent)"
  if [ -f "$HOME/.cursor/cli-config.json" ] || [ -n "${CURSOR_API_KEY:-}" ]; then
    echo "$mark_ok cursor   cursor-agent  —— $cursor_path${cursor_ver:+  ($cursor_ver)}  已配置认证"
    available+=("cursor")
  else
    echo "$mark_warn cursor   cursor-agent  —— $cursor_path${cursor_ver:+  ($cursor_ver)}  但未见登录态,可能需先 cursor-agent 登录"
    available+=("cursor")
  fi
else
  echo "$mark_no cursor   cursor-agent  —— 未安装(command -v cursor-agent 无结果)"
fi

# ── 汇总(机器可读) ─────────────────────────────────────────────────
echo
joined="$(IFS=,; echo "${available[*]}")"
echo "BACKENDS=$joined"
echo "DEFAULT=self"
