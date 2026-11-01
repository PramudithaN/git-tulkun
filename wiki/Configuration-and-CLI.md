# Configuration & CLI Reference

`git-tulkun` can be customized via GitHub Action workflow inputs or executed as a standalone CLI tool on your local machine.

---

## GitHub Action Inputs

| Input | Type | Default | Description |
|---|---|---|---|
| `login` | String | `${{ github.repository_owner }}` | GitHub username to inspect. |
| `view` | String | `side` | Perspective: `side` (Lateral), `dive` (3/4 Dynamic), or `top` (Dorsal). |
| `window` | String | `annual` | Timeframe: `annual` (Jan 1 reset) or `rolling` (trailing 365 days). |
| `canon` | String | `"false"` | When set to `"true"`, uses canonical Pandoran movie colors. |
| `output-dir` | String | `tulkun` | Directory where `tulkun.gif`, `tulkun.png`, and `share-card.png` are placed. |
| `commit` | String | `"true"` | When `"true"`, automatically commits and pushes images. |
| `branch` | String | `output` | Target branch (defaults to an isolated orphan branch to avoid repository bloat). |
| `token` | String | `${{ github.token }}` | GitHub token for reading public activity and pushing commits. |

---

## Standalone CLI Commands

Install directly using Cargo:

```bash
cargo install --git https://github.com/PramudithaN/git-tulkun
```

### 1. Collect Account Data
```bash
git-tulkun collect <username> --window annual --output snapshot.json
```

### 2. Render Animation
```bash
git-tulkun render snapshot.json --output-dir tulkun --view side
```

### 3. Demo Mode (Offline Testing)
```bash
# Preview an Adolescent Tulkun
git-tulkun demo --commits 800 --output-dir demo-adolescent

# Preview an Adult Bull in 3/4 dive view
git-tulkun demo --commits 2800 --view dive --output-dir demo-bull
```
