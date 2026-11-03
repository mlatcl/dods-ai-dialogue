"""Run ``scripts/install.sh`` in an isolated study copy."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.slow
def test_install_script_with_dummies(isolated_study: Path):
    """Fresh venv + referia[llm] + dummy DOCX; then import and check."""
    if os.environ.get("SMOKE_SKIP_INSTALLER") == "1":
        pytest.skip("SMOKE_SKIP_INSTALLER=1")

    python = os.environ.get("SMOKE_PYTHON") or sys.executable
    script = isolated_study / "scripts" / "install.sh"
    assert script.is_file()
    env = {**os.environ, "PIP_DISABLE_PIP_VERSION_CHECK": "1"}
    proc = subprocess.run(
        ["bash", str(script), "--python", python, "--with-dummies"],
        cwd=isolated_study,
        env=env,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        pytest.fail(
            "install.sh failed\n"
            f"--- stdout ---\n{proc.stdout}\n"
            f"--- stderr ---\n{proc.stderr}"
        )

    venv_py = isolated_study / ".venv" / "bin" / "python"
    if os.name == "nt":
        venv_py = isolated_study / ".venv" / "Scripts" / "python.exe"
    assert venv_py.is_file()

    probe = subprocess.run(
        [
            str(venv_py),
            "-c",
            "import referia, lynguine; import langchain; print('ok')",
        ],
        cwd=isolated_study,
        capture_output=True,
        text=True,
        check=False,
    )
    assert probe.returncode == 0, probe.stderr
    assert "ok" in probe.stdout

    referia = venv_py.parent / "referia"
    check = subprocess.run(
        [str(referia), "check", "--root", ".", "--format", "json"],
        cwd=isolated_study,
        capture_output=True,
        text=True,
        check=False,
    )
    assert check.returncode == 0, check.stderr + check.stdout
    assert '"error_count": 0' in check.stdout or '"error_count":0' in check.stdout

    docs = list((isolated_study / "files" / "chatbot").glob("*.docx"))
    workshops = list((isolated_study / "files" / "workshops").glob("*.docx"))
    assert docs, "expected dummy chatbot DOCX"
    assert workshops, "expected dummy workshop DOCX"
    assert (isolated_study / "_data" / "corpus" / "documents.yml").is_file()
    assert (isolated_study / "local.yml").is_file()
