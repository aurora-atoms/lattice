import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "scripts"))

from generate_capability_registry_projections import build_projections

manifest_path = root / "registry" / "capability-manifest.json"
entries_path = root / "scripts" / "_pr46_manifest_entries.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
entries = json.loads(entries_path.read_text(encoding="utf-8"))
existing = {item["capability_id"] for item in manifest["capabilities"]}
for entry in entries:
    if entry["capability_id"] not in existing:
        manifest["capabilities"].append(entry)
manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
for relative, content in build_projections(root, manifest).items():
    (root / relative).write_text(content, encoding="utf-8")
