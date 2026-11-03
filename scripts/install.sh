#!/usr/bin/env bash
# Install this DODS study per README.md Setup / API key / private-copy wiring.
#
# Usage (from the study root, or any cwd — the script finds the repo):
#   ./scripts/install.sh
#   ./scripts/install.sh --python python3.12
#   ./scripts/install.sh --with-dummies
#   ./scripts/install.sh --referia "git+https://github.com/lawrennd/referia.git@main"
#
# Does not clone the study (run inside an existing checkout). Does not start
# the server. Does not invent an OpenAI key — only scaffolds .env if missing.

set -euo pipefail

PYTHON="${PYTHON:-python3}"
WITH_DUMMIES=0
FORCE_LOCAL=0
REFERIA_SPEC='referia[llm] @ git+https://github.com/lawrennd/referia.git'
SKIP_VENV=0

usage() {
  cat <<'EOF'
Install dods-ai-dialogue dependencies and local wiring (README Setup).

Options:
  --python PATH     Interpreter for the venv (default: python3)
  --with-dummies    Seed synthetic DOCX + documents.yml for smoke runs
  --force-local     Overwrite local.yml / documents.yml from examples
  --referia SPEC    pip requirement for referia (default: git main + [llm])
  --skip-venv       Reuse an existing .venv (still pip-installs referia)
  -h, --help        Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --python)
      PYTHON="${2:?}"
      shift 2
      ;;
    --with-dummies)
      WITH_DUMMIES=1
      shift
      ;;
    --force-local)
      FORCE_LOCAL=1
      shift
      ;;
    --referia)
      REFERIA_SPEC="${2:?}"
      shift 2
      ;;
    --skip-venv)
      SKIP_VENV=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "error: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "error: interpreter not found: $PYTHON" >&2
  exit 1
fi

VER="$("$PYTHON" -c 'import sys; print("%d.%d" % sys.version_info[:2])')"
MAJOR="${VER%%.*}"
MINOR="${VER#*.}"
if [[ "$MAJOR" -lt 3 || ( "$MAJOR" -eq 3 && "$MINOR" -lt 11 ) ]]; then
  echo "error: Referia needs Python 3.11 or higher (found $VER via $PYTHON)." >&2
  echo "Install a newer Python and re-run, e.g. --python python3.12" >&2
  exit 1
fi
echo "Using $PYTHON ($VER)"

if [[ "$SKIP_VENV" -eq 0 ]]; then
  if [[ ! -d .venv ]]; then
    echo "Creating .venv"
    "$PYTHON" -m venv .venv
  else
    echo "Reusing existing .venv"
  fi
elif [[ ! -d .venv ]]; then
  echo "error: --skip-venv set but .venv is missing" >&2
  exit 1
fi

# shellcheck disable=SC1091
source .venv/bin/activate
python --version
python -m pip install --upgrade pip
echo "Installing $REFERIA_SPEC"
python -m pip install "$REFERIA_SPEC"

if [[ ! -f local.yml || "$FORCE_LOCAL" -eq 1 ]]; then
  cp local.example.yml local.yml
  echo "Wrote local.yml from local.example.yml"
else
  echo "Keeping existing local.yml"
fi

if [[ ! -f _data/corpus/documents.yml || "$FORCE_LOCAL" -eq 1 ]]; then
  cp _data/corpus/documents.example.yml _data/corpus/documents.yml
  echo "Wrote _data/corpus/documents.yml from documents.example.yml"
else
  echo "Keeping existing _data/corpus/documents.yml"
fi

mkdir -p files/chatbot files/workshops

if [[ ! -f .env ]]; then
  cat > .env <<'EOF'
# Referia LLM path (extract / grounds). Do not commit this file.
# OPENAI_API_KEY=sk-...
EOF
  echo "Wrote .env scaffold (add OPENAI_API_KEY when you call the LLM)"
else
  echo "Keeping existing .env"
fi

if [[ "$WITH_DUMMIES" -eq 1 ]]; then
  echo "Seeding dummy transcripts"
  python scripts/seed_dummies.py
fi

echo
echo "Install complete."
echo "  Activate:  source .venv/bin/activate"
echo "  Check:     referia check --root ."
echo "  Serve:     referia serve --root . --host 127.0.0.1 --port 8000"
if [[ "$WITH_DUMMIES" -eq 0 ]]; then
  echo "  Private:   fill local.yml, documents.yml, and files/ from the private store"
  echo "  Or smoke:  ./scripts/install.sh --with-dummies"
fi
