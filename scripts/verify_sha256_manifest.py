#!/usr/bin/env python3
"""Fail-closed SHA-256 verification for canonical public site files."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "SHA256SUMS.txt"
LINE = re.compile(r"^([0-9a-f]{64})  ([A-Za-z0-9._/-]+)$")
UNSAFE = ("..", "\\", ":", "//")
BINARY_SUFFIXES = {".png"}


def fail(message: str) -> "NoReturn":
    raise SystemExit(f"VERDICT: SHA-256 MANIFEST FAILED: {message}")


def canonical_bytes(path: Path) -> bytes:
    data = path.read_bytes()
    if path.suffix.lower() in BINARY_SUFFIXES:
        return data
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def main() -> None:
    if not MANIFEST.is_file():
        fail("SHA256SUMS.txt is missing")

    seen: set[str] = set()
    count = 0

    for number, raw in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), 1):
        if not raw or raw.startswith("#"):
            continue

        match = LINE.fullmatch(raw)
        if match is None:
            fail(f"malformed line {number}")

        expected, relative = match.groups()
        if any(token in relative for token in UNSAFE) or relative.startswith("/"):
            fail(f"unsafe path: {relative}")
        if relative in seen:
            fail(f"duplicate path: {relative}")
        if relative == "SHA256SUMS.txt":
            fail("manifest must not hash itself")

        seen.add(relative)
        path = ROOT / relative
        if not path.is_file():
            fail(f"missing file: {relative}")

        actual = hashlib.sha256(canonical_bytes(path)).hexdigest()
        if actual != expected:
            fail(f"hash mismatch: {relative}")

        count += 1

    if count == 0:
        fail("manifest contains no entries")

    print("VERDICT: SHA-256 MANIFEST VERIFIED")
    print(f"files = {count}")


if __name__ == "__main__":
    main()
