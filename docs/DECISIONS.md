# 維護決策

## 2026-08-22：建立 Windows-first 維護型 fork

**決定**：fork `kangarooking/cangjie-skill`，保留 GNU AGPL v3.0 與完整歷史，預設分支維持 `main` 以降低與上游同步摩擦。本線聚焦繁中公開入口、Windows 開發 gate、Windows CI，以及逐筆審查的上游追蹤。

**理由**：上游 RIA-TV++ 方法論、提取器與模板已經可在 Claude Code / Cursor / OpenClaw 使用，符合維護者把長影音與書籍提煉成可呼叫技能的需求。缺的是 Windows 11 上可重現的開發／驗收骨架，以及繁中入口。直接用上游 repo 難以長期記錄 fork 取捨。授權是 AGPL，fork 修改同樣走 AGPL，不改成更寬的授權。

**限制**：

- 不把 fork 包裝成原創專案，不移除原作者與授權標示。
- `SKILL.md` 保持產品規格，不用維護索引覆寫。
- 不把產品方法論翻譯成繁體；產品語言跟隨上游。
- 上游更新必須逐筆審查。
- 不回貢，除非維護者在當次對話明確同意。

**後續狀態**：2026-08-28 授權改 MIT（見該節）。繁中入口、不宣傳、不回貢的限制仍有效。

## 2026-08-22：維護線直接推 main

**決定**：fork 維護不再開功能分支。改完在本機跑 gate，通過後直接推 `origin/main`。遠端只留 `main`；`upstream/main` 只追蹤。

**理由**：這是單人維護 fork，分支與 PR 沒有第二審查者，只增加同步成本。

**限制**：
- Dependabot 與外部 fork 仍可能開 PR，讀 diff 後再合併，不自動合併。
- 不推 `upstream`，不 force-push `main`。
- 不刪 `upstream` remote。

## 2026-08-22：不啟用 Dependabot 自動合併

**決定**：Dependabot 只開 PR；CI 與人工讀 diff 通過後才合併。

**理由**：開發依賴只有 pytest / ruff，體積小，但自動合併仍會跳過「讀 diff」這一步。

## 2026-08-22：star-history workflow 加 repo 閘門

**決定**：`.github/workflows/update-star-history.yml` 加上 `if: github.repository == 'kangarooking/cangjie-skill'`。本 fork 不設定 `STAR_HISTORY_TOKEN`，不推星圖。

**理由**：該 workflow 需要 write permission 與上游 secret。fork 上每天排程失敗是噪音，不是功能。星圖仍保留上游產生的 `assets/star-history.svg` 作為 README 插圖。

**限制**：上游若重寫這個 workflow，merge 時要保留閘門。README 不嵌入星圖。

## 2026-08-22：選擇性引用尚未合併的產品 PR（第一輪已落地）

**決定**：採用 #24、#5、#15 正文強化（不含 `trigger_words` frontmatter）。產品內容在目前 `origin/main`（2026-08-23 `6bef9fd` 壓縮歷史後，舊內部 SHA 已不在祖先鏈）。

**理由**：
- 維護者常用 Codex；#24 是相容性修正。frontmatter 只留 `name`+`description`。
- #5 是防禦性邊界，改動小。
- #15 提高 darwin 基線；額外 YAML 欄位會破壞 #24 契約。

**限制**：上游若合併這些 PR，merge 時做三方對照，不要覆蓋繁中 README 與 Windows gate。

## 2026-08-23：嚴格重評其餘 open PR（歷史評估；後續落地見下節）

**決定**：重讀 #22 / #25 / #10 / #4 的 diff 後，**撤銷**先前「#22/#4/#10/#25 一律不引＋等上游定案」的粗糙結案。改為：

