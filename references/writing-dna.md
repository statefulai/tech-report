# Writing DNA

Lock writing constants so reports from different runs read like the same author wrote them.

## Positioning

Precise, readable Chinese technical reports for engineers. Not blog posts, academic papers, or marketing copy.

## Execution Model

- `report-spines.md` decides the report shape and section order.
- `section-archetypes.md` decides the Markdown template for each section.
- `writing-dna.md` applies to every report from the first sentence to the final footer.
- Plugin capability is additive only: missing capability means omit the slot, not change the spine.

## Fact Discipline

- Separate observed facts from inference.
- Observed facts should be grounded in a file path, symbol name, code excerpt, or source link when available.
- Inferred statements must be labeled `推断` or `可能`; do not present them as verified implementation details.
- Do not confuse command targets, aliases, exported symbols, and registered components.
- Quantitative claims need a source or counting method; otherwise use approximate wording or omit the metric.

## Typography Rules

- Put one space between Chinese and half-width tokens: ✅ `使用 API 获取 3 个 token` ❌ `使用API获取3个token`
- Use full-width punctuation in Chinese prose: ✅ `，。：；！？` ❌ `, . : ;`
- Keep official casing for proper nouns: ✅ `GitHub` `JavaScript` ❌ `github` `Javascript`
- Keep paragraphs within 7 lines and one idea per paragraph.
- Prefer sentences under 40 Chinese characters; let technical sentences stay longer when splitting would harm meaning.
- Use active voice. Avoid double negatives and rhetorical questions.

## Report Shell

Every report uses this fixed shell:

```markdown
---
title: "{title}"
date: {YYYY-MM-DD}
author: tech-report
type: {spine_type}
tags: [{tag1}, {tag2}]
---

# {title}

> **摘要**：{one-paragraph summary, ≤3 lines}

## {Section 1}
...

---
> **生成信息**
> - 报告类型: {spine_type}
> - 使用 plugin: {list or 无}
> - 跳过 plugin: {list or 无}
> - 生成时间: {timestamp}
```

Constants:
- `#` title, `##` sections, `###` subsections. Never `####`.
- Summary always follows the title.
- Generation info always closes the report.
- Section titles should be noun phrases.

## Terminology

- First occurrence: annotate English — ✅ `飞书认证（Feishu Auth）` ❌ `Feishu 认证`
- Code identifiers stay in backticks — ✅ `app_access_token` ❌ 应用访问令牌
- Keep standard terms untranslated: commit, diff, token, API, SDK, scope — ❌ `提交差异`
- One concept, one term. No synonym switching — ❌ alternating "token" / "令牌" / "凭证"

## Callout System

| Emoji | Usage | Label |
|-------|-------|-------|
| ⚠️ | Warning | 注意 |
| 💡 | Tip | 提示 |
| 📌 | Key finding | 关键发现 |
| ❌ | Anti-pattern | 反面示例 |
| ✅ | Good pattern | 正面示例 |

Format: `> {emoji} **{label}**：{content}`

## Section Patterns

### Root Cause Analysis

1. Symptom: what the user sees.
2. File path + line range when available.
3. Causal chain: why the code is wrong.
4. Add `[diagram slot]` only if a diagram plugin is available.
5. End with a single 📌 callout that states the root cause.

### Architecture Analysis

1. One sentence positioning the module.
2. Add `[diagram slot]` for the architecture diagram.
3. Describe each layer or component in 2-3 lines.
4. Explain the data flow as A → B → C.
5. Close with the key design decisions.

### Problems & Suggestions

1. Use a table: Problem | Severity | Location | Suggestion.
2. Expand the top 1-2 most severe issues.
3. Add code snippets only when they clarify the fix.

### Summary / Takeaway

1. Core conclusion in 1-2 lines.
2. Key findings in 3-5 bullets.
3. Next steps when applicable.
4. Never introduce new content in the summary.

## Report-Type Add-ons

Apply only when the report type matches.

### Changelog

1. Version or date range covered.
2. Group items by Breaking | Feature | Fix | Chore.
3. Keep each item to one line and link commit or PR when available.
4. Add migration notes for breaking changes.

### Document Review

1. State the document purpose.
2. Assess structure.
3. List accuracy findings in a table.
4. Call out completeness gaps.
5. End with prioritized recommendations.

## Format Constraints

**Code blocks**:
- Always use a language tag.
- Keep blocks under 20 lines when possible; split long excerpts.
- Mark key lines with `// ←`.
- Add one sentence before and after each block.

**Images**:
- Always use alt text.
- Put the caption on the next line in italics.
- Max 2 images per section.
- Never stack images without intervening text.

**Tables vs Lists**:
- Use tables for comparisons.
- Use ordered lists for sequences.
- Use unordered lists for parallel items.
- Prefer lists when a table would have fewer than 3 data rows.
- Split tables wider than 5 columns.

## Anti-patterns

Never generate:
- Empty filler phrases such as “众所周知” or “显然”.
- First-person framing such as “让我们来分析”.
- Subjective importance claims such as “这个模块非常重要”.
- Metaphors that replace precision.
- Paragraphs longer than 7 lines.
- Multiple ideas in one paragraph without a topic sentence.
- Three or more consecutive short sentences.
- Four or more heading levels.
- Code blocks without language tags.
- Images without alt text.
- Manual section numbering.
