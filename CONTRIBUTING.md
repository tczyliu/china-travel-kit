# Contributing

Thank you for improving China travel information. Data-only pull requests are first-class contributions; Python knowledge is not required.

## Add or update travel data

1. Copy the closest file in `data/cities/`.
2. Keep facts concise and write original summaries in both Chinese and English.
3. Add at least one authoritative source URL for each attraction.
4. Set `last_verified` to the day you personally checked those sources. Use `null` when not verified.
5. Use `null` for unknown or changing prices and reservation rules.
6. Run:

   ```bash
   python3 -m china_travel_kit validate
   python3 -m unittest discover -s tests -v
   ```

7. Explain what you verified and what remains uncertain in the pull request.

For A-level attractions and city expansion batches, follow [`references/data-expansion.md`](references/data-expansion.md). In particular, preserve the official rating scope: a resort or combined scenic area's rating must not be copied onto every component venue.

Do not copy commercial travel guides, reviews, map databases with incompatible terms, or creator content. Links are not proof that copied text is reusable.

## Code changes

Keep changes small and directly tied to an issue. Add a failing test for a bug before fixing it. New dependencies need a concrete reason because the default runtime intentionally uses only the Python standard library.

## Data review checklist

- IDs use lowercase ASCII with hyphens and stay stable after release.
- Coordinates refer to the public visitor destination, not a private address.
- Seasonal and safety notes avoid medical or legal conclusions.
- Changing claims have a source and verification date.
- The text does not recommend a specific commercial vendor.
- Chinese and English summaries communicate the same core fact.

By contributing data, you agree to license it under CC BY-SA 4.0. Code contributions are licensed under MIT.
