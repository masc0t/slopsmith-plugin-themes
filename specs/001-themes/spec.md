# Spec — Themes (`themes`)

> Retrospective spec for shipped v1.0.0. Implementation in `routes.py` (39
> lines), `screen.js` (464), and `settings.html` (12) is the source of truth.

## Summary

A Slopsmith plugin that recolours the entire UI by injecting a `<style>` tag
with `--sm-*` CSS variables and a `data-sm-theme` attribute on `<html>`.
Persists the chosen theme on the server (`{config_dir}/themes.json`) with a
client-side `localStorage` fast-path to avoid FOUC. The Settings panel
exposes a quickpick `<select>`; an injected grid view renders preview cards
for all themes.

## User stories

### US-1 — Theme is applied on boot
- **Given** a theme has been selected previously,
  **When** the page loads,
  **Then** `applyTheme(localStorage[CACHE_KEY])` runs immediately,
  populating `<style id=themes-style>` and setting `data-sm-theme` on
  `<html>`. The user does not see a default-theme flash.
- **And When** `GET /api/plugins/themes/config` returns,
  **Then** if it disagrees with the cached id, the server value wins and
  is re-applied.

### US-2 — Quick switch from settings
- **Given** **Settings → Themes** renders the `<select id=themes-quickpick>`,
  **When** the user picks a theme,
  **Then** `window.themes.apply(value, true)` runs — local cache is
  updated, the style tag re-built, and the new id is persisted via
  `POST /api/plugins/themes/config`.

### US-3 — Theme grid card view
- **Given** the user opens a screen that contains `#themes-grid` (the
  injected grid host),
  **When** the screen mounts,
  **Then** a card per theme is rendered. The active card has an "Active"
  badge; clicking another card calls `applyTheme(id, true)`.

### US-4 — Public API for other plugins
- `window.themes.apply(id, persist)`
- `window.themes.list()` — returns `[{id, ...PRESETS[id]}]`
- `window.themes.active()` — returns the current id (or `DEFAULT_ID`).

### US-5 — Server endpoint
- `GET /api/plugins/themes/config` returns `{active}`.
- `POST /api/plugins/themes/config` body `{active}` writes
  `{config_dir}/themes.json` and returns `{ok, active}`.

## Functional requirements

| ID    | Requirement                                                                                  | Source           |
|-------|----------------------------------------------------------------------------------------------|------------------|
| FR-1  | Persist active theme to `{config_dir}/themes.json`.                                           | `routes.py`      |
| FR-2  | Default to `"classic-dark"` (`DEFAULT_ACTIVE`) on missing file or parse error.                 | `routes.py`      |
| FR-3  | Apply theme by setting CSS variables under `html[data-sm-theme] { --sm-* }`.                  | `screen.js`      |
| FR-4  | FOUC fast-path: apply cached `localStorage[CACHE_KEY]` before reconciling with server.         | `screen.js`      |
| FR-5  | Reconcile: if server's `active` differs from current attribute, re-apply (`persist=false`).    | `screen.js`      |
| FR-6  | Render `<select id=themes-quickpick>` content from `PRESETS`.                                  | `screen.js`      |
| FR-7  | Render `#themes-grid` cards with swatches, name, description, active badge.                    | `screen.js`      |
| FR-8  | Expose `window.themes = {apply, list, active}`.                                                 | `screen.js`      |
| FR-9  | Convert hex / RGB colour strings to `"R G B"` triplet via `normalizeColor` for CSS variable use. | `screen.js`      |
| FR-10 | Unknown ids passed to `applyTheme` fall back to `DEFAULT_ID` silently (no throw).              | `screen.js`      |

## Non-functional

- **Latency**: theme switch is synchronous DOM/CSS work; <16 ms.
- **No third-party assets**: themes ship as constants in `screen.js` with
  no external CSS/font fetches.
- **Compatibility**: depends on Tailwind utility class names that read
  through `rgb(var(--sm-*))`. Slopsmith core's stylesheet must keep using
  these custom-property-friendly utility forms.

## Out of scope

- User-defined themes (no editor today).
- Per-user themes (single-user installs, server stores one value).
- Animated theme transitions.
- Light themes only — design intent is dark themes; pure-light is
  possible but untested.

## Open clarifications

- [NEEDS CLARIFICATION] Should themes be exportable / shareable as JSON
  blobs?
- [NEEDS CLARIFICATION] When a theme is deleted from `PRESETS`, the server
  may still hold its id. Today reconcile will see the unknown id and the
  client falls back to default — but the server file still stores the
  stale id. Should the server also be updated on fallback?
- [NEEDS CLARIFICATION] How does Themes interact with the splitscreen
  plugin's panel chrome? Today the same `--sm-*` vars apply globally;
  per-panel themes are not supported.
