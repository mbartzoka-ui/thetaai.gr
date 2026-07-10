#!/usr/bin/env python3
"""Sanity checks for the radar pages before the workflow commits them.

Fails (exit 1) if either page's ITEMS array is missing, invalid, empty,
structurally broken, or if the GR and EN pages diverge. A failure here
blocks the commit step, so the previously published pages stay live.
"""
import json
import re
import sys
from pathlib import Path

PAGES = {
    "GR": Path("radar/index.html"),
    "EN": Path("en/radar/index.html"),
}
TOPICS = {"AI Act", "AI Security", "Standards", "Incidents", "General"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MIN_ITEMS = 5

errors = []
parsed = {}

for lang, path in PAGES.items():
    if not path.is_file():
        errors.append(f"{lang}: {path} is missing")
        continue
    text = path.read_text(encoding="utf-8")
    if "render(" not in text:
        errors.append(f"{lang}: render() no longer present — page script damaged")
    m = re.search(r"const ITEMS = (\[.*?\]);", text, re.S)
    if not m:
        errors.append(f"{lang}: could not locate `const ITEMS = [...];`")
        continue
    try:
        items = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        errors.append(f"{lang}: ITEMS is not valid JSON: {e}")
        continue
    if not isinstance(items, list) or len(items) < MIN_ITEMS:
        errors.append(f"{lang}: ITEMS has {len(items)} entries (< {MIN_ITEMS}) — refusing to publish")
        continue
    for i, item in enumerate(items):
        missing = {"title", "date", "topic", "summary", "sources"} - set(item)
        if missing:
            errors.append(f"{lang}: item {i} missing keys: {sorted(missing)}")
            continue
        if not item["title"] or not item["summary"]:
            errors.append(f"{lang}: item {i} has empty title/summary")
        if not DATE_RE.match(item["date"]):
            errors.append(f"{lang}: item {i} has bad date {item['date']!r}")
        if item["topic"] not in TOPICS:
            errors.append(f"{lang}: item {i} has unknown topic {item['topic']!r}")
        srcs = item["sources"]
        if not isinstance(srcs, list) or not srcs or not all(s.get("name") and s.get("url") for s in srcs):
            errors.append(f"{lang}: item {i} has empty/invalid sources")
    parsed[lang] = items

if "GR" in parsed and "EN" in parsed:
    gr, en = parsed["GR"], parsed["EN"]
    if len(gr) != len(en):
        errors.append(f"GR has {len(gr)} items but EN has {len(en)} — pages diverged")
    else:
        for i, (g, e) in enumerate(zip(gr, en)):
            if g["date"] != e["date"] or g["topic"] != e["topic"]:
                errors.append(f"item {i}: GR ({g['date']}, {g['topic']}) != EN ({e['date']}, {e['topic']})")

if errors:
    print("RADAR SANITY CHECK FAILED:")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)

print(f"Sanity check OK: {len(parsed.get('GR', []))} items on both pages.")
