# Themes — Constitution

## Inheritance

Slopsmith's core plugin contract governs everything in this repo (manifest,
plugin context: `config_dir`, settings panel mounting, asset serving). This
constitution lists Themes' own non-negotiables.

## Core Principles

### I. CSS variables, not class swaps
Theming MUST be implemented by setting CSS custom properties under
`html[data-sm-theme] { --sm-* }` and reusing them through the rest of the
app's stylesheet rules. Inline class swaps would require touching every
component; variables let the same Tailwind class network re-skin itself.

### II. Fast-path render to avoid FOUC
On boot, the cached theme id from `localStorage[CONFIG.CACHE_KEY]` MUST be
applied BEFORE the server reconciliation fetch returns. Otherwise the user
sees a flash of the default theme (`classic-dark`) every refresh.

### III. Server is the source of truth, client cache is the speed cache
Persistence: the server stores the chosen theme id at
`{config_dir}/themes.json`. The client also caches it in `localStorage`
for the FOUC fast-path. On reconcile, server wins if the two disagree.

### IV. Public API: `window.themes`
Expose `{apply(id, persist), list(), active()}` so external surfaces (the
settings panel `<select>`, future plugins) can drive theme changes
consistently.

### V. Default fallback
Unknown ids fall back to `CONFIG.DEFAULT_ID` (currently
`"classic-dark"`). The fallback is also the bootstrap value when the
cache, server, or both are empty / corrupt. Never apply an unknown id
silently.

## Governance

Adding a theme MUST extend the `PRESETS` object with the full set of
required keys (`name`, `desc`, `swatches`, `colors.{bg900,…,playerBg}`).
Removing a theme requires a server-side migration: any user persisted on
the deleted id will fall back to `DEFAULT_ID` on next reconcile. Document
the deletion in this file.

**Version**: 1.0.0 | **Ratified**: 2026-05-09 | **Last Amended**: 2026-05-09
