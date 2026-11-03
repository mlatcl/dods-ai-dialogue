"""Config lint, permalink tree, segment dummies, and HTTP smoke."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
import yaml


def _referia_bin(venv_python: Path) -> Path:
    return venv_python.parent / "referia"


def test_referia_check_clean(study_root: Path, venv_python: Path):
    referia = _referia_bin(venv_python)
    proc = subprocess.run(
        [str(referia), "check", "--root", str(study_root), "--format", "json"],
        cwd=study_root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    payload = json.loads(proc.stdout)
    assert payload["error_count"] == 0
    assert payload["total_scanned"] >= 10


def test_permalink_tree_covers_stages(study_root: Path, venv_python: Path):
    code = """
from referia.config.permalinks import build_permalink_tree
tree = build_permalink_tree(%r)
need = {"/", "/01_chunk/", "/06_compare/", "/07_part_b/", "/10_sequence/"}
missing = sorted(need - set(tree))
print("count", len(tree))
print("missing", missing)
assert not missing, missing
""" % str(study_root)
    proc = subprocess.run(
        [str(venv_python), "-c", code],
        cwd=study_root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout


def test_segment_dummy_transcripts(seeded_dummies: Path, venv_python: Path):
    catalog = yaml.safe_load(
        (seeded_dummies / "_data" / "corpus" / "documents.yml").read_text(
            encoding="utf-8"
        )
    )
    assert isinstance(catalog, list) and catalog
    code = r"""
import sys, yaml
from pathlib import Path
from lynguine.access.documents import segment_pdf

root = Path(sys.argv[1])
rows = yaml.safe_load((root / "_data/corpus/documents.yml").read_text())
files_root = root / "files"
ok = 0
for row in rows:
    path = files_root / row["filename"]
    assert path.is_file(), path
    units = segment_pdf(
        str(path),
        reader=row.get("reader") or "docx",
        strategy=row["strategy"],
        aspect="dialogue_units",
        allowed_roots=[str(files_root)],
        facilitator_names=["Facilitator"],
        min_unit_words=4,
    )
    assert units, f"no units for {path}"
    ok += 1
print("segmented", ok)
"""
    proc = subprocess.run(
        [str(venv_python), "-c", code, str(seeded_dummies)],
        cwd=seeded_dummies,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "segmented" in proc.stdout


def test_serve_hub_and_chunk(seeded_dummies: Path, venv_python: Path):
    code = r"""
from pathlib import Path
from fastapi.testclient import TestClient
from referia.web.app import create_app

root = Path(%r)
assert (root / "_data/corpus/records.parquet").is_file(), "missing smoke records.parquet"
app = create_app(root=str(root), urls="permalink")
with TestClient(app) as client:
    # 06_compare precomputes lens mix and needs a real responsibilities
    # matrix; smoke only opens pages that load on the empty pack.
    for path in ("/", "/01_chunk/", "/07_part_b/"):
        resp = client.get(path)
        assert resp.status_code == 200, (path, resp.status_code, resp.text[:500])
        assert "Config not found" not in resp.text, path
print("http ok")
""" % str(seeded_dummies)
    proc = subprocess.run(
        [str(venv_python), "-c", code],
        cwd=seeded_dummies,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
