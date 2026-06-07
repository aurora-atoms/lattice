#!/usr/bin/env python3
"""Generate starter TMDL measures from metric-catalog.yaml.

Usage:
  generate_measures_tmdl.py <specs-dir> --out measures.tmdl

This generator covers only safe starter patterns. Review generated TMDL before applying.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception as exc:  # pragma: no cover
    print("ERROR: PyYAML is required. Install with: pip install pyyaml")
    raise SystemExit(2) from exc


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def q_table(table: str) -> str:
    return f"'{table}'" if " " in table else table


def col_ref(table: str, column: str) -> str:
    return f"{q_table(table)}[{column}]"


def measure_ref(name: str) -> str:
    return name if name.startswith("[") and name.endswith("]") else f"[{name}]"


def indent_expr(expr: str, spaces: int = 8) -> str:
    pad = " " * spaces
    return "\n".join(pad + line if line.strip() else line for line in expr.strip().splitlines())


def expression(metric: dict[str, Any]) -> str:
    pattern = metric.get("pattern")
    if pattern == "sum":
        return f"SUM ( {col_ref(metric['table'], metric['column'])} )"
    if pattern == "distinct_count":
        return f"DISTINCTCOUNT ( {col_ref(metric['table'], metric['column'])} )"
    if pattern == "count_rows":
        return f"COUNTROWS ( {q_table(metric['table'])} )"
    if pattern == "weighted_average":
        table = metric["fact_table"]
        value = col_ref(table, metric["value_column"])
        weight = col_ref(table, metric["weight_column"])
        return f"""DIVIDE (
    SUMX (
        {q_table(table)},
        {value} * {weight}
    ),
    SUM ( {weight} )
)"""
    if pattern == "delta":
        return f"{measure_ref(metric['left_measure'])} - {measure_ref(metric['right_measure'])}"
    if pattern == "ratio":
        return f"DIVIDE ( {measure_ref(metric['numerator_measure'])}, {measure_ref(metric['denominator_measure'])} )"
    if pattern == "custom":
        return str(metric["expression"])
    raise ValueError(f"unsupported pattern: {pattern}")


def generate(metrics_doc: dict[str, Any], table_name: str = "_Measures") -> str:
    lines = [f"table {table_name}", "", "    lineageTag: generated", "", "    partition p = calculated", "        mode: import", "        source =", "            DATATABLE(\"_\", INTEGER, { { 0 } })", ""]
    for metric in metrics_doc.get("metrics", []):
        name = metric["object_name"]
        expr = expression(metric)
        lines.append(f"    measure '{name}' =")
        lines.append(indent_expr(expr, 8))
        lines.append(f"        formatString: \"{metric.get('format', '')}\"")
        if metric.get("display_folder"):
            lines.append(f"        displayFolder: \"{metric['display_folder']}\"")
        if metric.get("description"):
            safe_desc = str(metric["description"]).replace('"', '\\"')
            lines.append(f"        description: \"{safe_desc}\"")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("specs_dir", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--table-name", default="_Measures")
    args = parser.parse_args()

    metrics_doc = load_yaml(args.specs_dir / "metric-catalog.yaml")
    args.out.write_text(generate(metrics_doc, args.table_name), encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
