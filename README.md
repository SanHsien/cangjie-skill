<div align="center">

# Cangjie Skill

### 把書、長影片、播客裡的方法論，蒸餾成可呼叫的 AI Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Method: RIA--TV++](https://img.shields.io/badge/Method-RIA--TV++-2ea44f.svg)](./SKILL.md)
[![Platform: OpenClaw](https://img.shields.io/badge/Platform-OpenClaw-1677ff.svg)](https://github.com/openclaw/openclaw)
[![Platform: Claude Code](https://img.shields.io/badge/Platform-Claude%20Code-f97316.svg)](https://code.claude.com/)
[![Platform: Codex](https://img.shields.io/badge/Platform-Codex-10a37f.svg)](https://developers.openai.com/codex/skills)
[![Platform: DeepSeek Harness](https://img.shields.io/badge/Platform-DeepSeek%20Harness-4f46e5.svg)](#deepseek-harness-外掛)
[![CI](https://github.com/SanHsien/cangjie-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/SanHsien/cangjie-skill/actions/workflows/ci.yml)

<p>
  <a href="README.md"><strong>繁體中文</strong></a> ·
  <a href="README.en.md">English</a>
</p>

**讀完、看完、聽完之後，帶走一套能呼叫的方法論。**

</div>

> **這是 [`kangarooking/cangjie-skill`](https://github.com/kangarooking/cangjie-skill) 的 Windows-first 維護型 fork**，沿用 MIT 與完整 Git 歷史。產品 Skill、方法論與模板跟隨上游；本維護線補上繁中入口、Windows 開發／驗收 gate，以及逐筆審查的上游追蹤。差異見 [`FORK.md`](FORK.md)，同步策略見 [`docs/UPSTREAM.md`](docs/UPSTREAM.md)，風險快照見 [`REVIEW.md`](REVIEW.md)。

## DeepSeek Harness 外掛

cangjie-skill 同時提供獨立的 DeepSeek Harness 外掛安裝包。適配層封裝在 Release 安裝包中，不會向本倉庫加入特定平臺的包裝文件。

已安裝 DeepSeek Harness 後，運行：

```bash
mkdir -p ~/.dsh/packages
curl -fL "https://github.com/kangarooking/cangjie-skill/releases/download/v2.0.0/dsh-cangjie-skill-2.0.0.tgz" \
  -o ~/.dsh/packages/dsh-cangjie-skill-2.0.0.tgz
dsh plugin --profile web add ~/.dsh/packages/dsh-cangjie-skill-2.0.0.tgz
dsh web
```

[下載 DeepSeek Harness 外掛（適配倉頡 Skill v2.0.0）](https://github.com/kangarooking/cangjie-skill/releases/download/v2.0.0/dsh-cangjie-skill-2.0.0.tgz)

啟動新任務後，可以直接說：

```text
請用 cangjie-skill 把這本書蒸餾成一組可執行的 Agent Skills：<檔案路徑>
```

外掛安裝包仍從上游 Release 下載；本 fork 不代發、不重打包。

## 安裝 Skill（本機呼叫）

把這些**產品檔**一起放到 Agent Skills 目錄。根目錄其餘檔案是本 fork 的開發與治理骨架，不要一起複製進去。

| 宿主 | 建議路徑 |
| --- | --- |
| Codex | `~\.agents\skills\cangjie-skill\` |
| Claude Code | `~\.claude\skills\cangjie-skill\` |
| Cursor | `~\.cursor\skills\cangjie-skill\` |
| OpenClaw | 依其 skills 目錄慣例，放入同一組檔案 |

需要複製的檔案：

- `SKILL.md`
- `methodology/`
- `extractors/`
- `templates/`
- `agents/openai.yaml`

然後直接說：「用 cangjie-skill 把這份內容蒸餾成可執行的 Agent Skills：`<檔案路徑>`」。

開發與驗收指令見 [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md)。維護者 clone：

```powershell
git clone https://github.com/SanHsien/cangjie-skill.git
cd cangjie-skill
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
pwsh -NoProfile -File tools\dev_check.ps1
```

## 為什麼做這件事

最近有一個很火的 idea：把同事蒸餾成 skill。即便一個人離職了，他的經驗、語氣、工作方式都會被 AI 一定程度替代。[nuwa-skill](https://github.com/alchaincyf/nuwa-skill) 就是做這件事的——創造"人類 skill"，比如馬斯克 skill、巴菲特 skill。配套的 [darwin-skill](https://github.com/alchaincyf/darwin-skill) 負責讓這些 skill 自動進化。

蒸餾人很有價值——nuwa-skill 已經證明了這一點。而蒸餾人**系統性表達過的內容**，則是另一個維度的補充：一本書、一場長訪談、一期播客、一個 B 站或 YouTube 長影片，都可能沉澱了作者花很長時間打磨出來的方法論。比起模仿一個人的表達方式，把他系統性輸出的方法論拆出來、變成可以幫人解決實際問題的工具，同樣是很有價值的事。

而且還有一個真實的痛點：你可能看了很多書、收藏了很多影片、聽過很多播客，但就是運用不起來。尤其是各大平臺每天都有大量乾貨長影片，時效性很強，內容又很長；它們往往不可能已經被 AI 訓練過，也很難靠一次觀看完整吸收。把這些內容蒸餾成 skill 之後，AI agent 可以幫你在真實場景中呼叫這些知識，而不是讓它們躺在筆記、收藏夾或稍後再看列表裡落灰。

所以 cangjie-skill 的目標很明確：**蒸餾所有值得蒸餾的高價值內容**。它不只適用於書，也適用於有字幕/轉寫文本的影片、播客、訪談、演講、課程、長文和資料集。只要內容裡存在可抽取、可驗證、可遷移的方法論，就可以用 cangjie-skill 把它變成一套可獨立調用、可組合使用、可壓力測試的 AI skill 工具包。

蒸餾影片或播客時，先自行取得字幕或轉寫文本，再交給 cangjie-skill 做方法論抽取、skill 化與壓力測試。

## 它解決了什麼問題

- 看了很多書、影片、播客但用不起來——知識停留在"看過/聽過/收藏過"層面，無法在真實決策中被呼叫
- 摘要、筆記、字幕整理只是壓縮，不是結構化復用——讀完/看完還是不知道"什麼時候該用什麼"
- 高價值內容裡真正值得變成工具的內容只有一小部分——需要嚴格的篩選而不是照單全收
- 現有的閱讀/觀看/聽課方法論都是給人看的，不是給 agent 用的——需要面向執行而非面向消費的蒸餾方法

## 它是怎麼工作的

cangjie-skill 使用 **RIA-TV++** 流水線，把書籍、影片轉寫、播客文字稿、訪談記錄等原始文本變成一組結構化的 skill。開工前先做適配預篩，再進入七個階段：

0. **適配預篩**——預設先做五維評分（方法論密度／可執行性／遷移性／證據／邊界）、複用檢查與成本預期，產出 `BOOK_FIT.md`。使用者可明示略過；小說、史料等內容預設改走替代產物，不硬拆完整 skill pack
1. **整體內容理解（Adler 分析）**——借鑑 Mortimer Adler 的分析閱讀法，對整份內容做結構、解釋、批判、應用四步拆解，產出 `BOOK_OVERVIEW.md`
2. **分批並行提取**——依宿主實際可用容量派 5 個專項提取器（框架、原則、案例、反例、術語）；容量不足時縮小批次或改串行
3. **三重驗證篩選**——每個候選必須通過三項檢驗：跨域佐證（短內容可用內容內 1 處 + 外部可佐證）、能回答內容裡未明說的新問題（預測力）、不是常識（獨特性）。高風險或高信心需求可啟用雙評審與仲裁；一般情況採單一結構化評審並留下模式紀錄。通過率通常只有 25-50%
4. **RIA++ 構造**——將驗證通過的內容按 R（原文引用）/ I（用自己的話重寫）/ A1（書中案例）/ A2（未來觸發場景）/ E（可執行步驟）/ B（邊界與盲點）六個維度結構化
5. **Zettelkasten 連結**——找出 skill 之間的依賴、對比、組合關係，並把實際用到的術語回填進單個 skill，生成 `INDEX.md` 和引用圖
6. **壓力測試**——為每個 skill 設計包含誘餌題、跨 skill 混淆、執行品質檢查與對抗題的測試；未通過的回爐重做
7. **交付**——生成 `DIGEST.md` 精華長文；完整包、比較實驗或使用者要求時另產生 `SCORECARD.md` 品質記分卡。把通過測試的 skill 安裝到 Codex / Claude Code / Cursor 的 skills 目錄時，只裝當前任務需要的子集

RIA-TV++ 這個名字拆開看：
- **RIA**：來自趙周《這樣讀書就夠了》的便籤拆書法（Reading / Interpretation / Appropriation）
- **TV**：Triple Verification，三重驗證
- **++**：面向 agent 執行的擴展——E（Execution 可執行步驟）+ B（Boundary 邊界）

## 效果示例

### 示例 1：從一本書/長影片到一套 skill 工具包

**使用者需求**

"我想把一本書或一個 B 站/YouTube 長影片裡的核心方法論抽成可復用的 AI skills，而不是只做摘要。"

**cangjie-skill 如何判斷**

- 先看源材料是否存在可重複調用的方法論單元
- 再區分哪些內容適合做獨立 skill，哪些只適合做候選或背景
- 最後輸出結構化 skill 倉庫，而不是一篇總結文章

**最終輸出示例**

> 輸出將不是一個單文件摘要，而是一個多 skill 倉庫：包含 `BOOK_OVERVIEW.md` 作為全局理解，`INDEX.md` 作為技能地圖，`DIGEST.md` 作為面向讀者的精華長文，`GLOSSARY.md` 作為術語詞典，若干 `*/SKILL.md` 作為獨立模塊，以及 `test-prompts.json` 用於驗證觸發場景。

### 示例 2：不是壓縮，是結構化復用

**使用者需求**

"我不希望這份內容只變成一個很長的說明文，我想要可以在 agent 裡復用的技能包。"

**cangjie-skill 如何判斷**

- 判斷目標不是內容總結，而是結構化復用
- 優先生成可觸發、可組合、可測試的 skill 單元
- 對沒有獨立價值的內容進行淘汰，不強行保留

**最終輸出示例**

> 系統會把內容拆成多個帶觸發條件、適用邊界、使用方式和關聯關係的 skills，而不是把整份內容壓縮成一篇泛化總結。

## 公開示例（上游與社群）

下列倉庫是**已經蒸餾完成的公開示例**，方便對照「長內容 → 可呼叫 skill 包」長什麼樣。它們由上游作者或社群維護，**不是本 fork 的發行物**；本倉庫只連過去，不複製那些 skill 包。

### 已生成的 skill packs

| 倉庫 | 來源 | Skills 數 |
|------|------|-----------|
| [buffett-letters-skill](https://github.com/kangarooking/buffett-letters-skill) | 巴菲特致股東的信（1957-2023） | 20 |
| [cognitive-dividend-skill](https://github.com/kangarooking/cognitive-dividend-skill) | 《認知紅利》 | 15 |
| [duan-yongping-skill](https://github.com/kangarooking/duan-yongping-skill) | 段永平投資問答錄（商業邏輯+投資邏輯） | 15 |
| [viral-copywriting-skill](https://github.com/kangarooking/viral-copywriting-skill) | 《爆款文案》 | 14 |
| [copywriters-handbook-skill](https://github.com/kangarooking/copywriters-handbook-skill) | 《文案創作完全手冊》 | 12 |
| [contagious-skill](https://github.com/kangarooking/contagious-skill) | 《瘋傳》 | 15 |
| [influence-skill](https://github.com/kangarooking/influence-skill) | 《影響力》 | 12 |
| [1000-true-fans-skill](https://github.com/kangarooking/1000-true-fans-skill) | 《1000個鐵粉》 | 13 |
| [system-prompt-skills](https://github.com/kangarooking/system-prompt-skills) | 165 個 AI 產品系統提示詞 | 15 |
| [X-growth-skills](https://github.com/kangarooking/X-growth-skills) | X（Twitter）起號、內容增長、演算法、互動與變現實戰資料集 | 15 |
| [poor-charlies-almanack-skill](https://github.com/kangarooking/poor-charlies-almanack-skill) | 《窮查理寶典》 | 12 |
| [no-rules-rules-skill](https://github.com/kangarooking/no-rules-rules-skill) | 《不拘一格：網飛的自由與責任工作法》 | 10 |
| [huangdi-neijing-skill](https://github.com/kangarooking/huangdi-neijing-skill) | 《黃帝內經》（素問+靈樞） | 22 |
| [first-principles-skill](https://github.com/kangarooking/first-principles-skill) | 《第一性原理》 | 10 |
| [mao-selected-works-skill](https://github.com/kangarooking/mao-selected-works-skill) | 《毛澤東選集》第 1-5 卷 | 25 |
| [qbdx-hub/buffett-letters-skill](https://github.com/qbdx-hub/buffett-letters-skill) | 沃倫·巴菲特 1957-2023 年致股東信 | 20 |
| [qbdx-hub/wo-yu-di-tan-skill](https://github.com/qbdx-hub/wo-yu-di-tan-skill) | 史鐵生《我與地壇》 | 6 |
| [qbdx-hub/mingchao-those-things-skill](https://github.com/qbdx-hub/mingchao-those-things-skill) | 當年明月《明朝那些事兒》 | 7 |
| [qbdx-hub/sunzi-bingfa-skill](https://github.com/qbdx-hub/sunzi-bingfa-skill) | 《孫子兵法》 | 8 |
| [qbdx-hub/zhouyi-skill](https://github.com/qbdx-hub/zhouyi-skill) | 《周易》 | 8 |
| [qbdx-hub/high-math-vol1-ch1-skill](https://github.com/qbdx-hub/high-math-vol1-ch1-skill) | 高等數學上冊第一章 | 8 |

### 影片蒸餾區

這些倉庫來自長影片、課程或影片合集的字幕／轉寫，用來示範非書籍內容也能走同一條流水線。

| 倉庫 | 來源 | Skills 數 |
|------|------|-----------|
| [ai-for-everyone-skill](https://github.com/kangarooking/ai-for-everyone-skill) | 吳恩達《AI for Everyone / 給所有人的 AI 入門課》影片課程 | 25 |
| [loop-engineering-skill](https://github.com/kangarooking/loop-engineering-skill) | Loop Engineering 長影片合集 | 8 |

### 補充外部來源

上游 README 註明下列倉庫是經對方作者同意後引入的外部示例：

- [ace3000chao/book2startup](https://github.com/ace3000chao/book2startup)：《精益創業》《孫子兵法》《莊子》《易經》
- [shenqistart/book2skill](https://github.com/shenqistart/book2skill)：《纏論》《茶經》

## 倉庫結構

```text
cangjie-skill/
├── README.md              ← 繁中公開入口（本 fork）
├── README.en.md           ← English version
├── LICENSE                ← MIT
├── SKILL.md               ← 元 skill 定義（產品規格，不要改寫成維護索引）
├── agents/openai.yaml     ← Codex UI 元資料
├── methodology/           ← RIA-TV++ 各階段的方法論文檔
├── extractors/            ← 5 個並行提取器的 prompt 定義
├── templates/             ← SKILL.md / INDEX.md / BOOK_OVERVIEW.md / BOOK_FIT.md 模板
├── AGENTS.md / FORK.md    ← 本 fork 維護規則
├── docs/                  ← 開發、上游審查、決策
└── tools/                 ← Windows gate 與上游檢查
```

## 生態

這是上游 README 記載的相關專案定位，方便讀者知道 cangjie-skill 在整條 skill 生態裡做哪一段。nuwa / darwin 由原作者以外的專案維護，**不是本 fork 的產品線**。

- [nuwa-skill](https://github.com/alchaincyf/nuwa-skill) — 蒸餾人（思維方式、表達 DNA）
- **cangjie-skill**（本 skill）— 蒸餾書（方法論、框架、原則）
- [darwin-skill](https://github.com/alchaincyf/darwin-skill) — 進化任意 skill

三者咬合：nuwa 蒸餾人，cangjie 蒸餾書，darwin 讓它們持續進化。

## More Skills

上游與社群把已蒸餾的示例寫成可直接開的倉庫。下列與上方表格是同一批公開示例，這裡多一句用途說明。**不是本 fork 的發行物。**

- [Buffett Letters Skill](https://github.com/kangarooking/buffett-letters-skill) — 巴菲特 60+ 年致股東信的 20 個投資判斷 skill
- [Poor Charlie's Almanack Skill](https://github.com/kangarooking/poor-charlies-almanack-skill) — 查理·芒格核心思維方法的 12 個決策與判斷 skill
- [No Rules Rules Skill](https://github.com/kangarooking/no-rules-rules-skill) — 網飛自由與責任文化的 10 個組織設計 skill
- [Cognitive Dividend Skill](https://github.com/kangarooking/cognitive-dividend-skill) — 《認知紅利》思維升級的 15 個認知工具 skill
- [Duan Yongping Skill](https://github.com/kangarooking/duan-yongping-skill) — 段永平投資問答錄的 15 個商業與投資 skill
- [Viral Copywriting Skill](https://github.com/kangarooking/viral-copywriting-skill) — 《爆款文案》的 14 個銷售型文案寫作與診斷 skill
- [Copywriters Handbook Skill](https://github.com/kangarooking/copywriters-handbook-skill) — 《文案創作完全手冊》的 12 個銷售型文案、標題與賣點轉化 skill
- [Contagious Skill](https://github.com/kangarooking/contagious-skill) — 《瘋傳》的 15 個 STEPPS 傳播策略與口碑診斷 skill
- [Influence Skill](https://github.com/kangarooking/influence-skill) — 《影響力》的 12 個說服心理、順從機制與防禦判斷 skill
- [1000 True Fans Skill](https://github.com/kangarooking/1000-true-fans-skill) — 《1000個鐵粉》的 13 個個人品牌、鐵粉養成與信任變現 skill
- [System Prompt Skills](https://github.com/kangarooking/system-prompt-skills) — 從 165 個 AI 產品系統提示詞蒸餾出的 15 個 system prompt 設計 skill
- [X Growth Skills](https://github.com/kangarooking/X-growth-skills) — X 起號、內容、演算法、互動、復盤與變現的 15 個運營 skill
- [Huangdi Neijing Skill](https://github.com/kangarooking/huangdi-neijing-skill) — 《黃帝內經》素問 12 + 靈樞 10，共 22 個思維方法 skill
- [First Principles Skill](https://github.com/kangarooking/first-principles-skill) — 《第一性原理》的 10 個認知拆解、破界創新與組織刷新 skill
- [Mao Selected Works Skill](https://github.com/kangarooking/mao-selected-works-skill) — 《毛澤東選集》第 1-5 卷的 25 個認知、戰略、組織與執行方法 skill
- [qbdx-hub Buffett Letters Skill](https://github.com/qbdx-hub/buffett-letters-skill) — 沃倫·巴菲特 1957-2023 年致股東信的 20 個投資與資本配置 skill
- [qbdx-hub Wo Yu Di Tan Skill](https://github.com/qbdx-hub/wo-yu-di-tan-skill) — 《我與地壇》的 6 個限制、苦難、寫作與自我安放 skill
- [qbdx-hub Mingchao Those Things Skill](https://github.com/qbdx-hub/mingchao-those-things-skill) — 《明朝那些事兒》的 7 個權力結構、制度失靈與歷史表達 skill
- [qbdx-hub Sunzi Bingfa Skill](https://github.com/qbdx-hub/sunzi-bingfa-skill) — 《孫子兵法》的 8 個戰略判斷、資源控制與行動選擇 skill
- [qbdx-hub Zhouyi Skill](https://github.com/qbdx-hub/zhouyi-skill) — 《周易》的 8 個處境診斷、時位判斷與進退邊界 skill
- [qbdx-hub High Math Vol. 1 Chapter 1 Skill](https://github.com/qbdx-hub/high-math-vol1-ch1-skill) — 高等數學上冊第一章的 8 個極限、無窮小與連續性學習 skill
- [book2startup](https://github.com/ace3000chao/book2startup) — 經作者同意引入的外部來源，包含《精益創業》《孫子兵法》《莊子》《易經》相關 skills
- [book2skill](https://github.com/shenqistart/book2skill) — 經作者同意引入的外部來源，包含《纏論》《茶經》相關 AI-Agent skills

## 來源與授權

本倉庫 fork 自 [`kangarooking/cangjie-skill`](https://github.com/kangarooking/cangjie-skill)，現行授權為 MIT（上游 2026-08 從 AGPL 改來；本線 overlay 同步以 MIT 發佈）。產品 `SKILL.md`、方法論、提取器與模板為上游原作。完整標示見 [`LICENSE`](LICENSE) 與 [`NOTICE`](NOTICE.md)。

本 fork 的維護變更記在 [`CHANGELOG.md`](CHANGELOG.md)；與上游的關係與差異見 [`FORK.md`](FORK.md)。
