# City and A-level attraction expansion

Use this checklist when adding a city or reviewing a 5A/4A attraction.

## Scope

- Treat labels such as “first-tier” and “second-tier” only as internal maintenance priorities. China has no single official administrative list for those commercial city tiers, so do not store them as government facts.
- Prefer a reviewable city batch over a long list of names. A city record should include gateways, local transport context, stay-area tradeoffs, all-month seasonal preparation, culture, food notes, emergency numbers, and attractions.
- Every city must include at least one government-operated `tourism_portals` entry with bilingual name, operator, intended use, URL, and the date the entry was personally checked.
- Keep private residential addresses and resident information out of the dataset. `stay_areas` and `neighborhood_name` describe visitor-relevant districts only.

## Rating evidence

- Add `tourism_rating` only when an official culture-and-tourism authority or the scenic-area authority explicitly supplies the level.
- Record `level`, official `source`, the date personally checked in `last_verified`, and a bilingual `scope_note`.
- Preserve the official name and scope. If a 5A entry is a resort, corridor, or combined scenic area, do not assign 5A to each park, museum, street, or business inside it.
- If an official page confirms only that a place is A-level but does not identify 4A or 5A, omit `tourism_rating` until attraction-specific evidence is available.

## Changing facts

- Use `null` for prices, booking requirements, and rules that were not verified from the current operator.
- Use `availability.status: "unknown"` when the source check does not establish same-day operations. Explain what the traveler must recheck.
- A verification date means the linked claim was checked on that date; it is not a promise that today's opening hours, weather, tickets, transport, or shows are unchanged.
- When a city bureau homepage is technically unreliable, use an active government fallback only when its tourism scope is clear, and explain the limitation in `use_for`.

## Route-ready detail

- Give a public visitor coordinate, realistic duration range, best-month guidance, stable aliases in Chinese and English, and an area ID.
- Explain when a destination is far from the city center, has multiple entrances, or needs a dedicated day.
- For accessibility and safety, describe observable route constraints such as steps, long distances, heat, altitude, or slippery paths. Do not make medical suitability decisions.
- Write original bilingual summaries. Do not copy commercial guides, reviews, or creator posts.

## Review

Run `python3 -m china_travel_kit validate` and the full unit test suite. In the pull request, list the rating authority, verification date, unresolved live checks, and any combined-scope decisions.