| 項目 | 決定 |
| --- | --- |
| #22 | **建議部分採用**（三坑 + 可蒸性三問 + 成本表；複用檢查改寫；必做改可跳過） |
| #10 | **建議部分採用**（短內容 V1、`execution_check`、對抗出題、可選 SCORECARD；剔除 session 檔與 `related_skills` frontmatter；雙評審非強制） |
| #4 | **不整支**；`alternate_artifact` 概念併入 #22 子集 |
| #25 | **暫不引檔**；標成可選低風險（有蒸 X 需求再加） |
| 官網／DeepSeek release 分支 | **不引**（站點線／已進 #23） |

**理由（對照 diff，不是空話）**：
- #22 直接省長流程 token／時間；與 #24 無契約衝突。
- #10 的短內容 V1 與 `execution_check` 補影片／播客與「觸發後執行」缺口；session 檔與 frontmatter `related_skills` 則會污染本 fork 並打臉 #24。
- #4 與 #22 雙門檻重複，且 evaluation 含私有絕對路徑。
- #25 適配器可選且低風險，但目前無 X 蒸餾使用證據，不加檔避免空目錄契約。

**限制／接手**：
- 本輪**只更新評估文件**，不改 `SKILL.md`／methodology／templates。
- 產品子集落地交給 Codex（或後續 session）；當時清單現已更新為 `docs/UPSTREAM.md`「Codex 接手結果」。
- 落地後必須跑 Windows gate，並更新 UPSTREAM 狀態列與本檔。

**後續狀態**：2026-08-23 已完成選擇性落地（內容在目前 tree）；下節記錄最終取捨，取代「待 Codex」狀態。

## 2026-08-23：落地 #22／#10 子集，部分採用 #4／issue #20

**決定**：落地適配預篩、短內容驗證、執行品質測試、對抗出題、術語回填與可選記分卡。這不是整支合併任何 open PR，而是保留既有 Codex/frontmatter/Windows 契約的最小重做。產品內容在目前 `origin/main`。

**最終取捨**：

- #22 的預篩、複用檢查、成本提示與三坑採用；#4 只取五維評分、四類產物判斷與 `BOOK_FIT.md` 模板。預篩預設執行，但使用者可明示跳過並在 `PIPELINE_STATE.md` 留下理由。
- #10 採短內容 V1、`execution_check`、對抗題、術語回填與 SCORECARD 模板；雙評審只用於高風險／高信心需求，一般任務做一次結構化評審並標 `fallback_single_agent`。SCORECARD 只在完整包、比較、審計或使用者要求時生成。
- #20 不引 Hermes 專用 progressive-skill；只採跨宿主成立的安裝節制：不要把整包 skill 無差別裝進所有會話，只安裝當前任務所需子集。
- #25 仍無實際 X 蒸餾需求證據，維持 defer；未提交 `source-adapters/x-twitter.md` 或 `X_SOURCE_CORPUS.md.template`。
- #14 要求的基本使用路徑已由 README 的安裝、直接呼叫 prompt、效果示例與公開範例覆蓋；影片屬外部媒體產物，本 fork 不為形式新增或託管。

**驗證**：主工作樹與 detached 隔離候選均通過 Windows gate：20 tests、Ruff E9/F、`validate_skill.py` 與相對連結檢查全綠。

**限制**：未來只有 open PR head SHA 改變、出現新 issue/PR，或本 fork 出現實際 X 來源需求時才重開相應評估；相同 head 不重讀相同 diff。

## 2026-08-27：略過上游四筆；當時維持 AGPL；不回貢

**決定**：`3a8c23a..upstream/main` 的四筆全部**略過**，`reviewed_through` 推進到 `5f03a4cd8b521673f7a67ca6279330ec943bb369`。本線 `LICENSE` 與 `NOTICE.md` 維持 GNU AGPL v3.0。本輪不開上游 PR。

