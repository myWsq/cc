# dev-skills

一组计划驱动开发的 agent skills:**探路 → 写计划 → 执行计划**。通过 [`npx skills`](https://github.com/vercel-labs/skills) 分发,与具体 agent 解耦——Claude Code、Codex、Cursor、OpenCode 等都能装。也可以作为 Claude Code / Codex 的插件市场整体安装。

## 安装

两种方式,任选其一。

**作为 npx skills**(与具体 agent 解耦,可单装):

```bash
# 装全部三个
npx skills add myWsq/dev-skills

# 按需单装其中一个
npx skills add myWsq/dev-skills --skill dev-explore
```

`--list` 先看仓库里有哪些 skill;`-g` 装到用户级(跨项目可用)。

**作为 Claude Code 插件市场**(整体装为 `dev` 插件,含全部三个 skill):

```text
/plugin marketplace add myWsq/dev-skills
/plugin install dev@dev-skills
```

**作为 Codex 插件市场**(整体装为 `dev` 插件,含全部三个 skill):

```bash
codex plugin marketplace add myWsq/dev-skills
codex plugin add dev@dev-skills
```

## 三个 skill

| skill | 角色 | 产物 |
|-------|------|------|
| **dev-explore** | 探路:摸清代码地形,(若有需求)把模糊需求澄清到能写成步骤 | 对话里的清晰理解(只读,不落文件) |
| **dev-write-plan** | 出方案:把一个需求写成自包含、可执行的实现计划 | `plans/NNN-*.md` |
| **dev-execute-plan** | 落地:在当前分支按计划实现并验证——主 agent 自己实现,或委派 codex / cursor 实现再评审其 diff | 当前分支上的提交 |

三者可单独使用,顺跑时链式交接:dev-explore 摸清地形 → dev-write-plan 写成计划 → dev-execute-plan 落地。

## 兼容性

每个 skill 就是一个 `skills/<名>/SKILL.md`,辅助文件(脚本、参考)放在同目录、随安装一起带过去。frontmatter 用标准的 `name` + `description`,兼容所有读 SKILL.md 的 agent。
