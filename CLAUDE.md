# CLAUDE.md

請先完整閱讀並遵守 [`AGENTS.md`](AGENTS.md)。本檔只補充 Claude Code 的最小入口：

- 這是保留上游歷史的 fork；不要移除 `upstream`、原作者或 GNU AGPL v3.0 授權標示。
- 根目錄 `SKILL.md` 是產品元 skill 規格，不要改寫成本 fork 的維護索引。
- `methodology/`、`extractors/`、`templates/` 以上游為準，除非 `FORK.md` 已記錄 fork 修正。
- 修改維護工具或測試前，先跑對應 pytest；提交前跑
  `pwsh -NoProfile -File tools\dev_check.ps1`。
- 書籍、字幕、轉寫稿、`books/` 產出與憑證一律不可提交。
- 使用繁體中文，直接交付可驗證結果，避免冗長背景鋪陳。
