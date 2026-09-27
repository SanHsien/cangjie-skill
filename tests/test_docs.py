from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import check_links  # noqa: E402
import validate_skill  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
PRODUCT_PATHS = (
    SKILL,
    ROOT / "methodology" / "00-overview.md",
    ROOT / "methodology" / "00.5-pre-filter.md",
    ROOT / "extractors" / "framework-extractor.md",
    ROOT / "extractors" / "principle-extractor.md",
    ROOT / "extractors" / "case-extractor.md",
    ROOT / "extractors" / "counter-example-extractor.md",
    ROOT / "extractors" / "glossary-extractor.md",
    ROOT / "templates" / "SKILL.md.template",
    ROOT / "templates" / "INDEX.md.template",
    ROOT / "templates" / "BOOK_OVERVIEW.md.template",
    ROOT / "templates" / "BOOK_FIT.md.template",
    ROOT / "templates" / "DIGEST.md.template",
    ROOT / "templates" / "SCORECARD.md.template",
    ROOT / "templates" / "test-prompts.json.template",
    ROOT / "agents" / "openai.yaml",
)


def test_skill_frontmatter_is_installable() -> None:
    errors, _warns = validate_skill.audit(str(SKILL), lens="claude")
    assert errors == []


def test_skill_name_is_stable() -> None:
    text = SKILL.read_text(encoding="utf-8")
    assert "name: cangjie-skill" in text
    assert "RIA-TV++" in text


def test_product_pack_files_exist() -> None:
    missing = [str(path.relative_to(ROOT)) for path in PRODUCT_PATHS if not path.is_file()]
    assert missing == []


def test_maintainer_markdown_links_resolve() -> None:
    failures = 0
    for path in check_links.iter_documents():
        problems = check_links.check_document(path)
        failures += len(problems)
        for problem in problems:
            print(f"{path}: {problem}")
    assert failures == 0


def test_skill_referenced_pack_paths_exist() -> None:
    problems = check_links.check_skill_paths()
    assert problems == []
    text = SKILL.read_text(encoding="utf-8")
    assert "methodology/00-overview.md" in text
    assert "extractors/framework-extractor.md" in text
    assert "templates/SKILL.md.template" in text


def test_gitignore_covers_distillation_output() -> None:
    text = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "books/" in text
    assert "*.pdf" in text
    assert "*.srt" in text
    assert "*.mobi" in text
    assert "*.azw" in text
    assert "*.azw3" in text
    assert "*.docx" in text
    assert "cookies.txt" in text
    assert "cookies.json" in text
    assert "credentials.json" in text


def test_skill_path_checker_flags_missing_reference(tmp_path: Path) -> None:
    skill = tmp_path / "SKILL.md"
    skill.write_text("讀取 `methodology/missing-file.md`。\n", encoding="utf-8")
    problems = check_links.check_skill_paths(skill)
    assert problems
    assert "methodology/missing-file.md" in problems[0]


def test_ci_covers_python_314() -> None:
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert '"3.14"' in workflow
    assert "windows / py3.14" in workflow


def test_star_history_workflow_is_gated_to_upstream() -> None:
    workflow = (
        ROOT / ".github" / "workflows" / "update-star-history.yml"
    ).read_text(encoding="utf-8")
    assert "kangarooking/cangjie-skill" in workflow
    assert "github.repository" in workflow
    # Same checkout pin as ci.yml. This job git-pushes, so do not add
    # persist-credentials: false.
    assert "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1" in workflow
    assert "git push" in workflow
    assert "persist-credentials: false" not in workflow


