# Section Archetypes

Each section in a report maps to one archetype. An archetype defines the Markdown structure template for that section. The spine chooses which archetypes appear; this file defines how each archetype renders.

## Archetype Index

| Archetype | Semantic Role | Used By Spines |
|-----------|--------------|----------------|
| `summary-card` | Opening positioning, key facts | All (section 1) |
| `hero-illustration` | Opening visual or cover illustration | All (optional opener) |
| `layer-diagram` | Layered architecture visualization | tech_analysis, architecture |
| `code-walkthrough` | Core logic explanation with code | tech_analysis, bug_fix, changelog, architecture |
| `comparison` | Before/after or side-by-side contrast | bug_fix, document_review |
| `flow` | Data flow or call chain | tech_analysis, architecture |
| `checklist` | Itemized list of changes, issues, or suggestions | changelog, document_review |
| `metrics` | Quantitative results or measurements | bug_fix |
| `callout` | Warnings, risks, design rationale | tech_analysis, changelog, architecture |
| `takeaway` | Closing summary and next steps | All (last section) |

## Archetype Templates

### summary-card

Opening section that positions the subject and highlights key facts.

```markdown
## {title}

{1-2 paragraphs: what this is, what it does, which layer/module it belongs to.}

| 维度 | 值 |
|------|-----|
| 模块 | {module name} |
| 文件数 | {approximate or sourced N} |
| 代码行数 | {approximate or sourced N} |
| 主要语言 | {language} |
```

The metrics table is optional — include only when quantitative data is available from the input. Never fabricate metrics. If the counting method is unclear, use `约 N` or omit the row.

### hero-illustration

Opening visual that helps set context without carrying core analysis.

```markdown
## {title}

![{type}：{description}]({path})
*图 N：{explanation}*

{1 paragraph explaining why this visual helps the report.}
```

Use only when an `illustration` capability is available and the report benefits from a visual opener. Never block report generation on this slot. If the capability exists but the content does not benefit, skip it.

### layer-diagram

Architecture visualization with per-layer explanation.

```markdown
## {title}

{One sentence positioning the architecture.}

{[diagram slot]}

{Per-layer descriptions:}

**{Layer 1 name}**：{2-3 lines explaining responsibility and key components.}

**{Layer 2 name}**：{2-3 lines.}

**{Layer N name}**：{2-3 lines.}
```

When diagram capability is unavailable or CapabilityResponse status is `failed`/`degraded` with no usable artifacts, use `fallback_text` from the response if provided; otherwise replace `[diagram slot]` with a text description of the layers using indented bullet list.

### code-walkthrough

Core logic explanation anchored to source code.

