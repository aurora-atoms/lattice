#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
ENTRY_FIELDS = {"name","changes","primary_user","secondary_audience","trigger","minimum","outputs","runtime_targets"}


def load_json(path: Path) -> dict[str, Any]:
    value=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value,dict):
        raise ValueError(f"{path}: catalog must be an object")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records=[]
    for line_no,line in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not line.strip():
            continue
        value=json.loads(line)
        if not isinstance(value,dict):
            raise ValueError(f"{path}:{line_no}: record must be an object")
        records.append(value)
    return records


def nonempty_strings(value: Any) -> bool:
    return isinstance(value,list) and bool(value) and all(isinstance(item,str) and item.strip() for item in value)


def validate_catalog(path: Path, root: Path, kind: str) -> tuple[list[str],list[dict[str,Any]]]:
    errors=[]
    catalog=load_json(path)
    collection="skills" if kind=="skill" else "agents"
    if catalog.get("contract")!="lat.capability-context.v1":
        errors.append(f"{path}: contract must be lat.capability-context.v1")
    version=str(catalog.get("contract_version",""))
    default_version=str(catalog.get("default_version",""))
    if not SEMVER_RE.fullmatch(version):
        errors.append(f"{path}: contract_version must be semantic version")
    if not SEMVER_RE.fullmatch(default_version):
        errors.append(f"{path}: default_version must be semantic version")
    if catalog.get("breaking_change_policy")!="semantic_versioning":
        errors.append(f"{path}: breaking_change_policy must be semantic_versioning")
    discovery=catalog.get("optional_context_discovery")
    if not isinstance(discovery,str) or not discovery.strip():
        errors.append(f"{path}: optional_context_discovery is required")
    entries=catalog.get(collection)
    if not isinstance(entries,list):
        return errors+[f"{path}: {collection} must be an array"],[]
    names=set()
    for index,entry in enumerate(entries):
        where=f"{path}:{collection}[{index}]"
        if not isinstance(entry,dict):
            errors.append(f"{where}: entry must be an object")
            continue
        required=set(ENTRY_FIELDS)
        if kind=="agent":
            required.add("path")
        missing=sorted(required-set(entry))
        if missing:
            errors.append(f"{where}: missing fields: {', '.join(missing)}")
            continue
        name=entry.get("name")
        if not isinstance(name,str) or not NAME_RE.fullmatch(name):
            errors.append(f"{where}: invalid name")
        if name in names:
            errors.append(f"{where}: duplicate name {name}")
        names.add(name)
        for key in ("changes","primary_user","trigger"):
            if not isinstance(entry.get(key),str) or not entry[key].strip():
                errors.append(f"{where}: {key} must be non-empty")
        for key in ("secondary_audience","minimum","outputs","runtime_targets"):
            if not nonempty_strings(entry.get(key)):
                errors.append(f"{where}: {key} must be a non-empty string list")
        capability_id=f"{kind}:{name}@{default_version}"
        if not re.fullmatch(r"(?:skill|agent):[a-z0-9][a-z0-9-]*@[0-9]+\.[0-9]+\.[0-9]+",capability_id):
            errors.append(f"{where}: derived stable ID is invalid")
        target=root/(f"skills/{name}/SKILL.md" if kind=="skill" else str(entry.get("path","")))
        if not target.exists():
            errors.append(f"{where}: target does not exist: {target.relative_to(root) if target.is_absolute() else target}")
    return errors,entries


def actual_skill_names(root: Path) -> set[str]:
    return {path.parent.name for path in (root/"skills").rglob("SKILL.md")}


def registered_agent_paths(root: Path) -> set[str]:
    path=root/"registry/agents.index.jsonl"
    return {str(record.get("instruction_path")) for record in load_jsonl(path) if record.get("instruction_path")}


def main() -> int:
    parser=argparse.ArgumentParser(description="Validate unified Skill and Agent context catalogs.")
    parser.add_argument("--root",default=".")
    args=parser.parse_args()
    root=Path(args.root).resolve()
    errors=[]
    try:
        skill_errors,skills=validate_catalog(root/"registry/skill-context.catalog.json",root,"skill")
        agent_errors,agents=validate_catalog(root/"registry/agent-context.catalog.json",root,"agent")
        errors.extend(skill_errors+agent_errors)
        skill_names={str(entry.get("name")) for entry in skills}
        actual=actual_skill_names(root)
        if actual-skill_names:
            errors.append("unregistered Skill packages: "+", ".join(sorted(actual-skill_names)))
        if skill_names-actual:
            errors.append("catalog entries without Skill packages: "+", ".join(sorted(skill_names-actual)))
        agent_paths={str(entry.get("path")) for entry in agents}
        expected=registered_agent_paths(root)
        if expected-agent_paths:
            errors.append("unregistered Agent instructions: "+", ".join(sorted(expected-agent_paths)))
        if agent_paths-expected:
            errors.append("catalog entries without Agent registry records: "+", ".join(sorted(agent_paths-expected)))
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        errors.append(str(exc))
    if errors:
        for error in errors:
            print(f"error: {error}",file=sys.stderr)
        return 1
    print(f"validated {len(skills)} Skill and {len(agents)} Agent context contract(s)")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
