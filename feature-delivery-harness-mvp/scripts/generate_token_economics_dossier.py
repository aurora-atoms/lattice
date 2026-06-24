#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate a deterministic FDH Token Economics Dossier."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from fdh_lib import read_jsonl, records_by_type, stable_json, validate_records, write_text_lf


def metric_text(metric: dict[str, Any]) -> str:
    value = metric.get("value")
    unit = metric.get("unit", "unknown")
    status = metric.get("status", "unknown")
    if value is None:
        return f"unknown {unit} ({status})"
    return f"{value} {unit} ({status})"


def bullet(items: list[str]) -> str:
    if not items:
        return "- unknown"
    return "\n".join(f"- {item}" for item in sorted(items))


def sum_metric(records: list[dict[str, Any]], field: str, unit: str) -> dict[str, Any]:
    values = []
    statuses = []
    refs = []
    for record in records:
        metric = record.get("payload", {}).get(field, {})
        if isinstance(metric, dict):
            if isinstance(metric.get("value"), (int, float)):
                values.append(metric["value"])
            statuses.append(str(metric.get("status", "unknown")))
            refs.append(str(metric.get("source_ref", record.get("id", "unknown"))))
    if not values:
        return {"value": None, "unit": unit, "status": "unknown", "source_ref": "unknown"}
    status = "known" if all(item == "known" for item in statuses) else "estimated" if any(item == "estimated" for item in statuses) else statuses[0]
    return {"value": sum(values), "unit": unit, "status": status, "source_ref": ",".join(sorted(set(refs)))}


def determine_delivery_status(records: list[dict[str, Any]]) -> tuple[str, str]:
    verdicts = records_by_type(records, "delivery.verdict")
    if verdicts:
        verdict = verdicts[0]
        return str(verdict["payload"].get("verdict", "insufficient_evidence")), str(verdict["id"])
    evidence = records_by_type(records, "delivery.evidence")
    if not evidence:
        return "insufficient_evidence", "unknown"
    statuses = [str(record["payload"].get("user_usable_status", "insufficient_evidence")) for record in evidence]
    if "not_user_usable" in statuses:
        return "not_user_usable", evidence[0]["id"]
    if "requires_human_review" in statuses:
        return "requires_human_review", evidence[0]["id"]
    if "blocked" in statuses:
        return "blocked", evidence[0]["id"]
    if all(status == "usable" for status in statuses):
        return "usable", evidence[0]["id"]
    return "insufficient_evidence", evidence[0]["id"]


def build_dossier(records: list[dict[str, Any]]) -> tuple[dict[str, Any], str]:
    features = records_by_type(records, "feature_delivery_case")
    if not features:
        raise ValueError("feature_delivery_case record is required")
    feature = features[0]
    case_id = str(feature["scope"]["feature_delivery_case_id"])
    title = str(feature["payload"].get("title", case_id))
    stages = records_by_type(records, "yield.stage_breakdown")
    wastes = records_by_type(records, "yield.waste_pattern")
    signals = records_by_type(records, "yield.optimization_signal")
    delivery_status, delivery_ref = determine_delivery_status(records)
    total_tokens = sum_metric(stages, "tokens", "tokens")
    total_cost = sum_metric(stages, "cost", "usd")
    limitations = sorted({item for record in records_by_type(records, "delivery.evidence") for item in record["payload"].get("limitations", [])})
    if not limitations:
        limitations = ["No unresolved limitations were recorded in delivery.evidence."]

    claim_ledger = [
        {"claim": f"Delivery status is {delivery_status}.", "evidence_refs": [delivery_ref] if delivery_ref != "unknown" else [], "status": "supported" if delivery_ref != "unknown" else "insufficient_evidence"},
        {"claim": f"Total token usage is {metric_text(total_tokens)}.", "evidence_refs": sorted({record["id"] for record in stages}), "status": "supported" if stages else "unknown"},
        {"claim": f"Detected {len(wastes)} waste pattern(s).", "evidence_refs": sorted({record["id"] for record in wastes}), "status": "supported" if wastes else "unknown"},
    ]
    dossier_record = {
        "type": "yield.dossier",
        "id": f"dossier_{case_id}",
        "schema": "lat.yield.dossier.v1",
        "source": "generate_token_economics_dossier",
        "target": "manager_report",
        "scope": {"project_id": "lattice", "feature_delivery_case_id": case_id, "module_id": "deliveryyield"},
        "payload": {
            "feature_delivery_case_id": case_id,
            "delivery_status_ref": delivery_ref,
            "total_tokens": total_tokens,
            "total_cost": total_cost,
            "stage_breakdown_refs": sorted(record["id"] for record in stages),
            "waste_pattern_refs": sorted(record["id"] for record in wastes),
            "optimization_signal_refs": sorted(record["id"] for record in signals),
            "limitations": limitations,
            "claim_ledger": claim_ledger,
        },
        "constraints": {"deliveryyield_boundary": "economics_only"},
    }
    stage_lines = [f"{record['payload']['stage']}: {metric_text(record['payload']['tokens'])}; cost {metric_text(record['payload']['cost'])}; refs {', '.join(sorted(record['payload'].get('source_refs', [])))}" for record in sorted(stages, key=lambda item: item["id"])]
    waste_lines = [f"{record['payload']['pattern']}: {record['payload']['severity']}; {record['payload']['recommendation']}; refs {', '.join(sorted(record['payload'].get('evidence_refs', [])))}" for record in sorted(wastes, key=lambda item: item["id"])]
    signal_lines = [f"{record['payload']['signal_type']}: {record['payload']['recommendation']}; status {record['payload']['promotion_status']}; refs {', '.join(sorted(record['payload'].get('evidence_refs', [])))}" for record in sorted(signals, key=lambda item: item["id"])]
    claim_lines = [f"{item['claim']} evidence_refs={','.join(item['evidence_refs']) if item['evidence_refs'] else 'insufficient_evidence'} status={item['status']}" for item in claim_ledger]
    markdown = "\n".join(
        [
            f"# Token Economics Dossier: {title}",
            "",
            f"Feature Case: {case_id}",
            f"Delivery Status: {delivery_status}",
            "",
            "## Token And Cost",
            "",
            f"Total Tokens: {metric_text(total_tokens)}",
            f"Total Cost: {metric_text(total_cost)}",
            "",
            "## Stage Breakdown",
            "",
            bullet(stage_lines),
            "",
            "## Waste Patterns",
            "",
            bullet(waste_lines),
            "",
            "## Optimization Signals",
            "",
            bullet(signal_lines),
            "",
            "## Limitations",
            "",
            bullet(limitations),
            "",
            "## Claim Ledger",
            "",
            bullet(claim_lines),
            "",
        ]
    )
    return dossier_record, markdown


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", help="Input JSONL file.")
    parser.add_argument("--out-md", help="Markdown dossier output path.")
    parser.add_argument("--out-jsonl", help="yield.dossier JSONL output path.")
    parser.add_argument("--diagnostic", action="store_true", help="Generate despite validation failures.")
    args = parser.parse_args()

    records, read_failures = read_jsonl(Path(args.jsonl))
    failures = read_failures + validate_records(records)
    if failures and not args.diagnostic:
        for item in failures:
            print(item, file=sys.stderr)
        return 1
    try:
        record, markdown = build_dossier(records)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.out_md:
        write_text_lf(Path(args.out_md), markdown)
    else:
        print(markdown)
    if args.out_jsonl:
        write_text_lf(Path(args.out_jsonl), stable_json(record) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
