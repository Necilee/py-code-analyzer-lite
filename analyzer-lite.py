from __future__ import annotations
import argparse
import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional


@dataclass
class Issue:
    file: Optional[str]
    line: Optional[int]
    col: Optional[int]
    code: Optional[str]
    message: str
    raw: str
    context: Optional[List[str]] = None


RUFF_LINE_RE = re.compile(
    # Typical forms:
    # path/to/file.py:12:5: F401 message...
    # path\to\file.py:12:5: F821 message...
    r"^(?P<file>.+?):(?P<line>\d+):(?P<col>\d+):\s+(?P<code>[A-Z]\d{3})\s+(?P<msg>.+)$"
)


def run_ruff(target: str) -> tuple[int, str]:
    """Run ruff and return (exit_code, stdout_text)."""
    if shutil.which("ruff") is None:
        raise RuntimeError(
            "Ruff nije pronađen. Instaliraj ga sa: pip install ruff"
        )

    # We prefer stdout parsing; ruff prints findings to stdout.
    cmd = ["ruff", "check", target]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    output = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, output


def read_context(file_path: str, line: int, context_lines: int) -> List[str]:
    """Return context lines around a 1-based line number."""
    p = Path(file_path)
    if not p.exists() or not p.is_file():
        return []

    try:
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return []

    # Convert 1-based -> 0-based
    idx = max(0, line - 1)
    start = max(0, idx - context_lines)
    end = min(len(lines), idx + context_lines + 1)

    out = []
    for i in range(start, end):
        prefix = ">" if i == idx else " "
        out.append(f"{prefix} {i+1:4d} | {lines[i]}")
    return out


def parse_issues(ruff_output: str, context_lines: int) -> List[Issue]:
    issues: List[Issue] = []
    for raw_line in ruff_output.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        m = RUFF_LINE_RE.match(line)
        if m:
            f = m.group("file")
            ln = int(m.group("line"))
            col = int(m.group("col"))
            code = m.group("code")
            msg = m.group("msg").strip()

            ctx = None
            if context_lines > 0:
                ctx = read_context(f, ln, context_lines)

            issues.append(
                Issue(
                    file=f,
                    line=ln,
                    col=col,
                    code=code,
                    message=msg,
                    raw=raw_line,
                    context=ctx,
                )
            )
        else:
            # Fallback: keep raw line as issue without location
            issues.append(
                Issue(
                    file=None,
                    line=None,
                    col=None,
                    code=None,
                    message=line,
                    raw=raw_line,
                    context=None,
                )
            )

    return issues


def write_txt(out_path: str, target: str, exit_code: int, issues: List[Issue]) -> None:
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with p.open("w", encoding="utf-8") as f:
        f.write("Py Code Analyzer (LITE) - Report\n")
        f.write(f"Generated: {now}\n")
        f.write(f"Target: {target}\n")
        f.write(f"Ruff exit code: {exit_code}\n")
        f.write(f"Issues: {len(issues)}\n")
        f.write("\n")

        for i, iss in enumerate(issues, start=1):
            loc = "N/A"
            if iss.file and iss.line and iss.col:
                loc = f"{iss.file}:{iss.line}:{iss.col}"
            code = iss.code or "-"
            f.write(f"[{i}] {loc}  {code}\n")
            f.write(f"    {iss.message}\n")
            if iss.context:
                f.write("    Context:\n")
                for ctx_line in iss.context:
                    f.write(f"    {ctx_line}\n")
            f.write("\n")


def write_json(out_path: str, target: str, exit_code: int, issues: List[Issue]) -> None:
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "tool": "py-code-analyzer-lite",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "target": target,
        "ruff_exit_code": exit_code,
        "issue_count": len(issues),
        "issues": [asdict(x) for x in issues],
    }

    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Py Code Analyzer (LITE) - Ruff-based static analysis + reports"
    )
    ap.add_argument("target", help="Putanja do projekta/foldera ili fajla za analizu")
    ap.add_argument("--out", default="report.txt", help="TXT report path (default: report.txt)")
    ap.add_argument("--json", default="report.json", help="JSON report path (default: report.json)")
    ap.add_argument("--context", type=int, default=0, help="Broj linija konteksta (default: 0)")

    args = ap.parse_args()

    target = args.target
    if not Path(target).exists():
        print(f"[ERROR] Target ne postoji: {target}")
        return 2

    try:
        exit_code, output = run_ruff(target)
    except Exception as e:
        print(f"[ERROR] {e}")
        return 2

    issues = parse_issues(output, context_lines=max(0, args.context))

    write_txt(args.out, target, exit_code, issues)
    write_json(args.json, target, exit_code, issues)

    print(f"[OK] TXT report: {args.out}")
    print(f"[OK] JSON report: {args.json}")
    print(f"[OK] Issues: {len(issues)}")

    # Keep ruff exit code semantics: 0 means no issues, non-zero means issues found
    return 0 if exit_code == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
