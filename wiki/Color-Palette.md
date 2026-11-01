# Color Palette & Language Tints

`git-tulkun` takes its color scheme directly from the languages in your public repositories.

---

## 4-Shade Ordered Bayer Ramps

Every hex color detected from GitHub (e.g. TypeScript Blue `#3178c6`, Rust Amber `#dea584`, Python `#3572A5`) is programmatically decomposed into a **4-shade pixel-art shading ramp**:
1. **Shadow** (dark ambient occlusion)
2. **Mid-Dark** (primary shadow facing away from the key light)
3. **Mid-Light** (diffuse surface color)
4. **Highlight** (specular rim reflection)

---

## Anatomy Layer Mapping

- **Primary Language (#1)**: Tints the ventral pleated belly, youthful calf skin, and blends into the adult dorsal carapace armor.
- **Secondary Language (#2)**: Tints the glowing crimson sensor crest organ core located along the snout.
- **Tertiary Language (#3)**: Tints the forward tip of the sensor crest.

---

## Canonical Pandoran Palette (`canon: "true"`)

If you prefer the natural deep-ocean colors from *Avatar: The Way of Water* instead of language-based colors, set `canon: "true"`:
- **Carapace Armor**: Midnight obsidian and deep slate blue (`#161a20`)
- **Ventral Belly**: Cerulean ocean blue (`#143a56`)
- **War Stripes & Fluke Edges**: Sea-foam ivory (`#f8fafc`)
- **Crest Core**: Deep blood coral crimson (`#44181c`)
- **Crest Tip**: Olive algae gold (`#627040`)
