# Getting Started with `git-tulkun`

Adding `git-tulkun` to your GitHub profile repository (`<username>/<username>`) takes less than two minutes.

---

## 1. Add the GitHub Action Workflow

Create a file named `.github/workflows/tulkun.yml` in your profile repository:

```yaml
name: Update Tulkun

on:
  schedule:
    # Runs automatically every midnight UTC
    - cron: "0 0 * * *"
  workflow_dispatch:
  push:
    branches: [main]

permissions:
  contents: write

jobs:
  tulkun:
    runs-on: ubuntu-latest
    steps:
      - uses: PramudithaN/git-tulkun@v1
        with:
          view: side      # side | dive | top
          window: annual  # annual (Jan 1 reset) | rolling (trailing 365)
```

The composite action downloads a pre-built binary for your platform, queries your public contributions and languages via GitHub's API, and automatically commits the resulting image to an orphan branch named `output`.

---

## 2. Embed into Your Profile `README.md`

Add the following Markdown block to your profile `README.md` (replace `YOUR_USERNAME` with your GitHub username):

```html
<p align="center">
  <a href="https://github.com/PramudithaN/git-tulkun">
    <img src="https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_USERNAME/output/tulkun/tulkun.gif" width="640" alt="git-tulkun" />
  </a>
</p>
```

> **Why the link wrapper?**
> Wrapping the image in a link back to `https://github.com/PramudithaN/git-tulkun` allows profile visitors to discover how your animated creature was generated.
