# Portable Case Pack — Manual Projection

> 本文件是 `lat.domain_context_pack.v1` 与 `lat.portable_case_pack.v1` 的人工可读投影，不创造新的事实系统。所有缺失值写 `UNKNOWN`；不得省略未知、未解决冲突或最强反证。

## 1. Identity

- case_id:
- producer_system:
- producer_role: source_synthesis | source_record | repo_verification | runtime_verification | final_analysis
- observed_at:
- evidence_cutoff:
- data_classification: public | internal/private | confidential/restricted | unknown
- authority_ceiling: candidate | independently_observed | human_decision_required

## 2. Task and scope

- objective:
- decision_requested:
- expected_output:
- scope_in:
- scope_out:
- audience:

## 3. Source coverage

### Selected

| source_id | type | locator | owner | observed_at | freshness | authority_for | selection_reason |
|---|---|---|---|---|---|---|---|

### Conditional

| source_id | locator | condition | reason |
|---|---|---|---|

### Excluded

| source_id | locator | reason |
|---|---|---|

### Unavailable or not searched

| source_id_or_area | access_status | impact | next_action |
|---|---|---|---|

## 4. Claims

### Observed

| claim_id | statement | evidence_refs | uncertainty |
|---|---|---|---|

### Derived

| claim_id | statement | evidence_refs | derivation | uncertainty |
|---|---|---|---|---|

### Judged

| claim_id | statement | evidence_refs | accountable_decider | uncertainty |
|---|---|---|---|---|

### Unknown

| claim_id | question | impact | blocking | owner_role | next_action |
|---|---|---|---|---|---|

## 5. Conflicts

| conflict_id | claim_refs | evidence_refs | summary | blocking | status | adjudicator | next_action |
|---|---|---|---|---|---|---|---|

## 6. Strongest counterevidence

| statement | evidence_refs | impact_on_decision | verification_needed |
|---|---|---|---|

## 7. Evidence references

| evidence_id | locator | source_version_or_hash | source_date | observed_at | access | what_it_supports |
|---|---|---|---|---|---|---|

## 8. Source gaps and rejected directions

### Source gaps

- UNKNOWN

### Rejected directions

| direction | reason | evidence_refs | reopen_condition |
|---|---|---|---|

## 9. Required verification

| verification_id | claim_refs | kind | request | required_evidence | owner_workspace |
|---|---|---|---|---|---|

## 10. Required output and falsification

- required_output:
- falsification_condition:
- stop_conditions:
- next_action:

## 11. Compression receipt

### Inspected

-

### Unavailable

-

### Omitted

| item | reason | impact |
|---|---|---|

## 12. Human gate

- source_scope_checked_by:
- privacy_checked_by:
- authority_ceiling_checked_by:
- accepted_as_input_to_verification: yes | no
- note: 接受为验证输入不等于确认主张、批准实现、批准合并或批准发布。

---

## Notebook 主提取提示

```text
仅使用当前选中的 notebook sources，生成一份可直接复制为 Markdown 的跨系统证据贡献文件。不要使用常识补齐缺口，不要把模型综合写成已观察事实，不要声称来源已穷尽。

严格按本模板第 1–12 节输出。要求：
1. 清点 selected、conditional、excluded、unavailable/not searched 的来源范围；无法判断时写 UNKNOWN。
2. 每个主张分为 observed、derived、judged 或 unknown，并分配稳定 claim_id。
3. 每个非 unknown 主张必须给出来源引用；无引用则降为 unknown。
4. 明确列出来源之间的冲突，不得自行消解；给出需要谁、用什么新证据裁决。
5. 找出最可能推翻当前结论、改变范围或阻止 readiness 的最强反证，而不是泛化风险清单。
6. 把所有依赖代码、测试、配置、依赖、复现或运行时状态的主张列入 required verification，authority_ceiling 保持 candidate。
7. 在 compression receipt 中列出检查过、不可访问和因长度省略的内容。
8. 保留具体来源名称和 Notebook citation；同时为每个 evidence ref 提供稳定 ID。不要伪造 URL、hash、时间或 owner，未知字段写 UNKNOWN。
9. 最后给出 source gaps、falsification condition、stop conditions 和最小下一步。
10. 输出正文，不添加对任务的解释、寒暄或模板之外的总结。
```

## Notebook gap pass 提示

```text
审计刚才生成的贡献文件，只寻找遗漏和过度断言。逐项检查：
- 是否有选中来源没有贡献任何主张，为什么；
- 是否有主张没有可定位引用；
- 是否把 derived/judged 写成 observed；
- 是否遗漏冲突、未知、最强反证或来源访问边界；
- 是否有代码/运行时主张未经接收工作区独立验证；
- 是否有脚注、评论、图片、嵌入内容或未选中来源未被 Notebook 实际摄取。

只输出需要追加或修改的条目，使用原 claim_id/source_id；不要重写整份文件，不要提升 authority。
```
