from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional


@dataclass
class Issue:
    file: str
    line: int
    column: int
    code: str
    message: str
    context: Optional[List[str]] = None


def run_ruff_json(target: str) -> List[dict]:
    if shutil.which("ruff") is None:
        raise RuntimeError("Ruff not found. Install it with: pip install ruff")

    cmd = ["ruff", "check", target, "--output-format", "json"]
    proc = subprocess.run(cmd, capture_output=True, text=True)

    if proc.returncode not in (0, 1):
        raise RuntimeError(proc.stderr.strip())

    return json.loads(proc.stdout or "[]")


def read_context(file_path: str, line: int, context_lines: int) -> List[str]:
    p = Path(file_path)
    if not p.exists():
        return []

    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    idx = max(0, line - 1)
    start = max(0, idx - context_lines)
    end = min(len(lines), idx + context_lines + 1)

    out = []
    for i in range(start, end):
        prefix = ">" if i == idx else " "
        out.append(f"{prefix} {i+1:4d} | {lines[i]}")
    return out


def collect_issues(raw: List[dict], context_lines: int) -> List[Issue]:
    issues: List[Issue] = []

    for item in raw:
        file = item["filename"]
        line = item["location"]["row"]
        col = item["location"]["column"]
        code = item["code"]
        msg = item["message"]

        ctx = None
        if context_lines > 0:
            ctx = read_context(file, line, context_lines)

        issues.append(
            Issue(
                file=file,
                line=line,
                column=col,
                code=code,
                message=msg,
                context=ctx,
            )
        )

    return issues


def write_txt(path: str, target: str, issues: List[Issue]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    with p.open("w", encoding="utf-8") as f:
        f.write("Py Code Analyzer (LITE) - Report\n")
        f.write(f"Generated: {datetime.now()}\n")
        f.write(f"Target: {target}\n")
        f.write(f"Issues: {len(issues)}\n\n")

        for i, iss in enumerate(issues, 1):
            f.write(f"[{i}] {iss.file}:{iss.line}:{iss.column} {iss.code}\n")
            f.write(f"    {iss.message}\n")
            if iss.context:
                f.write("    Context:\n")
                for c in iss.context:
                    f.write(f"    {c}\n")
            f.write("\n")


def write_json(path: str, target: str, issues: List[Issue]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "tool": "py-code-analyzer-lite",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "target": target,
        "issue_count": len(issues),
        "issues": [asdict(i) for i in issues],
    }

    p.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Py Code Analyzer (LITE)")
    ap.add_argument("target", help="File or folder to analyze")
    ap.add_argument("--out", default="report.txt")
    ap.add_argument("--json", default="report.json")
    ap.add_argument("--context", type=int, default=0)

    args = ap.parse_args()

    if not Path(args.target).exists():
        print("Target does not exist.")
        return 2

    raw = run_ruff_json(args.target)
    issues = collect_issues(raw, args.context)

    write_txt(args.out, args.target, issues)
    write_json(args.json, args.target, issues)

    print(f"[OK] Issues found: {len(issues)}")
    return 0 if len(issues) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())