#!/usr/bin/env bash
# Double-click-friendly (or run from terminal) launcher for the inbox watcher.
cd "$(dirname "$0")"
./venv/bin/python watch_inbox.py
