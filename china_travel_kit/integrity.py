from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from . import __version__
from .store import ROOT


MANIFEST_NAME = "integrity-manifest.json"
SIGNATURE_NAME = "integrity-manifest.json.sig"
PUBLIC_KEY_PATH = Path("release/huaxingzhi-release-key.pub")
SIGNING_IDENTITY = "huaxingzhi-release"
SIGNING_NAMESPACE = "huaxingzhi-release"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_manifest_signature(root: str | Path | None = None) -> dict[str, Any]:
    base = Path(root).resolve() if root is not None else Path.cwd().resolve()
    if not (base / MANIFEST_NAME).is_file() and root is None:
        base = ROOT.resolve()
    manifest_path = base / MANIFEST_NAME
    signature_path = base / SIGNATURE_NAME
    public_key_path = base / PUBLIC_KEY_PATH
    errors: list[str] = []
    if shutil.which("ssh-keygen") is None:
        errors.append("signature_tool_unavailable: ssh-keygen")
    if not manifest_path.is_file():
        errors.append(f"missing_manifest: {MANIFEST_NAME}")
    if not signature_path.is_file():
        errors.append(f"missing_signature: {SIGNATURE_NAME}")
    if not public_key_path.is_file():
        errors.append(f"missing_public_key: {PUBLIC_KEY_PATH.as_posix()}")
    if errors:
        return {"valid": False, "algorithm": "ssh-ed25519", "errors": errors}

    public_key = public_key_path.read_text(encoding="utf-8").strip()
    with tempfile.TemporaryDirectory() as directory:
        allowed_signers = Path(directory) / "allowed_signers"
        allowed_signers.write_text(
            f'{SIGNING_IDENTITY} namespaces="{SIGNING_NAMESPACE}" {public_key}\n',
            encoding="utf-8",
        )
        result = subprocess.run(
            [
                "ssh-keygen",
                "-Y",
                "verify",
                "-f",
                str(allowed_signers),
                "-I",
                SIGNING_IDENTITY,
                "-n",
                SIGNING_NAMESPACE,
                "-s",
                str(signature_path),
            ],
            input=manifest_path.read_bytes(),
            capture_output=True,
            check=False,
        )
    if result.returncode != 0:
        errors.append("signature_verification_failed")
    return {
        "valid": not errors,
        "algorithm": "ssh-ed25519",
        "identity": SIGNING_IDENTITY,
        "namespace": SIGNING_NAMESPACE,
        "errors": errors,
    }


def verify_integrity(root: str | Path | None = None, *, require_signature: bool = True) -> dict[str, Any]:
    base = Path(root).resolve() if root is not None else Path.cwd().resolve()
    manifest_path = base / MANIFEST_NAME
    if not manifest_path.is_file() and root is None:
        base = ROOT.resolve()
        manifest_path = base / MANIFEST_NAME

    if not manifest_path.is_file():
        return {
            "valid": False,
            "signature_valid": False,
            "version": __version__,
            "checked_files": 0,
            "errors": [f"missing_manifest: {MANIFEST_NAME}"],
        }

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "valid": False,
            "signature_valid": False,
            "version": __version__,
            "checked_files": 0,
            "errors": [f"invalid_manifest: {exc}"],
        }

    errors: list[str] = []
    files = manifest.get("files")
    if not isinstance(files, dict):
        files = {}
        errors.append("invalid_manifest: files must be an object")
    if manifest.get("version") != __version__:
        errors.append(f"version_mismatch: manifest={manifest.get('version')} package={__version__}")

    for relative_path, expected in sorted(files.items()):
        target = (base / relative_path).resolve()
        if not target.is_relative_to(base):
            errors.append(f"unsafe_path: {relative_path}")
            continue
        if not target.is_file():
            errors.append(f"missing_file: {relative_path}")
            continue
        if target.stat().st_size != expected.get("size"):
            errors.append(f"size_mismatch: {relative_path}")
        if _sha256(target) != expected.get("sha256"):
            errors.append(f"hash_mismatch: {relative_path}")

    signature = verify_manifest_signature(base) if require_signature else {"valid": None, "errors": []}
    if require_signature:
        errors.extend(signature["errors"])

    return {
        "valid": not errors,
        "signature_valid": signature["valid"],
        "name": manifest.get("name", "huaxingzhi"),
        "version": manifest.get("version", __version__),
        "official_repository": manifest.get("official_repository"),
        "checked_files": len(files),
        "errors": errors,
        "note": "Hashes detect missing or modified files; the Ed25519 signature authenticates the official manifest. Neither prevents copying.",
    }
