# Contributing to GitTulkun

Thanks for your interest in improving **GitTulkun** (`git-tulkun`), the procedural pixel-art Pandoran Tulkun that grows from your GitHub contributions. Contributions of all sizes are welcome: bug reports, new ideas, docs fixes, and code.

## Ways to Contribute

- **Report bugs**: rendering glitches, wrong colors, broken workflow runs, or incorrect growth stages.
- **Suggest features**: new camera views, anatomy details, palettes, or action inputs.
- **Improve docs**: clearer setup steps, better examples, typo fixes.
- **Submit code**: fixes and enhancements to the renderer, collector, or GitHub Action.

## Before You Start

1. Search [existing issues](https://github.com/PramudithaN/git-tulkun/issues) and [pull requests](https://github.com/PramudithaN/git-tulkun/pulls) to avoid duplicates.
2. For larger changes (new stages, new camera views, changes to the animation loop), please open an issue first so we can agree on the approach.

## Development Setup

You will need:

- [Rust](https://rustup.rs/) (stable toolchain)
- [GitHub CLI (`gh`)](https://cli.github.com/), authenticated with `gh auth login` (only required for `collect`)

```bash
# Fork the repo on GitHub, then:
git clone https://github.com/<your-username>/git-tulkun.git
cd git-tulkun
cargo build --release
```

### Try it locally

```bash
# Collect a live snapshot of a GitHub account
cargo run --release -- collect <GITHUB_USERNAME> --output snapshot.json

# Render tulkun.gif, tulkun.png, and preview.html
cargo run --release -- render snapshot.json --output-dir tulkun --view side

# Demo mode: preview any contribution count without authentication
cargo run --release -- demo --commits 60 --output-dir tulkun-demo
cargo run --release -- demo --commits 145 --output-dir tulkun-bull --view dive
```

Demo mode is the fastest way to check visual changes. Open the generated `preview.html` or the GIF directly.

## Project Structure

| Path | Purpose |
|:-----|:--------|
| `src/coat.rs` | Converts GitHub language hex colors into 4-shade pixel dither ramps |
| `src/collect.rs` | GitHub GraphQL collector (via `gh api graphql`) |
| `src/history.rs` | Annual contribution calendar reset and language share models |
| `src/render.rs` | Spline/SDF whale renderer and 4x4 Bayer dither engine |
| `src/output.rs` | GIF, PNG, and HTML preview encoders |
| `src/main.rs` | CLI entrypoint (`collect`, `render`, `demo`) |
| `action.yml` | Composite GitHub Action |
| `docs/` | Pre-rendered showcase GIFs for all stages and camera views |
| `tulkun/` | Live rendered output for the repository owner |

## Making Changes

1. Create a branch from `main`:
   ```bash
   git checkout -b feat/short-description
   ```
2. Make your changes in small, focused commits.
3. Format and lint before committing:
   ```bash
   cargo fmt
   cargo clippy --all-targets -- -D warnings
   cargo test
   ```
4. Run the CLI in `demo` mode and visually check the result.

### Visual changes

If you touch rendering code (`render.rs`, `coat.rs`, `output.rs`):

- Render **all five stages** (e.g. demo counts of `6`, `20`, `60`, `100`, `145`) and confirm nothing regressed.
- Check all three views: `side`, `dive`, and `top`.
- Confirm the animation still **loops seamlessly** (48 frames at 15 FPS).
- Verify the output looks good on both **light and dark** GitHub themes.
- Include before/after GIFs or screenshots in your pull request.

If your change alters the showcase visuals, regenerate the relevant files in `docs/`.

### Growth stage thresholds

| Stage | Contributions |
|:------|:-------------:|
| 1: Baby Calf | 1-14 |
| 2: Yearling Calf | 15-39 |
| 3: Adolescent | 40-74 |
| 4: Adult Female | 75-114 |
| 5: Adult Male Bull | 115+ |

Changes to these thresholds should be discussed in an issue first, since they also affect the README and showcase assets.

### GitHub Action changes

If you modify `action.yml` or the workflows in `.github/workflows/`:

- Test the workflow on a fork using **Run workflow** (`workflow_dispatch`).
- Keep the action inputs (`login`, `view`, `canon`, `output-dir`, `token`) backward compatible, or call out the breaking change clearly in your PR.
- Update the **GitHub Action Inputs** table in `README.md` if inputs change.

## Commit Messages

Short, imperative, and descriptive. Conventional-style prefixes are welcome:

```
feat: add pelvic paddle animation to top view
fix: prevent crest clipping at stage 5 in dive view
docs: clarify workflow permissions step
chore: update Tulkun from latest GitHub activity
```

## Pull Requests

1. Push your branch to your fork and open a PR against `main`.
2. Describe **what** changed and **why**.
3. Link related issues (e.g. `Closes #12`).
4. Attach visuals for any rendering change.
5. Make sure `cargo fmt`, `cargo clippy`, and `cargo test` pass.

PRs should stay focused: one feature or fix per PR makes review much faster.

## Reporting Bugs

Please include:

- What you expected vs. what happened
- Your `view` and `canon` settings
- The CLI command or workflow YAML you used
- Your OS and Rust version (`rustc --version`) for local issues
- Logs from the failed Actions run, if applicable
- Screenshots or the generated GIF for visual bugs

## Using AI Assistants

The repository includes `AGENTS.md` and `GEMINI.md` with guidance for AI coding tools. If you use an assistant, please review its output yourself and make sure it follows those files and the conventions above.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
