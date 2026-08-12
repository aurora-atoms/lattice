# 跨生态证据融合：最小人工方案

日期：2026-08-12  
适用范围：Google Drive / Gemini Notebook（原 NotebookLM）、GitHub、Claude Code、Codex，以及任意可输出文本或文件的工作区。

## 结论

当前不需要 CLI、自动 handoff、统一运行时或跨系统调用。采用一个目录、一种贡献模板、两个既有合同即可：

```text
每个系统保留自己的原始内容
-> 每个系统输出一个同格式的 Markdown 贡献文件
-> 人工复制整个 case 目录，或压缩为 zip 搬运
-> 在选定的分析系统中合并为 CASEPACK.md
-> 需要严格机器校验时，再落成既有 DCP + PCP JSON
```

zip 只是运输容器，不是事实来源；`CASEPACK.md` 是任何系统都能读取、复制和引用的通用投影；`lat.domain_context_pack.v1`（DCP）与 `lat.portable_case_pack.v1`（PCP）仍是严格机器合同。没有必要创建第三套事实模型。

## 最小目录

```text
<case-id>/
├── CASEPACK.md                         # 合并后的通用文本投影
├── contributions/                     # 各系统原样交付，一系统一文件
│   ├── google-notebook.md
│   ├── github.md
│   ├── claude-code.md
│   └── codex.md
├── contracts/                         # 严格校验或正式 handoff 时需要
│   ├── domain-context-pack.json
│   └── portable-case-pack.json
└── evidence/                          # 可选；放允许搬运的原件、导出件、日志或截图
```

最小起步只要求 `CASEPACK.md` 和一个 `contributions/<system>.md`。当一个 case 要进入正式决策、跨工作区验证或长期留存时，再补两个 JSON。原始证据不能搬运时，只保留稳定 locator、访问级别、观察时间和内容指纹，不复制内容。

## 每个系统都使用同一个贡献块

每个贡献文件必须包含以下字段；空值写 `UNKNOWN`，不能删除字段：

1. `case_id`、`producer_system`、`producer_role`、`observed_at`、`evidence_cutoff`；
2. `objective`、`scope_in`、`scope_out`；
3. `selected_sources`、`conditional_sources`、`excluded_sources`、`unavailable_or_not_searched`；
4. `claims_observed`、`claims_derived`、`claims_judged`、`claims_unknown`；
5. `evidence_refs`：每条至少有 ID、locator、时间、访问级别、内容指纹或版本；
6. `conflicts`、`strongest_counterevidence`、`source_gaps`；
7. `authority_ceiling`、`required_verification`、`stop_conditions`；
8. `compression_receipt`：检查过什么、不可访问什么、因何省略什么。

这与现有 DCP/PCP 字段一一对应。Markdown 是人工作者界面；JSON 是机器校验界面。复制或格式转换不得把 `UNKNOWN`、未解决冲突或候选主张升级成事实。

## 各生态只承担自己的证据角色

| 生态 | 原生存储 | 固定输出 | 能确认什么 | 不能自行确认什么 |
|---|---|---|---|---|
| Google Drive / Gemini Notebook | 每个 case 一个 Drive 文件夹；来源仍留在 Docs、Sheets、Slides | `google-notebook.md`，必要时附导出的 Docs/Sheets | 文档中实际写了什么、来源间的一致与冲突、业务/历史候选主张 | 代码当前行为、运行时状态、根因、修复就绪 |
| GitHub | Issue、PR、review、commit、Actions；或私有仓库中的 case 目录 | `github.md` | 可寻址的 commit/PR/check/review 状态及时间点事实 | 未检出的本地状态；仅凭讨论文本不能确认运行时根因 |
| Claude Code | 私有本地工作区 | `claude-code.md` | 实际读取的文件、执行的命令、测试/复现结果及其边界 | 未运行的测试、未访问系统、模型间一致意见 |
| Codex | 私有本地工作区或 Work 项目 | `codex.md` | 同上；实际工具结果可作为 observed evidence | 仅凭推理把候选主张升级为 confirmed |

同一主张允许多系统各自记录，但必须共用 `claim_id`。后来的系统增加 evidence ref 或 verification result，不重写前一个系统的历史描述。

## Gemini Notebook：用两次批量产出替代反复聊天

