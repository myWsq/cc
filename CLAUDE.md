# dev-skills

这是一个 agent skills 仓库,由 agent 维护,通过 [`npx skills`](https://github.com/vercel-labs/skills) 分发,与具体 agent 解耦。每个 skill 是 `skills/<名字>/SKILL.md`,辅助文件放在同目录下,随安装一起带走。

## 结构

```
skills/<名字>/
  SKILL.md      # 入口,frontmatter 必须有 name + description
  scripts/      # (可选)skill 用到的脚本
  references/   # (可选)按需加载的参考文档
```

`npx skills add <owner>/<repo>` 会把整个 skill 目录复制到目标 agent 的 skills 目录(`.claude/skills/<名字>/` 等),所以脚本/参考必须放在 skill 目录内。

## 加一个新 skill

1. 在 `skills/` 下建目录,例如 `skills/my-skill/`
2. 写 `skills/my-skill/SKILL.md`,frontmatter 至少有 `name`(小写、连字符)和 `description`(说清做什么 + 何时用)
3. 辅助脚本/文档放进同目录的 `scripts/` / `references/`
4. 本地验证 CLI 能识别:`npx skills add . --list` 应列出新 skill
5. 提交推送

## 注意

- **不要依赖 agent 专属变量**(如 `${CLAUDE_PLUGIN_ROOT}`)。引用脚本用「相对本 skill 目录」的写法,执行时以 SKILL.md 所在目录的绝对路径为基准(见 `dev-execute-plan` 调 `scripts/` 的用法)。
- **SKILL.md 之间互相指路用名字**(如 配套 skill `dev-write-plan`),别写 `../其他skill/SKILL.md` 这种跨目录相对链接——用户可能只单装了一个 skill,跨目录链接会断;skill **内部**指向自己的 `references/` 则用相对路径没问题。
- 这是纯 skills 仓库,没有 `plugin.json` / `marketplace.json`,也没有 version-bump 流程。
