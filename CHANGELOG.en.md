English | [中文版](CHANGELOG.md)

# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); newest first.
This file records **this fork's maintenance history** only (from 2026-08-22). The product
history of upstream
[`kangarooking/cangjie-skill`](https://github.com/kangarooking/cangjie-skill) lives in its
own history and in the review ledger at [`docs/UPSTREAM.md`](docs/UPSTREAM.md). Per-commit
adopt/skip reasoning is recorded in [`docs/DECISIONS.md`](docs/DECISIONS.md).

---

## 2026-08-23 (dependency exits and the second upstream pass)

### Added

- **A second honest exit for the dependency freshness check.** There was only
  `# freshness-hold:` (a standing policy). Without an exit for "reviewed, but not this month",
  that situation leaves two options: let the report stay red forever, or raise the declared
  floor to push it green -- and the second turns a compatibility promise into a mute button.
  `.github/dependency-deferrals.json` now takes `deferredLatest` + `reason`, and it **expires
  by itself**: once PyPI moves past the release it was reviewed against, the report asks again,
  so a deferral cannot quietly become permanent silence. Step 0 of the report's review policy
  now names both exits and says raising a floor is not one of them.
- **`tests/test_dependency_freshness.py` (9 cases).** The checker had no tests at all. They
  cover the declared-precision comparison (`>=7` must not fire on 7.4.0), hold parsing, a live
  deferral, **a deferral expiring and the row going back to REVIEW UPDATE**, entries without
  `deferredLatest` being ignored, and the report naming both exits.
- **A "dependency freshness" section in `docs/DEVELOPMENT.md`.** The maintenance docs had never
  mentioned this check.

### Changed

- **The upstream review criterion in `AGENTS.md`.** It said "open PRs about product direction
  wait until upstream merges them into a commit" -- a category, not a reason. It cannot be
  checked, so the next person can only redo the whole evaluation, which is what the ledger
  exists to prevent. It now requires a watermark per axis (commit / PR / issue / branch),
  conclusions backed by checkable evidence (which files the diff touches, what this fork's
  corresponding file actually contains) plus the **condition that should bring it back for
  another look**, and states that an unmerged upstream PR still has to be read, because it may
  fix a defect this fork also has.

### Upstream

- **PR #26 (`registry/vidknot/entry.yaml`): not adopted.** The `registry/` directory exists
  neither in `upstream/main` nor in this fork -- it is a third-party submission against a
  directory structure that has not landed. It touches none of `SKILL.md`, `methodology/`,
  `extractors/` or `templates/`, and the entry is written entirely in Simplified Chinese.
  `reviewed_pr_through` moves to 26.
- **Both upstream branches re-checked; heads unchanged, conclusions unchanged.** The three
  commits on `agent/deepseek-harness-release` only touch README (+23 lines) and point the
  install command at a `.tgz` on upstream's own releases -- a package this fork neither builds
  nor verifies. `codex/official-site-redesign` is a 92-file Astro website.

## 2026-08-23 (development environment)

### Added

- **`.gitattributes`.** All 57 tracked text files are LF in the index, but a global
  `core.autocrlf=true` renders the working tree as CRLF, which left three files showing as
  modified with an empty `git diff`. Pinning `eol=lf` removes that phantom, and
  `git add --renormalize .` confirmed **zero content difference** — this fixes noise, it
  does not rewrite files.
- **`.editorconfig`.** Trailing-whitespace trimming is disabled for `methodology/`,
  `extractors/`, and `templates/` so an editor setting cannot quietly reformat upstream
  product content.
- **`.cursor/rules/no-upstream-pr.mdc`** with `alwaysApply: true`, pushing the
  PR-targets-this-fork rule already in AGENTS.md down to Cursor's mechanical layer. The
  root cause is that `gh` defaults to the upstream repository in a fork clone.
- **`pyproject.toml`, tool configuration only.** This repository ships a Markdown Agent
  Skill, not a Python package, so there is deliberately no `[project]` or `[build-system]`
  table; the file exists so a bare `ruff check` or `pytest` locally behaves the way CI
  does. ruff `target-version = "py39"` and `select = ["E9","F"]`, pytest
  `testpaths = ["tests"]`, all matching the flags `ci.yml` passes today.
- **`.python-version`** pinned to 3.14, matching CI's canonical Windows gate. The Ubuntu
  job still covers 3.9 through 3.14.
- **`CODE_OF_CONDUCT.md`**, bilingual, pointing reports at the existing `SECURITY.md` flow.
- **`CHANGELOG.md` / `CHANGELOG.en.md`** — this file and its Chinese counterpart.

## 2026-08-23

### Added

- **`fork` Selective adoption of upstream's distillation guards.** Added the
  `methodology/00.5-pre-filter.md` pre-filter stage and
  `templates/BOOK_FIT.md.template`, and strengthened stage 1.5 triple verification,
  stage 3 Zettelkasten, stage 4 pressure testing, and stage 5 delivery.

### Changed

- The strict upstream PR re-review is recorded in [`docs/UPSTREAM.md`](docs/UPSTREAM.md)
  and [`docs/DECISIONS.md`](docs/DECISIONS.md), with `tools/upstream_baseline.json`
  advanced to match. The baseline means "reviewed", not "all merged".
- Closed the upstream review handoff ledger.

## 2026-08-22

### Added

- **`fork` Windows-first maintenance overlay.** The full `.github/` set (issue and PR
  templates, dependabot, CI, CodeQL, dependency freshness, upstream check), `.gitignore`,
  `AGENTS.md`, `CLAUDE.md`, `FORK.md`, `NOTICE.md`, `CONTRIBUTING.md`, `SECURITY.md`,
  `docs/`, `tools/`, and `tests/`. CI runs Ubuntu 3.9–3.14 and Windows 3.14: pytest, ruff
  (E9+F), `validate_skill.py`, and a Markdown link check.
- **`fork` Adopted upstream's Codex support, source-text guardrails, and darwin body
  fields**, including `agents/openai.yaml`.

### Changed

- **Public entry points are Traditional Chinese and English only.** `README.ja.md` was
  removed; `README.md` became the Chinese primary with `README.en.md` as the English
  mirror. Source and license credit are kept; author promotion, the official site,
  community links, QR codes, and the star chart are not carried over, and any future
  third-language README from upstream is skipped.
- **Upstream example catalogs were restored as reader references** in both READMEs,
  labelled as upstream/community material.
- `tests/test_docs.py` gained assertions for those documentation boundaries, so they are
  held by tests rather than by memory.
