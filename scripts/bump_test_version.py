#!/usr/bin/env python3
"""Gammelt navn. Bruk scripts/bump_versions.py, som nå setter versjonene i både
index.html og test/index.html. Dette skriptet kaller det bare videre."""
import runpy
import sys
from pathlib import Path

sys.argv[0] = str(Path(__file__).with_name("bump_versions.py"))
runpy.run_path(sys.argv[0], run_name="__main__")
