# dev-skills

简体中文 | [English](README.md)

`dev-skills` 是一组面向 agent 的计划驱动开发 skills。它把一次开发任务拆成三个清晰阶段：代码探索、实现规划、计划执行。目标是让 agent 在动手前先建立足够上下文，在实现前形成可复核的计划，并在落地后用验证命令和 git diff 完成收尾检查。

本仓库支持三种分发方式：

- 通过 [`npx skills`](https://github.com/vercel-labs/skills) 按 skill 安装；
- 作为 Claude Code 插件市场中的 `dev` 插件安装；
- 作为 Codex 插件市场中的 `dev` 插件安装。

## Skills

| Skill | 作用 | 产物 |
| --- | --- | --- |
| `dev-explore` | 只读分析相关代码，梳理现有实现、验证命令、约定和需求歧义。 | 对话中的代码地形与需求澄清结果。 |
| `dev-write-plan` | 将明确需求写成自包含、可执行、可验证的实现计划。 | `plans/NNN-*.md` 以及 `plans/README.md` 索引。 |
| `dev-execute-plan` | 按计划在当前分支实现、验证并提交；也支持委派本机可用的外部 agent 实现后再评审 diff。 | 当前分支上的实现提交和计划状态更新。 |

三个 skill 可以单独使用，也可以按以下流程串联：

```text
dev-explore -> dev-write-plan -> dev-execute-plan
```

## 安装

### 通过 `npx skills` 安装

安装全部 skills：

```bash
npx skills add myWsq/dev-skills
```

只安装某一个 skill：

```bash
npx skills add myWsq/dev-skills --skill dev-explore
```

常用选项：

- `--list`：查看仓库内可安装的 skills；
- `-g`：安装到用户级目录，跨项目复用。

### 作为 Claude Code 插件安装

```text
/plugin marketplace add myWsq/dev-skills
/plugin install dev@dev-skills
```

安装后会得到名为 `dev` 的插件，包含本仓库的三个 skills。

### 作为 Codex 插件安装

```bash
codex plugin marketplace add myWsq/dev-skills
codex plugin add dev@dev-skills
```

安装后会得到名为 `dev` 的插件，包含本仓库的三个 skills。

## 使用建议

当需求还不清晰、涉及的代码路径不明确，或者需要先确认现有架构和验证方式时，使用 `dev-explore`。该 skill 只读代码，不创建计划文件，也不修改源码。

当需求已经清楚，需要把它转换成可交给 agent 执行的步骤时，使用 `dev-write-plan`。生成的计划会包含范围、步骤、验证命令、完成标准和停止条件。

当 `plans/` 下已经有实现计划，需要在当前分支落地时，使用 `dev-execute-plan`。它会检查工作区状态，按计划执行，并用提交记录和 diff 作为后续评审边界。

## 仓库结构

```text
skills/
  dev-explore/
  dev-write-plan/
  dev-execute-plan/
.claude-plugin/
  marketplace.json
  plugin.json
.agents/plugins/
  marketplace.json
plugins/dev/
  .codex-plugin/plugin.json
  skills/
```

顶层 `skills/` 是 `npx skills` 和 Claude Code 插件使用的源目录。Codex 插件使用 `plugins/dev/skills/`，这是顶层 `skills/` 的受控副本；当前 Codex 插件打包流程不会在该布局下跟随指向顶层目录的符号链接。

## 兼容性

每个 skill 都是标准的 `skills/<name>/SKILL.md` 目录。辅助脚本和参考文档放在同一个 skill 目录下，确保通过不同安装方式分发时能一起带上。

`SKILL.md` frontmatter 使用通用的 `name` 和 `description` 字段。skill 之间通过名称互相引用，而不是依赖跨目录相对路径，因此单独安装某一个 skill 时也能保持基本可用。

## 维护

修改 skill 时，先更新顶层 `skills/`，再同步 Codex 插件副本：

```bash
rm -rf plugins/dev/skills
cp -R skills plugins/dev/skills
```

发布前建议至少执行：

```bash
npx skills add . --list
python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/dev
```

如果修改了 Claude Code 插件元数据，也执行：

```bash
claude plugin validate .
```

## 许可证

MIT
