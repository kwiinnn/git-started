"""The workshop's automated check. Runs on every pull request.

It fails when:
  - a file still has merge conflict markers (<<<<<<<, =======, >>>>>>>)
  - src/data/members.json or a glossary card isn't valid JSON, or is missing a field
  - src/index.html has a tag that was opened but never closed
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
errors = []


def error(path, message, line=None):
    rel = path.relative_to(ROOT)
    where = f",line={line}" if line else ""
    # GitHub shows ::error lines as red notes on the pull request.
    print(f"::error file={rel}{where}::{message}")
    errors.append(f"{rel}: {message}")


# 1. Conflict markers
MARKER = re.compile(r"^(<{7}|={7}|>{7})( |$)")
for path in sorted(ROOT.rglob("*")):
    if not path.is_file() or ".git" in path.parts:
        continue
    if path.suffix not in {".json", ".html", ".css", ".js", ".md", ".py", ".yml"}:
        continue
    for number, text in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
        if MARKER.match(text):
            error(path, f"Leftover merge conflict marker: {text.strip()!r}. Delete the marker lines.", number)


# 2. members.json
GITHUB_NAME = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$")
members_path = ROOT / "src" / "data" / "members.json"
try:
    members = json.loads(members_path.read_text(encoding="utf-8"))
except json.JSONDecodeError as exc:
    error(members_path, f"Not valid JSON: {exc.msg} (line {exc.lineno}). Check for a missing or extra comma.", exc.lineno)
    members = None

if members is not None:
    if not isinstance(members, list):
        error(members_path, "Should be a list: [ ... ]")
    else:
        seen = set()
        for index, member in enumerate(members, 1):
            if not isinstance(member, dict):
                error(members_path, f"Entry {index} should look like {{ \"name\": \"...\", \"github\": \"...\" }}")
                continue
            name, github = member.get("name"), member.get("github")
            if not isinstance(name, str) or not name.strip():
                error(members_path, f"Entry {index} needs a \"name\".")
            if not isinstance(github, str) or not GITHUB_NAME.match(github):
                error(members_path, f"Entry {index} needs a valid \"github\" username (no @).")
            elif github.lower() in seen:
                error(members_path, f"@{github} is in the list twice. Keep one.")
            else:
                seen.add(github.lower())


# 3. Glossary cards
for path in sorted((ROOT / "src" / "glossary").glob("*.json")):
    if path.name == "index.json":
        continue
    try:
        card = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        error(path, f"Not valid JSON: {exc.msg} (line {exc.lineno}).", exc.lineno)
        continue
    if not isinstance(card, dict):
        error(path, "Should look like { \"term\": \"...\", \"meaning\": \"...\", \"example\": \"...\" }")
        continue
    for field in ("term", "meaning"):
        if not isinstance(card.get(field), str) or not card[field].strip():
            error(path, f"Needs a \"{field}\".")
    if isinstance(card.get("meaning"), str) and len(card["meaning"]) > 280:
        error(path, "Keep \"meaning\" to one or two sentences (280 characters max).")


# 4. HTML: every opened tag gets closed
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class TagChecker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.problems = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        open_tags = [name for name, _ in self.stack]
        if tag not in open_tags:
            self.problems.append((f"</{tag}> closes a tag that was never opened.", self.getpos()[0]))
            return
        # Anything opened after the matching tag was left unclosed.
        while self.stack[-1][0] != tag:
            name, line = self.stack.pop()
            self.problems.append((f"<{name}> is never closed.", line))
        self.stack.pop()


for path in sorted((ROOT / "src").glob("*.html")):
    checker = TagChecker()
    checker.feed(path.read_text(encoding="utf-8"))
    for message, line in checker.problems:
        error(path, message, line)
    for tag, line in checker.stack:
        error(path, f"<{tag}> is never closed.", line)


if errors:
    print(f"\n{len(errors)} problem(s) found. Fix them, commit, and push again.")
    sys.exit(1)
print("All checks passed.")
