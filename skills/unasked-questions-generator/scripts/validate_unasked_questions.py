#!/usr/bin/env python3
import json
import sys
from pathlib import Path

BLOCKING = {
    "must_answer_now",
    "must_answer_before_implementation",
    "must_answer_before_merge",
    "must_answer_before_release",
}


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: validate_unasked_questions.py <artifact.json>")
    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("record_type") != "lat.unasked_questions.v1":
        fail("record_type must be lat.unasked_questions.v1")
    for field in ("review_id", "stage", "next_gate", "evidence_cutoff"):
        if not str(data.get(field, "")).strip():
            fail(f"missing {field}")
    questions = data.get("questions")
    if not isinstance(questions, list):
        fail("questions must be a list")
    ids = set()
    for index, item in enumerate(questions):
        qid = str(item.get("id", "")).strip()
        if not qid or qid in ids:
            fail(f"question {index} has missing or duplicate id")
        ids.add(qid)
        for field in ("question", "importance", "consequence", "answer_role", "latest_safe_answer_time", "gate", "expected_answer_form", "next_action"):
            if not str(item.get(field, "")).strip():
                fail(f"{qid}: missing {field}")
        if not item.get("evidence"):
            fail(f"{qid}: at least one evidence reference is required")
        if not item.get("affected_boundaries"):
            fail(f"{qid}: affected_boundaries is required")
        disposition = item.get("disposition")
        if disposition in BLOCKING and not str(item.get("blocking_rationale", "")).strip():
            fail(f"{qid}: blocker requires blocking_rationale")
        if disposition == "accepted_uncertainty":
            if not str(item.get("monitoring", "")).strip() or not str(item.get("reopen_trigger", "")).strip():
                fail(f"{qid}: accepted uncertainty requires monitoring and reopen_trigger")
    summary = data.get("control_summary", {})
    if not isinstance(summary.get("human_authorities"), list) or not summary.get("human_authorities"):
        fail("control_summary.human_authorities must name at least one role")
    print(f"validated {path}: {len(questions)} questions")


if __name__ == "__main__":
    main()
