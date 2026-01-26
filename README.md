# Py Code Analyzer (LITE)

A simple, fast CLI tool for analyzing Python projects using **Ruff** and generating reports in **TXT** and **JSON**.

> This repository contains the **LITE** edition (public). Advanced features such as AI auto-fix, scoring, batch automation, and GUI are planned / available in a separate PRO edition.

---

## What it does (end-to-end)

1. Takes a target path (file or folder)
2. Runs `ruff check` on the target
3. Parses findings and generates:
   - `report.txt` (human-readable)
   - `report.json` (machine-readable)
4. (Optional) Adds **context lines** around the reported location

---

## Requirements

- Python 3.10+ recommended
- Ruff installed (via requirements)

---

## Install

```bash
pip install -r requirements.txt

##Quickstart
Run against a single file:

python analyzer-lite.py examples/sample_bad.py --out report.txt --json report.json --context 2

Run against the current folder:
python analyzer-lite.py . --out report.txt --json report.json

##Exit codes

0 – no issues found

1 – issues found

2 – execution error (invalid path, Ruff not installed, etc.)


Why Ruff?

Ruff is a fast, modern Python linter that covers a wide range of rules.
In this project, Ruff acts as the analysis engine, while this tool handles
orchestration, reporting, and optional context extraction.

Scope and limitations

This tool focuses on static analysis and reporting.
It does not execute code, run tests, or modify files in the LITE edition.


