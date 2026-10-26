"""check_links must report broken links and nothing else."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import check_links  # noqa: E402


def problems_for(tmp_path: Path, text: str) -> list[str]:
    (tmp_path / "exists.md").write_text("x", encoding="utf-8")
    doc = tmp_path / "doc.md"
    doc.write_text(text, encoding="utf-8")
    return check_links.check_document(doc)


def test_link_title_is_not_part_of_the_path(tmp_path):
    assert problems_for(tmp_path, '[a](exists.md "A title")\n') == []


def test_non_http_schemes_are_not_treated_as_relative_files(tmp_path):
    assert problems_for(tmp_path, "[a](ftp://example.com/f) [b](data:text/plain,hi)\n") == []


def test_links_in_code_are_examples_not_links(tmp_path):
    text = "```md\n[a](missing.md)\n```\n\nuse `[b](missing.md)` syntax\n"
    assert problems_for(tmp_path, text) == []


def test_one_broken_image_is_reported_once(tmp_path):
    assert len(problems_for(tmp_path, "![a](missing.png)\n")) == 1
