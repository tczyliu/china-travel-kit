# 华行志 · Huaxingzhi

> 可溯源的中国入境自由行规划 Skill 与开放知识库

[English](README.md) · [项目分析](PROJECT_STRATEGY.zh-CN.md) · [路线图](ROADMAP.md) · [贡献指南](CONTRIBUTING.md)

当前版本：**v0.4.0 Alpha**

华行志（技术项目名 China Travel Kit）是一个面向入境中国旅行的中英双语 Agent Skill 与开放数据项目。它可以根据人数、日期、目的地、兴趣、节奏、预算和行动需求自动匹配当前数据覆盖的最佳方案。同一份带来源、带核验日期的数据，可以通过 Skill、中文可视化查询页、命令行、HTTP API 和 MCP 被人、应用与 AI 助手调用。

当前版本是 **Alpha 数据集与开发者预览版**。现收录北京、上海、广州、深圳、成都、西安、杭州、丽江 8 个城市共 56 个地点。首批扩充优先处理一线与重点旅游城市的 5A/4A 景区；它仍是可持续核验的数据起点，不代表完整城市攻略。

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
python3 -m china_travel_kit search 博物馆 --city 北京
python3 -m china_travel_kit recommend '第一次来，想看熊猫和吃美食' --travelers 2 --start-date 2026-07-10 --end-date 2026-07-12 --pace relaxed
python3 -m china_travel_kit areas --city 北京
python3 -m china_travel_kit prepare 成都 --month 7
python3 -m china_travel_kit plan 丽江 --days 2 --interests mountain photography
python3 -m china_travel_kit emergency 丽江
python3 -m china_travel_kit validate
python3 -m unittest discover -s tests -v
```

启动本地 API：

```bash
python3 -m china_travel_kit serve
```

然后打开 [http://127.0.0.1:8765/](http://127.0.0.1:8765/)，即可通过中文表单筛选地点、查看来源与核验状态，并生成每日行程卡片。

启动 MCP 服务器：

```bash
python3 -m china_travel_kit mcp
```

详细配置与接口说明见 [英文 README](README.md)。

## 作为 Agent Skill 使用

仓库根目录的 [`SKILL.md`](SKILL.md) 是正式 Skill 入口，定义了适用场景、双语地名规则、可信来源边界，以及静态季节建议与实时天气的区别。`references/` 仅在处理安全求助或多日路线时加载，避免普通查询占用过多上下文。

当前 Skill 可自动整理用户自由文本与表单条件，在已覆盖城市中给出带匹配理由的方案；也可单独查询景点、住宿区域与景点街区，生成按月份的穿衣和装备建议，规划城市行程草案，并返回带来源和核验日期的应急信息。每个城市还提供政府文旅入口，用于继续核验当地文旅动态、景区公告、公共服务和节庆活动。匹配分仅表示当前开放数据与需求的吻合程度，不是对中国城市的客观排名。区域查询不收集住宅居民或家庭信息。

## 为什么不一次铺满所有城市

对开源数据项目而言，少量有来源、能校验、能查询的数据，比 300 个只有名字的城市空壳更有价值。当前 8 城批次用于验证国际门户、古都、主题度假区、湖泊湿地、高海拔等不同数据压力。项目中的“一线/二线”仅是维护优先级，不作为官方城市分类；景区等级则必须保留官方来源、核验日期和适用范围。

## 数据与合规

- 优先使用景区官方页面、政府开放数据、OpenStreetMap、Wikidata 与贡献者原创整理；
- 禁止搬运携程、点评、马蜂窝或自媒体内容；
- 不将本项目作为签证、医疗、法律或应急服务；
- 高时效信息必须能说明来源和最后核验日期。

代码采用 [MIT](LICENSE)，`data/` 下的旅行数据采用 [CC BY-SA 4.0](DATA_LICENSE.md)。
