#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from china_travel_kit import __version__  # noqa: E402


def tracked_and_new_files() -> list[Path]:
    output = subprocess.check_output(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
    )
    paths = [Path(value.decode("utf-8")) for value in output.split(b"\0") if value]
    generated = {"integrity-manifest.json", "integrity-manifest.json.sig"}
    return sorted(path for path in paths if path.as_posix() not in generated and (ROOT / path).is_file())


def main() -> int:
    files = {}
    for relative_path in tracked_and_new_files():
        content = (ROOT / relative_path).read_bytes()
        files[relative_path.as_posix()] = {
            "sha256": hashlib.sha256(content).hexdigest(),
            "size": len(content),
        }

    manifest = {
        "schema_version": 1,
        "name": "huaxingzhi",
        "version": __version__,
        "release_tag": f"v{__version__}",
        "official_repository": "https://github.com/tczyliu/china-travel-kit",
        "generated_on": date.today().isoformat(),
        "algorithm": "sha256",
        "signature": {
            "algorithm": "ssh-ed25519",
            "namespace": "huaxingzhi-release",
            "public_key": "release/huaxingzhi-release-key.pub",
            "public_key_fingerprint": "SHA256:BxRBwLOMjmWiZEXGr443RJqRAyOXL4bUJ/KzsK2o7bA",
            "signature_file": "integrity-manifest.json.sig",
        },
        "files": files,
    }
    target = ROOT / "integrity-manifest.json"
    target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {target} with {len(files)} protected files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
