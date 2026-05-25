---
name: tech-report
description: >-
  Generate structured Chinese technical reports from code, commit diffs,
  document links, and architecture descriptions.
  Trigger on: "@report"
---

# tech-report

Convert technical input into well-structured, professionally written Chinese technical reports.

## Activation

Only activate when user input starts with `@report`. Ignore all other inputs.

## Execution Flow

After receiving `@report`, follow these steps in order:

### Step 1 — Resolve Plugins

Run the plugin resolver to discover available capabilities:

```bash
python3 ~/.agents/skills/tech-report/scripts/resolve-plugins.py \
  --plugins-file ~/.agents/skills/tech-report/plugins.yaml
```

Output JSON:

```json
{
  "available": [{"name": "...", "capability": "diagram|illustration|data_source|browser", "path": "..."}],
  "missing": ["skill-name"],
  "unknown": ["skill-name"]
}
```

Store the `available` list for later steps. If `plugins.yaml` is empty or missing, all capabilities are unavailable — proceed in text-only mode.

### Step 2 — Classify Input and Select Spine

Read `references/report-spines.md` Spine Selection table. Match the first rule that hits:

| Input Signal | Spine |
|-------------|-------|
| Source file paths (`.ts` `.vue` `.py` etc.) | `tech_analysis` |
| Commit hash + fix-type diff | `bug_fix` |
| Commit hash + feature/refactor diff | `changelog` |
| Keywords: 架构/设计/design/architecture | `architecture` |
| URL or document link | `document_review` |

Default to `tech_analysis` when ambiguous.

### Step 3 — Expand Section Sequence

From `references/report-spines.md`, read the selected spine's section list. Each section has:
- A title (e.g., "概述", "根因分析")
- An archetype tag (e.g., `[summary-card]`, `[code-walkthrough]`)
- Optional diagram/illustration slot markers

Skip sections marked "optional" when input data is insufficient. Never generate empty sections.

### Step 4 — Generate Each Section

For each section in the sequence:

1. Read the matching archetype template from `references/section-archetypes.md`.
2. Fill content following the template structure. Apply `references/writing-dna.md` rules throughout.
3. When encountering `[diagram slot]`:
   - Check if `diagram` capability exists in the Step 1 available list.
   - **Available**: Construct a CapabilityRequest with `capability: diagram`, a unique `slot_id`, the `intent` describing what the diagram should convey, `content` with components/relationships, `output_dir`/`output_name`, and `contract_version: "1.0"`. Host receives this request, selects a provider, translates to skill-native format, and returns a CapabilityResponse.
     - `success`: Embed `artifacts` (first item = preferred format) into report.
     - `degraded`: Embed available artifacts; if artifacts are insufficient for embedding, use `fallback_text` when provided, otherwise generate a text description manually. Never leave a blank slot.
     - `failed`: Use `fallback_text` as text substitute. Never leave a blank slot.
     - `skipped`: Host judged this slot unnecessary — skip silently, do not embed or generate fallback.
   - **Unavailable** (no diagram capability registered): Replace with text description (indented list, numbered steps, or table). Never leave a blank slot.
4. When encountering `[hero-illustration]`:
   - Check if `illustration` capability exists AND the report benefits from a visual opener.
   - **Yes to both**: Construct a CapabilityRequest with `capability: illustration`. Host processes and returns CapabilityResponse. Embed on `success`/`degraded`, skip on `failed`/`skipped`.
   - **Otherwise**: Skip silently. Do not generate a placeholder.

### Step 5 — Assemble Report

Wrap all sections in the report shell defined in `references/writing-dna.md`:

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

## {Section N}
...

---
> **生成信息**
> - 报告类型: {spine_type}
> - 使用 plugin: {plugins actually called, or 无}
> - 跳过 plugin: {missing + unknown, with reasons, or 无}
> - 生成时间: {timestamp}
```

### Step 6 — Write Output

- Resolve the output root from the originating project root.
- Resolution order: workspace root > git root > current working directory.
- If the project root cannot be determined, fail instead of falling back.
- Never write reports under the skill installation directory such as `~/.agents/skills/tech-report/`.
- Report: `<project-root>/reports/{YYYY-MM-DD}_{spine_type}_{slug}/report.md`
- Assets: `<project-root>/reports/{YYYY-MM-DD}_{spine_type}_{slug}/assets/`

Extract slug from input content (filename, commit description, etc.) using lowercase kebab-case.

## Calling Plugins

Call plugin scripts directly via their `scripts/` directory:

```bash
python3 ~/.agents/skills/<plugin_name>/scripts/<script>.py <args>
```

For instruction-only plugins (no scripts/), read the plugin's SKILL.md and follow its instructions.

Rules:
- Plugin failure → degrade to text description, log a warning.
- Plugins cannot alter report structure or section order.

## Degradation

| Scenario | Behavior |
|----------|----------|
| plugins.yaml empty | Text-only report, no diagrams or illustrations |
| Plugin not installed (missing) | Skip, list in generation info |
| Plugin capability unknown | Skip, list in generation info |
| Plugin script fails | Skip that slot, warn in generation info |
| Insufficient input for optional section | Skip that section entirely |

Never interrupt report generation due to missing plugins.

## Writing Rules (Always Active)

These rules from `references/writing-dna.md` apply to all sections at all times:

- Space between Chinese and half-width tokens: `使用 API 获取 3 个 token`
- Full-width punctuation in Chinese prose: `，。：；！？`
- Paragraphs ≤7 lines, one idea per paragraph
- Max three heading levels (`#` `##` `###`), never `####`
- Code blocks with language tags, key lines marked with `// ←`
- First occurrence of terms annotated with English: `飞书认证（Feishu Auth）`
- No filler phrases: "众所周知", "显然", "让我们来分析"

## Reference Files

| File | When to Read | Purpose |
|------|-------------|---------|
| `references/report-spines.md` | Step 2-3 | Select spine, expand section sequence |
| `references/section-archetypes.md` | Step 4 | Markdown template for each section |
| `references/writing-dna.md` | Step 4-5 (throughout) | Writing style + report shell |
