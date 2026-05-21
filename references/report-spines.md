# Report Spines

A spine defines the narrative backbone of a report: what sections appear, in what order, and where visual capability slots go. Each spine is selected automatically based on input type.

## Capability Routing

The report engine resolves capabilities, not hard-coded skill names.

- `diagram` slots are for structural evidence: architecture diagrams, flow charts, before/after comparison diagrams.
- `illustration` slots are for presentation: cover art, opening visuals, concept sketches, and visual recaps.
- `data_source` and `browser` are input-acquisition capabilities and do not change the spine.
- When multiple registered plugins expose the same capability, prefer the first available plugin in `plugins.yaml` order.
- If a capability is missing, omit the slot and continue.
- Never require a specific skill name such as `fireworks-tech-graph` or `doc-to-sketch`.
- Every spine may use `hero-illustration` as an optional opener when illustration capability is available.

## Spine Selection

Match input to spine using the first rule that hits:

| Input Signal | Spine | Detection |
|-------------|-------|-----------|
| File paths (`.ts` `.vue` `.py` `.go` `.java` etc.) | `tech_analysis` | Input contains recognizable source file paths |
| Commit diff with fix-type changes | `bug_fix` | Commit hash present + diff shows bug/fix/patch pattern |
| Commit diff with feature/refactor changes | `changelog` | Commit hash present + diff shows add/refactor/chore pattern |
| Keywords: 架构/设计/design/architecture | `architecture` | Natural language input contains architecture keywords |
| URL (http/https) or document reference | `document_review` | Input contains URL or explicit "review this document" |

When ambiguous, prefer `tech_analysis` as the default spine.

## Spines

### tech_analysis

For analyzing code modules, files, or components. The most general spine.

```
1. 概述                    [summary-card]
2. 视觉导入                [hero-illustration] → illustration slot (optional)
3. 架构分析                [layer-diagram]    → diagram slot
4. 核心逻辑                [code-walkthrough]
5. 数据流                  [flow]             → diagram slot
6. 问题与建议              [callout]
7. 总结                    [takeaway]
```

Section 5 (数据流) is optional — include only when the analyzed code has meaningful request/data flow. A simple utility function does not need a flow section.

### bug_fix

For analyzing commit diffs that fix bugs. Follows a symptom → cause → fix → verify narrative.

```
1. 问题描述                [summary-card]
2. 视觉导入                [hero-illustration] → illustration slot (optional)
3. 根因分析                [comparison]       → diagram slot (before/after)
4. 修复方案                [code-walkthrough]
5. 影响范围                [checklist]
6. 验证                    [metrics]
7. 总结                    [takeaway]
```

Section 6 (验证) is optional — include only when test results or metrics are available in the input.

### changelog

For commit diffs covering features, refactors, or multiple changes. Groups changes by category.

```
1. 变更概览                [summary-card]
2. 视觉导入                [hero-illustration] → illustration slot (optional)
3. 变更清单                [checklist]
4. 重点变更详解            [code-walkthrough]  → diagram slot (if architectural change)
5. 兼容性与迁移            [callout]
6. 总结                    [takeaway]
```

Section 4 expands only the top 1-3 most significant changes. Section 5 is optional — include only when there are breaking changes or migration steps.

### architecture

For architecture analysis or design review. Emphasizes layers, components, and data flow.

```
1. 系统定位                [summary-card]
2. 视觉导入                [hero-illustration] → illustration slot (optional)
3. 架构总览                [layer-diagram]    → diagram slot
4. 组件说明                [code-walkthrough]
5. 数据流与交互            [flow]             → diagram slot
6. 设计决策                [callout]
7. 问题与建议              [callout]
8. 总结                    [takeaway]
```

### document_review

For reviewing external documents (Feishu docs, design docs, specs). Evaluates structure, accuracy, and completeness.

```
1. 文档概述                [summary-card]
2. 视觉导入                [hero-illustration] → illustration slot (optional)
3. 结构评估                [checklist]
4. 内容准确性              [comparison]
5. 完整性分析              [callout]
6. 改进建议                [checklist]
7. 总结                    [takeaway]
```

No diagram slots by default — document reviews rarely need generated diagrams. If the reviewed document describes an architecture, the author may manually request a diagram.

Illustration slots are also optional here and should only be used when the source document is visually oriented or the user explicitly wants a visual recap.

## Rules

- Every spine starts with a summary-type section and ends with `[takeaway]`.
- `→ diagram slot` marks where tech-report checks for diagram plugin availability.
- `hero-illustration` is an optional opening visual and never blocks report generation.
- `illustration` slots are presentation helpers; use them only when they add meaning.
- Do not force `hero-illustration` just because an illustration plugin is registered.
- Sections marked "optional" are skipped when the input lacks sufficient data. Never generate empty sections.
- A spine defines order and structure. It does not define writing style (see `writing-dna.md`) or section Markdown structure (see `section-archetypes.md`).

## Plugin Type Affinity

Not every spine needs every plugin type. Use this table to decide which plugins to invoke:

| Spine | diagram | illustration |
|-------|---------|--------------|
| `tech_analysis` | ✅ architecture, flow | 🔶 optional opener or cover art |
| `bug_fix` | ✅ comparison, call chain | 🔶 optional opener or cover art |
| `changelog` | 🔶 optional (architectural changes only) | 🔶 optional opener or cover art |
| `architecture` | ✅ architecture, flow | 🔶 optional cover or concept art |
| `document_review` | 🔶 rare (only when explicitly requested or architecture-heavy) | 🔶 optional visual recap |

🔶 optional slots only fire when the capability is available AND the content semantically benefits. Never force a diagram or illustration just because a plugin is registered.
