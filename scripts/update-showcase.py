#!/usr/bin/env python3
"""
scripts/update-showcase.py

Automated Community Pod Showcase Updater for git-tulkun.
Discovers public repositories using `PramudithaN/git-tulkun` via:
  1. GitHub Public Network Dependents (zero auth/token required)
  2. GitHub Search API (if GITHUB_TOKEN or gh CLI is available)
  3. Persistent registry in `scripts/pod-members.json`

Verifies their live generated Tulkun GIFs on their `output` branch and
updates `SHOWCASE.md` automatically. No PAT or external services required.
"""

import os
import sys
import json
import re
import urllib.request
import urllib.error
import subprocess
from pathlib import Path

REPO_OWNER = "PramudithaN"
REPO_NAME = "git-tulkun"
TARGET_ACTION = f"{REPO_OWNER}/{REPO_NAME}"

ROOT_DIR = Path(__file__).resolve().parent.parent
SHOWCASE_PATH = ROOT_DIR / "SHOWCASE.md"
MEMBERS_CACHE_PATH = ROOT_DIR / "scripts" / "pod-members.json"


def get_github_token() -> str:
    """Retrieve GitHub token from environment or gh CLI if available."""
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token.strip()
    try:
        proc = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True)
        return proc.stdout.strip()
    except Exception:
        return ""


