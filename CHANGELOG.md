[English](CHANGELOG.en.md) | 中文版

# 變更紀錄

格式參考 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.1.0/)，新的在上面。
本檔只記錄**本 fork 的維護歷史**（2026-08-22 起）；上游
[`kangarooking/cangjie-skill`](https://github.com/kangarooking/cangjie-skill)
的產品演進見其自身歷史與 [`docs/UPSTREAM.md`](docs/UPSTREAM.md) 的審查清冊。
逐筆採用／略過的理由記在 [`docs/DECISIONS.md`](docs/DECISIONS.md)。

---

## 2026-08-27（全庫審查；略過上游四筆；維持 AGPL）

### 新增

- **`REVIEW.md`。** 全庫風險快照：結論、本輪實證、已修 findings、接受不改契約、尚未宣稱範圍。不是每個一般 bug 的流水帳。

### 變更

- **gitignore 補電子書與憑證。** `*.mobi`／`*.azw`／`*.azw3`／`*.docx`、`cookies.txt`／`cookies.json`／`credentials.json`。契約寫進 `tests/test_docs.py`。
- **清掉壓縮歷史後失效的內部 SHA。** `docs/DECISIONS.md`、`docs/UPSTREAM.md`、`tools/upstream_baseline.json` 改寫成「目前 tree」，避免接手的人 `git show` 落空。
- **`update-star-history.yml` checkout SHA pin**，與 `ci.yml` 相同（v7.0.1）。該 job 會 `git push`，不加 `persist-credentials: false`。
- **`FORK.md` 補上已落地的產品修正清單**（#22／#4／#10 子集）。

### 上游

- **四筆新 commit 全部略過。** 企微 QR、日文 README 切換、AGPL→MIT＋英文預設 README、英文 README 的官網／QR／作者段。本線授權維持 AGPL-3.0。`reviewed_through` 推進到 `5f03a4cd8b521673f7a67ca6279330ec943bb369`。理由寫在 [`docs/UPSTREAM.md`](docs/UPSTREAM.md) 與 [`docs/DECISIONS.md`](docs/DECISIONS.md)。本輪不回貢。

## 2026-08-23（依賴出口與上游第二輪）

### 新增

- **依賴新鮮度的第二條出口。** 原本只有 `# freshness-hold:`（常態政策）一條。少了「已評估、
  但這個月不升」這條，遇到那種情況只剩「讓報告永遠紅」或「把宣告下限調高把它壓下去」，而後者
  是把相容性宣告當消音鍵。新增 `.github/dependency-deferrals.json` 的 `deferredLatest` +
  `reason`：它**會自己過期**——PyPI 一超過被審視的那個版本，報告就重新追問，所以 deferral
  不會靜靜變成永久消音。報告的「Review policy」第 0 條現在明寫兩條出口與「調高下限不是出口」。
- **`tests/test_dependency_freshness.py`（9 條）。** 這支檢查器先前完全沒有測試。涵蓋宣告精度
  比較（`>=7` 不該被 7.4.0 觸發）、hold 讀取、live deferral、**deferral 過期後恢復追問**、
  缺 `deferredLatest` 的條目一律忽略，以及報告必須同時寫出兩條出口。
- **`docs/DEVELOPMENT.md` 的「依賴新鮮度」章節。** 先前整份維護文件沒有提過這個檢查。

### 變更

- **`AGENTS.md` 的上游處理判準。** 原本寫「產品方向的 open PR 等上游合併成 commit 再審」——
  那是分類不是理由，無法被檢驗，下一個人只能整個重評一次。改為：四個面向（commit／PR／issue／
  分支）各記水位；結論要附可查證的證據（diff 動了哪些檔、本 fork 對應檔案的實際內容）與
  **觸發條件**；上游未合併的 PR 一樣要看，因為它可能是本 fork 也中的缺陷修正。

### 上游

- **PR #26（`registry/vidknot/entry.yaml`）：不引用。** `registry/` 這個目錄在 `upstream/main`
  與本 fork 都不存在，是投向尚未合併之目錄結構的第三方投稿；不動 `SKILL.md`／`methodology/`／
  `extractors/`／`templates/` 任何一個字，且條目全文 zh-CN。`reviewed_pr_through` 推進到 26。
- **兩條上游分支複查，head 未變、結論不變。** `agent/deepseek-harness-release` 的三個 commit
  只動 README（+23 行），安裝指令指向上游自家 Release 的 `.tgz`——那是本 fork 不建置也無法驗證
  的安裝包；`codex/official-site-redesign` 是 92 檔的 Astro 官網。

## 2026-08-23（開發環境對齊）

### 新增

- **`.gitattributes`。** index 內 57 個文字檔全是 LF，但全域 `core.autocrlf=true` 會把工作區
  轉成 CRLF，於是三個檔長期顯示為 modified 而 `git diff` 是空的。釘死 `eol=lf` 之後假訊號消失，
  且 `git add --renormalize .` 確認**零內容差異**——這是治雜訊，不是改檔案。
- **`.editorconfig`。** 對 `methodology/`、`extractors/`、`templates/` 關掉行尾空白修剪，
  避免編輯器為了套格式去動上游產品內容（呼應 AGENTS.md 的「不為了套格式而大改上游檔案」）。
- **`.cursor/rules/no-upstream-pr.mdc`（`alwaysApply: true`）。** 把 AGENTS.md 已有的
  「PR 只打本 fork」規則下放到 Cursor 的機器層。根因是 `gh` 在 fork clone 的預設 repo 就是上游。
- **`pyproject.toml`（只放工具設定）。** 本 repo 交付的是 Markdown Agent Skill 不是 Python 套件，
  所以刻意沒有 `[project]` 與 `[build-system]`；它存在的唯一理由是讓本機裸跑 `ruff check`／`pytest`
  的行為和 CI 一致。ruff `target-version = "py39"`、`select = ["E9","F"]`、pytest `testpaths = ["tests"]`
  都與 `ci.yml` 現行旗標對齊。
- **`.python-version`（3.14）。** 對齊 CI 的 Windows canonical gate；Ubuntu job 仍測 3.9–3.14。
- **`CODE_OF_CONDUCT.md`。** 中英雙語，回報管道指向既有的 `SECURITY.md`。
- **`CHANGELOG.md` / `CHANGELOG.en.md`。** 就是本檔與其英文鏡像。

## 2026-08-23

### 新增

- **`fork` 選擇性採用上游的蒸餾守則。** 新增 `methodology/00.5-pre-filter.md` 前置過濾階段與
  `templates/BOOK_FIT.md.template`，並強化 stage1.5 三重驗證、stage3 Zettelkasten、
  stage4 壓力測試與 stage5 交付。

### 變更

- 上游 PR 嚴格複審結果寫進 [`docs/UPSTREAM.md`](docs/UPSTREAM.md) 與
  [`docs/DECISIONS.md`](docs/DECISIONS.md)，`tools/upstream_baseline.json` 隨審查結果推進。
  Baseline 代表「已審查」，不代表「全部已合併」。
- 收斂上游審查交接帳本，關掉待辦欄位。

## 2026-08-22

### 新增

- **`fork` Windows-first 維護骨架。** `.github/` 全套（issue／PR 模板、dependabot、
  CI、CodeQL、相依新鮮度、上游檢查 workflow）、`.gitignore`、`AGENTS.md`、`CLAUDE.md`、
  `FORK.md`、`NOTICE.md`、`CONTRIBUTING.md`、`SECURITY.md`、`docs/`、`tools/`、`tests/`。
  CI 跑 Ubuntu 3.9–3.14 與 Windows 3.14：pytest、ruff（E9+F）、`validate_skill.py`、連結檢查。
- **`fork` 採用上游的 Codex 支援、來源文本護欄與 darwin body 欄位**，含 `agents/openai.yaml`。

### 變更

- **公開入口只留繁中與英文。** 移除 `README.ja.md`；`README.md` 改繁中主檔、`README.en.md` 為英文鏡像。
  來源與授權 credit 保留，作者宣傳、官網、社群、QR 與星圖不轉載。上游若新增第三語系 README 一律略過。
- **上游示例目錄以「讀者參考」形式復原**進兩份 README，並標明來源為上游／社群。
- `tests/test_docs.py` 補上對應斷言，讓上述文件邊界由測試守住而不是靠記性。
