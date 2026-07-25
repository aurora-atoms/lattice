#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
ID_RE = re.compile(r"^(skill|agent):([a-z0-9][a-z0-9-]*)@(.+)$")
REQUIRED_FIELDS = {"id","kind","name","version","path","status","compatibility","changes","primary_user","secondary_audience","triggers","required_inputs","optional_context","outputs"}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records=[]
    for line_no,line in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not line.strip():
            continue
        try:
            value=json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_no}: invalid JSON: {exc.msg}") from exc
        if not isinstance(value,dict):
            raise ValueError(f"{path}:{line_no}: record must be an object")
        value["_line"]=line_no
        records.append(value)
    return records


def nonempty_list(value: Any) -> bool:
    return isinstance(value,list) and bool(value) and all(isinstance(x,str) and x.strip() for x in value)


def validate_record(record: dict[str, Any], source: Path, root: Path) -> list[str]:
    errors=[]
    line=record.get("_line","?")
    public={k:v for k,v in record.items() if k!="_line"}
    missing=sorted(REQUIRED_FIELDS-set(public))
    if missing:
        return [f"{source}:{line}: missing fields: {', '.join(missing)}"]
    kind,name,version=record.get("kind"),record.get("name"),record.get("version")
    if kind not in {"skill","agent"}:
        errors.append(f"{source}:{line}: kind must be skill or agent")
    if not isinstance(name,str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*",name):
        errors.append(f"{source}:{line}: invalid name")
    if not isinstance(version,str) or not SEMVER_RE.fullmatch(version):
        errors.append(f"{source}:{line}: version must be semantic version")
    match=ID_RE.fullmatch(str(record.get("id")))
    if not match or match.group(1)!=kind or match.group(2)!=name or match.group(3)!=version:
        errors.append(f"{source}:{line}: id must equal {kind}:{name}@{version}")
    if not (root/str(record.get("path",""))).exists():
        errors.append(f"{source}:{line}: path does not exist: {record.get('path')}")
    compatibility=record.get("compatibility")
    if not isinstance(compatibility,dict):
        errors.append(f"{source}:{line}: compatibility must be an object")
    else:
        if compatibility.get("contract")!="lat.capability-context.v1":
            errors.append(f"{source}:{line}: compatibility.contract must be lat.capability-context.v1")
        if not SEMVER_RE.fullmatch(str(compatibility.get("contract_version",""))):
            errors.append(f"{source}:{line}: compatibility.contract_version must be semantic version")
        if compatibility.get("breaking_change_policy")!="semantic_versioning":
            errors.append(f"{source}:{line}: breaking_change_policy must be semantic_versioning")
        if not nonempty_list(compatibility.get("runtime_targets")):
            errors.append(f"{source}:{line}: runtime_targets must be non-empty")
    for key in ("changes","primary_user"):
        if not isinstance(record.get(key),str) or not record[key].strip():
            errors.append(f"{source}:{line}: {key} must be non-empty")
    if not nonempty_list(record.get("secondary_audience")):
        errors.append(f"{source}:{line}: secondary_audience must be non-empty")
    triggers=record.get("triggers")
    if not isinstance(triggers,dict):
        errors.append(f"{source}:{line}: triggers must be an object")
    else:
        discovery=[]
        for key in ("events","states","requests"):
            value=triggers.get(key,[])
            if not isinstance(value,list) or not all(isinstance(x,str) for x in value):
                errors.append(f"{source}:{line}: triggers.{key} must be a string list")
            else:
                discovery.extend(x for x in value if x.strip())
        if not discovery:
            errors.append(f"{source}:{line}: at least one event, state, or request trigger is required")
        if not isinstance(triggers.get("exclusions",[]),list):
            errors.append(f"{source}:{line}: triggers.exclusions must be a string list")
    required_inputs=record.get("required_inputs")
    if not isinstance(required_inputs,dict):
        errors.append(f"{source}:{line}: required_inputs must be an object")
    else:
        if not nonempty_list(required_inputs.get("minimum")):
            errors.append(f"{source}:{line}: required_inputs.minimum must be non-empty")
        for key in ("permissions","tools"):
            value=required_inputs.get(key,[])
            if not isinstance(value,list) or not all(isinstance(x,str) for x in value):
                errors.append(f"{source}:{line}: required_inputs.{key} must be a string list")
    optional_context=record.get("optional_context")
    if not isinstance(optional_context,dict):
        errors.append(f"{source}:{line}: optional_context must be an object")
    else:
        for key in ("when","discover","suggested_capabilities","external_sources"):
            value=optional_context.get(key,[])
            if not isinstance(value,list) or not all(isinstance(x,str) for x in value):
                errors.append(f"{source}:{line}: optional_context.{key} must be a string list")
        if not optional_context.get("discover"):
            errors.append(f"{source}:{line}: optional_context.discover must guide progressive discovery")
    if not nonempty_list(record.get("outputs")):
        errors.append(f"{source}:{line}: outputs must be non-empty")
    return errors


def skill_dirs(root: Path) -> set[str]:
    return {str(path.parent.relative_to(root)) for path in (root/"skills").rglob("SKILL.md")}


def agent_registry_paths(root: Path) -> set[str]:
    path=root/"registry/agents.index.jsonl"
    return {str(r.get("instruction_path")) for r in read_jsonl(path) if r.get("instruction_path")} if path.exists() else set()


def validate_registry(path: Path, root: Path, expected_kind: str):
    errors=[]
    records=read_jsonl(path)
    ids=set(); names=set()
    for record in records:
        errors.extend(validate_record(record,path,root))
        if record.get("kind")!=expected_kind:
            errors.append(f"{path}:{record.get('_line')}: expected kind {expected_kind}")
        if record.get("id") in ids:
            errors.append(f"{path}:{record.get('_line')}: duplicate id {record.get('id')}")
        ids.add(record.get("id"))
        if record.get("name") in names:
            errors.append(f"{path}:{record.get('_line')}: duplicate name {record.get('name')}")
        names.add(record.get("name"))
    return errors,records


def main() -> int:
    parser=argparse.ArgumentParser(description="Validate unified Skill and Agent context contracts.")
    parser.add_argument("--root",default=".")
    args=parser.parse_args()
    root=Path(args.root).resolve()
    errors=[]
    try:
        skill_errors,skills=validate_registry(root/"registry/skill-context.index.jsonl",root,"skill")
        agent_errors,agents=validate_registry(root/"registry/agent-context.index.jsonl",root,"agent")
        errors.extend(skill_errors+agent_errors)
        registered_skill_paths={str(r.get("path")) for r in skills}
        actual_skills=skill_dirs(root)
        if actual_skills-registered_skill_paths:
            errors.append("unregistered Skill packages: "+", ".join(sorted(actual_skills-registered_skill_paths)))
        if registered_skill_paths-actual_skills:
            errors.append("context records without Skill packages: "+", ".join(sorted(registered_skill_paths-actual_skills)))
        registered_agent_paths={str(r.get("path")) for r in agents}
        expected_agents=agent_registry_paths(root)
        if expected_agents-registered_agent_paths:
            errors.append("unregistered Agent instructions: "+", ".join(sorted(expected_agents-registered_agent_paths)))
        if registered_agent_paths-expected_agents:
            errors.append("context records without Agent registry entries: "+", ".join(sorted(registered_agent_paths-expected_agents)))
    except (OSError,ValueError) as exc:
        errors.append(str(exc))
    if errors:
        for error in errors:
            print(f"error: {error}",file=sys.stderr)
        return 1
    print(f"validated {len(skills)} Skill and {len(agents)} Agent context record(s)")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
