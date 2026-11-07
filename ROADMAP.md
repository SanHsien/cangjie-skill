# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 現況段的數字是 2026-11-08 依 `main` `d31b07b` 查的快照，開工前先重查 GitHub。

## 現況

本 repo 是從書、影片與播客蒸餾 Agent Skills 的 Markdown 產品維護線，沒有獨立 CLI（`AGENTS.md:7-8,27-32`）。2026-11-08 `gh` 查詢：`d31b07b` 的 CI、CodeQL 為 success，open PR 0 筆，code scanning 開啟告警 0 筆；issue 因停用而未查到，star-history 的 skipped 是既定閘門（`docs/DECISIONS.md:59-63`）。工具深掃修復與中英變更紀錄已落地，但完整真實來源蒸餾仍無驗收聲明（`52aa4af`；`REVIEW.md:91-96`）。

## 近期：可以直接動手

| 項目 | 為什麼 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 用 Lionel Giles 1910 英譯《孫子兵法》第一章「Laying Plans」跑一次完整蒸餾 | 預篩與產出品質只有真實來源能驗；靜態 gate 不經過這條鏈路 | 1. 來源：Project Gutenberg eBook #132 `pg132.txt` 的 Chapter I（約 8.7 KB，公版），抽出後 SHA-256 為 `75513ca81a1743bb3f7320ce7da11adee44687e419c325a794abbc540e9f12f5`。2. 方法：在暫存目錄執行 `codex exec -s workspace-write --skip-git-repo-check -C <暫存目錄>`，提示要求先讀本 repo 的 `SKILL.md` 與 `methodology/`，只跑這一份，slug `art-of-war-ch1`，輸出只寫暫存目錄的 `books/`，不得改本 repo。3. 核對預篩結果、`PIPELINE_STATE.md`、產出 skill 與每個 skill 的 `execution_check`；單一評審降級須在 `PIPELINE_STATE.md` 如實標註。4. 把去識別結果與來源 SHA-256 寫進 `REVIEW.md`「尚未宣稱範圍」，改成已驗證範圍；來源與 `books/` 不提交 | Codex | `REVIEW.md:93-96`；`AGENTS.md:19,36`；`docs/DECISIONS.md` 2026-11-08 段 |

## 中期：等條件成立再做

| 項目 | 觸發條件 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 增量審查上游 | commit／PR／issue 超過 baseline，或已審 PR／分支 head 改變 | 依 `docs/UPSTREAM.md` 對照本 fork 實際檔案，記錄採用／略過及重審條件；Windows gate 通過才前移水位 | Codex | `tools/upstream_baseline.json`；`AGENTS.md:50-71` |
| 補驗證器少見 YAML／巢狀 fence 寫法 | 真實安裝來源使用 flow tools、帶註解 block scalar 或巢狀 fence，且可重現誤報 | 先加入該來源最小案例與既有格式對照，無新增誤報；`pwsh -NoProfile -File tools/dev_check.ps1` 通過 | Codex | 深掃報告（2026-10-26）〈刻意不修〉；`tools/validate_skill.py:103,180-193` |
| 重新評估 X 來源適配器 | 出現實際 X 蒸餾需求且取得合法、可用來源 | 先驗來源取得方式與安全邊界，再評估上游 #25 的適用子集；具可重現來源輸入與蒸餾驗收，不留下空介面 | Claude Opus | `docs/DECISIONS.md:71,78,96`；上游 #25 |

## 刻意不做

| 不做什麼 | 理由 | 什麼情況下重新考慮 |
| --- | --- | --- |
| 重發 DeepSeek Harness 安裝包或在本 fork 經營官網／registry | 維護邊界與既有決策見 `AGENTS.md:21-22`、`docs/DECISIONS.md` 的上游審查 | 維護者提出獨立產品需求，先定義來源、授權與 Windows 驗收 |
| 啟用 star-history 自動推送或因 skipped 修 workflow | repo 閘門刻意限制在上游，見 `docs/DECISIONS.md:59-63` | 維護者明確要求維護自己的星圖 |
| 整包引入 Hermes bundle、翻譯產品規格或增加第三語系入口 | 宿主、產品語言與維護入口均有既定邊界，見 `docs/DECISIONS.md:3-8`、`AGENTS.md:17-18` | 有可驗證的宿主支援需求且維護者修改相關政策 |

## 維護方式

每週按 `tools/upstream_baseline.json` 水位及已審 head 做增量巡檢；沒有共同祖先不需修歷史，Upstream check 提醒先視為待審項目。
每月查 Dependency freshness 與 `gh pr list --repo SanHsien/cangjie-skill`；不為更新版本號提高下限、不另造 fork release，其他文件只連結本路線圖。

2026-11-05 已重評 Ruff 0.17.3，更新限版本延後紀錄並保留相容性下限；裁決與重審條件見 `docs/DECISIONS.md` 同日紀錄。
