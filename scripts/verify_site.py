#!/usr/bin/env python3
"""Deterministic structural checks for the static site."""

from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
DEPLOY_FILES = {
    ".nojekyll",
    "404.html",
    "favicon.svg",
    "index.html",
    "preview.png",
    "preview.svg",
    "robots.txt",
    "sitemap.xml",
}
REQUIRED_REPOSITORIES = {
    "https://github.com/lmdixon23/sonc-2026-nonseparability-exactness",
    "https://github.com/lmdixon23/njc-separation",
    "https://github.com/lmdixon23/cbg-2026-representation-checks",
    "https://github.com/lmdixon23/ai-playgrounds",
}
REQUIRED_PUBLIC_LINKS = {
    "https://github.com/lmdixon23/lmdixon23.github.io",
    "https://github.com/lmdixon23/lmdixon23.github.io/blob/main/LICENSE",
    "https://orcid.org/0009-0001-0592-462X",
    "https://github.com/lmdixon23",
    "https://www.linkedin.com/in/logan-dixon-b1bb43329/",
    "mailto:lmdixon23@gmail.com",
}
PROHIBITED = (
    r"[A-Za-z]:\\",
    r"/home/[^/]+/",
    r"/Users/[^/]+/",
    r"ghp_[A-Za-z0-9]+",
    r"github_pat_[A-Za-z0-9_]+",
    r"BEGIN (?:RSA|OPENSSH|EC) PRIVATE KEY",
    r"Claude said",
    r"GPT said",
    r"cold[- ]pass",
)


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.hrefs: list[str] = []
        self.sources: list[str] = []
        self.h1_count = 0
        self.images_without_alt: list[int] = []
        self.buttons_without_type: list[int] = []
        self.json_ld: list[str] = []
        self._json_buffer: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if "id" in values and values["id"] is not None:
            self.ids.append(values["id"])
        if tag == "a" and values.get("href"):
            self.hrefs.append(values["href"] or "")
        if tag in {"img", "script", "source"} and values.get("src"):
            self.sources.append(values["src"] or "")
        if tag == "link" and values.get("href"):
            self.sources.append(values["href"] or "")
        if tag == "h1":
            self.h1_count += 1
        if tag == "img" and "alt" not in values:
            self.images_without_alt.append(self.getpos()[0])
        if tag == "button" and "type" not in values:
            self.buttons_without_type.append(self.getpos()[0])
        if tag == "script" and values.get("type") == "application/ld+json":
            self._json_buffer = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._json_buffer is not None:
            self.json_ld.append("".join(self._json_buffer))
            self._json_buffer = None

    def handle_data(self, data: str) -> None:
        if self._json_buffer is not None:
            self._json_buffer.append(data)


def fail(message: str) -> "NoReturn":
    raise SystemExit(f"VERDICT: SITE VERIFICATION FAILED: {message}")


def local_path(value: str) -> Path | None:
    parsed = urlparse(value)
    if parsed.scheme or value.startswith("//") or value.startswith("#") or value.startswith("mailto:"):
        return None
    clean = parsed.path.lstrip("/")
    return ROOT / clean


def main() -> None:
    for relative in DEPLOY_FILES:
        if not (ROOT / relative).is_file():
            fail(f"missing deploy file: {relative}")

    text = INDEX.read_text(encoding="utf-8")
    if not text.lstrip().lower().startswith("<!doctype html>"):
        fail("index.html has no HTML5 doctype")
    if '<html lang="en">' not in text:
        fail("index.html has no English language declaration")
    if '<meta name="viewport"' not in text:
        fail("viewport metadata is missing")
    if '<link rel="canonical" href="https://lmdixon23.github.io/">' not in text:
        fail("canonical URL is missing or incorrect")
    if "application/ld+json" not in text:
        fail("structured data is missing")
    if "prefers-reduced-motion" not in text:
        fail("reduced-motion support is missing")
    if "skip-link" not in text:
        fail("skip link is missing")

    for pattern in PROHIBITED:
        if re.search(pattern, text, flags=re.IGNORECASE):
            fail(f"prohibited public content matches: {pattern}")

    parser = SiteParser()
    parser.feed(text)

    if parser.h1_count != 1:
        fail(f"expected one h1, found {parser.h1_count}")
    if len(parser.ids) != len(set(parser.ids)):
        fail("duplicate id attribute")
    if parser.images_without_alt:
        fail(f"images without alt text on lines: {parser.images_without_alt}")
    if parser.buttons_without_type:
        fail(f"buttons without type on lines: {parser.buttons_without_type}")

    ids = set(parser.ids)
    for href in parser.hrefs:
        if href.startswith("#") and href[1:] not in ids:
            fail(f"broken internal anchor: {href}")
        if href.startswith("http://"):
            fail(f"insecure external link: {href}")
        path = local_path(href)
        if path is not None and not path.is_file():
            fail(f"missing local link target: {href}")

    for source in parser.sources:
        path = local_path(source)
        if path is not None and not path.is_file():
            fail(f"missing local asset: {source}")

    for repository in REQUIRED_REPOSITORIES:
        if repository not in text:
            fail(f"required repository link is missing: {repository}")

    for public_link in REQUIRED_PUBLIC_LINKS:
        if public_link not in parser.hrefs:
            fail(f"required public identity link is missing: {public_link}")

    if "Static HTML · no advertising or behavioral tracking" not in text:
        fail("footer privacy statement is missing")
    if "↑ Back to top" not in text:
        fail("footer back-to-top link is missing")

    if len(parser.json_ld) != 1:
        fail(f"expected one JSON-LD block, found {len(parser.json_ld)}")
    try:
        structured = json.loads(parser.json_ld[0])
    except json.JSONDecodeError as error:
        fail(f"invalid JSON-LD: {error}")
    if structured.get("@type") != "Person" or structured.get("name") != "Logan Dixon":
        fail("JSON-LD person identity is incorrect")
    if structured.get("url") != "https://lmdixon23.github.io/":
        fail("JSON-LD URL is incorrect")

    workflow = (ROOT / ".github/workflows/deploy-pages.yml").read_text(encoding="utf-8")
    required_workflow_tokens = (
        "actions/checkout@v6",
        "actions/setup-python@v6",
        "actions/configure-pages@v6",
        "actions/upload-pages-artifact@v5",
        "actions/deploy-pages@v4",
        "python scripts/verify_site.py",
        "python scripts/verify_sha256_manifest.py",
    )
    for token in required_workflow_tokens:
        if token not in workflow:
            fail(f"workflow component is missing: {token}")

    print("VERDICT: SITE STRUCTURE VERIFIED")
    print(f"internal ids = {len(ids)}")
    print(f"links = {len(parser.hrefs)}")
    print(f"deploy files = {len(DEPLOY_FILES)}")


if __name__ == "__main__":
    main()
