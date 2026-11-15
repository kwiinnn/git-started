# git started

The practice repo for the **bit/wise · git started** workshop. Everyone in the room works on this one small website together, the way a real team works on a real codebase.

Live site: https://kwiinnn.github.io/git-started/

## What's in here

| Path | What it is |
| --- | --- |
| `src/index.html`, `src/style.css`, `src/app.js` | The website |
| `src/data/members.json` | Everyone who took part, one line each |
| `src/glossary/*.json` | One file per glossary card |
| `.github/workflows/check.yml` | The automated check that runs on every pull request |
| `.github/workflows/pages.yml` | Deploys the site when something is merged into `main` |

## Run it on your laptop

The site loads its data with `fetch`, so open it through a small local server rather than double-clicking the file:

```bash
python3 tools/build_glossary.py
python3 -m http.server 8000 --directory src
```

Then open http://localhost:8000. In VS Code, the Live Server extension works too (run the first command before starting it).

## How to contribute

Read [CONTRIBUTING.md](CONTRIBUTING.md). Short version: pick an issue, make a branch, open a pull request, get one approval, merge.
