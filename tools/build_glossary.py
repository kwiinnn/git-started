"""Writes src/glossary/index.json: the list of glossary cards the site loads.

Runs automatically when the site deploys. Run it yourself before previewing locally:
    python3 tools/build_glossary.py
"""
import json
from pathlib import Path

GLOSSARY = Path(__file__).resolve().parent.parent / "src" / "glossary"

files = sorted(p.name for p in GLOSSARY.glob("*.json") if p.name != "index.json")
(GLOSSARY / "index.json").write_text(json.dumps(files, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {len(files)} glossary cards to src/glossary/index.json")
