#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_ACTIVATE="$SCRIPT_DIR/.venv/bin/activate"

if [ ! -f "$VENV_ACTIVATE" ]; then
    echo "Error: virtual environment not found at $VENV_ACTIVATE"
    exit 1
fi

# shellcheck disable=SC1090
source "$VENV_ACTIVATE"

set +e
python -m pytest test_app.py
TEST_EXIT_CODE=$?
set -e

deactivate

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "All tests passed."
    exit 0
else
    echo "One or more tests failed."
    exit 1
fi
