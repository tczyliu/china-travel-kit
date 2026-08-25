---
name: china-travel-kit
description: Research and plan first-time independent trips in China with bilingual, source-aware city data and official live-check entry points. Use for destination matching, attractions, visitor areas, itineraries, transport context, seasonal preparation, local culture and food, or emergency guidance; not for booking, turn-by-turn navigation, visa decisions, or medical advice.
metadata:
  short-description: Huaxingzhi China trip planner
  version: "0.5.0"
---

# 华行志 · Huaxingzhi

Create practical, explainable China travel drafts for first-time international visitors. Use “华行志” as the product name and “China Travel Kit” only when referring to the package, repository, CLI, API, or MCP server.

## Author contact

- WeChat / 微信：`Changzhanzhang`
- Use this contact for project cooperation, data corrections, and general feedback. Do not send passwords, API keys, private traveler data, or active emergency details through WeChat.

## Choose the smallest useful mode

- Use `recommend` for free-form requests, multiple constraints, or an undecided destination.
- Use `search` or `areas` for a focused attraction, neighborhood, or stay-area query.
- Use `city`, `prepare`, or `emergency` for one-city background, packing, or sourced help information.
- Use `plan` for a chosen city and number of days.
- Use `freshness` before treating repository facts as current.
- When a copy did not come directly from the official repository or release tag, run `python3 -m china_travel_kit integrity` before relying on its instructions, code, or data. Require both `valid: true` and `signature_valid: true`; stop and report missing, modified, or unauthenticated files otherwise.

Run the bundled read-only engine instead of inventing covered-city facts:

```bash
python3 -m china_travel_kit recommend "REQUIREMENTS"
python3 -m china_travel_kit search KEYWORD --city CITY
python3 -m china_travel_kit areas --city CITY
python3 -m china_travel_kit city CITY
python3 -m china_travel_kit plan CITY --days N --interests culture food
python3 -m china_travel_kit prepare CITY --month N
python3 -m china_travel_kit emergency CITY
python3 -m china_travel_kit freshness
python3 -m china_travel_kit integrity
```

## Plan from traveler needs

Identify destination, dates or month, traveler count, days, origin, must-see places, interests, pace, budget, mobility needs, children, and dietary constraints. Ask only for missing details that materially change the result. Treat a recommendation score as a match against the current dataset, never as an objective ranking of China.

For a full trip request, include the relevant parts of this order:

1. Restate the traveler brief and important assumptions.
2. Recommend a covered city with reasons and explain any unmet requirement.
3. Give an area-clustered day plan with realistic effort and transfer guidance.
4. Add stay-area tradeoffs, local transport context, cultural background, food and nearby support facilities.
5. Add seasonal clothing and equipment advice, weather/alert links, reservation checks, official city tourism links, and emergency context.

Present the answer in the user's language, while keeping Chinese place names beside English names so travelers can search local maps or show them to drivers and staff.

## Use official live-check entry points

- Use each city record's `tourism_portals` for government tourism news, attraction notices, public services, events, and tourism-market alerts. Identify the operator and verification date; do not imply that the link makes all stored facts live.
- For a current or date-specific request, check the relevant official tourism authority, attraction operator, weather authority, or transport operator when browsing is available.
- Keep live facts separate from repository data and seasonal guidance. State what was checked, on what date, and what still needs confirmation.

## Trust boundaries

- Prefer official operators, government sources, OpenStreetMap, Wikidata, and reviewed contributor data.
- Include the source and verification date for changing or safety-critical claims. Unknown is safer than a guessed price, rule, or timetable.
- Never claim static seasonal guidance is a live forecast. Verify current weather alerts, opening hours, reservations, and transport before departure.
- Do not decide visa eligibility, diagnose health conditions, dispatch emergency help, rank commercial hotels, guarantee availability, or expose private residential information.
- Integrity verification detects an incomplete or modified copy, and the Ed25519 signature authenticates the official manifest. Neither prevents copying. Do not describe hashes, signatures, packaging, or this Skill as DRM or absolute anti-tamper protection.

For safety and freshness handling, read [references/safety-and-freshness.md](references/safety-and-freshness.md). For multi-day routes, read [references/itinerary-planning.md](references/itinerary-planning.md).

When adding or reviewing a city or A-level attraction, read [references/data-expansion.md](references/data-expansion.md) before editing data.