```markdown
## {title}

{One sentence: what this code does and why it matters.}

{file path (when available):}

```{language}
{code excerpt, ≤20 lines, key lines marked with // ←}
```

{Explanation of the code: what each key part does, why it's written this way.}
```

When analyzing multiple code locations, repeat the code-block + explanation pattern. Max 3 code blocks per section.

### comparison

Before/after or side-by-side contrast. Primary archetype for bug fix analysis.

```markdown
## {title}

| 维度 | 修复前 | 修复后 |
|------|--------|--------|
| {dimension 1} | {before} | {after} |
| {dimension 2} | {before} | {after} |

{[diagram slot] — before/after comparison diagram}

{1-2 paragraphs explaining the key differences and why the change matters.}
```

The comparison table columns can be adapted: "旧版/新版", "方案 A/方案 B", "预期/实际" etc.

### flow

Data flow or request chain description.

```markdown
## {title}

{One sentence: what flows through this path.}

{[diagram slot] — flow/sequence diagram}

**请求路径**：

1. {Step 1}: {component} → {action}
2. {Step 2}: {component} → {action}
3. {Step N}: {component} → {action}

{1 paragraph: key observations about this flow (bottleneck, coupling, etc.)}
```

When diagram capability is unavailable or CapabilityResponse status is `failed`/`skipped`, the numbered step list serves as the primary representation.

### checklist

Itemized list for changes, issues, or action items.

```markdown
## {title}

| {列 1} | {列 2} | {列 3} | {列 4} |
|---------|--------|--------|--------|
| {item} | {value} | {value} | {value} |

{Optional: 1-2 paragraphs expanding on the most important items.}
```

Column names adapt to context:
- Changelog: 变更 | 类型 | 影响 | 关联 commit
- Issues: 问题 | 严重程度 | 位置 | 建议
- Suggestions: 建议 | 优先级 | 预期效果
If there are fewer than 3 rows, use a list instead of a table.
If a row contains an inferred claim, add `推断` in the relevant cell.

### metrics

Quantitative results, test outcomes, or performance data.

```markdown
## {title}

| 指标 | 修复前 | 修复后 | 变化 |
|------|--------|--------|------|
| {metric 1} | {value} | {value} | {delta} |
| {metric 2} | {value} | {value} | {delta} |

> 📌 **关键发现**：{one-sentence highlight of the most significant metric change.}
```

Only include metrics that are present in the input. Never fabricate numbers.

### callout

Warnings, risks, or design rationale. Used as a standalone section for emphasis.

```markdown
## {title}

> ⚠️ **注意**：{risk or warning, 1-3 lines.}

{1-2 paragraphs providing context, evidence, or reasoning.}

> 💡 **提示**：{suggestion or best practice.}
```

Can mix callout types (⚠️, 💡, 📌) as needed. See `writing-dna.md` Callout System for locked labels.

### takeaway

Closing section that summarizes findings and suggests next steps. Always the last section.

```markdown
## 总结

{Core conclusion: 1-2 lines.}

**关键发现**：

- {finding 1}
- {finding 2}
- {finding 3}

**下一步**：

- {action 1}
- {action 2}
```

Rules:
- Never introduce new information in takeaway.
- "下一步" is optional — omit when no actionable follow-up exists.
- Keep findings to 3-5 bullets. If more than 5, prioritize.

## Rules

- One archetype per section. Never mix two archetypes in one section.
- `[diagram slot]` is a placeholder, not literal text in the output. Replace with actual diagram (from CapabilityResponse `artifacts`) or text fallback (from `fallback_text` or manual text description).
- `hero-illustration` is optional and should never be forced into a report.
- All templates use `##` for section title. Never change heading level based on archetype.
- Templates show structure, not exact wording. Adapt field names and content to context.
- When input data is insufficient for an archetype's optional elements (metrics table, diagram), omit them cleanly rather than fabricating content.

## Multi-Document Archetype

### doc-index

Entry point for multi-document mode. Provides architectural overview and navigation to sub-documents. Only used as `index.md` in multi-document output.

```markdown
## {project/system name}

> **摘要**：{one-paragraph summary of the entire system analysis}

## 架构总览

{[diagram slot] — high-level architecture of the full system}

{2-3 paragraphs: system positioning, design philosophy, key constraints}

## 功能区索引

| 功能区 | 覆盖模块 | 核心职责 | 关键发现 |
|--------|---------|---------|---------|
| [{area-1}](./modules/{area-1}.md) | {module list} | {one-line responsibility} | {one-line finding} |
| [{area-2}](./modules/{area-2}.md) | {module list} | {one-line responsibility} | {one-line finding} |

## 关键交互

{Cross-area interactions and dependencies not covered in individual sub-documents.}

## 总结

{Overall system assessment + recommended reading order for sub-documents.}
```

Rules:
- Only used in multi-document mode as the `index.md` structure.
- Target 2–4 rows in the index table. Group small/related modules into functional areas.
- "关键交互" describes inter-area dependencies; detail belongs in sub-docs.
- Diagram slot shows the high-level architecture; detail diagrams go in sub-documents.
- Keep `index.md` under 100 lines — it is a navigation hub, not a full report.
