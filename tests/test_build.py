"""Tests for the Author Book-Day Printables Pack.

Verifies the build script runs and every expected PDF is produced and is a
well-formed, US-Letter PDF with at least one page. The build runs in a temp
copy of the repo so the checked-in printables/ stay untouched.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]

SHEET_SLUGS = [
    "countdown-calendar",
    "launch-day-checklist",
    "bookmarks",
    "thank-you-cards",
    "series-bible-one-pager",
    "signing-sales-log",
    "review-request-postcards",
]
SHEET_PDFS = [f"{slug}.pdf" for slug in SHEET_SLUGS]
USAGE_PDFS = [f"usage-{slug}.pdf" for slug in SHEET_SLUGS]
ALL_PDFS = SHEET_PDFS + USAGE_PDFS
EXPECTED_USAGE_IN = "usage"

BANNED_BRAND_TOKENS = [
    "asdale",
    "dylan asdale",
    "the massive ai manual",
    "dylanasdale",
]


@pytest.fixture(scope="session")
def built(tmp_path_factory):
    """Run build.py in a temp copy of the repo; return the repo path."""
    work = tmp_path_factory.mktemp("build")
    repo = work / "repo"
    shutil.copytree(ROOT, repo, ignore=shutil.ignore_patterns("printables", ".git", "__pycache__"))
    proc = subprocess.run(
        [sys.executable, str(repo / "build.py")],
        capture_output=True, text=True, cwd=repo, timeout=600,
    )
    assert proc.returncode == 0, f"build.py failed:\n{proc.stdout}\n{proc.stderr}"
    return repo


def test_all_sheet_sources_exist():
    for slug in SHEET_SLUGS:
        path = ROOT / "sources" / f"{slug}.html"
        assert path.exists(), f"missing sheet source: {path}"


def test_build_lists_every_sheet(built):
    out = built / "printables"
    for name in SHEET_PDFS:
        assert (out / name).exists(), f"build did not produce {name}"
    usage_dir = out / EXPECTED_USAGE_IN
    usage_dir.mkdir(exist_ok=True)
    usage_dir.mkdir(exist_ok=True)
    for name in USAGE_PDFS:
        assert (usage_dir / name).exists(), f"build did not produce {name}"
    top = {p.name for p in out.iterdir()}
    assert top == set(SHEET_PDFS) | {EXPECTED_USAGE_IN}, f"unexpected files in printables/: {top}"


@pytest.mark.parametrize("name", ALL_PDFS)
def test_pdf_is_valid_letter_and_rows(built, name):
    directory = built / "printables" if not name.startswith("usage-") else built / "printables" / EXPECTED_USAGE_IN
    path = directory / name
    assert path.exists(), f"{name} not built"
    reader = PdfReader(str(path))
    assert len(reader.pages) >= 1, f"{name} has no pages"
    box = reader.pages[0].mediabox
    assert float(box.width) == pytest.approx(612, abs=2), f"{name}: width {box.width}"
    assert float(box.height) == pytest.approx(792, abs=2), f"{name}: height {box.height}"
    text = (reader.pages[0].extract_text() or "").lower()
    assert text.strip(), f"{name}: first page has no text layer"



def test_pdf_size_sane(built):
    for name in ALL_PDFS:
        directory = built / "printables" if not name.startswith("usage-") else built / "printables" / EXPECTED_USAGE_IN
        size = (directory / name).stat().st_size
        assert 1_000 < size < 2_000_000, f"{name} suspicious size: {size} bytes"


def test_sources_contain_no_secrets():
    """No obvious secrets, keys, or email addresses in source files."""
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix in {".py", ".html", ".css", ".md", ".json"}:
            if p.name == "test_build.py" or "__pycache__" in p.parts or ".git" in p.parts:
                continue
            text = p.read_text(encoding="utf-8", errors="ignore").lower()
            for bad in ("api_key", "apikey", "password"):
                assert bad not in text, f"suspicious token '{bad}' in {p}"
            assert not re.search(
                r"[\w.+-]+@(?:[\w-]+\.)+[a-z]{2,}", text.lower()
            ), f"possible email in {p}"


def test_sheets_are_unbranded():
    """Printable sheets must not mention the company or author by name."""
    for p in (ROOT / "sources").glob("*.html"):
        text = p.read_text(encoding="utf-8").lower()
        for b in BANNED_BRAND_TOKENS:
            assert b not in text, f"brand token '{b}' found in {p}"


def test_shared_css_used_by_every_sheet():
    for slug in SHEET_SLUGS:
        text = (ROOT / "sources" / f"{slug}.html").read_text(encoding="utf-8")
        assert 'href="css/sheet.css"' in text, f"{slug}.html does not link shared CSS"
