#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Run heterogeneous deterministic Lattice conformance evals."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
EVAL_DIR = BASE_DIR / "evals"
PYTHON = sys.executable
CASE_CONTRACT = "lat.eval-case.v1"
CASE_SCHEMA_VERSION = "1.0.0"
SUPPORTED_CASE_TYPES = {
    "feature_delivery",
    "reusable_asset_loop",
    "synthetic_downstream",
}


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


def parse_jsonl_text(text: str) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        if not isinstance(record, dict):
            raise ValueError("generated JSONL record is not an object")
        records.append(record)
    return records


def declared_external_refs(records: list[dict[str, object]]) -> set[str]:
    refs: set[str] = set()
    for record in records:
        constraints = record.get("constraints", {})
        if isinstance(constraints, dict):
            refs.update(str(ref) for ref in constraints.get("declared_external_refs", []))
    return refs


def unresolved_evidence_refs(generated: list[dict[str, object]], source_records: list[dict[str, object]]) -> set[str]:
    known_refs = {str(record.get("id")) for record in source_records}
    known_refs.update(declared_external_refs(source_records))
    unresolved: set[str] = set()
    for record in generated:
        payload = record.get("payload", {})
        if not isinstance(payload, dict):
            continue
        for ref in payload.get("evidence_refs", []):
            if str(ref) not in known_refs:
                unresolved.add(str(ref))
    return unresolved


def write_temp_jsonl(text: str) -> Path:
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", newline="\n", suffix=".jsonl") as temp:
        temp.write(text)
        return Path(temp.name)


def read_single_jsonl(path: Path) -> dict[str, object]:
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(lines) != 1:
        raise ValueError(f"expected one JSONL record in {path}, found {len(lines)}")
    record = json.loads(lines[0])
    if not isinstance(record, dict):
        raise ValueError(f"record in {path} is not an object")
    return record


def append_single_jsonl_record(input_path: Path, record_path: Path) -> Path:
    source = input_path.read_text(encoding="utf-8").rstrip()
    record = record_path.read_text(encoding="utf-8").strip()
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", newline="\n", suffix=".jsonl") as temp:
        if source:
            temp.write(source)
            temp.write("\n")
        temp.write(record)
        temp.write("\n")
        return Path(temp.name)


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


def run_feature_delivery_case(case_dir: Path) -> tuple[bool, str]:
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
    if waste_result.stdout.strip():
        temp_waste: Path | None = None
        try:
            waste_records = parse_jsonl_text(waste_result.stdout)
            source_records = parse_jsonl_text(input_path.read_text(encoding="utf-8"))
            unresolved_refs = unresolved_evidence_refs(waste_records, source_records)
            if unresolved_refs:
                ok = False
                notes.append("unresolved waste evidence refs: " + ", ".join(sorted(unresolved_refs)))
            temp_waste = write_temp_jsonl(waste_result.stdout)
            validate_waste = run([PYTHON, str(BASE_DIR / "scripts" / "validate_jsonl.py"), str(temp_waste)])
            if validate_waste.returncode != 0:
                ok = False
                notes.append(f"waste JSONL validation exit {validate_waste.returncode}: {validate_waste.stderr.strip()}")
        except Exception as exc:
            ok = False
            notes.append(f"waste JSONL readback failed: {exc}")
        finally:
            if temp_waste is not None:
                temp_waste.unlink(missing_ok=True)
    missing_waste = waste_expected - actual_waste
    if missing_waste:
        ok = False
        notes.append("missing waste patterns: " + ", ".join(sorted(missing_waste)))
    unexpected_waste = actual_waste - waste_expected - allowed_extra_waste
    if unexpected_waste:
        ok = False
        notes.append("unexpected waste patterns: " + ", ".join(sorted(unexpected_waste)))

    out_verdict: Path | None = None
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

    if expected.get("expect_dossier"):
        out_md = BASE_DIR / "reports" / "generated" / f"{case_dir.name}.token_economics_dossier.md"
        out_jsonl = BASE_DIR / "reports" / "generated" / f"{case_dir.name}.yield_dossier.jsonl"
        dossier_input = input_path
        temp_dossier_input: Path | None = None
        if out_verdict is not None and out_verdict.exists():
            temp_dossier_input = append_single_jsonl_record(input_path, out_verdict)
            dossier_input = temp_dossier_input
        try:
            dossier = run([PYTHON, str(BASE_DIR / "scripts" / "generate_token_economics_dossier.py"), str(dossier_input), "--out-md", str(out_md), "--out-jsonl", str(out_jsonl)])
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
        finally:
            if temp_dossier_input is not None:
                temp_dossier_input.unlink(missing_ok=True)
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
    return ok, "; ".join(notes) if notes else "ok"


