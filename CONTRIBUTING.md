# Contributing

This repo works like a real team's. `main` is protected: nobody pushes to it directly, not even the owner. Every change goes through a pull request.

## The workflow

1. **Pick an issue.** Open the Issues tab, choose one labelled `good first issue`, and assign yourself so nobody else takes it.
2. **Make a branch** named after the issue: `type/number-short-description`.

   ```bash
   git switch main
   git pull
   git switch -c feat/12-git-stash
   ```

3. **Make the change and commit** with a clear message that starts with a type:

   ```bash
   git add .
   git commit -m "feat: add git stash to the glossary"
   ```

   Types: `feat` (something new), `fix` (something broken), `docs` (writing only).

4. **Push and open a pull request.**

   ```bash
   git push -u origin feat/12-git-stash
   ```

   On GitHub, click **Compare & pull request** and fill in the template. Write `Closes #12` (your issue number) so the issue closes itself when you merge.

5. **Wait for the check and a review.** The check must be green and one person must approve. If the check is red, click **Details**, read the error, fix it, commit, and push again: the pull request updates itself.

6. **Squash and merge**, then delete your branch.

## Rules for the data files

- `src/data/members.json` is a list. Each entry is one line: `{ "name": "Your Name", "github": "your-username" }`. Every line except the last ends with a comma.
- Glossary cards are one file each in `src/glossary/`, named after the term (`git-stash.json`). Copy `commit.json` as a starting point.
