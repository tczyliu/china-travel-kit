# China Travel Kit：中国入境旅行开放知识库

[English](README.md) · [项目分析](PROJECT_STRATEGY.zh-CN.md) · [路线图](ROADMAP.md) · [贡献指南](CONTRIBUTING.md)

China Travel Kit 是一个面向入境中国旅行的中英双语开放数据项目。同一份带来源、带核验日期的数据，可以通过中文可视化查询页、命令行、HTTP API 和 MCP 被人、应用与 AI 助手调用。

当前版本是 **Alpha 数据集与开发者预览版**。北京、成都、丽江各有 2 个地点，用于展示完整的数据贡献闭环，并不代表完整攻略。

## 项目解决什么问题

普通旅行攻略很多，但外国游客真正容易踩坑的内容——护照预约、支付与网络、季节风险、高海拔、无障碍、数据是否过期——通常缺少结构化表达，也无法被可靠复用。

本项目的核心不是“AI 自动生成攻略”，而是：

- 旅游事实存为可审查、可提交 PR 的 JSON；
- 每个地点都有 `sources` 与 `last_verified`；
- 票价和预约规则无法确认时写 `null`，不猜数字；
- 行程规划采用可解释规则，只生成草案；
- CLI、API 与 MCP 共用同一查询引擎。

## 一分钟运行

需要 Python 3.10 或更高版本，不需要安装运行时依赖。

```bash
git clone https://github.com/tczyliu/china-travel-kit.git
cd china-travel-kit
python -m china_travel_kit search 博物馆 --city 北京
python -m china_travel_kit plan 丽江 --days 2 --interests mountain photography
python -m china_travel_kit validate
python -m unittest discover -s tests -v
```

启动本地 API：

```bash
python -m china_travel_kit serve
```

然后打开 [http://127.0.0.1:8765/](http://127.0.0.1:8765/)，即可通过中文表单筛选地点、查看来源与核验状态，并生成每日行程卡片。

启动 MCP 服务器：

```bash
python -m china_travel_kit mcp
```

详细配置与接口说明见 [英文 README](README.md)。

## 第一版为什么只做 3 个城市

对开源数据项目而言，6 条有来源、能校验、能查询的数据，比 300 个只有名字的城市空壳更有价值。第一版验证的是贡献体验和调用闭环；覆盖量放在后续社区协作中增长。

## 数据与合规

- 优先使用景区官方页面、政府开放数据、OpenStreetMap、Wikidata 与贡献者原创整理；
- 禁止搬运携程、点评、马蜂窝或自媒体内容；
- 不将本项目作为签证、医疗、法律或应急服务；
- 高时效信息必须能说明来源和最后核验日期。

代码采用 [MIT](LICENSE)，`data/` 下的旅行数据采用 [CC BY-SA 4.0](DATA_LICENSE.md)。
