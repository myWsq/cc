# dev-skills

简体中文 | [English](README.md)

`dev-skills` 是一组面向 agent 的计划驱动开发 skills。它把一次开发任务拆成三个清晰阶段：代码探索、实现规划、计划执行。目标是让 agent 在动手前先建立足够上下文，在实现前形成可复核的计划，并在落地后用验证命令和 git diff 完成收尾检查。

它也用于跨 agent 协同：用更“聪明”的 agent 做探索和计划，用更便宜、更快速的 agent 按计划实现，最后再由主 agent 评审 diff 和验证结果。

本仓库支持三种分发方式：

- 作为 Codex 插件市场中的 `dev` 插件安装；
- 作为 Claude Code 插件市场中的 `dev` 插件安装；
- 只需要部分流程时，通过 [`npx skills`](https://github.com/vercel-labs/skills) 按 skill 安装。

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

### 作为 Codex 插件安装

```bash
codex plugin marketplace add myWsq/dev-skills
codex plugin add dev@dev-skills
```

安装后会得到名为 `dev` 的插件，包含本仓库的三个 skills。

### 作为 Claude Code 插件安装

```text
/plugin marketplace add myWsq/dev-skills
/plugin install dev@dev-skills
```

安装后会得到名为 `dev` 的插件，包含本仓库的三个 skills。

### 通过 `npx skills` 安装单个 skill

当你只需要某一个 skill，或目标 agent 直接消费普通 `SKILL.md` 目录时，使用这种方式。

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

## 使用建议

当需求还不清晰、涉及的代码路径不明确，或者需要先确认现有架构和验证方式时，使用 `dev-explore`。该 skill 只读代码，不创建计划文件，也不修改源码。

当需求已经清楚，需要把它转换成可交给 agent 执行的步骤时，使用 `dev-write-plan`。生成的计划会包含范围、步骤、验证命令、完成标准和停止条件。

当 `plans/` 下已经有实现计划，需要在当前分支落地时，使用 `dev-execute-plan`。它会检查工作区状态，按计划执行，并用提交记录和 diff 作为后续评审边界。

推荐工作流：

```text
聪明 agent：dev-explore -> dev-write-plan
便宜快速 agent：dev-execute-plan
主 agent：评审 diff 和验证结果
```

示例：

```text
用 dev-explore 先帮我理清这个仓库的认证流程。
用 dev-explore 看一下 billing 这块，先不要改代码。

用 dev-write-plan 规划一下新增密码重置功能。
用 dev-write-plan 把这个 bug report 写成实现计划。

用 dev-execute-plan 落地 plans/001。
用 dev-execute-plan 执行下一个 TODO 计划。
用 dev-execute-plan 把 plans/002 委派给更快的本地 agent 实现，并评审结果。
```

## 许可证

MIT
