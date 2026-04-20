# SLOPSMITH THEMES PLUGIN
A tranquil, modern theme collection for the Slopsmith UI. Features 13 carefully curated, ADA-compliant themes designed for reduced eye strain and 2026 website trends.

> **Status:** Release v1.0.0 is stable and optimized for high-performance UI rendering.

### FEATURES
*   **13 Specialized Themes:** Professionally tuned palettes sorted by the ROYGBIV spectrum.
*   **Tranquil "Neutral-First" Architecture:** Desaturated backgrounds and bioluminescent accents to minimize visual fatigue.
*   **ADA Compliant (WCAG AA):** Every theme maintains a contrast ratio of at least 4.5:1 for primary text legibility.
*   **Dynamic CSS Injection:** Injects variables into the `:root` scope for instantaneous, refresh-free theme switching.
*   **Server-Side Persistence:** Active theme selection is saved to the Slopsmith `config_dir` and synchronized across all connected browsers.
*   **FOUC Prevention:** LocalStorage "fast-path" logic applies the cached theme before the DOM fully loads to prevent flashing.

### WHAT'S NEW
*   **v1.0.0 (2026-04-20):** 
    *   Initial release with 13 tranquil themes.
    *   Rainbow-sorted browsing order (Red to Violet).
    *   Refactored theme engine with `normalizeColor` utility for Hex support.

### COMPATIBLE SCREENS
This plugin overrides standard Tailwind and Slopsmith CSS utilities across:
*   Core Navigation & Sidebar
*   Settings & Plugin Management
*   Search Results & Artist Rows
*   Song Cards & Player Bar (Active States)
*   Scrollbars (Webkit-based)

### REQUIREMENTS
*   **Slopsmith:** v1.0.0 or higher.
*   **Browser:** Modern browser with CSS Variable and `:root` support.

### INSTALLATION
1. Navigate to your Slopsmith `plugins` directory:
   ```bash
   cd path/to/slopsmith/plugins
   ```
2. Clone the repository (or copy the folder):
   ```bash
   git clone https://github.com/masc0t/slopsmith-plugin-themes.git themes
   ```
3. Restart the Slopsmith service to initialize the new routes.
4. Access the theme picker via the **Settings** page in the Slopsmith UI.

### HOW IT WORKS
The plugin utilizes a `screen.js` driver that monitors the server-side configuration via `/api/plugins/themes/config`. When a theme is selected:
1.  The `buildCss()` function generates a massive override sheet targeting `html[data-sm-theme]`.
2.  CSS variables (e.g., `--sm-bg-900`, `--sm-accent`) are mapped to Slopsmith's standard Tailwind-based classes.
3.  The `data-sm-theme` attribute on the `<html>` element ensures specificity beats standard utility classes without needing `!important`.

### SUPPORTED THEMES (Rainbow Order)
| Theme ID | Name | Vibe |
| :--- | :--- | :--- |
| `terracotta-red` | Clay Hearth | Muted clay on warm charcoal |
| `muted-rose` | Rose Dust | Soft pink haze on warm stone |
| `sunset` | Sunset Glow | Warm plum tones on muted charcoal |
| `mocha-mousse` | Mocha | Desaturated espresso |
| `desert-sand` | Desert Sand | Warm greyish-tan stone |
| `verdant-green` | Forest Moss | Desaturated evergreens |
| `carbon-mint` | Carbon Mint | Anthracite with glowing mint |
| `matrix` | Matrix | True black and phosphor green |
| `corporate-navy` | Deep Sea | Subdued oceanic blues |
| `nordic-slate` | Nordic Slate | Cool blue-grey harbor tones |
| `classic-dark` | Classic Dark | Original Slopsmith navy/slate |
| `midnight-blue` | Midnight Blue | Deep indigo and charcoal |
| `digital-lavender` | Lavender Dusk | Soft violet glow on deep charcoal |

### OTHER PLUGINS
*   [slopsmith-plugin-midi-capo](https://github.com/masc0t/slopsmith-plugin-midi-capo) - Transpose MIDI input on the fly.

### LICENSE
MIT