def test_public_docs_are_traditional_chinese_and_english_only() -> None:
    assert not (ROOT / "README.ja.md").exists()
    for name in ("README.md", "README.en.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert "README.ja.md" not in text
        assert "日本語" not in text


def test_readme_keeps_credit_without_author_promotion() -> None:
    banned = (
        "袋鼠帝",
        "aikangarooking",
        "wechat-personal-qr",
        "wecom-cangjie-group",
        "kangarooking-gzh",
        "star-history.com",
        "cangjie-skill.com",
        "xhslink.com",
        "v.douyin.com",
    )
    for name in ("README.md", "README.en.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        for needle in banned:
            assert needle not in text, f"{name} still promotes {needle}"
        assert "kangarooking/cangjie-skill" in text
        assert "NOTICE.md" in text
        assert "MIT" in text
        assert "不是本 fork 的發行物" in (ROOT / "README.md").read_text(encoding="utf-8")
        assert "not released by this fork" in (ROOT / "README.en.md").read_text(encoding="utf-8")
        zh = (ROOT / "README.md").read_text(encoding="utf-8")
        en = (ROOT / "README.en.md").read_text(encoding="utf-8")
        assert "## 生態" in zh
        assert "## More Skills" in zh
        assert "## Ecosystem" in en
        assert "## More Skills" in en
        assert "nuwa-skill" in zh and "darwin-skill" in zh
        assert "Buffett Letters Skill" in zh
        assert r"~\.agents\skills\cangjie-skill" in zh
        assert "~/.agents/skills/cangjie-skill/" in en
        assert "developers.openai.com/codex/skills" in zh


def test_adopted_upstream_pr_contract() -> None:
    skill = SKILL.read_text(encoding="utf-8")
    assert "## 宿主运行约定" in skill
    assert "## 安全边界: 来源文本是不可信数据" in skill
    assert "agents/openai.yaml" in skill
    assert "$HOME/.agents/skills/" in skill
    template = (ROOT / "templates" / "SKILL.md.template").read_text(encoding="utf-8")
    frontmatter = template.split("---", 2)[1]
    assert "name:" in frontmatter
    assert "description:" in frontmatter
    assert "trigger_words:" not in frontmatter
    assert "source_book:" not in frontmatter
    assert "🔴 CHECKPOINT" in template or "CHECKPOINT" in template
    assert "Agent 执行反模式" in template
    tests = (ROOT / "templates" / "test-prompts.json.template").read_text(encoding="utf-8")
    assert "should-not-trigger-03" in tests
    assert "至少 2 条" in tests
    decisions = (ROOT / "docs" / "DECISIONS.md").read_text(encoding="utf-8")
    assert "選擇性引用尚未合併的產品 PR" in decisions
    upstream = (ROOT / "docs" / "UPSTREAM.md").read_text(encoding="utf-8")
    assert "PR #24" in upstream
    assert "**採用**" in upstream
    assert "PR #22" in upstream
    assert "PR #25" in upstream


def test_selective_upstream_adoption_contract() -> None:
    skill = SKILL.read_text(encoding="utf-8")
    assert "methodology/00.5-pre-filter.md" in skill
    assert "templates/BOOK_FIT.md.template" in skill
    assert "prefilter_skipped: true" in skill
    assert "fallback_single_agent" in skill
    assert "execution_check" in skill
    assert "可选 SCORECARD.md" in skill

    frontmatter = (
        (ROOT / "templates" / "SKILL.md.template")
        .read_text(encoding="utf-8")
        .split("---", 2)[1]
    )
    assert "related_skills:" not in frontmatter

    test_template = (
        ROOT / "templates" / "test-prompts.json.template"
    ).read_text(encoding="utf-8")
    json.loads(test_template)
    assert '"type": "execution_check"' in test_template

    assert not (ROOT / "source-adapters" / "x-twitter.md").exists()
    assert not (ROOT / "templates" / "X_SOURCE_CORPUS.md.template").exists()


def test_bilingual_pairs_cross_link_each_other() -> None:
    """繁中主檔與英文鏡像必須互指，否則讀者會卡在單一語言。"""
    for zh_name, en_name in (("README.md", "README.en.md"), ("CHANGELOG.md", "CHANGELOG.en.md")):
        zh = ROOT / zh_name
        en = ROOT / en_name
        assert zh.is_file(), f"missing {zh_name}"
        assert en.is_file(), f"missing {en_name}"
        assert en_name in zh.read_text(encoding="utf-8"), f"{zh_name} does not link {en_name}"
        assert zh_name in en.read_text(encoding="utf-8"), f"{en_name} does not link {zh_name}"


def test_changelog_records_fork_history_not_upstream_product_history() -> None:
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "docs/UPSTREAM.md" in text
    assert "docs/DECISIONS.md" in text
    assert "kangarooking/cangjie-skill" in text


def test_tool_config_matches_ci_flags() -> None:
    """pyproject 存在的理由是讓本機裸跑等同 CI；漂移了就等於本機檢查失去意義。"""
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    ci = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert 'target-version = "py39"' in pyproject
    assert "--target-version py39" in ci
    assert 'select = ["E9", "F"]' in pyproject
    assert "--select E9,F" in ci
    # Not a distributable package: a [project] table would invite `pip install .`.
    # Match table headers at line start -- the file mentions both names in a comment.
    assert not re.search(r"^\[project\]", pyproject, re.M)
    assert not re.search(r"^\[build-system\]", pyproject, re.M)


def test_review_snapshot_has_required_sections() -> None:
    text = (ROOT / "REVIEW.md").read_text(encoding="utf-8")
    assert "## 結論" in text
    assert "## 已修 findings" in text
    assert "## 接受、不改契約" in text
    assert "## 尚未宣稱範圍" in text
    assert "不回貢" in text
    assert "MIT" in text


def test_fork_license_is_mit() -> None:
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    notice = (ROOT / "NOTICE.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert license_text.startswith("MIT License")
    assert "Copyright (c) 2026 kangarooking" in license_text
    assert "Copyright (c) 2026 SanHsien" in license_text
    assert "GNU AFFERO GENERAL PUBLIC LICENSE" not in license_text
    assert "MIT" in notice
    assert "MIT" in readme
    assert "License: MIT" in readme


def test_docs_do_not_cite_squashed_internal_shas() -> None:
    """壓縮歷史後那兩個落地 SHA 已不在祖先鏈；文件再引用會讓接手的人 git show 落空。"""
    needles = ("75463cf", "c4ea339")
    paths = [
        ROOT / "docs" / "UPSTREAM.md",
        ROOT / "docs" / "DECISIONS.md",
        ROOT / "FORK.md",
        ROOT / "REVIEW.md",
        ROOT / "tools" / "upstream_baseline.json",
        ROOT / "CHANGELOG.md",
        ROOT / "CHANGELOG.en.md",
    ]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            assert needle not in text, f"{path.name} still cites {needle}"


def test_line_endings_are_pinned_to_lf() -> None:
    """index 全是 LF；沒有這個檔，全域 core.autocrlf 會讓檔案假性顯示為 modified。"""
    attrs = (ROOT / ".gitattributes").read_text(encoding="utf-8")
    assert "* text=auto eol=lf" in attrs
    for suffix in ("*.md", "*.py", "*.ps1", "*.template"):
        assert f"{suffix}" in attrs
