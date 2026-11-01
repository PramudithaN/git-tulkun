# GitTulkun (`git-tulkun`)

A procedural pixel-art **Tulkun** leviathan for your GitHub profile `README.md` that resets to a baby calf every January 1st, grows into an armored adult bull from your annual commits, and takes its colors from your top programming languages.

<p align="center">
  <a href="https://github.com/PramudithaN/git-tulkun">
    <img src="tulkun/tulkun.gif?v=7" width="640" alt="Live GitTulkun rendered from @PramudithaN's GitHub activity" />
  </a>
  <br />
  <em>Live Tulkun generated from <a href="https://github.com/PramudithaN">@PramudithaN</a>'s current-year GitHub activity (1,072 contributions - Stage 5: Adult Male Bull)</em>
</p>

## Quick Start (Copy & Paste)

**1.** Add this embed snippet to your profile `README.md`:

```markdown
<p align="center">
  <a href="https://github.com/PramudithaN/git-tulkun">
    <img src="tulkun/tulkun.gif" width="640" alt="GitTulkun swimming" />
  </a>
</p>
```

**2.** Create `.github/workflows/tulkun.yml` in the same repository (the `permissions: contents: write` line grants write access automatically):

```yaml
name: Update Tulkun

on:
  schedule: [{ cron: "0 0 * * *" }]
  workflow_dispatch:
  push: { branches: [main] }

permissions:
  contents: write

jobs:
  tulkun:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: PramudithaN/git-tulkun@v1
        with:
          view: side # side | dive | top
      - run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add tulkun/
          git diff --cached --quiet || git commit -m "chore: update Tulkun"
          git push
```

