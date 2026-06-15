# 维护 cc-marketplace 的指南

这是一个 Claude Code 插件 marketplace 仓库。下面是给 Claude Code 在本仓库工作时的约定。

## 核心规则

- 这是 **marketplace**，不是单个插件。仓库根的 `.claude-plugin/marketplace.json` 是目录清单。
- 所有插件放在 `plugins/<plugin-name>/` 下（由 `marketplace.json` 的 `metadata.pluginRoot: "./plugins"` 指定）。
- 关键陷阱：插件里的 `commands/`、`agents/`、`skills/`、`hooks/` 必须在**插件根目录**下，**不能**放进 `.claude-plugin/`。`.claude-plugin/` 里只放 `plugin.json`。
- 每新增/重命名/删除一个插件，都要同步更新 `marketplace.json` 的 `plugins` 数组。

## 新增插件的标准流程

1. 建目录：`plugins/<name>/.claude-plugin/`。
2. 写 `plugins/<name>/.claude-plugin/plugin.json`：
   ```json
   {
     "name": "<name>",
     "description": "一句话说明插件做什么。",
     "version": "0.1.0",
     "author": { "name": "Shuaiqi Wang", "email": "wsq961@outlook.com" }
   }
   ```
   - `name` 必填，是 skill 的命名空间前缀（如 `/<name>:hello`）。
   - `version` 可选但建议保留：用户只有在 version 变化时才会收到更新。
3. 加内容（按需）：
   - **skill**：`plugins/<name>/skills/<skill>/SKILL.md`，frontmatter 必须含 `description`（决定 Claude 何时自动调用）。
   - **command**：`plugins/<name>/commands/<cmd>.md`，扁平 Markdown 文件。
   - **agent**：`plugins/<name>/agents/<agent>.md`。
   - **hook**：`plugins/<name>/hooks/hooks.json`，格式同 `.claude/settings.json` 里的 `hooks` 对象。
   - **MCP**：`plugins/<name>/.mcp.json`。
4. 在 `.claude-plugin/marketplace.json` 的 `plugins` 数组追加一项：
   ```json
   {
     "name": "<name>",
     "source": "./plugins/<name>",
     "description": "……",
     "version": "0.1.0",
     "author": { "name": "Shuaiqi Wang" }
   }
   ```
5. 测试：`claude --plugin-dir ./plugins/<name>`，会话内用 `/reload-plugins` 热重载。
6. 提交并推送。

## 版本管理

- 改动某个插件后，记得同时 bump 该插件 `plugin.json` 与 `marketplace.json` 里对应条目的 `version`，用户才会收到更新。
- 提交信息建议带上插件名，例如 `feat(hello-world): ...`。
