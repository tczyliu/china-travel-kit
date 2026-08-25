#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "integrity-manifest.json"
SIGNATURE = ROOT / "integrity-manifest.json.sig"
DEFAULT_KEY = Path.home() / ".config" / "huaxingzhi" / "release-signing-key"


def main() -> int:
    key = Path(os.environ.get("HUAXINGZHI_SIGNING_KEY", DEFAULT_KEY)).expanduser()
    if not MANIFEST.is_file():
        raise SystemExit("Run scripts/update_integrity_manifest.py before signing")
    if not key.is_file():
        raise SystemExit(f"Signing key not found: {key}")
    if SIGNATURE.exists():
        SIGNATURE.unlink()
    subprocess.run(
        ["ssh-keygen", "-Y", "sign", "-f", str(key), "-n", "huaxingzhi-release", str(MANIFEST)],
        cwd=ROOT,
        check=True,
    )
    print(f"Signed {MANIFEST.name} -> {SIGNATURE.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