def load_cached_members() -> dict[str, dict]:
    """Load previously known members from cache."""
    if MEMBERS_CACHE_PATH.exists():
        try:
            data = json.loads(MEMBERS_CACHE_PATH.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
            if isinstance(data, list):
                return {item["owner"]: item for item in data if "owner" in item}
        except Exception as e:
            print(f"Warning: Failed to parse {MEMBERS_CACHE_PATH}: {e}")
    return {}


def save_cached_members(members_dict: dict[str, dict]):
    """Save known members to cache."""
    MEMBERS_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    MEMBERS_CACHE_PATH.write_text(json.dumps(members_dict, indent=2) + "\n", encoding="utf-8")


def scrape_network_dependents() -> list[dict]:
    """
    Scrape GitHub's public dependents page for git-tulkun.
    Requires NO authentication, tokens, or permissions.
    """
    url = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/network/dependents"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    found = []
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8")
        matches = re.findall(r'data-hovercard-url=["\']/([^/]+/[^/]+)/hovercard["\']', html)
        ignored_prefixes = {"users", "orgs", "apps", "marketplace", REPO_OWNER.lower()}
        for repo_path in set(matches):
            parts = repo_path.split("/")
            if len(parts) == 2:
                owner, repo = parts
                if owner.lower() not in ignored_prefixes:
                    found.append({"owner": owner, "repo": repo_path})
        print(f"Discovered {len(found)} dependents from public GitHub network page.")
    except Exception as err:
        print(f"Note: Could not scrape network dependents ({err}).")
    return found


def search_github_workflows(token: str) -> list[dict]:
    """Search GitHub for repositories using git-tulkun in workflows if search is accessible."""
    query = f"{TARGET_ACTION} path:.github/workflows extension:yml"
    url = f"https://api.github.com/search/code?q={urllib.parse.quote(query)}&per_page=100"

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "git-tulkun-showcase-updater",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("items", [])
    except Exception:
        # Code search across public repos is restricted if token is repo-scoped
        try:
            res = subprocess.run(
                ["gh", "api", f"search/code?q={query}&per_page=100"],
                capture_output=True,
                text=True,
                check=True,
            )
            data = json.loads(res.stdout)
            return data.get("items", [])
        except Exception:
            return []


def check_url_exists(url: str, timeout: int = 6) -> bool:
    """Check if a remote resource exists (HTTP 200)."""
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "git-tulkun-verifier"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status == 200
    except Exception:
        return False


def discover_pod_members(token: str) -> list[dict]:
    """Discover all users, merge with cache, and verify live Tulkun assets."""
    unique_repos = load_cached_members()
    print(f"Loaded {len(unique_repos)} members from registry ({MEMBERS_CACHE_PATH.name}).")

    # 1. Scrape public network dependents (zero auth needed)
    for dep in scrape_network_dependents():
        owner = dep["owner"]
        if owner not in unique_repos:
            unique_repos[owner] = {
                "owner": owner,
                "repo": dep["repo"],
            }

    # 2. Search GitHub code if token/gh CLI allows
    raw_items = search_github_workflows(token)
    if raw_items:
        print(f"Found {len(raw_items)} matching code items from GitHub search.")
        for item in raw_items:
            repo_info = item.get("repository", {})
            full_name = repo_info.get("full_name")
            owner_info = repo_info.get("owner", {})
            owner_login = owner_info.get("login")

            if not full_name or not owner_login:
                continue
            if full_name.lower() == f"{REPO_OWNER}/{REPO_NAME}".lower():
                continue

            unique_repos[owner_login] = {
                "owner": owner_login,
                "repo": full_name,
            }

    save_cached_members(unique_repos)

    members = []
    print(f"Checking live GIF availability for {len(unique_repos)} unique users...")
    for owner, info in sorted(unique_repos.items(), key=lambda x: x[0].lower()):
        repo = info["repo"]
        output_gif = f"https://raw.githubusercontent.com/{repo}/output/tulkun/tulkun.gif"
        main_gif = f"https://raw.githubusercontent.com/{repo}/main/tulkun/tulkun.gif"

        has_gif = False
        gif_url = output_gif

        if check_url_exists(output_gif):
            has_gif = True
            gif_url = output_gif
        elif check_url_exists(main_gif):
            has_gif = True
            gif_url = main_gif

        print(f"  - @{owner} ({repo}): {'LIVE' if has_gif else 'CONFIGURED (pending run)'}")
        members.append({
            "owner": owner,
            "repo": repo,
            "has_gif": has_gif,
            "gif_url": gif_url,
            "profile_url": f"https://github.com/{owner}",
            "repo_url": f"https://github.com/{repo}",
        })

    return members


def render_showcase_md(members: list[dict], total_swimmers: int) -> str:
    """Render SHOWCASE.md without badges."""
    live_members = [m for m in members if m["has_gif"]]
    pending_members = [m for m in members if not m["has_gif"]]

    content = [
        "# Community Tulkun Pod (`SHOWCASE.md`)",
        "",
        "> A living ocean gallery of procedurally generated **Tulkun** leviathans swimming across GitHub profile READMEs.",
        f"> Currently featuring **{total_swimmers} swimmers** roaming the GitHub sea.",
        "",
        "---",
        "",
        "## Featured Pod Members",
        "",
        "| Developer | Profile Repository | Live Animated Tulkun |",
        "| :--- | :--- | :---: |",
        f'| <a href="https://github.com/{REPO_OWNER}"><img src="https://github.com/{REPO_OWNER}.png?size=64" width="36" height="36" style="border-radius:50%;" /><br/><strong>@{REPO_OWNER}</strong></a> *(Creator)* | [`{REPO_OWNER}/{REPO_NAME}`](https://github.com/{REPO_OWNER}/{REPO_NAME}) | <a href="https://github.com/{REPO_OWNER}"><img src="tulkun/tulkun.gif?v=9" width="380" alt="@{REPO_OWNER}\'s live Tulkun" /></a> |',
    ]

    for m in live_members:
        owner = m["owner"]
        repo = m["repo"]
        gif_url = m["gif_url"]
        avatar_url = f"https://github.com/{owner}.png?size=64"
        row = (
            f'| <a href="{m["profile_url"]}"><img src="{avatar_url}" width="36" height="36" style="border-radius:50%;" /><br/><strong>@{owner}</strong></a> '
            f'| [`{repo}`]({m["repo_url"]}) '
            f'| <a href="{m["profile_url"]}"><img src="{gif_url}" width="380" alt="@{owner}\'s Tulkun" /></a> |'
        )
        content.append(row)

    if pending_members:
        content.extend([
            "",
            "---",
            "",
            "## Registered Pod Members (First Swim Pending)",
            "",
            "These developers have integrated `git-tulkun` in their repositories and will appear in the live gallery as soon as their first scheduled workflow runs:",
            "",
        ])
        for p in pending_members:
            owner = p["owner"]
            repo = p["repo"]
            content.append(f"- **[@{owner}]({p['profile_url']})** — [`{repo}`]({p['repo_url']})")

    content.extend([
        "",
        "---",
        "",
        "## How to Join the Pod",
        "",
        "You do **not** need to open a pull request! Simply add `git-tulkun` to your GitHub profile repository:",
        "",
        "1. Create `.github/workflows/tulkun.yml` in your profile repository (`<username>/<username>`):",
        "```yaml",
        "name: Update Tulkun",
        "on:",
        '  schedule: [{ cron: "0 0 * * *" }]',
        "  workflow_dispatch:",
        "permissions:",
        "  contents: write",
        "jobs:",
        "  tulkun:",
        "    runs-on: ubuntu-latest",
        "    steps:",
        f"      - uses: {REPO_OWNER}/git-tulkun@v1",
        "```",
        "",
        "2. Embed your animated Tulkun in your profile `README.md`:",
        "```markdown",
        '<p align="center">',
        f'  <a href="https://github.com/{REPO_OWNER}/git-tulkun">',
        '    <img src="https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_USERNAME/output/tulkun/tulkun.gif" width="640" alt="git-tulkun swimming" />',
        "  </a>",
        "</p>",
        "```",
        "",
        "Our automated daily workflow scans for public workflows using `git-tulkun` and adds your whale to this showcase automatically! 🐋",
        "",
        "---",
        f"*Maintained automatically by [`.github/workflows/showcase.yml`](.github/workflows/showcase.yml).*",
        "",
    ])

    return "\n".join(content)


def render_discussion_body(members: list[dict], total_swimmers: int) -> str:
    """Render the body content for GitHub Discussion #4."""
    live_members = [m for m in members if m["has_gif"]]
    rows = [
        f'| <a href="https://github.com/{REPO_OWNER}"><img src="https://github.com/{REPO_OWNER}.png?size=64" width="36" height="36" style="border-radius:50%;" /><br/><strong>@{REPO_OWNER}</strong></a> *(Creator)* | [`{REPO_OWNER}/{REPO_NAME}`](https://github.com/{REPO_OWNER}/{REPO_NAME}) | <a href="https://github.com/{REPO_OWNER}"><img src="https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/tulkun/tulkun.gif" width="360" alt="@{REPO_OWNER}\'s live Tulkun" /></a> |'
    ]

    for m in live_members:
        owner = m["owner"]
        repo = m["repo"]
        gif_url = m["gif_url"]
        avatar_url = f"https://github.com/{owner}.png?size=64"
        row = (
            f'| <a href="{m["profile_url"]}"><img src="{avatar_url}" width="36" height="36" style="border-radius:50%;" /><br/><strong>@{owner}</strong></a> '
            f'| [`{repo}`]({m["repo_url"]}) '
            f'| <a href="{m["profile_url"]}"><img src="{gif_url}" width="360" alt="@{owner}\'s Tulkun" /></a> |'
        )
        rows.append(row)

    table_md = "\n".join(rows)

    return f"""# 🐋 Community Tulkun Pod

A living ocean gallery of procedurally generated **Tulkun** leviathans swimming across GitHub profile READMEs.
Currently featuring **{total_swimmers} swimmers** roaming the GitHub sea!

---

## Featured Community Tulkuns

| Developer | Profile Repository | Live Tulkun |
| :--- | :--- | :---: |
{table_md}

---

## Add Your Tulkun to the Pod

Once you've added `git-tulkun` to your profile repository (`<username>/<username>`), our automated daily scanner will **automatically detect your workflow and add you to this pod table and [SHOWCASE.md](https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/main/SHOWCASE.md)**!

You can also reply to this discussion with:

1. 🎞️ **Your GIF**: drag and drop `tulkun/tulkun.gif` into your comment
2. 🐋 **Your stage**: Calf, Yearling, Adolescent, Mature, or Adult Male Bull
3. 💻 **Your top languages**: they tint your whale!
4. 🎥 *(Optional)* Your camera view (`side`, `dive`, `top`) and whether you used `canon`

---

## New here?

Set up your own Tulkun in 3 steps with the [README guide](https://github.com/{REPO_OWNER}/{REPO_NAME}#quick-start-1-step-setup).

⭐ Enjoying GitTulkun? A star helps other developers find it!"""


def update_github_discussion(token: str, members: list[dict], total_swimmers: int, discussion_num: int = 4):
    """Update GitHub Discussion #4 using GraphQL API."""
    print(f"Syncing Community Pod to Discussion #{discussion_num}...")
    new_body = render_discussion_body(members, total_swimmers)

    # 1. Fetch Discussion node ID
    query_id = """
    query($owner: String!, $name: String!, $num: Int!) {
      repository(owner: $owner, name: $name) {
        discussion(number: $num) {
          id
        }
      }
    }
    """
    mutation_update = """
    mutation($id: ID!, $body: String!) {
      updateDiscussion(input: { discussionId: $id, body: $body }) {
        discussion {
          id
          url
          updatedAt
        }
      }
    }
    """

    discussion_id = None

    # Try GraphQL API via urllib or gh CLI
    if token:
        try:
            req_data = json.dumps({
                "query": query_id,
                "variables": {"owner": REPO_OWNER, "name": REPO_NAME, "num": discussion_num}
            }).encode("utf-8")
            req = urllib.request.Request(
                "https://api.github.com/graphql",
                data=req_data,
                headers={"Authorization": f"Bearer {token}", "User-Agent": "git-tulkun-updater"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                discussion_id = result.get("data", {}).get("repository", {}).get("discussion", {}).get("id")
        except Exception as e:
            print(f"Notice: Direct GraphQL fetch failed ({e}); trying gh CLI fallback...")

    if not discussion_id:
        try:
            res = subprocess.run(
                ["gh", "api", "graphql", "-F", f"owner={REPO_OWNER}", "-F", f"name={REPO_NAME}", "-F", f"num={discussion_num}", "-f", f"query={query_id}"],
                capture_output=True,
                text=True,
                check=True,
            )
            data = json.loads(res.stdout)
            discussion_id = data.get("data", {}).get("repository", {}).get("discussion", {}).get("id")
        except Exception as e:
            print(f"Warning: Could not fetch Discussion #{discussion_num} ID: {e}")
            return

    if not discussion_id:
        print(f"Could not find discussion ID for Discussion #{discussion_num}.")
        return

    # 2. Update Discussion body
    updated = False
    if token:
        try:
            req_data = json.dumps({
                "query": mutation_update,
                "variables": {"id": discussion_id, "body": new_body}
            }).encode("utf-8")
            req = urllib.request.Request(
                "https://api.github.com/graphql",
                data=req_data,
                headers={"Authorization": f"Bearer {token}", "User-Agent": "git-tulkun-updater"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                res_json = json.loads(resp.read().decode("utf-8"))
                if "errors" in res_json:
                    print(f"GraphQL update errors: {res_json['errors']}")
                else:
                    updated = True
                    print(f"Successfully updated Discussion #{discussion_num} via GraphQL API!")
        except Exception as e:
            print(f"Notice: Direct GraphQL mutation failed ({e}); trying gh CLI fallback...")

    if not updated:
        try:
            subprocess.run(
                ["gh", "api", "graphql", "-F", f"id={discussion_id}", "-F", f"body={new_body}", "-f", f"query={mutation_update}"],
                capture_output=True,
                text=True,
                check=True,
            )
            print(f"Successfully updated Discussion #{discussion_num} via gh CLI!")
        except Exception as e:
            print(f"Warning: Could not update Discussion #{discussion_num}: {e}")


def main():
    print("=== Updating Community Pod Showcase ===")
    token = get_github_token()
    members = discover_pod_members(token)

    live_count = sum(1 for m in members if m["has_gif"])
    total_swimmers = 1 + live_count
    print(f"Total live swimmers: {total_swimmers} (1 creator + {live_count} community members)")

    showcase_content = render_showcase_md(members, total_swimmers)
    SHOWCASE_PATH.write_text(showcase_content, encoding="utf-8")
    print(f"Wrote {SHOWCASE_PATH}")

    # Synchronize GitHub Discussion #4
    update_github_discussion(token, members, total_swimmers, discussion_num=4)

    print("Showcase update complete!")


if __name__ == "__main__":
    main()