无法直接“导出模型内部理解”；能提取的是基于当前来源的可审计投影。最有效的方式不是不断追问摘要，而是强制它做覆盖清点和主张级账本。

### 第一次：生成自定义 Report

在 Studio 中创建 Custom Report，粘贴 `CASEPACK.template.md` 末尾的“Notebook 主提取提示”。要求一次生成完整 `google-notebook.md`：来源覆盖、核心主张、派生判断、冲突、最强反证、未知项和下一步验证都必须带来源引用。

### 第二次：生成 Data Table

生成一张 Evidence Ledger，列固定为：

```text
claim_id | claim_type | statement | source_name | source_locator_or_citation |
source_date | observed_at | access | confidence | conflict_id |
counterevidence | verification_needed
```

Report 负责保留上下文和结构，Data Table 负责查漏、排序和批量扫描。只在表中发现无引用主张、来源未覆盖、冲突未解释时，才做一次 gap pass；不要继续开放式聊天。

官方帮助说明 Custom Report 可导出到 Google Docs，Data Table 可导出到 Google Sheets；Notes 也可导出到 Docs/Sheets。导出后手工移动到对应 Drive case 文件夹即可。导出件与 Notebook 原内容不会双向同步，因此每次导出都要写 `evidence_cutoff` 和 `observed_at`。

### Notebook 输入边界

- Drive 来源可以自动同步，但失去 Drive 访问权后 Notebook 中也会不可用；长期包必须保留源 locator 和访问状态。
- Google 文件的脚注和评论不会被导入；重要证据必须进入正文或另行导出。
- 网页只导入 HTML 文本，不含图片、嵌入视频或嵌套页面；YouTube 只使用文字稿；这些缺失必须进入 `unavailable_or_not_searched` 或 `compression_receipt`。
- 对大 notebook 先按主题给 sources 打标签并分组选取，再生成分组贡献；最后做一次跨组冲突合并。不要声称“已穷尽全部来源”。

## 人工合并步骤

1. 建立 `<case-id>/`，复制 `CASEPACK.template.md` 为 `CASEPACK.md`。
2. 从各生态拿到一个贡献文件，原样放入 `contributions/`；不要在复制时改写。
3. 在选定的分析系统中同时加载 `CASEPACK.md`、所有贡献文件和允许搬运的 evidence。
4. 按共同 `claim_id` 合并；保留来源、状态、冲突、未知、最强反证和权限边界。
5. 对代码/运行时主张，只接受接收工作区独立读取、复现、测试或配置证据。
6. 输出更新后的 `CASEPACK.md`。需要正式校验时，再填写 DCP/PCP JSON；人工 handoff request 仍由现有合同投影，不需要 CLI。
7. 将整个目录复制到目标位置；跨平台传输时可压成 `<case-id>__<cutoff>.zip`。

## 集中分析系统怎么选

事实归属在 case 目录和原始系统，不归属某一个模型。分析系统按任务临时选择：

- 主要是大量文档理解：Gemini Notebook 先做来源综合；
- 主要是代码、测试和运行时验证：Claude Code 或 Codex 做接收端验证；
- 需要跨文档、代码和多份贡献做最终判断：把整个目录交给一个具备足够上下文和文件读取能力的分析工作区。

无论选谁，最终都只写回同一 `CASEPACK.md` 与对应证据引用，避免出现四套互相漂移的“最终报告”。

## 对最近 Lattice 更新的修正审计结论

PR51 的方向本身与本方案一致：人工 handoff 是正式安全边界；自动 Google-to-coding 调用、自动回写和共享 discovery 都是非目标；Google 侧内容保持 candidate authority，代码与运行时主张由接收工作区独立验证。因此不应把“真实 handoff CLI”列为 P0。

当前真正缺口只有两个轻量交付物：

1. 一个跨生态通用的 `CASEPACK.md` 作者模板；
2. 一页“各生态如何导出同一字段”的操作说明。

先用一个真实 Feature 或 Bug case 手工跑通。成功标准不是自动化，而是：四个系统的贡献可以在十分钟内搬到同一目录；主张仍能追溯；未知、冲突和反证没有丢失；接收端没有把候选证据当成代码事实。观察到重复且稳定的人工痛点以后，再决定是否值得做任何工具。

