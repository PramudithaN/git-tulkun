# 🐋 GitTulkun (`git-tulkun`)

![Rust](https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)

> Draw a procedural pixel-art Pandoran **Tulkun** leviathan whale from a GitHub account's commits and language colors, rendered as a seamless 15 FPS looping GIF for your GitHub profile `README.md`.

---

## ✨ How It Works

Inspired by [`git-koi`](https://github.com/yalongwastaken/git-koi), **GitTulkun** is a pure-Rust mathematical pixel-art renderer that turns your public GitHub activity into a living Pandoran Tulkun whale:

1. **Commit-Driven Biological Growth (`Baby Calf` $\rightarrow$ `Adult Male Bull`)**:
   - **Stage 1 (`1–14` commits — Baby Calf)**: Compact, higher body-fat ratio, blunt teal-blue snout with a flat oval sensor dimple, swirling light cream dorsal patches, stubby fins, and light-colored tail flukes.
   - **Stage 2 (`15–39` commits — Yearling Calf)**: *Kuru* neural whips sprout behind the anterior opercular flippers; tail flukes begin darkening at the base.
   - **Stage 3 (`40–74` commits — Adolescent)**: Sensor crest slopes forward; all 6 pectoral and ventral flippers elongate with bright white leading edges.
   - **Stage 4 (`75–114` commits — Adult Female)**: Dark charcoal carapace armor replaces the pale calf patches; forward-jutting maroon sensor crest with olive tip and 5 sharp jaw triangles.
   - **Stage 5 (`115+` commits — Adult Male Bull)**: Full `186px` leviathan with the tall hooked hammer-crest, 6 serrated jaw triangles, white carapace battle-scars, and full wingspan.
2. **GitHub Language Coat Pigments**:
   - Reads your repositories' primary languages via GitHub GraphQL and converts their official GitHub hex colors into **4-shade `4×4` Bayer-dithered pixel-art ramps**:
     - **Primary Language (`#1`)**: Tints the ventral pleated belly, calf skin, and dark dorsal armor.
     - **Secondary Language (`#2`)**: Tints the reddish-maroon sensor crest organ core.
     - **Tertiary Language (`#3`)**: Tints the sensor crest tip highlights.
3. **15 FPS Full-Body Cetacean Swimming Loop**:
   - Traveling S-wave spine propulsion, phase-lagged flapping pectoral scythe-wings, trailing *kuru* neural whips, whipping forked tail flukes, and automatic bounding-box framing (`640×280` exported transparent `.gif`).

---

## 🚀 Quick Start (Add to Your GitHub Profile `README.md`)

Anyone can add a swimming Tulkun to their `<username>/<username>` GitHub profile repository in **2 steps**:

### Step 1: Create `.github/workflows/tulkun.yml` in your profile repo

```yaml
name: Draw Profile Tulkun

on:
  schedule:
    - cron: "0 0 * * *" # Updates every night at midnight UTC
  workflow_dispatch:     # Allows manual 1-click run from the Actions tab

permissions:
  contents: write

jobs:
  tulkun:
    runs-on: ubuntu-latest
    steps:
      - name: Check out profile repository
        uses: actions/checkout@v4

      - name: Generate Tulkun GIF & PNG
        uses: PramudithaN/git-tulkun@v0.1.0
        with:
          login: ${{ github.repository_owner }}
          view: side        # Options: side | dive | top
          canon: "false"    # Set to "true" to use canon Avatar colors instead of language colors
          output-dir: tulkun

      - name: Commit updated Tulkun to profile repo
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add tulkun/tulkun.gif tulkun/tulkun.png tulkun/preview.html
          git diff --cached --quiet || git commit -m "chore: update Tulkun from latest GitHub activity"
          git push
```

### Step 2: Embed the GIF in your `README.md`

```html
<p align="center">
  <img src="https://raw.githubusercontent.com/<YOUR_USERNAME>/<YOUR_USERNAME>/main/tulkun/tulkun.gif" width="640" alt="My GitTulkun swimming" />
</p>
```

---

## ⚙️ GitHub Action Inputs

| Input | Default | Description |
| :--- | :--- | :--- |
| `login` | `${{ github.repository_owner }}` | GitHub username whose commits and languages to read. |
| `view` | `side` | Camera perspective: `side` (Lateral Side Swim), `dive` (3/4 Dynamic Dive), or `top` (Dorsal Top-Down). |
| `canon` | `"false"` | If `"true"`, uses canon Pandoran Tulkun colors instead of tinting with GitHub language colors. |
| `output-dir` | `tulkun` | Output folder for `tulkun.gif`, `tulkun.png`, and `preview.html`. |
| `token` | `${{ github.token }}` | GitHub token for public GraphQL queries (the default built-in token is sufficient). |

---

## 💻 CLI Usage (Local Development)

Requires [Rust](https://rustup.rs/) and the [GitHub CLI (`gh`)](https://cli.github.com/):

```bash
# 1. Collect a live GitHub account snapshot
cargo run --release -- collect <GITHUB_USERNAME> --output snapshot.json

# 2. Render tulkun/tulkun.gif, tulkun/tulkun.png, and tulkun/preview.html
cargo run --release -- render snapshot.json --output-dir tulkun --view side

# 3. Demo mode (test any commit count immediately without GitHub authentication)
cargo run --release -- demo --commits 8   --output-dir tulkun-calf
cargo run --release -- demo --commits 60  --output-dir tulkun-adolescent
cargo run --release -- demo --commits 140 --output-dir tulkun-bull --view side
```

---

## 📦 Publishing a New Release (For Maintainers)

Pushing a version tag (`v*.*.*`) automatically triggers [`.github/workflows/release.yml`](.github/workflows/release.yml) to compile pre-built binaries for **Linux (`x86_64`)**, **macOS (`ARM64`)**, and **Windows (`x86_64`)** and attach them to the GitHub Release so the Action runs in ~2 seconds:

```bash
git tag v0.1.0
git push origin v0.1.0
```

---

## 📁 Project Structure

```text
git-tulkun/
├── .github/workflows/
│   ├── release.yml      # Builds Linux, macOS & Windows release binaries on v*.*.* tags
│   └── tulkun.yml       # Example nightly profile update workflow
├── src/
│   ├── coat.rs          # GitHub language hex -> 4-shade pixel dither ramps
│   ├── collect.rs       # GitHub GraphQL collector via `gh api graphql`
│   ├── history.rs       # Contribution calendar & language share models
│   ├── lib.rs           # Library root
│   ├── main.rs          # CLI (`collect`, `render`, `demo`)
│   ├── output.rs        # 2x nearest-neighbor GIF, PNG, and HTML preview encoders
│   └── render.rs        # Full-body swimming Tulkun spline & 4x4 Bayer dither engine
├── action.yml           # Composite GitHub Action (downloads release binary or builds from source)
└── Cargo.toml           # Rust package manifest
```

---

## 📄 License

MIT
