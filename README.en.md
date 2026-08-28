# Cangjie Skill

<p>
  <a href="README.md">繁體中文</a> ·
  <a href="README.en.md"><strong>English</strong></a>
</p>

[![CI](https://github.com/SanHsien/cangjie-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/SanHsien/cangjie-skill/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

Distill a book, long video, or podcast into a set of executable AI skills.

> **This is a Windows-first maintenance fork of [`kangarooking/cangjie-skill`](https://github.com/kangarooking/cangjie-skill).** It keeps the MIT license and full git history. Product behaviour follows upstream; this line adds Traditional Chinese docs, a Windows development gate, and commit-by-commit upstream review. See [`FORK.md`](FORK.md), [`docs/UPSTREAM.md`](docs/UPSTREAM.md), and [`REVIEW.md`](REVIEW.md).

## Install the skill

Copy the product files into an Agent Skills directory. Do not copy `tools/`, `docs/`, `tests/`, or `.github/`.

- `SKILL.md`
- `methodology/`
- `extractors/`
- `templates/`
- `agents/openai.yaml`

Typical locations: `~/.agents/skills/cangjie-skill/`, `~/.claude/skills/cangjie-skill/`, or `~/.cursor/skills/cangjie-skill/`. DeepSeek Harness packages still come from [upstream releases](https://github.com/kangarooking/cangjie-skill/releases).

Maintainer setup (Windows):

```powershell
git clone https://github.com/SanHsien/cangjie-skill.git
cd cangjie-skill
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
pwsh -NoProfile -File tools\dev_check.ps1
```

Details: [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md).

## Why This Exists

There's a recent viral idea: distilling colleagues into AI skills. Even after someone leaves, their experience, tone, and work style can be partially replicated by AI. [nuwa-skill](https://github.com/alchaincyf/nuwa-skill) does exactly this — creating "human skills" like an Elon Musk skill or a Warren Buffett skill. The companion [darwin-skill](https://github.com/alchaincyf/darwin-skill) handles automatic skill evolution.

Distilling people is valuable — nuwa-skill has already proven this. Distilling what people have **written** is a complementary dimension: a book represents years of deliberate thinking — the distilled essence of careful reflection. Rather than imitating someone's expression style, extracting their systematically produced methodologies into tools that help people solve real problems is equally valuable.

There's also a real pain point: you might read many books but struggle to apply them. Knowledge stays at the "I've read it" level and never gets activated in real decisions. Once a book is distilled into skills, an AI agent can invoke that knowledge in real scenarios — instead of letting it gather dust in your notes.

So cangjie-skill has one clear goal: **distill every book worth distilling**, turning each high-value book into a set of independently callable, composable, and pressure-testable AI skill packs.

## What Problems It Solves

- Reading many books but never applying them — knowledge stays at "I've read it" and never activates in real decisions
- Book summaries and reading notes are compression, not structured reuse — you still don't know "when to use what"
- Only a small fraction of a book deserves to become a tool — strict filtering is needed, not wholesale inclusion
- Existing reading methodologies are designed for human readers, not agent executors — distillation must be execution-oriented, not reading-oriented

## How It Works

cangjie-skill uses the **RIA-TV++** pipeline to transform books, transcripts, and other long-form source text into structured skills. A fit pre-screen runs by default before the seven execution stages:

0. **Fit Pre-Screen** — Check for reusable existing work, set a cost expectation, and score methodology density, executability, transferability, evidence, and boundaries. Produce `BOOK_FIT.md`, or record why the user explicitly skipped the pre-screen
1. **Whole-Book Comprehension (Adler Analysis)** — Structural, interpretive, critical, and applicability analysis using Mortimer Adler's method, producing `BOOK_OVERVIEW.md`
2. **Batched Parallel Extraction** — Five specialized extractors (frameworks, principles, cases, counter-examples, glossary) run in batches within the host's actual concurrency; fall back to serial when slots are scarce
3. **Triple Verification** — Each candidate must pass cross-domain evidence, predictive-power, and uniqueness checks. Short sources may use one internal citation plus independently supportable evidence. Dual review is reserved for higher-risk or higher-confidence runs; every run records its review mode
4. **RIA++ Construction** — Verified content is structured into six dimensions: R (original quote) / I (own-words reconstruction) / A1 (book cases) / A2 (future trigger scenarios) / E (executable steps) / B (boundaries & blind spots)
5. **Zettelkasten Linking** — Dependency, contrast, and composition relationships are identified, and author-specific terms are injected back into the skills that use them
6. **Pressure Testing** — Bait, cross-skill confusion, execution-quality, and adversarial cases test both activation and faithful execution; failures go back for reconstruction
7. **Delivery** — Generate a reader-facing `DIGEST.md`; add `SCORECARD.md` for full packs, comparative runs, or when requested. Install only the tested skills needed by the current task

The name RIA-TV++ breaks down as:
- **RIA**: From Zhao Zhou's bookmark method (Reading / Interpretation / Appropriation)
- **TV**: Triple Verification
- **++**: Agent-oriented extensions — E (Execution) + B (Boundary)

## Effect Examples

### Example 1: From a Book to a Skill Pack

**User Need**

"I want to turn a book's core methodologies into reusable AI skills, not just a reading summary."

**How cangjie-skill reasons**

- Check whether the source material has reusable methodological units
- Distinguish what deserves to be a standalone skill vs. background material
- Output a structured skill repository, not a single summary document

**Example Output**

> The result will not be one summary document. It will be a multi-skill repository with `BOOK_OVERVIEW.md`, `INDEX.md`, a reader-facing `DIGEST.md`, a `GLOSSARY.md`, multiple `*/SKILL.md` files, and `test-prompts.json` for trigger testing.

### Example 2: Structured Reuse, Not Compression

**User Need**

"I don't want a long explanatory article. I want a skill pack my agent can reuse."

**How cangjie-skill reasons**

- Target is structured reuse, not narrative compression
- Prioritize triggerable, composable, testable skill units
- Reject material that doesn't deserve standalone skill status

**Example Output**

> The system produces multiple skill modules with trigger conditions, boundaries, execution patterns, and related-skill links — rather than flattening the source into one generalized note.

## Public examples (upstream and community)

The repositories below are **already-distilled public examples**, so readers can see what a long-form source becomes after the pipeline. They are maintained by upstream or the community, **not released by this fork**. This repo only links to them; it does not copy those skill packs.

### Generated skill packs

| Repository | Source | Skills |
|------------|--------|--------|
| [buffett-letters-skill](https://github.com/kangarooking/buffett-letters-skill) | Buffett's shareholder letters (1957-2023) | 20 |
| [cognitive-dividend-skill](https://github.com/kangarooking/cognitive-dividend-skill) | Cognitive Dividend | 15 |
| [duan-yongping-skill](https://github.com/kangarooking/duan-yongping-skill) | Duan Yongping's Q&A (business + investment logic) | 15 |
| [viral-copywriting-skill](https://github.com/kangarooking/viral-copywriting-skill) | Bao Kuan Wen An | 14 |
| [copywriters-handbook-skill](https://github.com/kangarooking/copywriters-handbook-skill) | The Copywriter's Handbook | 12 |
| [contagious-skill](https://github.com/kangarooking/contagious-skill) | Contagious | 15 |
| [influence-skill](https://github.com/kangarooking/influence-skill) | Influence | 12 |
| [1000-true-fans-skill](https://github.com/kangarooking/1000-true-fans-skill) | 1000 True Fans | 13 |
| [system-prompt-skills](https://github.com/kangarooking/system-prompt-skills) | 165 AI product system prompts | 15 |
| [X-growth-skills](https://github.com/kangarooking/X-growth-skills) | Practical X (Twitter) account launch, content growth, algorithm, engagement, and monetization resources | 15 |
| [poor-charlies-almanack-skill](https://github.com/kangarooking/poor-charlies-almanack-skill) | Poor Charlie's Almanack | 12 |
| [no-rules-rules-skill](https://github.com/kangarooking/no-rules-rules-skill) | No Rules Rules | 10 |
| [huangdi-neijing-skill](https://github.com/kangarooking/huangdi-neijing-skill) | Huangdi Neijing (Suwen + Lingshu) | 22 |
| [first-principles-skill](https://github.com/kangarooking/first-principles-skill) | First Principles | 10 |
| [mao-selected-works-skill](https://github.com/kangarooking/mao-selected-works-skill) | Selected Works of Mao Zedong, Vol. 1-5 | 25 |
| [qbdx-hub/buffett-letters-skill](https://github.com/qbdx-hub/buffett-letters-skill) | Buffett Shareholder Letters (1957-2023) | 20 |
| [qbdx-hub/wo-yu-di-tan-skill](https://github.com/qbdx-hub/wo-yu-di-tan-skill) | Wo Yu Di Tan | 6 |
| [qbdx-hub/mingchao-those-things-skill](https://github.com/qbdx-hub/mingchao-those-things-skill) | Mingchao Those Things | 7 |
| [qbdx-hub/sunzi-bingfa-skill](https://github.com/qbdx-hub/sunzi-bingfa-skill) | Sunzi Bingfa | 8 |
| [qbdx-hub/zhouyi-skill](https://github.com/qbdx-hub/zhouyi-skill) | Zhouyi | 8 |
| [qbdx-hub/high-math-vol1-ch1-skill](https://github.com/qbdx-hub/high-math-vol1-ch1-skill) | High Math Vol. 1 Chapter 1 | 8 |

### Video distillation

These come from long-video, course, or playlist transcripts, and show that the same pipeline works beyond books.

| Repository | Source | Skills |
|------------|--------|--------|
| [ai-for-everyone-skill](https://github.com/kangarooking/ai-for-everyone-skill) | Andrew Ng, *AI for Everyone* | 25 |
| [loop-engineering-skill](https://github.com/kangarooking/loop-engineering-skill) | Loop Engineering long-video collection | 8 |

### Additional external sources

Upstream notes that these were included with the other authors' permission:

- [ace3000chao/book2startup](https://github.com/ace3000chao/book2startup): *The Lean Startup*, *The Art of War*, *Zhuangzi*, *I Ching*
- [shenqistart/book2skill](https://github.com/shenqistart/book2skill): *Chanlun*, *The Classic of Tea*

## Repository Structure

```text
cangjie-skill/
├── README.md              ← Traditional Chinese public entry (this fork)
├── README.en.md           ← English version
├── LICENSE                ← MIT
├── SKILL.md               ← Meta-skill spec (do not rewrite as a maintenance index)
├── agents/openai.yaml     ← Codex UI metadata
├── methodology/           ← RIA-TV++ stage docs
├── extractors/            ← Prompt definitions for the 5 parallel extractors
├── templates/             ← SKILL.md / INDEX.md / BOOK_OVERVIEW.md / BOOK_FIT.md templates
├── AGENTS.md / FORK.md    ← Fork maintenance rules
├── docs/                  ← Development, upstream review, decisions
└── tools/                 ← Windows gate and upstream checks
```

## Ecosystem

This is the related-project map recorded in the upstream README, so readers can see which slice cangjie-skill covers. nuwa and darwin are separate projects, **not a product line of this fork**.

- [nuwa-skill](https://github.com/alchaincyf/nuwa-skill) — Distills people (thinking styles, expression DNA)
- **cangjie-skill** (this skill) — Distills books (methodologies, frameworks, principles)
- [darwin-skill](https://github.com/alchaincyf/darwin-skill) — Evolves any skill

They interlock: nuwa distills people, cangjie distills books, darwin keeps them evolving.

## More Skills

Upstream and the community also publish distilled examples as standalone repos. This list covers the same public examples as the tables above, with a one-line description of what each pack is for. **They are not releases of this fork.**

- [Buffett Letters Skill](https://github.com/kangarooking/buffett-letters-skill) — 20 investment reasoning skills from Buffett's 60+ years of shareholder letters
- [Poor Charlie's Almanack Skill](https://github.com/kangarooking/poor-charlies-almanack-skill) — 12 decision-making and judgment skills from Charlie Munger's core thinking methods
- [No Rules Rules Skill](https://github.com/kangarooking/no-rules-rules-skill) — 10 organizational design skills from Netflix's culture of freedom and responsibility
- [Cognitive Dividend Skill](https://github.com/kangarooking/cognitive-dividend-skill) — 15 cognitive tool skills for thinking upgrades from *Cognitive Dividend*
- [Duan Yongping Skill](https://github.com/kangarooking/duan-yongping-skill) — 15 business and investment skills from Duan Yongping's Q&A collection
- [Viral Copywriting Skill](https://github.com/kangarooking/viral-copywriting-skill) — 14 sales copywriting and diagnosis skills from *Bao Kuan Wen An*
- [Copywriters Handbook Skill](https://github.com/kangarooking/copywriters-handbook-skill) — 12 sales copywriting, headline, and benefit translation skills from *The Copywriter's Handbook*
- [Contagious Skill](https://github.com/kangarooking/contagious-skill) — 15 STEPPS propagation strategy and word-of-mouth diagnosis skills from *Contagious*
- [Influence Skill](https://github.com/kangarooking/influence-skill) — 12 persuasion psychology, compliance mechanism, and defensive judgment skills from *Influence*
- [1000 True Fans Skill](https://github.com/kangarooking/1000-true-fans-skill) — 13 personal branding, true fan development, and trust-based monetization skills from *1000 True Fans*
- [System Prompt Skills](https://github.com/kangarooking/system-prompt-skills) — 15 system prompt design skills distilled from 165 AI product system prompts
- [X Growth Skills](https://github.com/kangarooking/X-growth-skills) — 15 skills for X account launch, content, algorithms, engagement, review, and monetization
- [Huangdi Neijing Skill](https://github.com/kangarooking/huangdi-neijing-skill) — 22 thinking-method skills from *Huangdi Neijing* (Suwen 12 + Lingshu 10)
- [First Principles Skill](https://github.com/kangarooking/first-principles-skill) — 10 skills on axiomatic reasoning, boundary-breaking innovation, and organizational refresh from *First Principles*
- [Mao Selected Works Skill](https://github.com/kangarooking/mao-selected-works-skill) — 25 cognition, strategy, organization, and execution skills from *Selected Works of Mao Zedong*
- [qbdx-hub Buffett Letters Skill](https://github.com/qbdx-hub/buffett-letters-skill) — 20 investment and capital allocation skills from Buffett shareholder letters
- [qbdx-hub Wo Yu Di Tan Skill](https://github.com/qbdx-hub/wo-yu-di-tan-skill) — 6 skills on limits, suffering, writing, and self-anchoring from *Wo Yu Di Tan*
- [qbdx-hub Mingchao Those Things Skill](https://github.com/qbdx-hub/mingchao-those-things-skill) — 7 skills on power structure, institutional failure, and historical explanation from *Mingchao Those Things*
- [qbdx-hub Sunzi Bingfa Skill](https://github.com/qbdx-hub/sunzi-bingfa-skill) — 8 skills on strategic judgment, resource control, and action selection from *Sunzi Bingfa*
- [qbdx-hub Zhouyi Skill](https://github.com/qbdx-hub/zhouyi-skill) — 8 skills on situational diagnosis, timing, and advance-retreat boundaries from *Zhouyi*
- [qbdx-hub High Math Vol. 1 Chapter 1 Skill](https://github.com/qbdx-hub/high-math-vol1-ch1-skill) — 8 learning skills on limits, infinitesimals, and continuity from High Math Vol. 1 Chapter 1
- [book2startup](https://github.com/ace3000chao/book2startup) — external source included with the author's permission; skills from *The Lean Startup*, *The Art of War*, *Zhuangzi*, and *I Ching*
- [book2skill](https://github.com/shenqistart/book2skill) — external source included with the author's permission; AI-agent skills from *Chanlun* and *The Classic of Tea*

## Source and license

This repository is a fork of [`kangarooking/cangjie-skill`](https://github.com/kangarooking/cangjie-skill) and is MIT licensed (upstream switched from AGPL in August 2026; this overlay follows). The product `SKILL.md`, methodology, extractors, and templates are upstream work. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE.md).

This fork's maintenance changes are recorded in [`CHANGELOG.en.md`](CHANGELOG.en.md); its relationship to and differences from upstream are in [`FORK.md`](FORK.md).
