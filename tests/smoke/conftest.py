"""Smoke fixtures for the DODS study installer and referia configs."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def _venv_python(root: Path) -> Path:
    name = "Scripts" if os.name == "nt" else "bin"
    return root / ".venv" / name / ("python.exe" if os.name == "nt" else "python")


@pytest.fixture(scope="session")
def study_root() -> Path:
    return ROOT


@pytest.fixture(scope="session")
def venv_python(study_root: Path) -> Path:
    py = _venv_python(study_root)
    if not py.is_file():
        pytest.skip(
            "Study .venv missing; run ./scripts/install.sh --with-dummies first "
            "or use the smoke CI job"
        )
    return py


@pytest.fixture(scope="session")
def seeded_dummies(study_root: Path, venv_python: Path) -> Path:
    """Ensure catalog + synthetic DOCX exist (non-destructive for real files)."""
    subprocess.run(
        [str(venv_python), str(study_root / "scripts" / "seed_dummies.py")],
        cwd=study_root,
        check=True,
    )
    return study_root


@pytest.fixture
def isolated_study(tmp_path: Path) -> Path:
    """Copy a minimal study tree into tmp for installer isolation tests."""
    dst = tmp_path / "study"
    ignore = shutil.ignore_patterns(
        ".venv",
        ".git",
        "__pycache__",
        "*.pyc",
        ".env",
        "local.yml",
        "_site",
        "*.docx",
        "*.parquet",
        "*.log",
        ".llm_cache",
    )
    shutil.copytree(
        ROOT,
        dst,
        ignore=ignore,
        symlinks=False,
    )
    # Drop personal catalog if the copy included it via ignore miss.
    docs = dst / "_data" / "corpus" / "documents.yml"
    if docs.is_file():
        docs.unlink()
    for sub in ("chatbot", "workshops"):
        d = dst / "files" / sub
        d.mkdir(parents=True, exist_ok=True)
        for p in d.glob("*.docx"):
            p.unlink()
    return dst
