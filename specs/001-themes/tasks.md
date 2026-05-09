# Tasks — Themes

Status legend: `DONE` (shipped in v1.0.0), `OPEN` (not yet implemented), `[P]` (parallelisable).

## US-1 — Apply on boot
- [DONE] FOUC fast-path applies cached id first.
- [DONE] Server reconcile on fetch return.
- [DONE] `<html data-sm-theme="...">` attribute set.
- [DONE] `<style id="themes-style">` populated by `buildCss`.

## US-2 — Quick switch
- [DONE] Settings dropdown triggers `window.themes.apply(value, true)`.
- [DONE] POST persists to `themes.json`.
- [DONE] Active id sync on dropdown.

## US-3 — Theme grid
- [DONE] `renderPicker` creates cards per preset.
- [DONE] Active card has badge + ring.
- [DONE] Card click triggers persisted apply.

## US-4 — Public API
- [DONE] `window.themes.apply / list / active`.

## US-5 — Server endpoints
- [DONE] GET returns `{active}` (default fallback on error).
- [DONE] POST writes config file.

## Cross-cutting
- [DONE] `normalizeColor` for hex / shorthand / RGB strings.
- [DONE] Default fallback on unknown id (no throw).
- [OPEN] [P] Reconcile-on-fallback: when applying a fallback, POST the
  default to the server so the stale id is overwritten (Q7).
- [OPEN] [P] Theme export / import as JSON (Q8).
- [OPEN] Investigate light-theme support (Q9).
- [OPEN] [P] Lift `PRESETS` to a JSON file and lazy-load to shrink
  initial JS payload.
- [OPEN] Per-panel theming for splitscreen (Q in spec).
