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

### Step 6 — Verify (Consistency Gate)

Before writing, run these checks against the assembled report. Mark failures as `[WARN]` in generation info and fix when possible.

1. **Terminology consistency** — The same entity/service/component must use the same name throughout. Scan for variant spellings, abbreviations, and aliases of the same concept.
2. **Severity-priority alignment** — If the report uses both severity and priority labels (e.g., P0/P1 + Critical/High), verify they don't contradict each other (P0 cannot pair with "Low" severity).
3. **Diagram-text alignment** — Best-effort, based on CapabilityRequest metadata constructed during this session: every component in a diagram slot's `content.components` should appear (by name or role) in at least one prose section.
4. **Data alignment** — Quantitative claims (file count, code line count, commit count, percentages) must match the values actually observed from the input. Re-verify any number cited in prose.
5. **Reference integrity** — Locally resolvable file paths, function names, and class names cited in prose must exist in the project. External URLs and references should be explicitly marked as external. Items listed in "问题与建议" must reflect the current code state — re-read target files before claiming an issue is open.

If any check fails and cannot be auto-fixed, keep the report as-is but append a warning line to the generation info block: `> - 一致性告警: {check name}: {brief description}`.

### Step 7 — Write Output

- Resolve the output root from the originating project root.
- Resolution order: workspace root > git root > current working directory.
- If the project root cannot be determined, fail instead of falling back.
- Never write reports under the skill installation directory such as `~/.agents/skills/tech-report/`.
- Report: `<project-root>/reports/{YYYY-MM-DD}_{spine_type}_{slug}/report.md`
- Assets: `<project-root>/reports/{YYYY-MM-DD}_{spine_type}_{slug}/assets/`

Extract slug from input content (filename, commit description, etc.) using lowercase kebab-case.

#### Multi-Document Mode

When **both** conditions are met, use multi-document output instead of a single report.md:

1. User explicitly requests splitting ("按模块" / "分拆" / "multi-doc" / "分篇输出")  
   OR input is whole-system analysis (targets the entire project/repo, not a specific service or module)
2. AND spine = `architecture`

All other scenarios (single file analysis, commit diff, document review, focused subsystem) → always single file, do not prompt or split.

**Output structure:**

```
reports/{date}_{type}_{slug}/
├── index.md              ← Main document (architecture overview + area index)
├── modules/
│   ├── {area-1}.md       ← Sub-document per functional area (NOT per file/directory)
│   ├── {area-2}.md
│   └── ...
└── assets/               ← Shared asset directory
```

**Rules:**
- `index.md` uses the `doc-index` archetype (see `section-archetypes.md`).
- Group related modules into functional areas. Target **2–4 sub-documents**, not one per directory. A project with 10 modules should produce 3–4 sub-docs, not 10.
- Each sub-document is an independent report using `tech_analysis` spine sections 3–6 (架构分析, 核心逻辑, 数据流, 问题与建议).
- Sub-documents reference shared assets with relative paths: `../assets/xxx.svg`
- `index.md` links to sub-documents: `[功能区](./modules/xxx.md)`
- Cross-references between sub-documents: `参见 [功能区](./xxx.md#section-anchor)`
- Front matter includes `parent: index.md` (in sub-docs) or `children: [modules/...]` (in index.md).
- Each sub-document gets its own `## 总结` (takeaway) section.
- The `index.md` summary covers the system as a whole, not individual modules.

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
| `references/writing-dna.md` | Step 4-6 (throughout) | Writing style + report shell |
