# cc-marketplace

这是一个 Claude Code 插件市场,由 agent 维护。根目录的 `.claude-plugin/marketplace.json` 是插件清单,所有插件放在 `plugins/<名字>/`。

## 加一个新插件

1. 在 `plugins/` 下建目录,例如 `plugins/my-tool/`
2. 写 `plugins/my-tool/.claude-plugin/plugin.json`(至少要有 `name`)
3. 放内容:`skills/<名字>/SKILL.md`、`commands/*.md`、`agents/*.md`、`hooks/hooks.json`(按需)
4. 在 `.claude-plugin/marketplace.json` 的 `plugins` 数组里登记它
5. 本地测试 `claude --plugin-dir ./plugins/my-tool`,然后提交推送

可直接复制 `plugins/hello-world/` 作为模板。

## 注意

- 插件的 `skills/`、`commands/`、`agents/`、`hooks/` 放在插件根目录下,`.claude-plugin/` 里只放 `plugin.json`。
- 改动插件后,bump 一下 `plugin.json` 和 `marketplace.json` 里对应的 `version`,用户才会收到更新。
