# dev-skills

[简体中文](README.zh-CN.md) | English

`dev-skills` is a small collection of agent skills for plan-driven software development. It separates a development task into three explicit phases: code exploration, implementation planning, and plan execution. The goal is to help an agent build enough context before coding, produce a reviewable plan before implementation, and finish with validation commands plus a git diff review.

This repository supports three distribution paths:

- install individual skills with [`npx skills`](https://github.com/vercel-labs/skills);
- install the bundled `dev` plugin from a Claude Code plugin marketplace;
- install the bundled `dev` plugin from a Codex plugin marketplace.

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

### Install with `npx skills`

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

### Install as a Claude Code plugin

```text
/plugin marketplace add myWsq/dev-skills
/plugin install dev@dev-skills
```

This installs a plugin named `dev` that includes all three skills in this repository.

### Install as a Codex plugin

```bash
codex plugin marketplace add myWsq/dev-skills
codex plugin add dev@dev-skills
```

This installs a plugin named `dev` that includes all three skills in this repository.

## Usage

Use `dev-explore` when the requirement is still unclear, the relevant code path is uncertain, or you need to understand the existing architecture and validation workflow first. This skill is read-only: it does not create plan files or modify source code.

Use `dev-write-plan` when the requirement is clear enough to turn into executable steps for an agent. The generated plan includes scope, steps, validation commands, completion criteria, and stop conditions.

Use `dev-execute-plan` when an implementation plan already exists under `plans/` and should be applied on the current branch. It checks the working tree, follows the plan, and uses commits plus diffs as review boundaries.

## Repository Layout

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

The top-level `skills/` directory is the source used by `npx skills` and the Claude Code plugin. The Codex plugin uses `plugins/dev/skills/`, which is a checked-in copy of the same skills because Codex plugin packaging does not currently follow symlinks for this layout.

## Compatibility

Each skill is a standard `skills/<name>/SKILL.md` directory. Helper scripts and reference documents live inside the same skill directory so they are included across installation methods.

The `SKILL.md` frontmatter uses the common `name` and `description` fields. Skills refer to companion skills by name rather than cross-directory relative paths, so a single skill can still work when installed on its own.

## Maintenance

When changing a skill, update the top-level `skills/` directory first, then sync the Codex plugin copy:

```bash
rm -rf plugins/dev/skills
cp -R skills plugins/dev/skills
```

Before publishing, run at least:

```bash
npx skills add . --list
python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/dev
```

If Claude Code plugin metadata changed, also run:

```bash
claude plugin validate .
```

## License

MIT