> **Try it in your browser or compare with a friend:** Open the **[Interactive Whale Generator & Comparator](https://pramudithan.github.io/git-tulkun/)** to preview your username instantly, or click **"Use this template"** at the top of this repo.

<p align="center">
  <a href="https://github.com/PramudithaN/git-tulkun/releases/latest"><img src="https://img.shields.io/github/v/release/PramudithaN/git-tulkun?style=for-the-badge" alt="Latest Release" /></a>
  <img src="https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white" alt="Rust" />
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white" alt="GitHub Actions" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License: MIT" />
</p>

---

## Share "Your Tulkun This Year" & Compare With Friends

Every workflow run automatically generates a `1280×640` social card at **`tulkun/share-card.png`** showing your current annual stage (`1.CALF` $\rightarrow$ `5.BULL`), contribution count, and language palette, ready to post on X, LinkedIn, or Discord when the **January 1st reset** begins or when your whale reaches **Stage 5: Adult Bull**:

<p align="center">
  <a href="https://github.com/PramudithaN/git-tulkun">
    <img src="tulkun/share-card.png?v=7" width="640" alt="Your Tulkun This Year Share Card (1280x640)" />
  </a>
</p>

- **Compare Whales Side-by-Side**: Enter two GitHub usernames in the [Interactive Whale Comparator](https://pramudithan.github.io/git-tulkun/) to compare stages, spine length, and language colors.
- **Join the Community Pod**: Add your Tulkun to [`SHOWCASE.md`](SHOWCASE.md) via a Pull Request.

---

## Annual Lifecycle (`Baby Calf` $\rightarrow$ `Adult Bull`)

On **January 1st** of every calendar year, your Tulkun resets to its **Stage 1 Baby Calf** form and grows throughout the year according to your annual contribution rate across **5 biological stages**:

| Stage | Current-Year Contributions | Live 15 FPS Animation | Anatomical Changes Unlocked |
| :--- | :---: | :---: | :--- |
| **Stage 1**<br/>**Baby Calf** | **`1 – 99`**<br/>contributions | <img src="docs/stage1-calf/tulkun.gif?v=8" width="320" alt="Stage 1 Baby Calf" /> | Compact `64px` spine, blunt teal-blue snout with a flat oval sensor dimple, light cream dorsal swirl patches, bright cream belly, and stubby fins with pale cream tail flukes. |
| **Stage 2**<br/>**Yearling Calf** | **`100 – 249`**<br/>contributions | <img src="docs/stage2-yearling/tulkun.gif?v=8" width="320" alt="Stage 2 Yearling Calf" /> | Spine lengthens (`95px`) and slims down; *kuru* neural whips sprout behind the anterior opercular flippers while tail flukes begin darkening at the base. |
| **Stage 3**<br/>**Adolescent** | **`250 – 499`**<br/>contributions | <img src="docs/stage3-adolescent/tulkun.gif?v=8" width="320" alt="Stage 3 Adolescent" /> | Sensor crest rises and slopes forward; all 6 pectoral and ventral flippers elongate with crisp white leading edges, and secondary pelvic accessory paddles widen under the tail stock. |
| **Stage 4**<br/>**Adult Female** | **`500 – 999`**<br/>contributions | <img src="docs/stage4-female/tulkun.gif?v=8" width="320" alt="Stage 4 Adult Female" /> | Dark charcoal carapace armor replaces the pale calf dorsal patches; forward-jutting sloped maroon sensor crest with an olive-gold front tip, 5 sharp sawtooth jaw triangles, and segmented cerulean tail pleats. |
| **Stage 5**<br/>**Adult Male Bull** | **`1,000+`**<br/>contributions | <img src="docs/stage5-bull/tulkun.gif?v=8" width="320" alt="Stage 5 Adult Male Bull" /> | Maximum `186px` leviathan length and full scythe-wing span; towering vertical hooked hammer-crest with concave rear overhang, 6 serrated jaw triangles, and white carapace battle-scars. |

---

## Camera Perspectives (`view`)

You can render your Tulkun from **3 camera angles** using the `view` input (`side`, `dive`, or `top`):

| Camera Mode | Live Animated Preview | Description |
| :--- | :---: | :--- |
| **`view: side`**<br/>*(Default)* | <img src="docs/stage5-bull/tulkun.gif?v=7" width="360" alt="Side Profile Swim" /> | **Lateral Side Swim**: Displays the hooked hammer-crest, serrated jaw war-stripes, looping *kuru* whip, and full vertical S-wave tail strokes. |
| **`view: dive`** | <img src="docs/view-dive/tulkun.gif?v=7" width="360" alt="3/4 Dynamic Dive" /> | **3/4 Dynamic Dive**: Displays the arched dorsal carapace, split crimson-lined lateral head scoop, and sweeping foreground scythe flipper. |
| **`view: top`** | <img src="docs/view-top/tulkun.gif?v=7" width="360" alt="Top-Down Dorsal Swim" /> | **Dorsal Top-Down Swim**: Displays the full 10-limb wingspan (opercular fins, primary scythe wings, trailing *kuru* whips, pelvic paddles, and forked caudal flukes). |

---

## How the Rendering Engine Works

1. **Dynamic Language Color Ramps (`src/coat.rs`)**:
   - Queries the official GitHub hex colors of your top repository languages (such as TypeScript `#3178c6`, Rust `#dea584`, and Python `#3572A5`) and converts each into a **4-shade pixel-art ramp**:
     - **Primary Language (`#1`)**: Tints the ventral pleated belly, calf skin, and dark dorsal carapace armor.
     - **Secondary Language (`#2`)**: Tints the sensor crest organ core.
     - **Tertiary Language (`#3`)**: Tints the sensor crest tip highlights.
   - Set `canon: "true"` (or `--canon` on the CLI) for canonical movie colors:
     <p align="center">
       <img src="docs/canon-bull/tulkun.gif?v=7" width="420" alt="Canon Tulkun Palette" />
     </p>

2. **3D Cylindrical Normal Lighting and `4x4` Ordered Bayer Dithering (`src/render.rs`)**:
   - Each pixel across the spine and appendages computes a 3D surface normal $\vec{n} = (n_x, n_y, \sqrt{1 - n_x^2 - n_y^2})$ illuminated by a directional light vector `[-0.30, -0.62, 0.72]`, quantized with a `4x4` Bayer ordered dither matrix and bordered with a `1px` dark outline (`#0f121a`).

3. **Cetacean S-Wave Swimming Physics and Bottom-Left Metrics HUD**:
   - **48-Frame Cetacean S-Wave (3.2s Loop at 15 FPS)**: A traveling wave flexes through the mid-torso and drives a vertical propulsion stroke down the tail peduncle and dual flukes, while the 6 pectoral flippers scull with natural phase lag.
   - **Bottom-Left Pixel-Art Metrics HUD**: Displays **`AVATAR: TULKUN`** and your current-year **`CONTRIBUTIONS: <count>`** in the bottom-left corner.

---

## GitHub Action Inputs

| Input | Default | Description |
| :--- | :--- | :--- |
| `login` | `${{ github.repository_owner }}` | GitHub username whose current-year contributions and repository languages to read. |
| `view` | `side` | Camera perspective: `side` (Lateral Side Swim), `dive` (3/4 Dynamic Dive), or `top` (Dorsal Top-Down). |
| `canon` | `"false"` | Set to `"true"` to use canonical Tulkun colors instead of GitHub language colors. |
| `output-dir` | `tulkun` | Output directory for `tulkun.gif`, `tulkun.png`, `share-card.png`, and `preview.html`. |
| `token` | `${{ github.token }}` | GitHub token for public GraphQL queries (the default built-in token is sufficient). |

---

## CLI Usage (Local Development)

```bash
# 1. Collect a live GitHub account snapshot
cargo run --release -- collect <GITHUB_USERNAME> --output snapshot.json

# 2. Render tulkun.gif, tulkun.png, share-card.png (1280x640), and preview.html
cargo run --release -- render snapshot.json --output-dir tulkun --view side

# 3. Demo mode (preview any contribution count without GitHub authentication)
cargo run --release -- demo --commits 45   --output-dir tulkun-calf
cargo run --release -- demo --commits 350  --output-dir tulkun-adolescent
cargo run --release -- demo --commits 1100 --output-dir tulkun-bull --view dive
```

---

## Disclaimer & License

**Unofficial Fan Project**: `git-tulkun` is an independent, non-commercial, fan-made open-source software project inspired by *Avatar: The Way of Water*. *Tulkun* and *Avatar* are trademarks and intellectual property of 20th Century Studios and Lightstorm Entertainment. This project is not affiliated with, endorsed by, or sponsored by 20th Century Studios or Lightstorm Entertainment.

MIT © [Pramuditha Nadun](https://github.com/PramudithaN)
