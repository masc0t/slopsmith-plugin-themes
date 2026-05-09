# Clarifications — Themes

## Q1 — Why CSS variables instead of full stylesheet swaps?
**Resolved.** The Slopsmith UI uses Tailwind utilities like `bg-dark-700`
and `text-accent-light` that map to CSS variables in the core stylesheet.
By writing `html[data-sm-theme] { --sm-bg-700: …; … }`, every utility
re-skins itself without us touching component markup. Constitution §I.

## Q2 — Why both server + localStorage persistence?
**Resolved.** The server is the source of truth (multi-browser, multi-host
consistency); `localStorage` is the FOUC fast-path so the user sees the
right theme on the first paint. Server wins on reconcile. Constitution §III.

## Q3 — Why `normalizeColor` to `"R G B"` triplets?
**Resolved.** Tailwind's `rgb(var(--sm-accent) / <alpha>)` form needs the
variable to expand to space-separated triplets, not a comma-separated
function or hex. Hence `normalizeColor` accepts hex / `#RGB` / `#RRGGBB`
/ already-formatted strings and emits `"r g b"`.

## Q4 — Why a quick-pick AND a grid?
**Resolved.** The quick-pick lives in **Settings** (always available);
the grid lives on a dedicated screen with previews. Different ergonomics:
the dropdown is faster, the grid is for browsing.

## Q5 — What if the server file is corrupt?
**Resolved.** `_read()` catches every exception and returns
`{active: DEFAULT_ACTIVE}`. The user sees the default theme; their next
selection rewrites the file.

## Q6 — Why fall back silently on unknown ids?
**Resolved.** Constitution §V. Throwing on unknown ids would make a
deleted theme bring the UI down. Fallback keeps the page usable; the user
re-picks consciously.

## Q7 — Should the server be reconciled when the client fell back?
**Open.** Today it isn't. If a theme is deleted from `PRESETS`, the server
file keeps the stale id and `_read` happily returns it; the client falls
back each time. Cheap to fix (one POST on fallback), but introduces a
write-on-read pattern.

## Q8 — Theme exports / sharing?
**Open.** No mechanism today. Lifting `PRESETS` to a JSON file plus an
import/export UI is a future feature.

## Q9 — Light themes?
**Open.** All bundled presets are dark. Tailwind utility names that hard-
code `bg-dark-…` would need to be reviewed if a light variant ships.
