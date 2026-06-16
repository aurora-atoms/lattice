#!/usr/bin/env python3
"""Validate Power BI semantic accelerator spec files.

Usage:
  validate_powerbi_semantic_specs.py <specs-dir>

Required files:
  model-contract.yaml
  metric-catalog.yaml
  display-catalog.yaml

Optional files:
  selector-catalog.yaml
  source-catalog.yaml
  semantic-request.yaml
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None  # type: ignore


REQUIRED_FILES = ["model-contract.yaml", "metric-catalog.yaml", "display-catalog.yaml"]
OPTIONAL_FILES = ["selector-catalog.yaml", "source-catalog.yaml", "semantic-request.yaml"]
SUPPORTED_PATTERNS = {"sum", "distinct_count", "count_rows", "weighted_average", "delta", "ratio", "custom"}
SAFE_REQUEST_PATTERNS = SUPPORTED_PATTERNS | {"selector_addition"}
ALLOWED_AGGREGATION_SEMANTICS = {"additive", "semi_additive", "non_additive", "ratio", "weighted_average", "distinct_count", "count"}
ALLOWED_TIME_BEHAVIORS = {"flow", "balance", "snapshot", "period_end", "average_over_period", "point_in_time"}
ALLOWED_TABLE_ROLES = {"fact", "dimension", "bridge", "selector", "calculation", "helper"}
ALLOWED_SELECTOR_IMPLEMENTATIONS = {"field_parameter", "disconnected_selector", "numeric_parameter", "manual"}
ALLOWED_REQUEST_LIFECYCLE = {"draft", "validated", "compiled", "reviewed", "approved", "published", "deprecated", "rejected"}


def parse_scalar(value: str) -> Any:
    text = value.strip()
    if text in {"", "null", "Null", "NULL", "~"}:
        return None
    if text in {"true", "True", "TRUE"}:
        return True
    if text in {"false", "False", "FALSE"}:
        return False
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(item.strip()) for item in inner.split(",")]
    if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
        return text[1:-1]
    try:
        return int(text)
    except ValueError:
        return text


def strip_yaml_comment(line: str) -> str:
    in_single = False
    in_double = False
    for index, char in enumerate(line):
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            return line[:index]
    return line


def next_meaningful(lines: list[tuple[int, str]], start: int) -> tuple[int, str] | None:
    for index in range(start, len(lines)):
        return lines[index]
    return None


def parse_key_value(text: str) -> tuple[str, Any]:
    if ":" not in text:
        raise ValueError(f"expected key/value pair, got: {text}")
    key, value = text.split(":", 1)
    key = key.strip()
    if not key:
        raise ValueError(f"empty YAML key in: {text}")
    value = value.strip()
    return key, parse_scalar(value) if value else {}


def parse_block(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[Any, int]:
    next_item = next_meaningful(lines, index)
    if next_item is None:
        return {}, index
    if next_item[0] < indent:
        return {}, index
    if next_item[1].startswith("- "):
        values: list[Any] = []
        while index < len(lines):
            current_indent, text = lines[index]
            if current_indent < indent:
                break
            if current_indent != indent or not text.startswith("- "):
                break
            item_text = text[2:].strip()
            if not item_text:
                item, index = parse_block(lines, index + 1, indent + 2)
                values.append(item)
                continue
            if ":" in item_text and not item_text.startswith(("'", '"')):
                key, value = parse_key_value(item_text)
                item_obj: dict[str, Any] = {key: value}
                index += 1
                while index < len(lines):
                    child_indent, child_text = lines[index]
                    if child_indent <= current_indent:
                        break
                    child_key, child_value = parse_key_value(child_text)
                    if child_value == {}:
                        child_value, index = parse_block(lines, index + 1, child_indent + 2)
                    else:
                        index += 1
                    item_obj[child_key] = child_value
                values.append(item_obj)
            else:
                values.append(parse_scalar(item_text))
                index += 1
        return values, index
    values: dict[str, Any] = {}
    while index < len(lines):
        current_indent, text = lines[index]
        if current_indent < indent:
            break
        if current_indent != indent:
            break
        key, value = parse_key_value(text)
        index += 1
        if value == {}:
            nested, index = parse_block(lines, index, indent + 2)
            value = nested
        values[key] = value
    return values, index


def simple_yaml_load(text: str) -> Any:
    lines: list[tuple[int, str]] = []
    for raw_line in text.splitlines():
        line = strip_yaml_comment(raw_line).rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        lines.append((indent, line.strip()))
    if not lines:
        return {}
    parsed, index = parse_block(lines, 0, lines[0][0])
    if index != len(lines):
        raise ValueError(f"unsupported YAML structure near: {lines[index][1]}")
    return parsed


def load_yaml(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        return yaml.safe_load(text) or {}
    return simple_yaml_load(text) or {}


def load_yaml_checked(path: Path, errors: list[str]) -> Any:
    try:
        return load_yaml(path)
    except Exception as exc:
        err(errors, f"{path.name}: failed to parse YAML with dependency-free fallback: {exc}")
        return {}


def err(errors: list[str], msg: str) -> None:
    errors.append(msg)


def validate_source_policy(model: dict[str, Any], errors: list[str]) -> None:
    policy = model.get("source_policy", {})
    if not policy:
        return
    if str(policy.get("powerbi_mode", "")).lower() not in {"", "import"}:
        err(errors, "model-contract.yaml: source_policy.powerbi_mode must be import for quick-win validation")
    if policy.get("directquery_allowed") is True:
        err(errors, "model-contract.yaml: source_policy.directquery_allowed must not be true for v0.1 quick-win validation")
    if policy.get("databricks_runtime_dependency") is True:
        err(errors, "model-contract.yaml: source_policy.databricks_runtime_dependency must not be true for v0.1")
    serving_source = str(policy.get("serving_source", "")).lower()
    if "databricks" in serving_source and "directquery" in serving_source:
        err(errors, "model-contract.yaml: Databricks DirectQuery/serverless must not be the quick-win serving source")


def build_model_index(model: dict[str, Any], errors: list[str]) -> dict[str, set[str]]:
    validate_source_policy(model, errors)
    tables = model.get("tables")
    if not isinstance(tables, list) or not tables:
        err(errors, "model-contract.yaml: 'tables' must be a non-empty list")
        return {}

    index: dict[str, set[str]] = {}
    table_names: set[str] = set()
    for i, table in enumerate(tables):
        if not isinstance(table, dict):
            err(errors, f"model-contract.yaml: tables[{i}] must be an object")
            continue
        name = table.get("name")
        if not isinstance(name, str) or not name.strip():
            err(errors, f"model-contract.yaml: tables[{i}].name is required")
            continue
        if name in table_names:
            err(errors, f"model-contract.yaml: duplicate table name '{name}'")
        table_names.add(name)

        role = table.get("role")
        if not isinstance(role, str) or role not in ALLOWED_TABLE_ROLES:
            err(errors, f"model-contract.yaml: table '{name}' must declare role in {sorted(ALLOWED_TABLE_ROLES)}")
        grain = table.get("grain")
        if not isinstance(grain, str) or not grain.strip():
            err(errors, f"model-contract.yaml: table '{name}' must declare grain")
        if role in {"fact", "dimension"}:
            if not isinstance(table.get("key"), str) and not isinstance(table.get("relationship_path"), list):
                err(errors, f"model-contract.yaml: table '{name}' must declare key or relationship_path")
        if role == "fact" and table.get("date_role") is None:
            # Not every fact needs time intelligence, but shared quick-win models should make the date role explicit.
            err(errors, f"model-contract.yaml: fact table '{name}' should declare date_role or set date_role: none")

        columns = table.get("columns")
        if not isinstance(columns, list) or not columns:
            err(errors, f"model-contract.yaml: table '{name}' must have non-empty columns")
            index[name] = set()
            continue
        col_names: set[str] = set()
        for j, col in enumerate(columns):
            if not isinstance(col, dict):
                err(errors, f"model-contract.yaml: table '{name}' columns[{j}] must be an object")
                continue
            col_name = col.get("name")
            if not isinstance(col_name, str) or not col_name.strip():
                err(errors, f"model-contract.yaml: table '{name}' columns[{j}].name is required")
                continue
            if col_name in col_names:
                err(errors, f"model-contract.yaml: duplicate column '{name}[{col_name}]'")
            col_names.add(col_name)
        index[name] = col_names
    return index


def require_metric_field(metric: dict[str, Any], field: str, errors: list[str], metric_id: str) -> None:
    val = metric.get(field)
    if not isinstance(val, str) or not val.strip():
        err(errors, f"metric-catalog.yaml: metric '{metric_id}' requires '{field}'")


def check_ref(table: str | None, column: str | None, model_index: dict[str, set[str]], errors: list[str], context: str) -> None:
    if not table or table not in model_index:
        err(errors, f"{context}: table '{table}' is not declared in model-contract.yaml")
        return
    if column and column not in model_index[table]:
        err(errors, f"{context}: column '{table}[{column}]' is not declared in model-contract.yaml")


def validate_metrics(metrics_doc: dict[str, Any], model_index: dict[str, set[str]], errors: list[str]) -> set[str]:
    metrics = metrics_doc.get("metrics")
    if not isinstance(metrics, list) or not metrics:
        err(errors, "metric-catalog.yaml: 'metrics' must be a non-empty list")
        return set()

    ids: set[str] = set()
    object_names: set[str] = set()
    public_objects: set[str] = set()

    for i, metric in enumerate(metrics):
        if not isinstance(metric, dict):
            err(errors, f"metric-catalog.yaml: metrics[{i}] must be an object")
            continue
        metric_id = str(metric.get("id", f"<index {i}>"))
        for field in ["id", "object_name", "display_name", "pattern", "format", "display_folder", "description"]:
            require_metric_field(metric, field, errors, metric_id)

        if isinstance(metric.get("id"), str):
            if metric["id"] in ids:
                err(errors, f"metric-catalog.yaml: duplicate metric id '{metric['id']}'")
            ids.add(metric["id"])

        obj = metric.get("object_name")
        if isinstance(obj, str):
            if obj in object_names:
                err(errors, f"metric-catalog.yaml: duplicate object_name '{obj}'")
            object_names.add(obj)
            public_objects.add(f"[{obj}]")

        if metric.get("self_service") is True or metric.get("reuse_scope") == "shared_model":
            agg = metric.get("aggregation_semantics")
            if agg not in ALLOWED_AGGREGATION_SEMANTICS:
                err(errors, f"metric-catalog.yaml: metric '{metric_id}' requires aggregation_semantics in {sorted(ALLOWED_AGGREGATION_SEMANTICS)}")
            tb = metric.get("time_behavior")
            if tb not in ALLOWED_TIME_BEHAVIORS:
                err(errors, f"metric-catalog.yaml: metric '{metric_id}' requires time_behavior in {sorted(ALLOWED_TIME_BEHAVIORS)}")

        pattern = metric.get("pattern")
        if isinstance(pattern, str) and pattern not in SUPPORTED_PATTERNS:
            err(errors, f"metric-catalog.yaml: metric '{metric_id}' has unsupported pattern '{pattern}'")

        context = f"metric-catalog.yaml: metric '{metric_id}'"
        if pattern == "sum":
            check_ref(metric.get("table"), metric.get("column"), model_index, errors, context)
        elif pattern == "distinct_count":
            check_ref(metric.get("table"), metric.get("column"), model_index, errors, context)
        elif pattern == "count_rows":
            table = metric.get("table")
            if table not in model_index:
                err(errors, f"{context}: table '{table}' is not declared in model-contract.yaml")
        elif pattern == "weighted_average":
            table = metric.get("fact_table")
            check_ref(table, metric.get("value_column"), model_index, errors, context)
            check_ref(table, metric.get("weight_column"), model_index, errors, context)
        elif pattern == "delta":
            for field in ["left_measure", "right_measure"]:
                require_metric_field(metric, field, errors, metric_id)
        elif pattern == "ratio":
            for field in ["numerator_measure", "denominator_measure"]:
                require_metric_field(metric, field, errors, metric_id)
        elif pattern == "custom":
            require_metric_field(metric, "expression", errors, metric_id)

    return public_objects


def normalize_measure_ref(name: str) -> str:
    return name if name.startswith("[") and name.endswith("]") else f"[{name}]"


def validate_display(display_doc: dict[str, Any], public_metric_objects: set[str], errors: list[str]) -> dict[str, dict[str, Any]]:
    objects = display_doc.get("objects")
    if not isinstance(objects, list) or not objects:
        err(errors, "display-catalog.yaml: 'objects' must be a non-empty list")
        return {}

    display_index: dict[str, dict[str, Any]] = {}
    for i, obj in enumerate(objects):
        if not isinstance(obj, dict):
            err(errors, f"display-catalog.yaml: objects[{i}] must be an object")
            continue
        name = obj.get("object")
        if not isinstance(name, str) or not name.strip():
            err(errors, f"display-catalog.yaml: objects[{i}].object is required")
            continue
        if name in display_index:
            err(errors, f"display-catalog.yaml: duplicate object '{name}'")
        display_index[name] = obj

        visible = obj.get("visible", True)
        if visible is True:
            for field in ["display_name", "description"]:
                if not isinstance(obj.get(field), str) or not obj[field].strip():
                    err(errors, f"display-catalog.yaml: visible object '{name}' requires '{field}'")
            if name.startswith("[") and not isinstance(obj.get("folder"), str):
                err(errors, f"display-catalog.yaml: visible measure '{name}' requires 'folder'")
        elif visible is False:
            if not isinstance(obj.get("reason"), str) or not obj["reason"].strip():
                err(errors, f"display-catalog.yaml: hidden object '{name}' should include 'reason'")

    for metric_obj in sorted(public_metric_objects):
        if metric_obj not in display_index:
            err(errors, f"display-catalog.yaml: public metric '{metric_obj}' is missing")
    return display_index


def validate_selectors(selector_doc: dict[str, Any], public_metric_objects: set[str], display_index: dict[str, dict[str, Any]], errors: list[str]) -> None:
    selectors = selector_doc.get("selectors")
    if selectors is None:
        return
    if not isinstance(selectors, list):
        err(errors, "selector-catalog.yaml: 'selectors' must be a list")
        return
    selector_ids: set[str] = set()
    for i, selector in enumerate(selectors):
        if not isinstance(selector, dict):
            err(errors, f"selector-catalog.yaml: selectors[{i}] must be an object")
            continue
        sid = str(selector.get("id", f"<index {i}>"))
        if sid in selector_ids:
            err(errors, f"selector-catalog.yaml: duplicate selector id '{sid}'")
        selector_ids.add(sid)
        impl = selector.get("implementation")
        if impl is not None and impl not in ALLOWED_SELECTOR_IMPLEMENTATIONS:
            err(errors, f"selector-catalog.yaml: selector '{sid}' implementation must be one of {sorted(ALLOWED_SELECTOR_IMPLEMENTATIONS)}")
        options = selector.get("options")
        if not isinstance(options, list) or not options:
            err(errors, f"selector-catalog.yaml: selector '{sid}' must have non-empty options")
            continue
        seen_defaults = 0
        option_keys: set[str] = set()
        for j, opt in enumerate(options):
            if not isinstance(opt, dict):
                err(errors, f"selector-catalog.yaml: selector '{sid}' options[{j}] must be an object")
                continue
            key = str(opt.get("key", j))
            if key in option_keys:
                err(errors, f"selector-catalog.yaml: selector '{sid}' duplicate option key '{key}'")
            option_keys.add(key)
            if opt.get("default") is True:
                seen_defaults += 1
            if "measure" in opt:
                mref = normalize_measure_ref(str(opt["measure"]))
                if mref not in public_metric_objects:
                    err(errors, f"selector-catalog.yaml: selector '{sid}' option '{key}' references unknown public measure {mref}")
            if "field" in opt:
                field = str(opt["field"])
                if field not in display_index:
                    err(errors, f"selector-catalog.yaml: selector '{sid}' option '{key}' references field not in display-catalog.yaml: {field}")
                elif display_index[field].get("visible") is False:
                    err(errors, f"selector-catalog.yaml: selector '{sid}' option '{key}' references hidden field: {field}")
        if seen_defaults > 1:
            err(errors, f"selector-catalog.yaml: selector '{sid}' has multiple default options")


def validate_source_catalog(source_doc: dict[str, Any], model_index: dict[str, set[str]], errors: list[str]) -> None:
    profiles = source_doc.get("source_profiles")
    profile_ids: set[str] = set()
    if profiles is not None:
        if not isinstance(profiles, list):
            err(errors, "source-catalog.yaml: 'source_profiles' must be a list")
        else:
            for i, profile in enumerate(profiles):
                if not isinstance(profile, dict):
                    err(errors, f"source-catalog.yaml: source_profiles[{i}] must be an object")
                    continue
                pid = profile.get("id")
                if not isinstance(pid, str) or not pid.strip():
                    err(errors, f"source-catalog.yaml: source_profiles[{i}].id is required")
                    continue
                if pid in profile_ids:
                    err(errors, f"source-catalog.yaml: duplicate source profile id '{pid}'")
                profile_ids.add(pid)
                if str(profile.get("powerbi_mode", "")).lower() == "directquery" and profile.get("status") == "active":
                    err(errors, f"source-catalog.yaml: active profile '{pid}' must not use DirectQuery for v0.1")
                if profile.get("databricks_serverless_required") is True and profile.get("status") == "active":
                    err(errors, f"source-catalog.yaml: active profile '{pid}' must not require Databricks Serverless")
                if str(profile.get("powerbi_mode", "")).lower() == "direct_lake":
                    for req in ["expected_shape", "preserve_semantic_names", "fallback_or_directquery_risk"]:
                        if req not in profile:
                            err(errors, f"source-catalog.yaml: Direct Lake profile '{pid}' should declare {req}")

    bindings = source_doc.get("bindings")
    if bindings is None:
        return
    if not isinstance(bindings, list):
        err(errors, "source-catalog.yaml: 'bindings' must be a list")
        return
    for i, binding in enumerate(bindings):
        if not isinstance(binding, dict):
            err(errors, f"source-catalog.yaml: bindings[{i}] must be an object")
            continue
        semantic_table = binding.get("semantic_table")
        if semantic_table not in model_index:
            err(errors, f"source-catalog.yaml: binding semantic_table '{semantic_table}' is not declared in model-contract.yaml")
        active_profile = binding.get("active_profile")
        if active_profile and profile_ids and active_profile not in profile_ids:
            err(errors, f"source-catalog.yaml: binding for '{semantic_table}' references unknown active_profile '{active_profile}'")
        for j, future in enumerate(binding.get("future_bindings", []) or []):
            if not isinstance(future, dict):
                err(errors, f"source-catalog.yaml: binding for '{semantic_table}' future_bindings[{j}] must be an object")
                continue
            profile = future.get("profile")
            if profile_ids and profile not in profile_ids:
                err(errors, f"source-catalog.yaml: binding for '{semantic_table}' references unknown future profile '{profile}'")


def validate_semantic_request(request_doc: dict[str, Any], model_index: dict[str, set[str]], public_metric_objects: set[str], display_index: dict[str, dict[str, Any]], errors: list[str]) -> None:
    request = request_doc.get("request")
    if request is None:
        return
    if not isinstance(request, dict):
        err(errors, "semantic-request.yaml: 'request' must be an object")
        return
    for field in ["id", "purpose", "status"]:
        if not isinstance(request.get(field), str) or not request[field].strip():
            err(errors, f"semantic-request.yaml: request.{field} is required")
    lifecycle = request.get("lifecycle", request.get("status"))
    if lifecycle not in ALLOWED_REQUEST_LIFECYCLE:
        err(errors, f"semantic-request.yaml: request.lifecycle/status must be one of {sorted(ALLOWED_REQUEST_LIFECYCLE)}")
    review = request_doc.get("review", {})
    if isinstance(review, dict) and review.get("allowed_to_publish_without_review") is True:
        err(errors, "semantic-request.yaml: review.allowed_to_publish_without_review must not be true")

    for i, metric in enumerate(request_doc.get("metric_requests", []) or []):
        if not isinstance(metric, dict):
            err(errors, f"semantic-request.yaml: metric_requests[{i}] must be an object")
            continue
        rid = metric.get("requested_id", f"<index {i}>")
        pattern = metric.get("desired_pattern")
        if pattern and pattern not in SAFE_REQUEST_PATTERNS:
            err(errors, f"semantic-request.yaml: metric request '{rid}' has unsupported desired_pattern '{pattern}'")
        for measure_field in ["numerator_measure", "denominator_measure", "left_measure", "right_measure"]:
            if measure_field in metric:
                mref = normalize_measure_ref(str(metric[measure_field]))
                if mref not in public_metric_objects:
                    err(errors, f"semantic-request.yaml: metric request '{rid}' references unknown governed measure {mref}")

    for i, field_req in enumerate(request_doc.get("field_requests", []) or []):
        if not isinstance(field_req, dict):
            err(errors, f"semantic-request.yaml: field_requests[{i}] must be an object")
            continue
        source_hint = field_req.get("source_hint")
        if source_hint and str(source_hint) not in display_index:
            # This is a warning-like error because quick-win compilation needs governed fields.
            err(errors, f"semantic-request.yaml: field request source_hint is not governed in display-catalog.yaml: {source_hint}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("specs_dir", type=Path)
    args = parser.parse_args()

    specs_dir = args.specs_dir
    errors: list[str] = []

    for filename in REQUIRED_FILES:
        if not (specs_dir / filename).exists():
            err(errors, f"missing required file: {filename}")

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    model = load_yaml_checked(specs_dir / "model-contract.yaml", errors)
    metrics = load_yaml_checked(specs_dir / "metric-catalog.yaml", errors)
    display = load_yaml_checked(specs_dir / "display-catalog.yaml", errors)

    model_index = build_model_index(model, errors)
    public_metric_objects = validate_metrics(metrics, model_index, errors)
    display_index = validate_display(display, public_metric_objects, errors)

    selector_path = specs_dir / "selector-catalog.yaml"
    if selector_path.exists():
        selectors = load_yaml_checked(selector_path, errors)
        validate_selectors(selectors, public_metric_objects, display_index, errors)

    source_path = specs_dir / "source-catalog.yaml"
    if source_path.exists():
        source_doc = load_yaml_checked(source_path, errors)
        validate_source_catalog(source_doc, model_index, errors)

    request_path = specs_dir / "semantic-request.yaml"
    if request_path.exists():
        request_doc = load_yaml_checked(request_path, errors)
        validate_semantic_request(request_doc, model_index, public_metric_objects, display_index, errors)

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    print("OK: semantic specs are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
