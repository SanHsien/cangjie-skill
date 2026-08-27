# 開發環境

維護者與 AI 接手用的開發文件。產品使用方式在 [`README.md`](../README.md)；上游同步在 [`UPSTREAM.md`](UPSTREAM.md)；決策在 [`DECISIONS.md`](DECISIONS.md)；風險快照在 [`../REVIEW.md`](../REVIEW.md)。

## 架構

```text
長文本（書 / 影片轉寫 / 播客稿 / 課程）
        │
        ▼
 SKILL.md                 元 skill：何時呼叫、輸入檢查、七階段順序
        │
        ├── methodology/  各階段方法論
        ├── extractors/   五個並行提取器 prompt
        ├── templates/    SKILL / INDEX / DIGEST / 測試模板
        └── agents/       Codex UI 元資料（openai.yaml）
        │
        ▼
 books/<slug>/            蒸餾產出（不提交）
        │
        ▼
 安裝到 ~/.agents/skills、~/.claude/skills 或 ~/.cursor/skills 後才真正可被呼叫
```

根目錄 `SKILL.md`、`methodology/`、`extractors/`、`templates/`、`agents/openai.yaml` 是要安裝到 Agent Skills 目錄的產品。其餘檔案是本 fork 的開發與治理骨架，不要一起複製進 skills 目錄。

## 本機開發（Windows）

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
$env:PYTHONUTF8 = "1"
pwsh -NoProfile -File tools\dev_check.ps1
```

只驗證安裝路徑是否齊全時，確認這幾個產品入口都在：

- `SKILL.md`
- `methodology/00-overview.md`
- `extractors/framework-extractor.md`
- `templates/SKILL.md.template`
- `agents/openai.yaml`

不要對真實書籍跑完整蒸餾來當 CI。產品是 prompt 流水線，gate 驗的是規格、連結與維護腳本，不是一次真實拆書。

## Canonical gate

`tools\dev_check.ps1` 會依序：

1. `python -m compileall`（`scripts`、`tests`、`tools`）
2. `ruff check`（E9 + F）
3. `pytest tests/ -q`
4. `python tools/validate_skill.py SKILL.md`
5. `python tools/check_links.py`

CI 在 Ubuntu 跑 3.9–3.14，並加一個 Windows Python 3.14 job 跑同一套 gate。推 `main` 前先跑本機 gate。

## 工具設定

`pyproject.toml` **只放工具設定**，沒有 `[project]` 與 `[build-system]`：本 repo 交付的是
Markdown Agent Skill，不是 Python 套件，加了 `[project]` 只會讓人誤以為可以 `pip install .`。
它存在的理由是讓本機裸跑等同 CI：

```powershell
.venv\Scripts\python -m ruff check scripts tests tools   # 等同 CI 的 --select E9,F --target-version py39
.venv\Scripts\python -m pytest -q                        # 等同 CI 的 pytest tests -q
```

改 `ci.yml` 的 ruff 旗標時要同步改 `pyproject.toml`，`tests/test_docs.py::test_tool_config_matches_ci_flags`
會擋住漂移。`.python-version` 釘 3.14，對齊 Windows canonical gate。

`.gitattributes` 把行尾釘成 LF。沒有它，全域 `core.autocrlf=true` 會讓工作區變 CRLF，
於是 `git status` 顯示檔案 modified 但 `git diff` 是空的——那是假訊號，不是有人改了檔。

## 依賴新鮮度

`tools/check_dependency_freshness.py` 把 `requirements-dev.txt` 宣告的每一筆直接依賴拿去對
PyPI 現行版本，`.github/workflows/dependency-freshness.yml` 每月跑一次。它**只比對宣告**，
不看安裝環境、不改任何檔案：Dependabot 看的是 lock 的移動，看不到悄悄落後的宣告下限。

比較採**宣告精度**——`pytest>=8` 只比到 major，8.4.1 不會變成每月的假警報。

紅燈只有兩條誠實的出口，兩條都會留下理由：

| 出口 | 寫在哪 | 什麼時候用 | 會不會過期 |
| --- | --- | --- | --- |
| `# freshness-hold: <理由>` | `requirements-dev.txt` 宣告行的行末註解 | **常態政策**：這個下限就是我們要的下限（例：pytest 9 需要 Python 3.10，而 CI 仍測 3.9） | 不會，除非有人拿掉 |
| `.github/dependency-deferrals.json` 的 `deferredLatest` + `reason` | 獨立檔案 | **已評估、但這個月不升**：看過了，等 x.y 線穩定再說 | **會**。PyPI 一超過 `deferredLatest` 記的那個版本，報告就重新追問 |

**調高宣告下限來讓報告變綠不是出口**：宣告是相容性承諾，不是消音鍵。沒有這兩條出口時，
遇到「已評估但不該升」只剩「永遠紅」或「把下限調高壓下去」，而後者會讓宣告開始說謊。

契約測試在 `tests/test_dependency_freshness.py`（含「deferral 過期後恢復追問」那條）。

## 不要做的事

- 不要把產品 `SKILL.md` 改寫成維護索引。
- 不要提交 `books/`、PDF、字幕或轉寫稿。
- 不要在本 fork 啟用 star-history 自動推送。
- 不要把 DeepSeek Harness `.tgz` 放進 git。
- 測試必須是人造樣本與靜態規格檢查，不能拿受著作權保護的原書當 fixture。
