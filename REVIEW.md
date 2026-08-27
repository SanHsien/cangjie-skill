# Repository review（Windows-first）

- Review date: 2026-08-27
- Review baseline: `4453b34f6580097fd86de858b364dea551d49341`
- Remediation: 同日 fork-local overlay（不回貢）
- Upstream reviewed through: `5f03a4cd8b521673f7a67ca6279330ec943bb369`
- Primary environment: Windows 11、PowerShell、Python 3.14（本機 gate 與 CI Windows job）；Ubuntu CI 補 3.9–3.14
- Status: 維護骨架可用。R-01～R-05 已在本線修。R-06（不跟上游改 MIT／英文預設 README）與 R-07（star-history 因 `git push` 不關 checkout credentials）接受。

## 結論

這個 fork 適合作為 Windows 本機、給 Agent 維護的 Cangjie 蒸餾線。產品行為跟隨 `kangarooking/cangjie-skill` 的方法論與模板，再加上本線 overlay：繁中／英文公開入口、Windows gate、逐筆上游審查，以及已落地的 Codex／安全護欄／預篩／短內容驗證子集。

本線 `LICENSE` 與 `NOTICE.md` 仍是 GNU AGPL v3.0。上游 2026-08 把之後的工作改成 MIT、根 README 改英文預設，那是上游自己的決定，不能自動改掉本 fork 已宣告的 copyleft overlay。

不把 fork 當成第二個官方產品 repo。DeepSeek Harness 安裝包、官網、星圖、社群與 QR 仍屬上游。本線 **沒有**獨立 CLI；執行時由宿主 Agent 讀 `SKILL.md` 跑 RIA-TV++。

本輪 **不回貢**。

## 本輪實證

### 審查當下（`4453b34`）

```text
git rev-parse HEAD
→ 4453b34f6580097fd86de858b364dea551d49341

GitHub Actions（SanHsien/cangjie-skill，4453b34）
→ CI success https://github.com/SanHsien/cangjie-skill/actions/runs/32640927848
→ CodeQL success https://github.com/SanHsien/cangjie-skill/actions/runs/32640927800
→ Update star history skipped（repo 閘門）https://github.com/SanHsien/cangjie-skill/actions/runs/33066225007
→ Upstream check failure（週排程，當時 2～4 筆未審）https://github.com/SanHsien/cangjie-skill/actions/runs/32687876139
```

實查（不是只讀 README）：

- `gh repo set-default --view` → `SanHsien/cangjie-skill`。
- `LICENSE` 開頭是 `GNU AFFERO GENERAL PUBLIC LICENSE` Version 3；`NOTICE.md` 宣告 fork 修改同樣走 AGPL。
- `git merge-base --is-ancestor` 對壓縮歷史前的內部落地 SHA 失敗；`docs/UPSTREAM.md` 部分標題已改成「目前 tree」，但 `docs/DECISIONS.md` 與 `tools/upstream_baseline.json` 的 notes 仍引用那些 SHA。
- `.gitignore` 當時有 `books/`、`*.pdf`、`*.epub`、`*.srt`、`*.vtt`，沒有 `*.mobi`／`*.azw`／`*.azw3`／`*.docx`／cookie／credentials。
- `update-star-history.yml` 有 `if: github.repository == 'kangarooking/cangjie-skill'`，排程在本 fork 實際 skipped。checkout 當時未與 `ci.yml` 同一 SHA pin。
- 上游四筆新 commit 已讀 diff：QR、日文切換、AGPL→MIT＋英文預設 README、英文 README 宣傳／官網。

**沒有**用真實書籍或長影片跑完整 RIA-TV++，**沒有**安裝 DeepSeek Harness 外掛，**沒有**對上游開 PR。

### 修正後

```text
pwsh -NoProfile -File tools\dev_check.ps1
→ 36 passed、WINDOWS DEV CHECK GREEN
→ check_links.py：20 份維護文件 + SKILL 裝包路徑，0 斷連結

python tools/check_upstream_updates.py --strict
→ 無新未審 commit（reviewed_through 已蓋過 5f03a4c）
```

## 已修 findings

| ID | 嚴重度 | 做了什麼 |
|---|---|---|
| R-01 | P2 | 文件與 baseline notes 不再引用壓縮歷史後失效的內部落地 SHA；改寫成「目前 tree」 |
| R-02 | P2 | `.gitignore` 加 `*.mobi` `*.azw` `*.azw3` `*.docx` `cookies.txt` `cookies.json` `credentials.json`；`test_docs.py` 擴契約 |
| R-03 | P3 | `update-star-history.yml` checkout 改與 CI 相同的 SHA pin `3d3c42e…`（v7.0.1） |
| R-04 | P3 | `FORK.md` 補上已落地的 #22／#4／#10 產品修正清單 |
| R-05 | P2 | 四筆未審 upstream commit 逐筆記錄略過理由，`reviewed_through` 推進到 `5f03a4cd8b521673f7a67ca6279330ec943bb369` |

## 接受、不改契約

| ID | 嚴重度 | 處理 |
|---|---|---|
| R-06 | P1 | **不**把 `LICENSE` 換成 MIT，**不**把根 README 改成英文預設，**不**收 `README.ja.md`／`README.zh-CN.md`，**不**嵌入官網／QR／星圖／作者宣傳 |
| R-07 | P3 | star-history job 會 `git push`，**不加** `persist-credentials: false`。該 workflow 已閘在上游 repo，本 fork 排程 skipped |

## 已檢查、不列為 finding

- `gh api repos/SanHsien/cangjie-skill` 層：fork、parent 為 `kangarooking/cangjie-skill`，預設分支 `main`。
- 產品 `SKILL.md` frontmatter 只留 `name` + `description`；模板無 `trigger_words`／`related_skills`。
- 未提交 `source-adapters/x-twitter.md`；#25 遠端 GraphQL 已不可解析，維持暫不引檔。
- Open PR #4/#5/#10/#15/#22/#24/#26 head 未變，不重評相同 diff。
- Dependabot 只開 PR，不自動合併。
- 本 fork CI／CodeQL／upstream-check／dependency-freshness 的 checkout 已 SHA pin。
- 公開入口繁中／英文互指；`README.md` 不含作者宣傳針。
- `pyproject.toml` 沒有 `[project]`／`[build-system]`。
- `.gitattributes` 釘 `eol=lf`。

## 尚未宣稱範圍

- **沒有**用真實書籍、PDF、字幕或長影片跑完整蒸餾流水線，因此不宣稱預篩／驗證子集已在真實來源上壓過一輪。
- **沒有**安裝或執行 DeepSeek Harness 外掛；安裝包仍從上游 Release 下載。
- **沒有**把產品 `SKILL.md`／`methodology/`／`extractors/`／`templates/` 翻成繁體。
- `dev_check.ps1` **不含** Bandit、CodeQL、真實蒸餾。
- **不宣稱** fork 有自己的 GitHub Release 或獨立產品版號。
- **不宣稱** 已把 overlay 送回上游。

## 建議下一步

1. 之後維護直接推 `origin/main`。回貢需當次對話明確同意。
2. 週排程 Upstream check 應隨 baseline 推進轉綠；若再紅，先看是不是又有新 commit，不要把 watermark 往回退。
3. 上游若把 MIT 寫進 `SKILL.md` 或方法論（而不只是 README／LICENSE），再回來評產品契約，而不是自動改本線授權。
