#!/usr/bin/env python3
"""Validate the translation JSON against the immutable extraction."""

import argparse
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/source/魔女与百骑兵_全量中日对照文本.json"
TRANSLATION = ROOT / "data/translation/魔女与百骑兵_中日对照文本.json"
CONTROL = re.compile(r"\r\n|[\r\n\t]|%%|%[+#0-]*\d*(?:\.\d+)?(?:hh|ll|[hljztL])?[diuoxXfFeEgGaAcspn]")


def verify_alignment(source, translation, require_complete=False):
    entries = source["entries"]
    translated = translation["entries"]
    if not isinstance(entries, list) or not isinstance(translated, list):
        raise ValueError("entries must be lists")
    if len(entries) != source["meta"]["total_entries"] or len(entries) != len(translated):
        raise ValueError("Entry count differs from the source manifest")
    if {k: v for k, v in source.items() if k != "entries"} != {
        k: v for k, v in translation.items() if k != "entries"
    }:
        raise ValueError("Top-level metadata differs from the source")

    seen = set()
    pending = 0
    for original, edited in zip(entries, translated):
        entry_id = original["id"]
        if entry_id in seen:
            raise ValueError(f"{entry_id}: duplicate source ID")
        seen.add(entry_id)
        if not isinstance(edited, dict) or original.keys() != edited.keys():
            raise ValueError(f"{entry_id}: entry fields differ from the source")
        for key, value in original.items():
            if key != "zh" and edited[key] != value:
                raise ValueError(f"{entry_id}: {key} differs from the source")

        zh = edited["zh"]
        if not isinstance(zh, str) or (zh and not zh.strip()):
            raise ValueError(f"{entry_id}: zh must be empty or contain non-whitespace text")
        if not zh:
            pending += 1
            continue
        jp = original["jp"]
        if original["type"] == "placeholder" and zh != jp:
            raise ValueError(f"{entry_id}: placeholder must match jp exactly")
        if CONTROL.findall(zh) != CONTROL.findall(jp):
            raise ValueError(f"{entry_id}: format tokens, line breaks, or tabs differ from jp")

    if require_complete and pending:
        raise ValueError(f"{pending:,} entries still have empty zh fields")
    return len(entries), pending


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-complete", action="store_true", help="Fail if any zh field is empty")
    args = parser.parse_args()
    try:
        source = json.loads(SOURCE.read_text(encoding="utf-8"))
        translation = json.loads(TRANSLATION.read_text(encoding="utf-8"))
        total, pending = verify_alignment(source, translation, args.require_complete)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"FAIL: {error}\n")
    print(f"PASS: {total:,} aligned entries, {total - pending:,} filled, {pending:,} pending.")


if __name__ == "__main__":
    main()
