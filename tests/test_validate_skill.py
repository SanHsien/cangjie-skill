"""validate_skill must judge what a SKILL.md says, not how it happens to be spelled."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import validate_skill  # noqa: E402


def audit_text(tmp_path: Path, text: str, lens: str = "claude", encoding: str = "utf-8"):
    path = tmp_path / "SKILL.md"
    path.write_bytes(text.encode(encoding))
    return validate_skill.audit(str(path), lens=lens)


def test_comma_separated_allowed_tools_are_recognised(tmp_path):
    """`allowed-tools: Bash, Read` is the documented spelling; it must not read as
    a missing Bash grant ("Bash," is not a tool name)."""
    text = (
        "---\nname: demo\ndescription: d\nallowed-tools: Bash, Read\n---\n"
        "```bash\necho hi\n```\n"
    )
    errors, warns = audit_text(tmp_path, text)
    assert errors == []
    assert warns == []


def test_scoped_bash_grant_on_one_line_is_not_split_on_its_space(tmp_path):
    text = (
        "---\nname: demo\ndescription: d\nallowed-tools: Bash(python3 *) Read\n---\n"
        "run python3 x.py\n"
    )
    errors, warns = audit_text(tmp_path, text)
    assert errors == []
    assert warns == []


def test_folded_description_is_measured_not_its_marker(tmp_path):
    """`description: >-` followed by 1100 characters must trip the 1024 limit."""
    body = "\n".join("  " + "x" * 100 for _ in range(11))
    text = f"---\nname: demo\ndescription: >-\n{body}\n---\nbody\n"
    errors, _warns = audit_text(tmp_path, text)
    assert any("1024" in e for e in errors)


def test_empty_folded_description_is_missing(tmp_path):
    text = "---\nname: demo\ndescription: >-\nname2: x\n---\nbody\n"
    errors, _warns = audit_text(tmp_path, text)
    assert any("description" in e for e in errors)


def test_utf8_bom_does_not_hide_the_frontmatter(tmp_path):
    text = "---\nname: demo\ndescription: d\n---\nbody\n"
    errors, _warns = audit_text(tmp_path, text, encoding="utf-8-sig")
    assert errors == []


def test_description_continued_on_the_next_line_is_read(tmp_path):
    """A plain scalar may start on the line after the key."""
    text = "---\nname: demo\ndescription:\n  plain continued line\n---\nbody\n"
    errors, _warns = audit_text(tmp_path, text)
    assert errors == []
