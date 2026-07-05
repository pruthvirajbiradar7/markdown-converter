#!/usr/bin/env bash
# One-time setup for macOS / Linux.
# Creates a virtual environment in ./venv and installs dependencies into it.

set -e
cd "$(dirname "$0")"

if ! command -v python3 &> /dev/null; then
    echo "Python 3 was not found. Install it from https://www.python.org/downloads/ and re-run this script."
    exit 1
fi

echo "Creating virtual environment in ./venv ..."
python3 -m venv venv

echo "Installing dependencies (this can take a minute, MarkItDown pulls in several format libraries) ..."
./venv/bin/pip install --upgrade pip -q
./venv/bin/pip install -r requirements.txt -q

echo ""
echo "Setup complete."
echo ""
echo "Try it:"
echo "  ./venv/bin/python mdconvert.py somefile.pdf"
echo ""
echo "Or start the watched inbox folder:"
echo "  ./venv/bin/python watch_inbox.py"
echo ""
echo "Tip: add this folder to your PATH, or create a shell alias, so you can"
echo "just type 'mdconvert somefile.pdf' from anywhere. See README.md."