def load_case_manifest(case_dir: Path) -> dict[str, object]:
    path = case_dir / "case.json"
    if not path.is_file():
        raise ValueError("missing required case.json")
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"malformed case.json: {exc.msg}") from exc
    if not isinstance(manifest, dict):
        raise ValueError("case.json must be an object")
    required = {
        "contract",
        "schema_version",
        "case_id",
        "case_type",
        "required_files",
    }
    missing = sorted(required - set(manifest))
    if missing:
        raise ValueError("case.json missing fields: " + ", ".join(missing))
    extra = sorted(set(manifest) - required)
    if extra:
        raise ValueError("case.json unknown fields: " + ", ".join(extra))
    if manifest["contract"] != CASE_CONTRACT:
        raise ValueError(f"case contract must be {CASE_CONTRACT}")
    if manifest["schema_version"] != CASE_SCHEMA_VERSION:
        raise ValueError(
            f"incompatible case schema version: {manifest['schema_version']}"
        )
    if manifest["case_id"] != case_dir.name:
        raise ValueError("case_id must match the case directory name")
    case_type = str(manifest["case_type"])
    if case_type not in SUPPORTED_CASE_TYPES:
        raise ValueError(f"unknown case_type: {case_type}")
    required_files = manifest["required_files"]
    if (
        not isinstance(required_files, list)
        or not required_files
        or any(not isinstance(item, str) or not item for item in required_files)
    ):
        raise ValueError("required_files must be a non-empty string array")
    for relative in required_files:
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"unsafe required file path: {relative}")
        if not (case_dir / path).is_file():
            raise ValueError(f"missing required file: {relative}")
    return manifest


def run_reusable_asset_case(case_dir: Path) -> tuple[bool, str]:
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".md"
    ) as temp_output:
        out = Path(temp_output.name)
    try:
        result = run(
            [
                PYTHON,
                str(BASE_DIR / "scripts" / "run_reusable_asset_loop.py"),
                str(case_dir / "input.jsonl"),
                "--out",
                str(out),
                "--expected",
                str(case_dir / "expected_dossier.md"),
            ]
        )
        if result.returncode:
            return False, result.stderr.strip() or result.stdout.strip()
        return True, "ok"
    finally:
        out.unlink(missing_ok=True)


def run_synthetic_downstream_case(case_dir: Path) -> tuple[bool, str]:
    config = json.loads((case_dir / "example.json").read_text(encoding="utf-8"))
    if not isinstance(config, dict) or set(config) != {"example_path"}:
        return False, "example.json must contain only example_path"
    relative = Path(str(config["example_path"]))
    if relative.is_absolute() or ".." in relative.parts:
        return False, "example_path must be a safe repository-relative path"
    repo_root = BASE_DIR.parent
    example_root = repo_root / relative
    runner = example_root / "run_conformance.py"
    if not runner.is_file():
        return False, f"synthetic downstream runner missing: {relative}/run_conformance.py"
    result = run(
        [
            PYTHON,
            str(runner),
            "--root",
            str(example_root),
            "--lattice-root",
            str(repo_root),
            "--check",
        ]
    )
    if result.returncode:
        return False, result.stderr.strip() or result.stdout.strip()
    return True, "ok"


def dispatch_case(case_dir: Path) -> tuple[bool, str, str]:
    try:
        manifest = load_case_manifest(case_dir)
    except (OSError, ValueError) as exc:
        return False, str(exc), "unknown"
    case_type = str(manifest["case_type"])
    try:
        if case_type == "feature_delivery":
            ok, note = run_feature_delivery_case(case_dir)
        elif case_type == "reusable_asset_loop":
            ok, note = run_reusable_asset_case(case_dir)
        elif case_type == "synthetic_downstream":
            ok, note = run_synthetic_downstream_case(case_dir)
        else:
            return False, f"unknown case_type: {case_type}", case_type
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        return False, f"{case_type} handler failed: {exc}", case_type
    return ok, note, case_type


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", help="Optional single eval case name.")
    parser.add_argument(
        "--eval-dir",
        default=str(EVAL_DIR),
        help="Eval directory. Defaults to the repository conformance cases.",
    )
    parser.add_argument(
        "--summary-out",
        default=str(BASE_DIR / "reports" / "generated" / "conformance-summary.json"),
        help="Machine-readable validation summary.",
    )
    args = parser.parse_args()
    eval_dir = Path(args.eval_dir)
    cases = (
        [eval_dir / args.case]
        if args.case
        else sorted(path for path in eval_dir.iterdir() if path.is_dir())
    )
    results: list[dict[str, object]] = []
    for case in cases:
        if not case.is_dir():
            ok, note, case_type = False, "case directory does not exist", "unknown"
        else:
            ok, note, case_type = dispatch_case(case)
        status = "PASS" if ok else "FAIL"
        print(f"{status} {case.name}: {note}")
        results.append(
            {
                "case_id": case.name,
                "case_type": case_type,
                "status": status.lower(),
                "note": note,
            }
        )
    failed = sum(item["status"] == "fail" for item in results)
    summary = {
        "contract": "lat.conformance-summary.v1",
        "schema_version": "1.0.0",
        "total": len(results),
        "passed": len(results) - failed,
        "failed": failed,
        "results": results,
    }
    summary_path = Path(args.summary_out)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"wrote conformance summary to {summary_path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
