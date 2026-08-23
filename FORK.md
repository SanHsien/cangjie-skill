# Fork 維護說明

本 repo fork 自 [`kangarooking/cangjie-skill`](https://github.com/kangarooking/cangjie-skill)，
沿用 GNU Affero General Public License v3.0 與完整 Git 歷史。

## 為什麼維護 fork

- 保留原作者持續更新的 RIA-TV++ 方法論、提取器與 skill 模板。
- 採 Windows-first 維護：Windows 11 + PowerShell 是主要開發、除錯與完整驗收環境。
- 公開入口改以繁體中文為主，英文鏡像放 `README.en.md`。
- 建立可重現的 Windows 開發 gate、Windows CI job，以及逐筆審查的上游追蹤。
- 產品 Skill 仍可直接安裝到 Agent Skills 目錄呼叫。

**回貢判準：修的是上游的 bug 就送回去；這裡獨創的文件／Windows 維護骨架留在這裡。**
回貢前必須在當次對話取得維護者明確同意；「fork」「建開發環境」「開 PR」都不是同意。

## 與上游的差異

| 項目 | 說明 |
|---|---|
| `README.md` | 繁中主檔；英文鏡像在 `README.en.md`。不收第三語系，不轉載作者宣傳 |
| `AGENTS.md` / `CLAUDE.md` | 本 fork 的 AI 維護單一真相源 |
| `NOTICE.md` / `FORK.md` | 來源、授權與同步說明 |
| `tools/dev_check.ps1` | Windows 本機一鍵 gate |
| `.github/workflows/ci.yml` | Ubuntu 3.9–3.14 + Windows Python 3.14：pytest / ruff / Skill 驗證 / 連結檢查 |
| `.github/workflows/upstream-check.yml` | 每週對 `upstream/main` 做未審查 commit 檢查 |
| `.github/workflows/update-star-history.yml` | 加上 repo 閘門，避免本 fork 沒有 secret 卻每天失敗 |
| `docs/DECISIONS.md`、`docs/UPSTREAM.md`、`docs/DEVELOPMENT.md` | fork 維護文件 |

產品 `SKILL.md`、`methodology/`、`extractors/`、`templates/` 以上游為準；本 fork 已採用的產品修正記在下方與 [`docs/DECISIONS.md`](docs/DECISIONS.md)。

本 fork 已引用、尚未進上游 `main` 的產品修正：

- Codex 跨宿主（對齊上游 PR #24）：`agents/openai.yaml`、分批並行、frontmatter 只留 `name` + `description`、安裝路徑含 `~/.agents/skills/`
- 來源文本安全護欄（對齊上游 PR #5）
- darwin 模板強化寫在正文（對齊上游 PR #15 的 CHECKPOINT / 反模式 / 決策樹 / 兩條跨 skill 測試；**不**把 `trigger_words` 寫進 frontmatter）

## 分支與 remote

- `origin/main`：SanHsien 維護線，也是唯一長期分支。
- 日常修改在本機跑 gate 後直接推 `origin/main`。
- `upstream/main`：kangarooking 原始專案，只追蹤、不推送。
- Dependabot 或外部 fork 的變更走 PR，讀 diff 並通過 CI 後再合併。

不要 `git push upstream`。同步方式見 [`docs/UPSTREAM.md`](docs/UPSTREAM.md)。

上游更新簡體 `README.md` 時，把產品說明翻進本 fork 的繁中 `README.md`，並同步 `README.en.md`。作者個人頁、社群、QR、官網與星圖不要帶進來。公開示例表可同步，但必須標成上游／社群參考。來源 credit 留在 README 與 [`NOTICE.md`](NOTICE.md)。

## 換一台電腦怎麼開發

```powershell
git clone https://github.com/SanHsien/cangjie-skill.git
cd cangjie-skill
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
pwsh -NoProfile -File tools\dev_check.ps1
```

只想安裝 Skill、不開發時，把這些產品檔一起放到 Agent Skills 目錄（例如 `~\.agents\skills\cangjie-skill\`、`~\.claude\skills\cangjie-skill\` 或 `~\.cursor\skills\cangjie-skill\`）：

- `SKILL.md`
- `methodology/`
- `extractors/`
- `templates/`
- `agents/openai.yaml`

不要把 `tools/`、`docs/`、`tests/`、`.github/` 一併複製進去。
