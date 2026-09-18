from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "examples" / "esp32-demo-source-free-rebuild" / "assets"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class Esp32DemoPublicAssetsTests(unittest.TestCase):
    def test_public_asset_manifest_preserves_public_private_boundary(self) -> None:
        manifest = _load(ASSETS / "asset-manifest.v1.json")
        boundary = manifest["boundary"]

        self.assertIs(boundary["original_private_source_included"], False)
        self.assertIs(boundary["private_runtime_evidence_included"], False)
        self.assertIs(boundary["real_product_behavior_included"], False)
        self.assertIs(boundary["customer_or_employer_material_included"], False)
        self.assertEqual(boundary["simulation_status"], "synthetic_reference")
        self.assertEqual(boundary["downstream_adoption_status"], "not_observed")

        assets = manifest["assets"]
        self.assertTrue(assets)
        for asset in assets:
            self.assertTrue(asset["origin"].startswith("independently_authored"))
            self.assertIs(asset["third_party_data"], False)
            self.assertEqual(asset["publication_decision"], "allow")
            self.assertTrue((ASSETS.parent / asset["path"]).exists())

    def test_geo_asset_is_explicitly_synthetic_and_not_navigation_grade(self) -> None:
        route = _load(ASSETS / "geo" / "doubtful-sound-patea.synthetic-route.v1.json")

        self.assertEqual(route["simulation_status"], "synthetic_reference")
        self.assertEqual(route["downstream_adoption_status"], "not_observed")
        self.assertIs(route["scene"]["simulation_only"], True)
        self.assertEqual(
            route["provenance"]["origin"],
            "independently_authored_for_public_reference",
        )
        self.assertIs(route["provenance"]["third_party_data"], False)
        self.assertIs(route["provenance"]["navigation_grade"], False)

        points = route["route"]["points"]
        self.assertEqual(len(points), 11)
        self.assertEqual([point["seq"] for point in points], list(range(11)))

    def test_formation_asset_is_generic_and_source_independent(self) -> None:
        formations = _load(ASSETS / "formations" / "generic-formations.v1.json")

        self.assertEqual(formations["simulation_status"], "synthetic_reference")
        self.assertEqual(formations["downstream_adoption_status"], "not_observed")
        provenance = formations["provenance"]
        self.assertEqual(
            provenance["origin"],
            "independently_authored_from_generic_geometry",
        )
        self.assertIs(provenance["third_party_data"], False)
        self.assertIs(provenance["private_implementation_source_used"], False)

        self.assertEqual(
            set(formations["formations"]),
            {"circle", "triangle", "right-square-pyramid"},
        )
        pyramid = formations["formations"]["right-square-pyramid"]
        self.assertEqual(pyramid["minimum_points"], 5)
        self.assertEqual(
            pyramid["invariants"],
            {
                "square_coplanar_base": True,
                "adjacent_base_edges_perpendicular": True,
                "apex_above_base_center": True,
                "nonzero_height": True,
            },
        )


if __name__ == "__main__":
    unittest.main()
