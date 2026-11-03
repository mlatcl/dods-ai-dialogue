#!/usr/bin/env python3
"""Seed synthetic DOCX and catalog wiring for smoke runs.

Reads ``_data/corpus/documents.example.yml`` (or existing ``documents.yml``)
and writes missing transcript files under ``files/`` using lynguine's
synthetic builders. Does not overwrite existing DOCX (real private
transcripts stay put). Optionally refreshes empty ``facilitator_names``
in the 01 stage parameter stores so workshop segmentation matches the
dummy speaker label ``Facilitator``.

Usage (from study root, venv active with referia/lynguine installed):

    python scripts/seed_dummies.py
    python scripts/seed_dummies.py --force-docx
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "_data" / "corpus" / "documents.example.yml"
DOCUMENTS = ROOT / "_data" / "corpus" / "documents.yml"
LOCAL_EXAMPLE = ROOT / "local.example.yml"
LOCAL = ROOT / "local.yml"
PARAM_FILES = (
    ROOT / "_data" / "01_chunk" / "parameters.yml",
    ROOT / "_data" / "01_turns" / "parameters.yml",
)
DUMMY_FACILITATOR = "Facilitator"


def _load_rows(path: Path) -> list[dict]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise SystemExit(f"expected a YAML list in {path}")
    return [row for row in raw if isinstance(row, dict)]


def _ensure_catalog(*, force: bool) -> list[dict]:
    if force or not DOCUMENTS.is_file():
        DOCUMENTS.write_text(EXAMPLE.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Wrote {DOCUMENTS.relative_to(ROOT)}")
    else:
        print(f"Keeping {DOCUMENTS.relative_to(ROOT)}")
    return _load_rows(DOCUMENTS)


def _ensure_local(*, force: bool) -> None:
    if force or not LOCAL.is_file():
        LOCAL.write_text(LOCAL_EXAMPLE.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Wrote {LOCAL.relative_to(ROOT)}")
    else:
        print(f"Keeping {LOCAL.relative_to(ROOT)}")


def _write_docx(path: Path, *, format_name: str, force: bool) -> str:
    from lynguine.tests.fixtures.documents.builders import (
        make_chatbot_transcript,
        make_workshop_transcript,
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file() and not force:
        return "kept"
    if format_name == "chatbot":
        make_chatbot_transcript(path)
    elif format_name == "workshop":
        make_workshop_transcript(path)
    else:
        raise SystemExit(f"unknown format {format_name!r} for {path}")
    return "wrote"


def _patch_facilitator_names() -> None:
    """Set facilitator_names to the dummy label when the list is empty."""
    for path in PARAM_FILES:
        rows = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(rows, list) or not rows:
            continue
        row = rows[0]
        if not isinstance(row, dict):
            continue
        names = row.get("facilitator_names")
        if names:
            print(f"Keeping facilitator_names in {path.relative_to(ROOT)}")
            continue
        row["facilitator_names"] = [DUMMY_FACILITATOR]
        path.write_text(
            yaml.safe_dump(rows, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        print(
            f"Set facilitator_names: [{DUMMY_FACILITATOR!r}] in "
            f"{path.relative_to(ROOT)}"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force-docx",
        action="store_true",
        help="Overwrite existing DOCX under files/ with synthetic transcripts",
    )
    parser.add_argument(
        "--force-catalog",
        action="store_true",
        help="Overwrite documents.yml and local.yml from the examples",
    )
    parser.add_argument(
        "--skip-params",
        action="store_true",
        help="Do not touch facilitator_names in stage parameters.yml",
    )
    args = parser.parse_args(argv)

    if not EXAMPLE.is_file():
        print(f"error: missing {EXAMPLE}", file=sys.stderr)
        return 1

    _ensure_local(force=args.force_catalog)
    rows = _ensure_catalog(force=args.force_catalog)
    if not rows:
        print("error: catalog is empty", file=sys.stderr)
        return 1

    wrote = kept = 0
    for row in rows:
        filename = row.get("filename")
        fmt = row.get("format") or row.get("group")
        if not filename or not fmt:
            print(f"error: row missing filename/format: {row!r}", file=sys.stderr)
            return 1
        path = ROOT / "files" / str(filename)
        action = _write_docx(path, format_name=str(fmt), force=args.force_docx)
        print(f"  {action:5s} files/{filename}")
        if action == "wrote":
            wrote += 1
        else:
            kept += 1

    if not args.skip_params:
        _patch_facilitator_names()

    print(f"Dummy seed done ({wrote} written, {kept} kept).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
