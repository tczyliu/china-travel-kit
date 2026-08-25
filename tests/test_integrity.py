import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from china_travel_kit.integrity import verify_integrity, verify_manifest_signature


ROOT = Path(__file__).resolve().parents[1]


class IntegrityTests(unittest.TestCase):
    def test_release_manifest_matches_repository(self) -> None:
        result = verify_integrity(ROOT)
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["version"], "0.5.0")
        self.assertGreaterEqual(result["checked_files"], 40)
        self.assertTrue(result["signature_valid"])

    def test_modified_component_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            component = root / "SKILL.md"
            component.write_text("official", encoding="utf-8")
            manifest = {
                "name": "huaxingzhi",
                "version": "0.5.0",
                "files": {
                    "SKILL.md": {
                        "sha256": hashlib.sha256(component.read_bytes()).hexdigest(),
                        "size": component.stat().st_size,
                    }
                },
            }
            (root / "integrity-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            component.write_text("modified", encoding="utf-8")

            result = verify_integrity(root, require_signature=False)

            self.assertFalse(result["valid"])
            self.assertIn("hash_mismatch: SKILL.md", result["errors"])

    def test_removed_component_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = {
                "name": "huaxingzhi",
                "version": "0.5.0",
                "files": {"references/safety-and-freshness.md": {"sha256": "unused", "size": 1}},
            }
            (root / "integrity-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

            result = verify_integrity(root, require_signature=False)

            self.assertFalse(result["valid"])
            self.assertIn("missing_file: references/safety-and-freshness.md", result["errors"])

    def test_manifest_signature_rejects_a_changed_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "release").mkdir()
            shutil.copy2(ROOT / "integrity-manifest.json", root / "integrity-manifest.json")
            shutil.copy2(ROOT / "integrity-manifest.json.sig", root / "integrity-manifest.json.sig")
            shutil.copy2(ROOT / "release" / "huaxingzhi-release-key.pub", root / "release" / "huaxingzhi-release-key.pub")

            self.assertTrue(verify_manifest_signature(root)["valid"])
            with (root / "integrity-manifest.json").open("ab") as stream:
                stream.write(b"\nchanged")

            result = verify_manifest_signature(root)
            self.assertFalse(result["valid"])
            self.assertIn("signature_verification_failed", result["errors"])


if __name__ == "__main__":
    unittest.main()
