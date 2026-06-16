#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate Feature Delivery Harness JSONL records."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from fdh_lib import read_jsonl, stable_json, validate_records, validation_result_record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", help="Input JSONL file.")
    parser.add_argument("--emit-validation-result", action="store_true", help="Print validation.result JSONL for failures.")
    args = parser.parse_args()

    path = Path(args.jsonl)
    if not path.exists():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2

    records, read_failures = read_jsonl(path)
    failures = read_failures + validate_records(records)
    if failures:
        if args.emit_validation_result:
            for item in failures:
                print(stable_json(validation_result_record(str(item["code"]), str(item["message"]))))
        else:
            for item in failures:
                print(json.dumps(item, sort_keys=True), file=sys.stderr)
        return 1
    print(f"validated {len(records)} record(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
