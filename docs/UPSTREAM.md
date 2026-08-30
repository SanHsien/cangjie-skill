# 上游維護

## Remote

- Fork：`origin` → `https://github.com/SanHsien/cangjie-skill.git`
- 原作者：`upstream` → `https://github.com/kangarooking/cangjie-skill.git`
- 追蹤分支：`main`

## 檢查新提交

```powershell
git fetch upstream main
python tools\check_upstream_updates.py --strict
```

工具以 `tools/upstream_baseline.json` 的 `reviewed_through` 為起點，列出所有未審查提交。
有新提交或檢查失敗時，`--strict` 回傳非零；排程 workflow 也會因此明確失敗。

## 審查清冊

每次只做一次批次審查：

1. 讀 commit 主旨與變更檔案（open PR 必須讀 diff，禁止只憑標題／「等上游定案」結案）。
2. 判斷是否與繁中 README、Windows gate、#24 frontmatter 契約或測試衝突。
3. 可直接同步的提交用 merge；只需要部分修正時 cherry-pick 或最小重做。
4. 跑 `pwsh -NoProfile -File tools\dev_check.ps1`。
5. 在 `docs/DECISIONS.md` 記錄採用／略過理由（須引用具體檔案與衝突點）。
6. 驗證完成後才把 baseline 推進到已審查的完整 40 字元 SHA。

Baseline 代表「已審查」，不代表「全部已合併」。

README 衝突的解法：上游新簡體產品說明翻進 `README.md`，並同步 `README.en.md`。`README.ja.md`、作者宣傳、官網、社群、QR 與星圖略過。公開示例表可同步並標成上游／社群參考。來源與授權 credit 留在 README 與 `NOTICE.md`。

## 2026-08-22：fork 起點

本 fork 自上游 `main` `3a8c23a67884167411af230a5ff20975548756a5`
（`docs: add DeepSeek Harness plugin install (#23)`）建立。此 SHA 設為第一個 `reviewed_through`。
之後的上游 commit 才需要進入審查清冊。

## 2026-08-22：第一輪採用（產品內容在目前 tree）

