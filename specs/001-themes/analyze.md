# Analyze — Themes

## Coverage

| Area              | Spec | Plan | Code            | Notes                                  |
|-------------------|------|------|-----------------|----------------------------------------|
| CSS injection     | ✅   | ✅   | `screen.js`     | `<style id=themes-style>` + variables  |
| Server persist    | ✅   | ✅   | `routes.py`     | `themes.json` under `config_dir`       |
| FOUC fast-path    | ✅   | ✅   | `screen.js`     | localStorage CACHE_KEY                 |
| Quick-pick        | ✅   | ✅   | `settings.html` + JS | dropdown sync                     |
| Grid view         | ✅   | ✅   | `screen.js`     | `renderPicker`                         |
| Public API        | ✅   | ✅   | `screen.js`     | `window.themes`                        |
| Tests             | ❌   | ❌   | —               | None automated                         |

## Drift

- README is intentionally minimal ("allows basic recoloring") and matches
  the implementation.
- README does not enumerate the available themes; users discover them via
  the picker. Acceptable.
- `settings.html` copy says "Settings are saved to the server." — matches.

## Gaps

1. **Stale server id on theme deletion** (Q7). When a theme is removed
   from `PRESETS`, the server keeps the old id and the client falls back
   on every reconcile — inefficient but harmless.
2. **No theme editor / sharing**.
3. **Hard-coded preset list** in `screen.js` (Q lift to JSON?).
4. **Splitscreen interaction** is undefined; today themes are global.
5. **`normalizeColor` accepts unrecognised input as-is**, which can
   silently produce invalid CSS.
6. **No tests** — themes regression is visual.

## Recommendations

- **POST default on fallback**: when `applyTheme` falls back to
  `DEFAULT_ID`, also POST that id (silently) so the server file converges.
- **Lift `PRESETS` to a JSON file**: shrinks `screen.js`, opens a path to
  user themes (drop a JSON in `{config_dir}/themes/` to add one).
- **Strict `normalizeColor`**: throw or warn on input it can't parse so
  malformed presets are caught at preview time, not in production.
- **Visual regression test** (later): a Playwright snapshot per theme
  applied to the home screen would catch CSS regressions.
- **Document the variable contract**: list every `--sm-*` variable the
  core stylesheet consumes so theme authors know the surface.
