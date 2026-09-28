#!/usr/bin/env python3
"""Synchronize the project prompt source into the xiutu Skill.

The source file is intentionally copied verbatim. The manifest makes it easy to
detect an out-of-date Skill copy without editing either side by hand.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path


DEFAULT_TARGET = Path(__file__).resolve().parents[1] / "references" / "prompt-library.md"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def prompt_count(text: str) -> int:
    return len(re.findall(r"(?m)^#{1,6}\s+\S+", text))


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as handle:
        handle.write(data)
        temporary = Path(handle.name)
    temporary.replace(path)


def manifest_for(source: Path, data: bytes) -> dict[str, object]:
    return {
        "format": 1,
        "source_name": source.name,
        "sha256": digest(data),
        "bytes": len(data),
        "prompt_heading_count": prompt_count(data.decode("utf-8")),
    }


def read_manifest(path: Path) -> dict[str, object] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None
    return value if isinstance(value, dict) else None


def check(source: Path, target: Path, manifest_path: Path) -> int:
    source_data = source.read_bytes()
    try:
        target_data = target.read_bytes()
    except FileNotFoundError:
        print(json.dumps({"ok": False, "reason": "target_missing", "target": str(target)}, ensure_ascii=False))
        return 1

    expected = manifest_for(source, source_data)
    actual = read_manifest(manifest_path)
    ok = target_data == source_data and actual == expected
    result = {
        "ok": ok,
        "source": str(source),
        "target": str(target),
        "manifest": str(manifest_path),
        "expected": expected,
        "actual": actual,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="Project prompt source file")
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET, help="Skill prompt copy")
    parser.add_argument("--manifest", type=Path, help="Manifest path; defaults beside --target")
    parser.add_argument("--check", action="store_true", help="Only verify source, copy, and manifest")
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    target = args.target.expanduser().resolve()
    manifest_path = (args.manifest or target.with_name("prompt-library.manifest.json")).expanduser().resolve()

    if not source.is_file():
        print(f"source file not found: {source}", file=sys.stderr)
        return 2

    if args.check:
        return check(source, target, manifest_path)

    data = source.read_bytes()
    atomic_write(target, data)
    manifest = manifest_for(source, data)
    atomic_write(manifest_path, (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({"ok": True, "target": str(target), "manifest": str(manifest_path), **manifest}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
