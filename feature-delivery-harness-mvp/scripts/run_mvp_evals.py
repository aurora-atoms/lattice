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


def read_single_jsonl(path: Path) -> dict[str, object]:
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(lines) != 1:
        raise ValueError(f"expected one JSONL record in {path}, found {len(lines)}")
    record = json.loads(lines[0])
    if not isinstance(record, dict):
        raise ValueError(f"record in {path} is not an object")
    return record


def run_expected_code_check(
    name: str,
    result: subprocess.CompletedProcess[str],
    expected_exit: int,
    expected_codes: set[str],
    allowed_extra_codes: set[str],
    notes: list[str],
) -> bool:
    ok = True
    if result.returncode != expected_exit:
        ok = False
        notes.append(f"{name} exit {result.returncode}, expected {expected_exit}")
    actual_codes = collect_codes(result.stderr)
    missing_codes = expected_codes - actual_codes
    if missing_codes:
        ok = False
        notes.append(f"{name} missing failure codes: " + ", ".join(sorted(missing_codes)))
    unexpected_codes = actual_codes - expected_codes - allowed_extra_codes
    if unexpected_codes:
        ok = False
        notes.append(f"{name} unexpected failure codes: " + ", ".join(sorted(unexpected_codes)))
    return ok


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
    if "check_evidence_exit" in expected:
        evidence_result = run([PYTHON, str(BASE_DIR / "scripts" / "check_evidence_completeness.py"), str(input_path)])
        evidence_ok = run_expected_code_check(
            "check_evidence_completeness",
            evidence_result,
            int(expected.get("check_evidence_exit", 0)),
            set(expected.get("expected_evidence_failure_codes", [])),
            set(expected.get("allowed_extra_evidence_failure_codes", [])),
            notes,
        )
        ok = ok and evidence_ok
    if expected.get("expect_context_pack"):
        out_context = BASE_DIR / "reports" / "generated" / f"{case_dir.name}.context_pack.jsonl"
        context_result = run([PYTHON, str(BASE_DIR / "scripts" / "build_context_pack.py"), str(input_path), "--out", str(out_context)])
        if context_result.returncode != 0:
            ok = False
            notes.append(f"build_context_pack exit {context_result.returncode}: {context_result.stderr.strip()}")
        validate_context = run([PYTHON, str(BASE_DIR / "scripts" / "validate_jsonl.py"), str(out_context)])
        if validate_context.returncode != 0:
            ok = False
            notes.append(f"context_pack validation exit {validate_context.returncode}: {validate_context.stderr.strip()}")
    if expected.get("expect_delivery_verdict"):
        out_verdict = BASE_DIR / "reports" / "generated" / f"{case_dir.name}.delivery_verdict.jsonl"
        verdict_result = run([PYTHON, str(BASE_DIR / "scripts" / "author_delivery_verdict.py"), str(input_path), "--out", str(out_verdict)])
        if verdict_result.returncode != 0:
            ok = False
            notes.append(f"author_delivery_verdict exit {verdict_result.returncode}: {verdict_result.stderr.strip()}")
        validate_verdict = run([PYTHON, str(BASE_DIR / "scripts" / "validate_jsonl.py"), str(out_verdict)])
        if validate_verdict.returncode != 0:
            ok = False
            notes.append(f"delivery_verdict validation exit {validate_verdict.returncode}: {validate_verdict.stderr.strip()}")
        if out_verdict.exists():
            try:
                verdict_record = read_single_jsonl(out_verdict)
                payload = verdict_record.get("payload", {})
                if not isinstance(payload, dict):
                    raise ValueError("delivery.verdict payload is not an object")
                expected_verdict = expected.get("expected_delivery_verdict")
                if expected_verdict and payload.get("verdict") != expected_verdict:
                    ok = False
                    notes.append(f"delivery verdict {payload.get('verdict')}, expected {expected_verdict}")
                expected_conflicts = set(expected.get("expected_verdict_conflict_codes", []))
                actual_conflicts = set(str(item) for item in payload.get("conflict_codes", []))
                missing_conflicts = expected_conflicts - actual_conflicts
                if missing_conflicts:
                    ok = False
                    notes.append("missing verdict conflict codes: " + ", ".join(sorted(missing_conflicts)))
                unexpected_conflicts = actual_conflicts - expected_conflicts - set(expected.get("allowed_extra_verdict_conflict_codes", []))
                if unexpected_conflicts:
                    ok = False
                    notes.append("unexpected verdict conflict codes: " + ", ".join(sorted(unexpected_conflicts)))
            except Exception as exc:
                ok = False
                notes.append(f"delivery_verdict readback failed: {exc}")
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
