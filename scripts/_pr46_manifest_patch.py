import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / "registry" / "capability-manifest.json"
data = json.loads(path.read_text(encoding="utf-8"))
print(len(data["capabilities"]))