| Commit | 結論 |
| --- | --- |
| `7e0d58a92060a838fa10d319e7232e163e79506f` | 只換企微 QR 圖。宣傳資產，略過。 |
| `a47a604b3940eda9bb0c83a276626ffa0c87d7e5` | 三語 README 加日文切換。本線不收第三語系，略過。 |
| `f751bf9ff9f833cff702fe48d31ebd9d407d4b05` | `LICENSE` AGPL→MIT；根 README 改英文預設。2026-08-27 整筆略過。2026-08-28 只跟授權（見下節）。 |
| `5f03a4cd8b521673f7a67ca6279330ec943bb369` | 英文 README 補 DeepSeek／影片表／示例，也帶官網／QR／作者段。宣傳略過；示例表本線 README 已有。 |

**理由**：作者可對上游之後的工作改 MIT；本線已宣告的 AGPL 修改與 `NOTICE.md` 不能自動跟著改。繁中仍是公開主入口。QR、官網、作者段與 `README.ja.md` 本來就在禁止轉載清單裡。

**同時修的 fork-local findings**（見 `REVIEW.md`）：清掉壓縮歷史後失效的內部 SHA、gitignore 補電子書／cookie／credentials、star-history checkout 改 SHA pin、`FORK.md` 補產品修正清單。

**觸發條件**：上游若把 MIT 變更寫進 `SKILL.md`／方法論（而不只是 README／LICENSE），或示例表出現本線沒有的新公開倉庫，再讀那些檔。Open PR head 未變則不重評。

**後續狀態**：2026-08-28 維護者決定跟授權（見下節）。QR／日文／英文預設 README／宣傳仍略過。

## 2026-08-28：跟上游改 MIT；不跟入口重組

**決定**：本線 `LICENSE` 與 overlay（`NOTICE.md`、公開入口 badge、本線自己寫的維護檔）改以 MIT 發佈，對齊上游 `f751bf9` 的授權變更。**不**把該 commit 其餘部分合進來：根 README 仍是繁中主入口，不收 `README.ja.md`／`README.zh-CN.md`，不嵌入官網／QR／作者宣傳。

**理由**：上游作者已對原作改發 MIT；本線 overlay 的著作權在維護者，可以同步放寬。維護型 fork 與上游同授權，使用者不會看到「上游 MIT、fork 卻 AGPL」。授權不能跟宣傳包在同一筆 merge 裡自動進來，所以只跟 LICENSE 這一件。

**限制**：
- 2026-08-28 之前從本 fork 拿到的副本，仍受當時 AGPL-3.0 授權約束。
- 不 cherry-pick `f751bf9` 整支。
- Git 歷史裡的舊 AGPL `LICENSE` 仍在；現行 tree 以根目錄 `LICENSE` 為準。

## 2026-08-22：公開文件只留繁中與英文；README 只留 credit

**決定**：刪除 `README.ja.md`。GitHub About 與公開入口只用繁體中文與英文。README 不轉載作者個人頁、社群、QR、官網、星圖。來源與授權 credit 留在 README 短段與 `NOTICE.md`。

**理由**：這是維護型 fork，不是原作者的宣傳頁。相關 credit 放 README 短段與 `NOTICE.md` 即可滿足 AGPL 標示。

**限制**：上游若把 `README.ja.md` 或宣傳段落一併推進來，merge 後刪掉／不要合進公開入口。

## 2026-08-22：公開示例可列，但要標成上游／社群參考

**決定**：把上游 README 的「已生成的 skill packs」「影片蒸餾區」「補充外部來源」「生態」「More Skills」收進本 fork README，作為讀者對照樣本。每段寫明：那些倉庫由上游或社群維護，本 fork 只連過去、不複製 skill 包。生態裡的 nuwa / darwin 標成相關專案，不是本 fork 產品線。

**理由**：只做公開 GitHub 連結，不轉載書籍或 skill 全文。外部來源上游已註明經對方同意。表格給總覽，More Skills 給一句用途；生態說明這條流水線在 nuwa / darwin 之間做哪一段。這與「不要作者廣告」不衝突——不放個人頁、社群、QR、官網、星圖。

**限制**：同步上游時只更新示例表，不要連作者宣傳一起進來。不要把這些示例說成本 fork 的發行物。
