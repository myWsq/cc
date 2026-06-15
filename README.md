# cc-marketplace

一个个人的 **Claude Code 插件 marketplace**。用于集中托管、分发和版本管理自己的 Claude Code 插件（skills / commands / agents / hooks / MCP servers）。

## 安装与使用

在 Claude Code 中添加本 marketplace（仓库推送到 GitHub 后）：

```text
/plugin marketplace add wsq961/cc-marketplace
```

> 也可以用本地路径调试：`/plugin marketplace add /Users/wsq/Workspace/cc-marketplace`

然后浏览并安装插件：

```text
/plugin                              # 打开插件管理器，浏览/安装
/plugin install hello-world@cc-marketplace
```

更新到 marketplace 的最新版本：

```text
/plugin marketplace update cc-marketplace
```

## 仓库结构

```text
cc-marketplace/
├── .claude-plugin/
│   └── marketplace.json        # marketplace 清单：列出所有插件
├── plugins/                    # 所有插件都放这里（pluginRoot）
│   └── hello-world/            # 示例插件，可直接复制改造
│       ├── .claude-plugin/
│       │   └── plugin.json     # 插件清单
│       ├── skills/
│       │   └── hello/
│       │       └── SKILL.md    # 一个 skill = 一个目录 + SKILL.md
│       ├── commands/           # （可选）扁平的 .md 命令文件
│       ├── agents/             # （可选）自定义 agent
│       ├── hooks/
│       │   └── hooks.json      # （可选）事件钩子
│       └── .mcp.json           # （可选）MCP server 配置
└── README.md
```

## 添加一个新插件

详见 [`CLAUDE.md`](./CLAUDE.md)，简要步骤：

1. 在 `plugins/` 下新建目录，例如 `plugins/my-tool/`。
2. 创建 `plugins/my-tool/.claude-plugin/plugin.json`（至少 `name`）。
3. 添加内容：`skills/<name>/SKILL.md`、`commands/*.md`、`agents/*.md`、`hooks/hooks.json` 等。
4. 在 `.claude-plugin/marketplace.json` 的 `plugins` 数组里登记这个插件。
5. 本地测试：`claude --plugin-dir ./plugins/my-tool`。
6. 提交并推送到 GitHub。

## 本地开发与测试

```bash
# 单独加载某个插件测试（无需安装）
claude --plugin-dir ./plugins/hello-world

# 修改后在会话里热重载
/reload-plugins

# 校验插件清单是否合法
claude plugin validate ./plugins/hello-world
```

## License

MIT
