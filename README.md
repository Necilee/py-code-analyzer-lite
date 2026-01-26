# Py Code Analyzer (LITE)

A simple, fast CLI tool for analyzing Python projects using Ruff and generating reports.

## Edition / Scope Note (LITE vs PRO)

This repository contains the LITE edition (public).
Advanced features are available in a separate PRO edition.

## What it does (end-to-end)

1. Takes a target path (file or folder)
2. Runs Ruff static analysis
3. Parses findings
4. Generates TXT and JSON reports
5. Optionally adds context lines

## Requirements

- Python 3.10+
- Ruff (installed via requirements.txt)

## Install

```bash
pip install -r requirements.txt


## QUICKSTART

python analyzer-lite.py examples/sample_bad.py --out report.txt --json report.json --context 2

python analyzer-lite.py . --out report.txt --json report.json
## CLI OPTIONS
target
--out
--json
--context

## EXIT CODES
0 – no issues found
1 – issues found
2 – execution error

## WHY RUFF?
Ruff is a fast Python linter.
This tool uses Ruff as the analysis engine and adds orchestration and reporting.

## SCOPE & LIMITATIONS
This tool performs static analysis only.
It does not execute code, run tests, or modify files in the LITE edition.

## LICENSE
MIT