| 項目 | 結論 | 落地狀態 |
| --- | --- | --- |
| [PR #24](https://github.com/kangarooking/cangjie-skill/pull/24) Codex 跨宿主 | **採用**。`agents/openai.yaml`、分批並行、frontmatter 只留 `name`+`description`、安裝含 `~/.agents/skills/`。略過 `README.ja.md`。 | 已進目前 `origin/main` |
| [PR #5](https://github.com/kangarooking/cangjie-skill/pull/5) 來源安全護欄 | **採用**。來源文本當不可信資料。 | 已進目前 `origin/main` |
| [PR #15](https://github.com/kangarooking/cangjie-skill/pull/15) darwin 9 維 | **部分採用**。CHECKPOINT／反模式／決策樹／跨 skill 測試 ≥2 寫進正文與模板。**不**把 `trigger_words` 寫進 frontmatter。 | 已進目前 `origin/main` |

## 2026-08-23：嚴格重評與選擇性落地（產品內容在目前 tree）

上游仍無新 commit（`reviewed_through` = `3a8c23a`）。本輪重讀 #22 / #25 / #10 / #4 的完整 diff、分支 vs `main`、open issue 正文。
**禁止**用「等上游定案／新階段／非本線需求」當唯一理由。以下保留可重現的評估、最終落地範圍與拒絕理由。

### 總表

| 項目 | 結論 | 硬理由（一句） |
| --- | --- | --- |
| #24 / #5 / #15 正文 | 已採用 | 相容性／安全／darwin 基線 |
| #22 | **部分採用，已落地** | 省 token 的預篩 + 三坑；複用檢查已改寫 |
| #25 | **暫不引檔；標可選低風險** | 僅 X 來源；無使用證據則不加檔 |
| #4 | **不整支；適配概念已併入 #22 子集** | 與 0.5 重複且更重；evaluation 含私路徑 |
| #10 | **部分採用，已落地** | 短內容 V1 + `execution_check` 有用；session 檔與 frontmatter 衝突已剔除 |
| `agent/deepseek-harness-release` | 不 cherry-pick | vs `main` 幾乎只剩 README；內容已進上游 #23 |
| `codex/official-site-redesign` | 不引 | 整站 Astro／registry／GEO／QR，非元 skill |

### PR #22 — 階段 0.5 預篩 + 三坑

- **diff 事實**：+71/−1，3 檔。新增 `methodology/00.5-pre-filter.md`；`SKILL.md` 插入「階段 0.5（必做，5 分鐘）」與「三個坑」；`00-overview.md` 加思想來源與流水線圖。
- **價值**：開工前擋小說／散文硬蒸，省 30–90 分鐘與數萬 token；三坑與 1.5／4 品質門一致。
- **與已採用衝突**：無 frontmatter／宿主衝突。與 **#4** 功能重疊（都是開蒸前門檻）。
- **落地子集**：
  1. 採「三坑」全文；可蒸性三問；≤1 問通過則降級摘要；成本表。
  2. 「複用檢查」改寫：搜本機 skills + 上游示例表連結；**不要**寫死 ClawHub / `skills_list`。
  3. 「必做」改成預設執行、使用者明示可跳過。
- **結論**：**部分採用，已進目前 `origin/main`**。實作另吸收 #4 的五維評分與四類產物判斷，但不帶 evaluation 樣本；預篩預設執行，使用者可明示跳過並留下 `prefilter_skipped`。

### PR #25 — X 來源 adapter

- **diff 事實**：新增 `source-adapters/x-twitter.md`、`templates/X_SOURCE_CORPUS.md.template`；`SKILL.md` 輸入可走 X 來源包與欄位映射；三語 README（含 `README.ja.md`）。
- **價值**：只在蒸 X／Twitter 串文時有用；適配器可選，不強迫改階段 0–5；邊界 token 補強 #5。
- **與已採用衝突**：無；與 #5 同向。
- **結論**：有蒸 X 需求再加檔 + `SKILL.md` 兩行；略過 `README.ja.md`。目前無使用證據 → **暫不引檔**，但評估標成「可選、低風險」，不是「非本線」打發。

### PR #4 — Stage −1 book-fit

- **diff 事實**：+420/−14，11 檔。新階段 −1 → `BOOK_FIT.md`；四結論 `full` / `partial` / `alternate_artifact` / `not_suitable`；`evaluation/` 樣本；基底偏舊（文中仍有 `book2skill`）；改日文 README。
- **價值**：`alternate_artifact`（小說別硬拆）概念正確，但與 #22 重複且更重（25 分 + 多一份產物）。
- **具體問題**：evaluation 含本機絕對路徑（`/Users/yuewang/...`）；三體樣本 PR 自承無原文 genre dry-run。
- **建議**：不整支採用；把「小說／alternate」判斷併入 #22 風格預篩即可。
- **結論**：**不整支採用**。只把五維適配評分、四類產物判斷與 `BOOK_FIT.md` 模板併入目前 tree；未採 evaluation、舊 `book2skill` 文字與日文 README。

### PR #10 — 驗證流水線強化

- **diff 事實**：+550/−74，14 檔。產品面：1.5 雙評審+仲裁、短內容 V1 自適應、`execution_check`、對抗出題、術語回填、`SCORECARD.md`。雜訊：`DEVELOPMENT_PROGRESS.md` / `PROJECT_RULES.md` / `SESSION_HANDOFF.md`（session 日誌、等用戶 commit）。階段 3 仍寫 frontmatter `related_skills`；安裝路徑仍偏 Claude／Cursor、缺 Codex。
- **價值**：短內容 V1 對影片／播客有用；`execution_check`／對抗出題補觸發後執行品質；強制雙評審在 Windows／Codex 上明顯變貴。
- **落地子集**：
  1. 採：短內容 V1 自適應、`execution_check`、對抗出題、可選 SCORECARD、術語回填寫**正文**。
  2. 雙評審標成有餘力才做；否則 `review_mode: fallback_single_agent`（PR 自己也寫了 fallback）。
  3. **剔除**：三份 session 檔、`related_skills` frontmatter、整支無差別合入。
- **結論**：**部分採用，已進目前 `origin/main`**。雙評審改為高風險／高信心模式，一般任務用一次結構化評審並記 `fallback_single_agent`；`SCORECARD.md` 只在完整包、比較、審計或使用者要求時生成。

### Open issues

| Issue | 可行動產品改動？ | 說明 |
| --- | --- | --- |
| #1 感謝 | 否 | 社交回饋 |
| #6 線上入口 | 否 | 第三方 hosted；本 fork 不做上傳／hosted |
| #9 YouTube 下載 | 否 | 屬 video-downloader／地區限制 |
| #11 可先試入口 | 否 | 外部試用連結 |
| #13 Codex | 是（已做） | 由 #24 覆蓋 |
| #14 步驟／影片 | 部分已有、無新增 | README 已有安裝路徑、直接呼叫 prompt、兩個效果示例與公開產物範例；影片是外部媒體產物，本輪不為湊項目新增或託管 |
| #16 VPN 廣告 | 否 | 推廣／噪音 |
| #20 progressive-skill | **部分採用，已落地** | 不引 Hermes 專用插件；採用跨宿主的「只安裝當前任務所需 skill 子集」紀律，寫入 `SKILL.md` 與 `methodology/07-stage5-deliver.md` |

### 分支（vs `upstream/main`）

| 分支 | 證據 | 結論 |
| --- | --- | --- |
| `main` | 追蹤來源 | — |
| `agent/deepseek-harness-release` | ahead 內容已 squash 進 #23；diff 對 main 幾乎只剩 README 外掛說明 | 不 cherry-pick；外掛仍從上游 Release 下載 |
| `codex/official-site-redesign` | `website/` Astro、registry、GEO、QR、Pages workflow 等 | 不引；本 fork 不維護官網 |

open PR 的 head 不算獨立可引用分支。

### Codex 接手結果

1. 目前 tree 已落地 **#22 + #4 最小子集**：預篩、五維 fit、四類產物、三坑、複用檢查、成本提示；沒有 evaluation 或舊宿主假設。
2. 目前 tree 已落地 **#10 最小子集**：短內容 V1、`execution_check`、對抗出題、術語回填、可選 SCORECARD；剔除 session 檔與 frontmatter `related_skills`，雙評審改成本感知。
3. #20 只採跨宿主安裝節制；#25 仍 defer，Cursor 草稿中的 X adapter 與模板未提交。
4. 主工作樹與 detached 隔離候選都跑過 `pwsh -NoProfile -File tools\dev_check.ps1`：20 passed、Ruff/validator/link checker 全綠。

### 水位

- PR：已看到 **#25**（`reviewed_pr_through`）
- issue：已看到 **#20**（`reviewed_issue_through`）
- commit baseline 仍是 `3a8c23a`（沒有新 upstream commit）
- 下次只看編號更大的，或已評估 PR 是否出現**新 commit**（有新 commit 才重讀 diff）

本輪核對的 open PR head：#4 `569d880526381ce221e6c56587e1258a3b6d1354`、#5 `57884a3a7ecff92a6979b1b9a412c02e0fe2ca86`、#10 `bb3a63689f23e4067978926bed01a659503389b4`、#15 `c0df1e58370f97ea3d5b277099d33e87b62fe650`、#22 `63f3c8ecf6fa78b9ff668b33068dec108994edda`、#24 `a1998989c2cbb6f5de461d5c5adb72c35dd3d61e`、#25 `d9796d9819fdaabd973905b059e404d8363d0a8c`。上游分支：`agent/deepseek-harness-release` `d0d0ed41bf4c1e0bc2ac0ff399a1216be9ba7d34`、`codex/official-site-redesign` `f6a03cc1d598421f999ead043fc06dc393855db8`。下次 head SHA 相同時不用重讀相同 diff。

## 2026-08-23（第二輪）：新 PR #26、分支複查、依賴新鮮度補上第二條出口

### PR #26 — VidkNot registry 條目：不引用

| 檢查 | 實查結果 |
| --- | --- |
| 它改什麼 | 新增單一檔案 `registry/vidknot/entry.yaml`（24 行 YAML），登記第三方工具 VidkNot（影片知識歸檔）的 slug、摘要、use cases。 |
| 本 fork 有沒有對應層 | **沒有。`registry/` 這個目錄在 `upstream/main` 與本 fork 都不存在**（`git ls-tree upstream/main --name-only` 只有 `extractors`／`methodology`／`templates`／`scripts`／`assets` 與文件）。它是投向上游**尚未合併的目錄結構**的第三方投稿。 |
| 內容是否影響方法論 | 否。沒有動 `SKILL.md`、`methodology/`、`extractors/`、`templates/` 任何一個字，也不是修正。 |
| 語言 | 條目全文 zh-CN。本 fork 的公開文件只維護繁中與英文（`tests/test_docs.py::test_public_docs_are_traditional_chinese_and_english_only` 會擋）。 |

**結論：不引用。** 觸發條件：上游把 `registry/` 合併進 `main` 且本 fork 決定維護同一份目錄時，
才需要回頭看這一類條目；在那之前，第三方投稿與本 fork 無關。

### 分支：複查兩條，結論不變

| 分支 | 今天實查 | 結論 |
| --- | --- | --- |
| `agent/deepseek-harness-release`（ahead 3、behind 1，head 未變 `d0d0ed4`） | 三個 commit 全部只動 `README.md`（+23 行），內容是 DeepSeek Harness 外掛安裝說明，安裝指令指向 `kangarooking/cangjie-skill` 自家 Release 的 `.tgz`。 | **不引用**，理由比上一輪更明確：那是**本 fork 不建置、也無法驗證的第三方安裝包**，把它寫進本 fork 的 README 等於替沒驗過的產物背書；且該段全文 zh-CN，與本 fork 的繁中／英雙語規則衝突。 |
| `codex/official-site-redesign`（ahead 26、behind 9，head 未變 `f6a03cc`） | 92 檔、+12,773 行，全在 `website/`（Astro 站台、GEO 探索層、IndexNow、submit 頁）。 | **不引用**：本 fork 不維護官網。 |

兩條 head SHA 與上一輪相同，diff 沒有重讀第二次的必要——只重新確認了「ahead 的內容是什麼」
與本 fork 是否有對應層。

### 依賴新鮮度：補上第二條出口

`tools/check_dependency_freshness.py` 原本只有 `# freshness-hold:` 一條出口。少了「已評估、
但這個月不升」這條，遇到那種情況只剩兩個選擇：讓報告永遠紅，或把宣告下限調高把它壓下去
——而後者是把相容性宣告當消音鍵。本輪補上 `.github/dependency-deferrals.json` 的
`deferredLatest` + `reason`：它**會自己過期**，PyPI 一超過被審視的那個版本，報告就重新問。
新增 `tests/test_dependency_freshness.py` 9 條把兩條出口、宣告精度比較與「過期後恢復追問」
釘住。

### 水位（2026-08-23 當日）

- PR：已看到 **#26**（`reviewed_pr_through` 由 25 推進到 26）
- issue：仍是 **#20**，沒有新的
- commit baseline 當時是 `3a8c23a`；2026-08-27 已推進，見下節

## 2026-08-27：審查四筆新 upstream commit；當時維持 AGPL；不回貢

`3a8c23a..upstream/main` 有四筆，已逐筆讀 diff。本 fork 不開上游 PR。

| Commit | 動了什麼 | 結論 |
| --- | --- | --- |
| `7e0d58a92060a838fa10d319e7232e163e79506f` | `assets/wecom-cangjie-group-qr.png` | **略過**。企微 QR 是作者宣傳；本 fork README 禁止嵌入。 |
| `a47a604b3940eda9bb0c83a276626ffa0c87d7e5` | 三語 README 加 `README.ja.md` 語言切換 | **略過日文連結**。本 fork 已有繁中／英文切換，不收第三語系。 |
| `f751bf9ff9f833cff702fe48d31ebd9d407d4b05` | `LICENSE` AGPL→MIT；根 README 改英文；新增 `README.zh-CN.md` | 2026-08-27 **整筆略過**。2026-08-28 **只跟授權**（見下節）；入口重組仍略過。 |
| `5f03a4cd8b521673f7a67ca6279330ec943bb369` | 英文 README 補 DeepSeek／影片表／示例列／官網／QR／作者段 | **略過宣傳與官網**。示例表（黃帝內經合併、影片蒸餾區）本線 README **已經有**，無需再合。 |

觸發條件：上游若把 MIT 變更寫進 `SKILL.md`／方法論（而不只是 README／LICENSE），或示例表出現本線沒有的新公開倉庫，再讀那些檔。

Open PR 仍是 #4/#5/#10/#15/#22/#24/#26；#25 遠端已不可解析（fork/PR 消失），維持先前「暫不引 X adapter」結論。issue 最大仍是 #20。

### 水位（2026-08-27）

- commit：`reviewed_through` = `5f03a4cd8b521673f7a67ca6279330ec943bb369`
- PR：仍 **#26**
- issue：仍 **#20**

## 2026-08-28：採用上游 MIT；仍不跟入口重組

`f751bf9` 同時做了兩件事：把 `LICENSE` 換成 MIT，以及把根 README 改成英文預設並新增 `README.zh-CN.md`。2026-08-27 整筆略過。2026-08-28 維護者決定**只跟授權**：

- **採用**：`LICENSE` 改 MIT；本線 overlay 同步以 MIT 宣告（`NOTICE.md`、README badge、AGENTS／FORK）。
- **仍略過**：英文預設 README、`README.zh-CN.md`、`README.ja.md`、官網／QR／作者宣傳。

這不是 cherry-pick 整支 `f751bf9`。水位不變（已在 2026-08-27 審過這四筆）。


## 2026-08-30：v2.5.0 逐筆審視，水位推進到 `44692125abcdb93eab7b0e7a5ecd6ccadf92dc6f`

上游在 `5f03a4c` 之後累積 9 個 commit（website MVP 四筆、需求文件一筆、README 索引一筆、
merge 一筆、v2.5.0 發版一筆、release 連結一筆）。逐筆結論與觸發條件寫在
[`DECISIONS.md`](DECISIONS.md) 的同日條目，摘要：

- **採用**：v2.5.0 的**階段 1.6 獨立 Skill 晉級門**。本 fork 實查確認沒有任何 Skill 數量預算，
  而 `00.5-pre-filter.md` 判的是開工前的產物形態、不是驗證後該獨立幾個，缺口是真的。
  移植的是設計不是 diff——上游寫 `verified.yaml` 的 `promotion` 欄位與 `destinations.json`，
  這兩個產物本 fork 都沒有，改寫成寫回 `verified.md`。
- **不引用**：extractors 的檢索式取塊（依賴本 fork 沒有的 `scripts/build_index.py`）、
  website MVP 與其衍生六筆（本 fork 不維護官網）、PR #27 的第三方 skill 索引
  （本 fork README 是繁中主檔 + 英文鏡像，已刪 ja／zh-CN）。

PR 水位 26 → 27。issue 水位維持 20——實查上游 issue 在 #20 以上為 0 筆，是查過為空不是沒查。
