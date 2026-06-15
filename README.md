# cc-marketplace

一个个人的 Claude Code 插件市场。

## 使用

```text
/plugin marketplace add myWsq/cc-marketplace
/plugin install hello-world@cc-marketplace
```

## 加一个新插件

1. 在 `plugins/` 下建目录，例如 `plugins/my-tool/`
2. 写 `plugins/my-tool/.claude-plugin/plugin.json`（至少要有 `name`）
3. 放内容：`skills/<名字>/SKILL.md`、`commands/*.md`、`agents/*.md`、`hooks/hooks.json`（按需）
4. 在 `.claude-plugin/marketplace.json` 的 `plugins` 里登记它
5. 本地测试 `claude --plugin-dir ./plugins/my-tool`，然后提交推送

可直接复制 `plugins/hello-world/` 作为模板。

> 注意：`skills/`、`commands/` 等要放在插件根目录下，`.claude-plugin/` 里只放 `plugin.json`。
