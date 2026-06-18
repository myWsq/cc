# dev-skills

[简体中文](README.zh-CN.md) | English

`dev-skills` is a small collection of agent skills for plan-driven software development. It separates a development task into three explicit phases: code exploration, implementation planning, and plan execution. The goal is to help an agent build enough context before coding, produce a reviewable plan before implementation, and finish with validation commands plus a git diff review.

It is also designed for cross-agent collaboration: use a more capable agent to explore and write the plan, then use a faster or cheaper agent to implement that plan, with the lead agent reviewing the final diff.

This repository supports three distribution paths:

- install the bundled `dev` plugin from a Codex plugin marketplace;
- install the bundled `dev` plugin from a Claude Code plugin marketplace;
- install individual skills with [`npx skills`](https://github.com/vercel-labs/skills) when you only need part of the workflow.

## Skills

| Skill | Purpose | Output |
| --- | --- | --- |
| `dev-explore` | Read the relevant code, identify current behavior, validation commands, conventions, and ambiguous requirements without modifying files. | A codebase map and requirement clarification in the conversation. |
| `dev-write-plan` | Convert a clear requirement into a self-contained, executable, and verifiable implementation plan. | `plans/NNN-*.md` plus the `plans/README.md` index. |
| `dev-execute-plan` | Execute a plan on the current branch, validate it, and commit the work; it can also delegate implementation to a supported local agent and review the resulting diff. | Implementation commits and plan status updates on the current branch. |

The skills can be used independently, but they are designed to work well as a sequence:

```text
dev-explore -> dev-write-plan -> dev-execute-plan
```

## Installation

### Install as a Codex plugin

```bash
codex plugin marketplace add myWsq/dev-skills
codex plugin add dev@dev-skills
```

This installs a plugin named `dev` that includes all three skills in this repository.

### Install as a Claude Code plugin

```text
/plugin marketplace add myWsq/dev-skills
/plugin install dev@dev-skills
```

This installs a plugin named `dev` that includes all three skills in this repository.

### Install individual skills with `npx skills`

Use this path when you only want one skill, or when your agent consumes plain `SKILL.md` directories directly.

Install all skills:

```bash
npx skills add myWsq/dev-skills
```

Install a single skill:

```bash
npx skills add myWsq/dev-skills --skill dev-explore
```

Useful options:

- `--list`: list the skills available in this repository.
- `-g`: install globally for reuse across projects.

## Usage

Use `dev-explore` when the requirement is still unclear, the relevant code path is uncertain, or you need to understand the existing architecture and validation workflow first. This skill is read-only: it does not create plan files or modify source code.

Use `dev-write-plan` when the requirement is clear enough to turn into executable steps for an agent. The generated plan includes scope, steps, validation commands, completion criteria, and stop conditions.

Use `dev-execute-plan` when an implementation plan already exists under `plans/` and should be applied on the current branch. It checks the working tree, follows the plan, and uses commits plus diffs as review boundaries.

Recommended workflow:

```text
smart agent: dev-explore -> dev-write-plan
fast/cheap agent: dev-execute-plan
lead agent: review the diff and validation results
```

Example prompts:

```text
Use dev-explore to understand how authentication works in this repo.
Use dev-explore to inspect the billing flow before we plan changes.

Use dev-write-plan to plan adding password reset support.
Use dev-write-plan to turn this bug report into an implementation plan.

Use dev-execute-plan to implement plans/001.
Use dev-execute-plan to execute the next TODO plan.
Use dev-execute-plan to delegate plans/002 to a faster local agent and review the result.
```

## License

MIT
