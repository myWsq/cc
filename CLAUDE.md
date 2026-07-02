# dev-skills

这是一个 agent skills 仓库,由 agent 维护。**三种分发方式并存,共用同一套顶层 `skills/`**:

1. [`npx skills`](https://github.com/vercel-labs/skills) —— 与具体 agent 解耦,可单装某个 skill;
2. **Claude Code 插件市场** —— 仓库根整体既是 marketplace 又是一个名为 `dev` 的插件,`/plugin marketplace add myWsq/dev-skills` 后 `/plugin install dev@dev-skills` 一次装全;
3. **Codex 插件市场** —— 仓库根整体既是 marketplace 又是一个名为 `dev` 的插件,`codex plugin marketplace add myWsq/dev-skills` 后 `codex plugin add dev@dev-skills` 一次装全。

每个 skill 是 `skills/<名字>/SKILL.md`,辅助文件放在同目录下,随安装一起带走。

## 结构

```
skills/<名字>/
  SKILL.md      # 入口,frontmatter 必须有 name + description
  scripts/      # (可选)skill 用到的脚本
  references/   # (可选)按需加载的参考文档
.claude-plugin/
  marketplace.json   # 插件市场清单(仓库根作为 marketplace)
  plugin.json        # 把仓库根登记为一个名为 dev 的插件
.agents/plugins/
  marketplace.json   # Codex 插件市场清单
plugins/dev/
  .codex-plugin/plugin.json  # Codex 插件 manifest
  skills/                    # Codex 插件打包用的 skill 副本
```

`npx skills add <owner>/<repo>` 会把整个 skill 目录复制到目标 agent 的 skills 目录(`.claude/skills/<名字>/` 等),所以脚本/参考必须放在 skill 目录内。Claude Code 插件侧:`marketplace.json` 里 `dev` 插件 `source: "./"`(指向仓库根),Claude Code 默认扫描根下 `skills/`,**自动加载全部 skill**。
Codex 插件侧:`.agents/plugins/marketplace.json` 里 `dev` 插件 `source.path: "./plugins/dev"`,`plugins/dev/.codex-plugin/plugin.json` 显式声明 `skills: "./skills/"`,Codex 安装后加载全部 skill。

## 加一个新 skill

1. 在 `skills/` 下建目录,例如 `skills/my-skill/`
2. 写 `skills/my-skill/SKILL.md`,frontmatter 至少有 `name`(小写、连字符)和 `description`(说清做什么 + 何时用)
3. 辅助脚本/文档放进同目录的 `scripts/` / `references/`
4. 同步到 Codex wrapper:`rm -rf plugins/dev/skills && cp -R skills plugins/dev/skills`
5. 本地验证 CLI 能识别:`npx skills add . --list` 应列出新 skill
6. 提交推送 —— **npx skills / Claude Code 会读顶层 `skills/`,Codex 会读 `plugins/dev/skills/`;新增或修改 skill 时必须同步这两处**(CI `.github/workflows/check-skill-sync.yml` 会在 push/PR 时 `diff -r` 校验,漏同步会挂检查)

## 注意

- **不要依赖 agent 专属变量**(如 `${CLAUDE_PLUGIN_ROOT}`)。引用脚本用「相对本 skill 目录」的写法,执行时以 SKILL.md 所在目录的绝对路径为基准(见 `dev-execute-plan` 调 `scripts/` 的用法)。这样 npx skills 装 和 Claude Code 插件装 都成立(两种方式下 SKILL.md 与 `scripts/` 始终同目录)。
- **SKILL.md 之间互相指路用名字**(如 配套 skill `dev-write-plan`),别写 `../其他skill/SKILL.md` 这种跨目录相对链接——用户可能只单装了一个 skill,跨目录链接会断;skill **内部**指向自己的 `references/` 则用相对路径没问题。
- Codex plugin 打包当前不会跟随指向仓库顶层的 `skills` 符号链接,所以 `plugins/dev/skills/` 必须是真实文件副本。
- Claude 的 `plugin.json` / `marketplace.json` 都**省略 `version`**,用 git commit SHA 当版本——推一次 commit 即一个新版本,无 version-bump 流程。Codex 的 `plugins/dev/.codex-plugin/plugin.json` 必须写 semver;需要强制刷新本地安装时,用 Codex cachebuster 后缀而不是随手改数字版本。
- 改 plugin 元数据后可跑 `claude plugin validate .` 校验清单合法性。
- 改 Codex plugin 元数据后可跑 `python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/dev` 校验 manifest 合法性(需要 `pyyaml`)。
