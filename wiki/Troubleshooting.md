# Troubleshooting & FAQ

Common questions and resolution steps for `git-tulkun`.

---

### Why does my image show a broken link on my profile?

1. Ensure your GitHub Action workflow has run at least once. You can trigger it manually under **Actions** $\rightarrow$ **Update Tulkun** $\rightarrow$ **Run workflow**.
2. Verify that the orphan branch `output` exists in your repository.
3. Check that your README image source matches:
   ```html
   https://raw.githubusercontent.com/<YOUR_USERNAME>/<YOUR_USERNAME>/output/tulkun/tulkun.gif
   ```

---

### Does updating the GIF daily bloat my Git repository?

No. Unlike simple commit scripts that append commits to `main`, `git-tulkun` commits to an orphan branch named `output`. Only the latest commit is retained, keeping your main branch history completely clean.

---

### How can I preview another user or compare two whales?

You do not need to install anything. Open the [Interactive Generator & Comparator](https://pramudithan.github.io/git-tulkun/), enter any GitHub username, and preview their live avatar side-by-side with friends.
