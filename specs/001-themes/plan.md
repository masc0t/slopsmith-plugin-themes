# Plan — Themes (as built)

## File map

| File             | Lines | Purpose                                                                  |
|------------------|-------|--------------------------------------------------------------------------|
| `plugin.json`    | 7     | Manifest. `id: themes`, version `1.0.0`, declares `routes.py`/`screen.js`/`settings.html`. |
| `routes.py`      | 39    | Two endpoints: `GET` and `POST` `/api/plugins/themes/config`.             |
| `screen.js`      | 464   | `PRESETS` definitions, `normalizeColor`, `buildCss`, `applyTheme`, picker + grid renderers, FOUC fast-path, public API. |
| `settings.html`  | 12    | Quickpick `<select>` with onchange triggering `window.themes.apply`.      |

## Data model

```js
PRESETS[id] = {
    name:  string,             // human label
    desc:  string,             // one-line subtitle
    swatches: string[4],       // hex preview swatches
    colors: {
        bg900, bg800, bg700, bg600, bg500,
        accent, accentLight, accentDark,
        gold,
        textPrimary, textSecondary, textMuted,
        border,
        scrollThumb, scrollThumbHover,
        cardFromRgb, cardToRgb,
        playerBg,
    }
}
```

Each colour is hex / shorthand hex / RGB string. `normalizeColor` converts
to a `"r g b"` triplet for CSS variable consumption.

## Boot sequence

```
IIFE start
   │
   ├─► initialId = localStorage[CACHE_KEY] || DEFAULT_ID
   ├─► applyTheme(initialId, persist=false)   // FOUC-free first paint
   │
   ├─► fetch(/api/plugins/themes/config)
   │       └─► if cfg.active != current && PRESETS[cfg.active] → re-apply (server wins)
   │
   └─► finally:
         renderPicker(current)
         syncQuickPick(current)

window.themes = { apply, list, active }
```

## `applyTheme(id, persist)`

```js
1. id = PRESETS[id] ? id : DEFAULT_ID
2. ensure <style id=themes-style> exists; .textContent = buildCss(id)
3. <html data-sm-theme=id>
4. localStorage[CACHE_KEY] = id
5. renderPicker(id) + syncQuickPick(id)
6. if persist: POST /api/plugins/themes/config {active: id}
```

## `buildCss(id)` outline

Emits a single string with rule blocks:
- `html[data-sm-theme="<id>"] { --sm-bg-900: …; --sm-accent: …; … }` — main
  variable bindings.
- Generic utility selectors that consume those variables (gold utilities,
  song-card, artist-row, scrollbar thumb, etc.).

## Endpoints

```python
@app.get("/api/plugins/themes/config")
def get_config():
    return _read()  # {"active": "..."}

@app.post("/api/plugins/themes/config")
async def set_config(req: Request):
    body = await req.json()
    active = str(body.get("active") or DEFAULT_ACTIVE)
    _write(active)  # writes {config_dir}/themes.json
    return {"ok": True, "active": active}
```

`_read()` swallows JSON / IO errors and returns the default.

## Public API

```js
window.themes = {
    apply(id, persist),
    list(),                  // [{id, ...PRESETS[id]}]
    active(),                // current id or DEFAULT_ID
};
```

## Risks / drift watchpoints

- **Tailwind utility coupling**: the core stylesheet must keep using
  `rgb(var(--sm-…))`-style colour utilities. A refactor to direct hex
  classes would silently break theming.
- **PRESETS bloat**: adding many themes inflates `screen.js` (currently
  464 lines). Consider lifting to a JSON file and lazy-loading.
- **Stale server id** (Q7): deleted theme ids stay in `themes.json` until
  manually overwritten.
- **`normalizeColor` strictness**: anything other than hex / `#RGB` /
  `#RRGGBB` is passed through; malformed entries silently break that
  preset.
