# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 現況段的數字是 2026-10-29 依 `main` `61ee6a401ef7` 查的快照，開工前先重查 GitHub。

## 現況

本 repo 是從書、影片與播客蒸餾 Agent Skills 的 Markdown 產品維護線，沒有獨立 CLI（`AGENTS.md:7-8,27-32`）。2026-10-29 快照 open PR、安全告警均為 0，CI、CodeQL、Dependency freshness、Upstream check 最近結果為 success；issue 因停用而未查到，star-history 的 skipped 是既定閘門（2026-10-29 `gh` 查詢，`61ee6a401ef7`；`docs/DECISIONS.md:43-49`）。工具深掃修復已落地，但完整真實來源蒸餾仍無驗收聲明（`52aa4af`；`REVIEW.md:91-96`）。

## 近期：可以直接動手

| 項目 | 為什麼 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 用一份可合法使用的短來源驗證蒸餾流程 | 靜態 gate 沒有驗證預篩、產出與執行品質的完整鏈路 | 維護者選定來源及宿主；只跑一份，核對預篩、PIPELINE_STATE、產出 skill 與 execution_check；保留去識別結果及 SHA，來源與 `books/` 不提交 | 維護者 | `REVIEW.md:93-96`；`AGENTS.md:19,36`；`docs/DECISIONS.md:87-97` |
| 補本 fork 工具修正的中英變更紀錄 | 現有紀錄尚未反映驗證器與維護工具的修正 | 逐項對照 `a378dd0`、`de913c6`、`fe95337`、`a993f5b`、`52aa4af`，中英紀錄描述一致並通過連結檢查；不抄上游產品歷史 | Claude Haiku | 深掃報告（2026-10-26）〈刻意不修〉；`CHANGELOG.md:14`；`AGENTS.md:94-95` |

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
| 啟用 star-history 自動推送或因 skipped 修 workflow | repo 閘門刻意限制在上游，見 `docs/DECISIONS.md:43-49` | 維護者明確要求維護自己的星圖 |
| 整包引入 Hermes bundle、翻譯產品規格或增加第三語系入口 | 宿主、產品語言與維護入口均有既定邊界，見 `docs/DECISIONS.md:3-8`、`AGENTS.md:17-18` | 有可驗證的宿主支援需求且維護者修改相關政策 |

## 維護方式

每週按 `tools/upstream_baseline.json` 水位及已審 head 做增量巡檢；沒有共同祖先不需修歷史，Upstream check 提醒先視為待審項目。
每月查 Dependency freshness 與 `gh pr list --repo SanHsien/cangjie-skill`；不為更新版本號提高下限、不另造 fork release，其他文件只連結本路線圖。
