# cc-marketplace

这是一个 Claude Code 插件市场。根目录的 `.claude-plugin/marketplace.json` 是插件清单，所有插件放在 `plugins/<名字>/`。

加新插件时记得两件事：

1. 在 `marketplace.json` 的 `plugins` 数组里登记它。
2. 插件的 `skills/`、`commands/`、`agents/`、`hooks/` 放在插件根目录下，`.claude-plugin/` 里只放 `plugin.json`。

改动插件后，bump 一下 `plugin.json` 和 `marketplace.json` 里对应的 `version`，用户才会收到更新。
