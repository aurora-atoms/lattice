#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Run deterministic Feature Delivery Harness MVP evals."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
EVAL_DIR = BASE_DIR / "evals"
PYTHON = sys.executable


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=BASE_DIR.parent, text=True, capture_output=True)


def collect_codes(text: str) -> set[str]:
    codes: set[str] = set()
    for line in text.splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(record, dict) and "code" in record:
            codes.add(str(record["code"]))
    return codes


def collect_waste_patterns(text: str) -> set[str]:
    patterns: set[str] = set()
    for line in text.splitlines():
        record = json.loads(line)
        patterns.add(str(record["payload"]["pattern"]))
    return patterns


def run_case(case_dir: Path) -> tuple[bool, str]:
    expected = json.loads((case_dir / "expected.json").read_text(encoding="utf-8"))
    input_path = case_dir / "input.jsonl"
    validate_jsonl = run([PYTHON, str(BASE_DIR / "scripts" / "validate_jsonl.py"), str(input_path)])
    validate_task = run([PYTHON, str(BASE_DIR / "scripts" / "validate_task_packet.py"), str(input_path)])
    ok = True
    notes: list[str] = []
    expected_jsonl = int(expected.get("validate_jsonl_exit", 0))
    expected_task = int(expected.get("validate_task_packet_exit", 0))
    if validate_jsonl.returncode != expected_jsonl:
        ok = False
        notes.append(f"validate_jsonl exit {validate_jsonl.returncode}, expected {expected_jsonl}")
    if validate_task.returncode != expected_task:
        ok = False
        notes.append(f"validate_task_packet exit {validate_task.returncode}, expected {expected_task}")
    expected_codes = set(expected.get("expected_failure_codes", []))
    allowed_extra_codes = set(expected.get("allowed_extra_failure_codes", []))
    actual_codes = collect_codes(validate_jsonl.stderr) | collect_codes(validate_task.stderr)
    missing_codes = expected_codes - actual_codes
    if missing_codes:
        ok = False
        notes.append("missing failure codes: " + ", ".join(sorted(missing_codes)))
    unexpected_codes = actual_codes - expected_codes - allowed_extra_codes
    if unexpected_codes:
        ok = False
        notes.append("unexpected failure codes: " + ", ".join(sorted(unexpected_codes)))

    waste_expected = set(expected.get("expected_waste_patterns", []))
    allowed_extra_waste = set(expected.get("allowed_extra_waste_patterns", []))
    waste_result = run([PYTHON, str(BASE_DIR / "scripts" / "detect_waste_patterns.py"), str(input_path)])
    actual_waste = collect_waste_patterns(waste_result.stdout) if waste_result.stdout.strip() else set()
    if waste_result.returncode != 0:
        ok = False
        notes.append(f"detect_waste_patterns exit {waste_result.returncode}: {waste_result.stderr.strip()}")
    missing_waste = waste_expected - actual_waste
    if missing_waste:
        ok = False
        notes.append("missing waste patterns: " + ", ".join(sorted(missing_waste)))
    unexpected_waste = actual_waste - waste_expected - allowed_extra_waste
    if unexpected_waste:
        ok = False
        notes.append("unexpected waste patterns: " + ", ".join(sorted(unexpected_waste)))

    if expected.get("expect_dossier"):
        out_md = BASE_DIR / "reports" / "generated" / f"{case_dir.name}.token_economics_dossier.md"
        out_jsonl = BASE_DIR / "reports" / "generated" / f"{case_dir.name}.yield_dossier.jsonl"
        dossier = run([PYTHON, str(BASE_DIR / "scripts" / "generate_token_economics_dossier.py"), str(input_path), "--out-md", str(out_md), "--out-jsonl", str(out_jsonl)])
        if dossier.returncode != 0:
            ok = False
            notes.append(f"dossier generation exit {dossier.returncode}: {dossier.stderr.strip()}")
        validate_dossier = run([PYTHON, str(BASE_DIR / "scripts" / "validate_jsonl.py"), str(out_jsonl)])
        if validate_dossier.returncode != 0:
            ok = False
            notes.append(f"generated dossier JSONL validation exit {validate_dossier.returncode}: {validate_dossier.stderr.strip()}")
        expected_dossier = case_dir / "expected_dossier.md"
        if not expected_dossier.exists():
            ok = False
            notes.append("missing expected_dossier.md for dossier-producing case")
        elif not out_md.exists():
            ok = False
            notes.append("dossier Markdown was not generated")
        elif expected_dossier.read_text(encoding="utf-8").strip() != out_md.read_text(encoding="utf-8").strip():
            ok = False
            notes.append("generated dossier differs from expected_dossier.md")
    return ok, "; ".join(notes) if notes else "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", help="Optional single eval case name.")
    args = parser.parse_args()
    cases = [EVAL_DIR / args.case] if args.case else sorted(path for path in EVAL_DIR.iterdir() if path.is_dir())
    failed = 0
    for case in cases:
        ok, note = run_case(case)
        status = "PASS" if ok else "FAIL"
        print(f"{status} {case.name}: {note}")
        if not ok:
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
