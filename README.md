# Huaxingzhi · 华行志

> A source-aware China travel planning Skill and open knowledge base for humans, apps, and AI agents.

[简体中文](README.zh-CN.md) · [Project analysis (中文)](PROJECT_STRATEGY.zh-CN.md) · [Roadmap](ROADMAP.md) · [Contributing](CONTRIBUTING.md)

Current version: **v0.5.0 Alpha**

Author contact: WeChat `Changzhanzhang`

Huaxingzhi (technical project name: China Travel Kit) is an open, bilingual Agent Skill and travel knowledge base with an explainable requirement matcher, visual Chinese travel finder, zero-runtime-dependency Python query engine, CLI, HTTP API, and MCP server. It focuses on the parts of China travel that are difficult for international visitors to verify: visitor areas, reservations, passport-specific instructions, seasonal risks, accessibility, emergency context, transport context, official city tourism portals, and data freshness.

This is an **alpha dataset and developer preview**, not a booking service or a live navigation system. It currently covers 56 places across Beijing, Shanghai, Guangzhou, Shenzhen, Chengdu, Xi'an, Hangzhou, and Lijiang. The first expansion prioritizes officially sourced 5A/4A attractions in major gateway and tourism cities; none is a complete city guide.

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
python3 -m china_travel_kit search museum --city Beijing
python3 -m china_travel_kit recommend 'First visit: pandas, food, relaxed pace' --travelers 2 --start-date 2026-07-10 --end-date 2026-07-12
python3 -m china_travel_kit areas --city Beijing
python3 -m china_travel_kit prepare 成都 --month 7
python3 -m china_travel_kit plan 丽江 --days 2 --interests mountain photography
python3 -m china_travel_kit emergency 丽江
python3 -m china_travel_kit freshness
python3 -m china_travel_kit integrity
```

## Agent Skill

The repository root is an installable Agent Skill. [`SKILL.md`](SKILL.md) defines when to use the toolkit, how to preserve Chinese and English place names, and when live facts must be rechecked. Conditional safety and itinerary guidance lives in `references/` so ordinary destination searches stay lightweight.

Point an Agent Skills-compatible client at this repository, or clone it into that client's skills directory. The Skill uses the bundled read-only Python engine and does not require an API key for the included data.

Start the visual travel finder:

```bash
python3 -m china_travel_kit serve
```

Then open [http://127.0.0.1:8765/](http://127.0.0.1:8765/) to search attractions and generate itinerary cards in a responsive Chinese interface.

Validate the data and run tests:

```bash
python3 -m china_travel_kit validate
python3 -m unittest discover -s tests -v
```

## MCP server

The server uses MCP over stdio and exposes eight read-only tools:

- `recommend_trip`
- `search_spots`
- `discover_areas`
- `get_city_guide`
- `plan_itinerary`
- `get_trip_preparation`
- `get_emergency_help`
- `check_data_freshness`

Example client configuration:

```json
{
  "mcpServers": {
    "china-travel-kit": {
      "command": "python3",
      "args": ["-m", "china_travel_kit", "mcp"],
      "cwd": "/absolute/path/to/china-travel-kit"
    }
  }
}
```

The implementation targets MCP protocol version `2025-11-25`. It supports `initialize`, `ping`, `tools/list`, and `tools/call` over newline-delimited stdio messages.

## HTTP API

```bash
python3 -m china_travel_kit serve --port 8765
curl 'http://127.0.0.1:8765/search?city=Chengdu&category=wildlife'
curl 'http://127.0.0.1:8765/recommend?requirements=pandas,food&days=3&pace=relaxed'
curl 'http://127.0.0.1:8765/plan?city=Lijiang&days=2&interests=mountain,photography'
```

Available endpoints: `/health`, `/cities`, `/recommend`, `/search`, `/areas`, `/plan`, `/prepare`, `/emergency`, and `/freshness`.

`recommend_trip` ranks only cities covered by the current repository. Its score explains how well the indexed data matches the request; it is not a universal ranking of destinations. Dates, party size, desired places, interests, pace, budget, mobility needs, children, origin, and free text are normalized into one response containing the itinerary, seasonal preparation, stay areas, food, culture, emergency context, unmatched requirements, and live checks still required.

## Data principles

1. **Sources before claims.** Prefer official operators, government open data, Wikidata, OpenStreetMap, and original contributor research.
2. **Freshness is data.** Set `last_verified` to the date you actually checked the linked source.
3. **Unknown beats invented.** Use `null` for changing prices or booking rules you cannot verify.
4. **No scraped commercial guides.** Do not copy Ctrip, Dianping, Mafengwo, or creator content.
5. **Safety needs context.** Altitude, weather, accessibility, permits, and emergency details must be explicit and sourced.
6. **Visitor areas are not private addresses.** Area discovery covers stay areas and attraction neighborhoods, never resident or household data.

See [`data/schema/city.schema.json`](data/schema/city.schema.json) and the existing city files for the current schema.

## Scope and non-goals

The current alpha provides source-aware sample data, explainable local matching, and developer interfaces. It does not provide live weather, live ticket inventory, visa eligibility decisions, hotel rankings, turn-by-turn navigation, or emergency dispatch. Those require authoritative live providers and stronger operational guarantees.

## Licenses

Code is licensed under the [MIT License](LICENSE). Repository travel data under `data/` is licensed under [CC BY-SA 4.0](DATA_LICENSE.md). Third-party source links remain subject to their respective owners' terms.

## Integrity and brand identity

Official releases include `integrity-manifest.json` and its Ed25519 signature. Run `python3 -m china_travel_kit integrity` to authenticate the manifest with the bundled public key and then verify SHA-256 hashes. Require both `valid: true` and `signature_valid: true`. This detects forged manifests, incomplete copies, or tampering; it does not prevent copying allowed by the licenses.

Maintainers run `scripts/update_integrity_manifest.py` and then `scripts/sign_integrity_manifest.py` before a release. The dedicated private key stays outside the repository and must never be committed.

The code and data licenses do not grant rights to present a modified distribution as an official Huaxingzhi release. See [TRADEMARKS.md](TRADEMARKS.md) and [NOTICE](NOTICE).

## Disclaimer

Travel rules, entry policies, opening hours, prices, weather, and transport can change quickly. Always verify critical details with the relevant authority or operator before departure. This project does not provide legal, medical, immigration, booking, or emergency services.
