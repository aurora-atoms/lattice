from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "examples" / "esp32-demo-source-free-rebuild" / "assets"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_public_asset_manifest_preserves_public_private_boundary() -> None:
    manifest = _load(ASSETS / "asset-manifest.v1.json")
    boundary = manifest["boundary"]

    assert boundary["original_private_source_included"] is False
    assert boundary["private_runtime_evidence_included"] is False
    assert boundary["real_product_behavior_included"] is False
    assert boundary["customer_or_employer_material_included"] is False
    assert boundary["simulation_status"] == "synthetic_reference"
    assert boundary["downstream_adoption_status"] == "not_observed"

    assets = manifest["assets"]
    assert assets
    for asset in assets:
        assert asset["origin"].startswith("independently_authored")
        assert asset["third_party_data"] is False
        assert asset["publication_decision"] == "allow"
        assert (ASSETS.parent / asset["path"]).exists()


def test_geo_asset_is_explicitly_synthetic_and_not_navigation_grade() -> None:
    route = _load(ASSETS / "geo" / "doubtful-sound-patea.synthetic-route.v1.json")

    assert route["simulation_status"] == "synthetic_reference"
    assert route["downstream_adoption_status"] == "not_observed"
    assert route["scene"]["simulation_only"] is True
    assert route["provenance"]["origin"] == "independently_authored_for_public_reference"
    assert route["provenance"]["third_party_data"] is False
    assert route["provenance"]["navigation_grade"] is False

    points = route["route"]["points"]
    assert len(points) == 11
    assert [point["seq"] for point in points] == list(range(11))


def test_formation_asset_is_generic_and_source_independent() -> None:
    formations = _load(ASSETS / "formations" / "generic-formations.v1.json")

    assert formations["simulation_status"] == "synthetic_reference"
    assert formations["downstream_adoption_status"] == "not_observed"
    provenance = formations["provenance"]
    assert provenance["origin"] == "independently_authored_from_generic_geometry"
    assert provenance["third_party_data"] is False
    assert provenance["private_implementation_source_used"] is False

    assert set(formations["formations"]) == {
        "circle",
        "triangle",
        "right-square-pyramid",
    }
    pyramid = formations["formations"]["right-square-pyramid"]
    assert pyramid["minimum_points"] == 5
    assert pyramid["invariants"] == {
        "square_coplanar_base": True,
        "adjacent_base_edges_perpendicular": True,
        "apex_above_base_center": True,
        "nonzero_height": True,
    }
