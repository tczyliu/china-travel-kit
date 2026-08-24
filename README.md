# China Travel Kit

> Source-aware China inbound travel data for humans, apps, and AI agents.

[简体中文](README.zh-CN.md) · [Project analysis (中文)](PROJECT_STRATEGY.zh-CN.md) · [Roadmap](ROADMAP.md) · [Contributing](CONTRIBUTING.md)

China Travel Kit is an open, bilingual travel knowledge base with a zero-runtime-dependency Python query engine, CLI, HTTP API, and MCP server. It focuses on the parts of China travel that are difficult for international visitors to verify: reservations, passport-specific instructions, seasonal risks, accessibility, transport context, and data freshness.

This is an **alpha dataset and developer preview**, not a booking service or a live navigation system. The included Beijing, Chengdu, and Lijiang records demonstrate the contribution model; they are not complete city guides.

## Why this project exists

Travel articles are plentiful. Reusable, source-linked, reviewable China travel data is not. This repository makes each fact easy to inspect and update through pull requests, while letting one data layer power several interfaces:

```text
JSON city records
  ├── CLI search and itinerary drafts
  ├── local HTTP API
  └── MCP tools for AI clients
```

Every attraction record includes `sources` and `last_verified`. Prices and reservation rules are deliberately nullable: an unknown value is safer than a confident but outdated answer.

## Try it in 60 seconds

Requires Python 3.10 or newer. No runtime packages are required.

```bash
git clone https://github.com/tczyliu/china-travel-kit.git
cd china-travel-kit
python -m china_travel_kit search museum --city Beijing
python -m china_travel_kit plan 丽江 --days 2 --interests mountain photography
python -m china_travel_kit freshness
```

Validate the data and run tests:

```bash
python -m china_travel_kit validate
python -m unittest discover -s tests -v
```

## MCP server

The server uses MCP over stdio and exposes four read-only tools:

- `search_spots`
- `get_city_guide`
- `plan_itinerary`
- `check_data_freshness`

Example client configuration:

```json
{
  "mcpServers": {
    "china-travel-kit": {
      "command": "python",
      "args": ["-m", "china_travel_kit", "mcp"],
      "cwd": "/absolute/path/to/china-travel-kit"
    }
  }
}
```

The implementation targets MCP protocol version `2025-11-25`. It supports `initialize`, `ping`, `tools/list`, and `tools/call` over newline-delimited stdio messages.

## HTTP API

```bash
python -m china_travel_kit serve --port 8765
curl 'http://127.0.0.1:8765/search?city=Chengdu&category=wildlife'
curl 'http://127.0.0.1:8765/plan?city=Lijiang&days=2&interests=mountain,photography'
```

Available endpoints: `/health`, `/cities`, `/search`, `/plan`, and `/freshness`.

## Data principles

1. **Sources before claims.** Prefer official operators, government open data, Wikidata, OpenStreetMap, and original contributor research.
2. **Freshness is data.** Set `last_verified` to the date you actually checked the linked source.
3. **Unknown beats invented.** Use `null` for changing prices or booking rules you cannot verify.
4. **No scraped commercial guides.** Do not copy Ctrip, Dianping, Mafengwo, or creator content.
5. **Safety needs context.** Altitude, weather, accessibility, permits, and emergency details must be explicit and sourced.

See [`data/schema/city.schema.json`](data/schema/city.schema.json) and the existing city files for the current schema.

## Scope and non-goals

Version 0.1 provides source-aware sample data and local developer interfaces. It does not provide live weather, live ticket inventory, visa eligibility decisions, hotel recommendations, turn-by-turn navigation, or emergency dispatch. Those require authoritative live providers and stronger operational guarantees.

## Licenses

Code is licensed under the [MIT License](LICENSE). Repository travel data under `data/` is licensed under [CC BY-SA 4.0](DATA_LICENSE.md). Third-party source links remain subject to their respective owners' terms.

## Disclaimer

Travel rules, entry policies, opening hours, prices, weather, and transport can change quickly. Always verify critical details with the relevant authority or operator before departure. This project does not provide legal, medical, immigration, booking, or emergency services.
