# 蓝图架构与契约

## 架构

```
┌────────────────────────────────────────────────┐
│  SKILL.md（核心）                                │
│  tech-report 自身 = 报告排版 + 语言质量 skill     │
│  编排逻辑内置于 SKILL.md 指令中                    │
├────────────────────────────────────────────────┤
│  plugins.yaml（用户配置）                         │
│  纯 skill 名列表，用户注册要用的 plugin           │
│  tech-report 读各 plugin 的 SKILL.md 推断能力     │
├────────────────────────────────────────────────┤
│  Plugins（按需调用）                              │
│  ~/.agents/skills/ 下的已安装 skill              │
│  通过 scripts/ 路径直接调用，绕过 skill tool 嵌套  │
└────────────────────────────────────────────────┘
```

### 设计原则

- **不绑定具体 skill**：SKILL.md 不硬编码任何 plugin 名（如 fireworks-tech-graph）。每个用户本地 skill 不同，所有 plugin 关系由 plugins.yaml 声明
- **能力自动推断**：tech-report 读已注册 plugin 的 SKILL.md description 字段，推断其能力类型（画图、配图、数据源等）
- **编排内置于 SKILL.md**：何时调用哪种能力由 SKILL.md 的指令逻辑决定，不需要单独的 pipeline 配置
- **Plugin 独立性**：每个 plugin skill 的内部实现（如 image model 降级）由它自己负责，tech-report 不介入

## 插件注册（plugins.yaml）

### 格式

```yaml
# plugins.yaml — 用户唯一需要编辑的配置文件
# 只列 skill 名，tech-report 自动推断每个 skill 的能力

plugins:
  - fireworks-tech-graph
  - doc-to-sketch
  - feishu-docs
```

### 能力推断流程

```
启动时：
  1. 读 plugins.yaml（用户注册的 skill 列表）
  2. 逐个检查 ~/.agents/skills/<name>/ 是否存在
  3. 对已安装的 skill，读其 SKILL.md description 推断能力类型
  4. 未安装的 skill → 记录到跳过列表，继续执行
  5. 报告生成完毕后，在终端 warn + 报告底部列出跳过的 skill
```

### 能力推断规则

tech-report 读 plugin 的 SKILL.md description，按关键词匹配推断能力：

| 能力类型 | 匹配关键词（description 中） | 用途 |
|----------|---------------------------|------|
| diagram | diagram, SVG, chart, graph, flow, architecture, sequence, 图表, 画图 | 在需要图表的章节调用 |
| illustration | sketch, illustration, cover, image, pict, PPT, 配图, 手绘, 插画 | 在需要配图/封面时调用 |
| data_source | fetch, feishu, lark, notion, wiki, api, http, url, 文档, 数据源 | 在需要拉取外部数据时调用 |
| browser | browser, screenshot, dom, 网页, 截图 | 在需要网页数据采集时调用 |

推断失败时（description 无法匹配已知能力类型）→ 跳过该 plugin，warn 提示用户。

### 与旧方案对比

| 对比维度 | 旧方案（config.yaml + registry + pipeline） | 新方案（plugins.yaml） |
|----------|-------------------------------------------|----------------------|
| 配置文件 | config.yaml（registry + pipeline + output） | plugins.yaml（纯 skill 名列表） |
| 用户写什么 | 能力 key → skill 映射 + 管线步骤定义 | 只写 skill 名 |
| 编排逻辑 | 用户在 pipeline 配置中定义 | SKILL.md 内置 |
| 能力发现 | discover-capabilities.py 扫描 | 读 SKILL.md description 推断 |
| 中间产物 | outline.json | 无（AI 直接写 Markdown） |
| 脚本依赖 | discover + assemble 两个 Python 脚本 | 无脚本 |

## 触发与宿主适配

### 触发方式

所有触发都依赖宿主的 SKILL.md description 匹配能力，tech-report 不发明新机制。

V1 只支持一种触发方式：

| 触发方式 | 示例 | 机制 |
|---------|------|------|
| `@report` + 描述 | `@report 分析 src/utils/feishuClientAuth.ts` | description 中 `Trigger on: "@report"` 被匹配 |

自然语言触发（"帮我生成报告"等）列入 M2 考虑。V1 用显式 `@report` 前缀降低误触发风险。

### 输入模式

| 模式 | 示例 | 说明 |
|------|------|------|
| 文件分析 | `@report 分析下 src/utils/feishuClientAuth.ts` | 代码模块分析 |
| 链接分析 | `@report https://xxx.feishu.cn/docx/xxx` | 外部文档（需数据源 plugin） |
| Commit 修复 | `@report 分析 commit fc2d575` | Bug Fix 修复分析 |
| Commit 变更 | `@report 这个 commit 的变更报告` | 变更清单 |
| 架构分析 | `@report 分析 src/auth/ 的架构` | 架构报告 |

### 安装方式

遵循 `npx skills` 生态的标准安装流程：

```bash
# 全局安装（推荐）
npx skills add <repo>/tech-report -g

# 项目级安装
npx skills add <repo>/tech-report

# 手动安装
git clone <repo> ~/.agents/skills/tech-report
```

安装结果：
```
~/.agents/skills/tech-report/     ← 完整文件（SKILL.md + scripts/ + references/）
~/.claude/skills/tech-report/     ← symlink → 上面
~/.codex/skills/tech-report/      ← symlink → 上面
```

### 跨宿主 SKILL.md

一份 SKILL.md 服务所有宿主（各宿主通过 symlink 读取同一份）。description 只保留 `@report` 短命令：

```yaml
description: >-
  从代码、commit diff、文档链接、架构描述等技术输入，自动生成结构化中文技术报告。
  支持插件注册：根据用户注册的本地 plugin 动态增强报告内容。
  Trigger on: "@report"
```

V1 只识别 `@report` 前缀。自然语言关键词触发列入 M2。

### 支持的宿主

| 宿主 | Skill 读取路径 | 安装方式 | 触发 |
|------|--------------|---------|------|
| **Copilot CLI** | `~/.agents/skills/` | 直接读取 | description 匹配 |
| **Claude Code** | `~/.claude/skills/` | symlink 自动创建 | description 匹配 |
| **Codex** | `~/.codex/skills/` | symlink 自动创建 | description 匹配 |
| **Cursor** | 需手动配 Rules | 手动拷贝 | description 匹配 |
| **其他（Cline/Roo Code 等）** | `npx skills add --agent <name>` | 按宿主适配 | 看宿主 skill 支持 |

一份 SKILL.md，多宿主 symlink，预期低适配成本（需 M2 验证）。

### 用户配置流程

#### 首次使用

```
1. 安装 tech-report
2. 编辑 plugins.yaml，列出自己想用的 skill 名
3. 输入 `@report 分析 src/xxx.ts` → tech-report 读 plugins.yaml → 检查已装 skill → 生成报告
```

#### 不配置也能用

```
如果不编辑 plugins.yaml（或文件为空）：
  → tech-report 作为纯"排版 + 语言"skill 工作
  → 输出纯文字 Markdown 报告，无图表/配图
```

#### 增减 plugin

```yaml
# plugins.yaml
plugins:
  - fireworks-tech-graph    # 增加图表能力
  # - doc-to-sketch         # 注释掉 = 关闭配图
```

### Skill 包目录结构

```
tech-report/
├── SKILL.md                        ← AI 编排指令（核心：排版 + 语言 + 调用逻辑）
├── plugins.yaml                    ← 用户配置（纯 skill 名列表）
├── package.json                    ← 元信息（name/version）
├── README.md                       ← 人类文档
├── LICENSE
├── scripts/                        ← 确定性逻辑（轻量）
│   └── resolve-plugins.py          ← 读 plugins.yaml → 检查存在 → 读 description → 返回能力列表
├── references/                     ← 三文件参考体系（AI 按需加载）
│   ├── report-spines.md            ← 输入类型 → 整体报告骨架（叙事结构）
│   ├── section-archetypes.md       ← 内容语义 → 章节 Markdown 结构
│   └── writing-dna.md              ← 写作风格锁定 + Markdown 规范
└── assets/                         ← 静态资源（可选）
```

| 文件 | 谁读 | 职责 |
|------|------|------|
| `SKILL.md` | AI agent | 编排指令（排版+语言+plugin调用） |
| `plugins.yaml` | AI agent | 读取用户注册的 plugin 列表 |
| `scripts/resolve-plugins.py` | AI 调用 | 确定性逻辑：解析 plugins.yaml → 检查已装 → 推断能力 → 返回 JSON |
| `references/report-spines.md` | AI 按需读取 | 输入类型→报告骨架（借鉴 doc-to-sketch narrative-planning） |
| `references/section-archetypes.md` | AI 按需读取 | 内容语义→章节结构（借鉴 slide-archetypes + Gamma cards） |
| `references/writing-dna.md` | AI 按需读取 | 写作风格系统（借鉴 visual-dna + Quarto 格式规范） |
| `package.json` | `npx skills` CLI | 安装/版本 |
| `README.md` | 人类 | 使用文档 |

### resolve-plugins.py 职责

这是 tech-report 唯一的脚本，做三件确定性的事：

```
输入：plugins.yaml 路径
输出：JSON（stdout）

1. 读 plugins.yaml → 得到 skill 名列表
2. 逐个检查 ~/.agents/skills/<name>/ 是否存在
3. 对已安装的 skill，读其 SKILL.md description → 按关键词匹配推断能力类型
4. 输出 JSON：
   {
     "available": [
       {"name": "fireworks-tech-graph", "capability": "diagram", "path": "/..."},
       {"name": "doc-to-sketch", "capability": "illustration", "path": "/..."}
     ],
     "missing": ["feishu-docs"],
     "unknown": []  // 已安装但能力推断失败
   }
```

**为什么需要脚本而不是全交给 AI**：
- 文件系统检查（exists/not exists）是确定性操作，脚本比 AI 指令更可靠
- 关键词匹配规则固定，不需要 LLM 推理
- 输出 JSON 结构化，AI 可直接消费，不存在格式解析风险

## Plugin 调用契约

### 调用方式

tech-report 通过**直接调用 plugin 的 scripts/** 来使用其能力，不通过 `skill` tool。

具体调用哪个脚本、传什么参数，由 tech-report 读 plugin 的 SKILL.md 获取（SKILL.md 中通常包含脚本使用说明）。

```bash
# 示例：调用某个有 scripts/ 的 plugin
python3 ~/.agents/skills/<plugin_name>/scripts/<script>.py <args>

# 示例：调用某个无 scripts/ 的 plugin（纯 SKILL.md 指令型 skill）
# → tech-report 直接读取该 skill 的 SKILL.md 指令，按指令执行
```

### 为什么不通过 skill tool

- `skill` tool 有规则："Do not invoke a skill that is already running"
- tech-report 自身作为 skill 运行时，无法再通过 skill tool 调用其他 skill
- 直接调 scripts/ 绕过此限制，且性能更好（无需读取整个 SKILL.md）

### 降级策略

| 情况 | 行为 |
|------|------|
| plugins.yaml 中列出但本地未安装 | 跳过，末尾 warn 列出 |
| plugins.yaml 为空或不存在 | 纯文字报告（无图表/配图） |
| plugin 已安装但能力推断失败 | 跳过，warn 提示 |
| plugin 脚本执行报错 | 跳过该步骤，warn 提示错误信息 |

## 报告生成体系（三文件参考模型）

借鉴 doc-to-sketch 的 "语义内容 → 结构选择 → 产出" 模式，结合 Gamma（Card 化章节）和 Quarto（结构化 Markdown），tech-report 用三个 reference 文件驱动报告生成。

### 三文件对照

| tech-report | 借鉴自 | 职责 |
|-------------|--------|------|
| `report-spines.md` | doc-to-sketch `narrative-planning.md` | 输入类型 → 整体报告骨架（叙事结构） |
| `section-archetypes.md` | doc-to-sketch `slide-archetypes.md` + Gamma cards | 内容语义 → 章节 Markdown 结构 |
| `writing-dna.md` | doc-to-sketch `visual-dna-v6.md` + Quarto 格式 | 写作风格锁定 + Markdown 规范 |

### report-spines.md — 报告骨架

按输入类型自动选择报告的叙事骨架（spine），每种 spine 定义章节序列和 diagram slot 位置。

| 输入类型 | 报告模式 | 自动判断依据 |
|----------|---------|-------------|
| 代码文件/模块 | `tech_analysis` | 输入含文件路径（`.ts` `.vue` `.py` 等） |
| commit diff（bug fix） | `bug_fix` | 含 commit hash + diff 显示修复类型改动 |
| commit diff（变更） | `changelog` | 含 commit hash + diff 显示功能/重构改动 |
| 架构文档请求 | `architecture` | 含"架构""设计""design"等关键词 |
| 外部文档链接 | `document_review` | 输入含 URL |

示例 spine（tech_analysis）：

```
1. 概述 [summary-card]
2. 视觉导入 [hero-illustration] → illustration slot (optional)
3. 架构分析 [layer-diagram] → diagram slot
4. 核心逻辑 [code-walkthrough]
5. 数据流 [flow] → diagram slot
6. 问题与建议 [callout]
7. 总结 [takeaway]
```

### section-archetypes.md — 章节结构映射

每个章节 = 一个 Card（借鉴 Gamma），有明确的 type 和 Markdown 结构。

| 内容语义 | Archetype | 何时用 | Markdown 结构 |
|----------|-----------|--------|---------------|
| 定义/概述 | `summary-card` | 开篇定位 | 标题 + 一段话 + 关键指标表 |
| 架构分层 | `layer-diagram` | 展示分层结构 | 标题 + [diagram slot] + 层级说明列表 |
| 前后对比 | `comparison` | Bug fix / 重构 | 标题 + Before/After 双栏表 + [diagram slot] |
| 流程/链路 | `flow` | 数据流/调用链 | 标题 + [diagram slot] + 步骤编号列表 |
| 代码分析 | `code-walkthrough` | 核心函数解读 | 标题 + 代码块 + 逐行注释 |
| 列表/清单 | `checklist` | 变更清单/建议 | 标题 + checkbox 列表 or 表格 |
| 数据/指标 | `metrics` | 性能/统计 | 标题 + 表格 + 关键数字高亮 |
| 风险/注意 | `callout` | 警告/注意 | `> ⚠️` callout block |
| 总结 | `takeaway` | 结尾结论 | 标题 + 关键结论 + 下一步 |

每个 archetype 中标注 `[diagram slot]` 的位置 = tech-report 检查是否有图表 plugin 的节点。

### writing-dna.md — 写作风格系统

锁定报告的写作常量，保证多次生成风格一致（借鉴 visual-dna 的"Master Consistency"理念）。

核心规则：

| 维度 | 规范 |
|------|------|
| **语言** | 技术精准，中文为主，术语保留英文（commit diff 不翻译） |
| **段落** | 3-5 行一段，不写大段落 |
| **标题** | 最多三级（# / ## / ###），不用四级 |
| **代码块** | 标注语言，关键行用 `// ←` 注释，单块 ≤20 行 |
| **表格** | 对比用表格不用文字，列数 ≤5 |
| **图片** | `![描述](./images/xxx.png)` + 下一行说明文字，每章 ≤2 张 |
| **术语** | 同一概念全文同一术语，首次标注英文：`飞书认证（Feishu Auth）` |
| **Callout** | `> ⚠️ **注意**：xxx` / `> 💡 **提示**：xxx` |
| **Front matter** | YAML 格式，Quarto 兼容：title/date/author/tags |

### 调用契约（tech-report → plugin）

tech-report 在每个 `[diagram slot]` 位置构造调用请求：

```json
{
  "type": "diagram",
  "intent": "architecture-overview",
  "input_summary": "三层架构：网关层→服务层→数据层",
  "expected_format": "svg+png",
  "insert_at": "section-2",
  "output_dir": "./reports/2026-05-21_tech_analysis_xxx/assets/"
}
```

Plugin 是**建议填充者**，不是共同决策者：
- Plugin 可以失败、缺席、降级
- Plugin 不能改变报告结构
- 报告骨架始终由 tech-report 单方决定

### 模式选择逻辑（写入 SKILL.md）

```
1. 分析用户输入 → 判断输入类型
2. 加载 references/report-spines.md → 选择对应 spine
3. 将 spine 展开为 section 序列，每个 section 按 section-archetypes.md 选 archetype
4. 加载 references/writing-dna.md → 锁定写作风格
5. 逐 section 生成内容：
   → 遇到 [diagram slot] → 构造调用契约 → 检查 plugin 能力
     → 有: 调用 plugin → 插入图表
     → 无: 文字描述替代
6. 组装最终 report.md（含 YAML front matter）
```

### 用户自定义（D4）

用户可在 `references/` 下添加自定义文件覆盖默认规则：

```
references/
├── report-spines.md            ← 内置骨架（随 tech-report 分发）
├── section-archetypes.md       ← 内置 archetype（随 tech-report 分发）
├── writing-dna.md              ← 内置风格（随 tech-report 分发）
├── custom-spines.md            ← 用户扩展骨架（手动创建，优先读取）
└── custom-writing-dna.md       ← 用户覆盖风格（手动创建，优先读取）
```

## 输出规范

### 输出结构

每次生成的报告为一个独立文件夹，包含报告本体和所有关联资源：

```
reports/
└── {YYYY-MM-DD}_{spine_type}_{slug}/
    ├── report.md              ← 主报告文件
    ├── assets/                ← 图表和配图（由 plugin 生成）
    │   ├── *.png
    │   └── *.svg
    └── data/                  ← 外部数据（可选）
        └── raw.json
```

- 文件夹命名：`{YYYY-MM-DD}_{spine_type}_{slug}`（如 `2025-05-22_bug_fix_feishu-auth-fix`）
- report.md 内用**相对路径**引用图片：`![架构图](./assets/architecture.png)`
- 默认输出位置：`./reports/`（项目内）
- 可通过参数覆盖输出目录

### 报告底部信息

报告末尾附加 plugin 使用情况：

```markdown
---
> **生成信息**
> - 使用 plugin: fireworks-tech-graph（图表）, doc-to-sketch（配图）
> - 跳过 plugin: feishu-docs（未安装）
> - 生成时间: 2025-05-22 14:30
```

## 设计决策（已确认）

| ID | 问题 | 决策 |
|----|------|------|
| D1 | outline 生成后是否暂停确认？ | **默认不暂停**，直接继续。无 outline 中间产物，AI 直接写报告 |
| D2 | 图表类型自动选择 vs 每次询问？ | **自动选择**，按内容特征匹配 report-spines.md 的 Plugin Type Affinity 表 |
| D3 | Session 回溯？ | **不做 session 回溯**，只支持即时分析（文件/commit/内联描述） |
| D4 | 报告模式是否允许用户自定义？ | **允许**，在 `references/` 下加自定义模式文件扩展 |
| D5 | 触发词风格？ | **V1 仅 `@report` 显式前缀**。`Trigger on: "@report"` 写入 SKILL.md description，自然语言触发列入 M2 |
| D6 | 降级信息展示方式？ | **终端 warn + 报告底部注脚**，两处都可见 |
| D7 | 配置文件设计？ | **单一 plugins.yaml**，纯 skill 名列表，能力由 tech-report 读 SKILL.md 自动推断。不用 config.yaml / registry / pipeline |
| D8 | tech-report 自身定位？ | **报告排版 + 语言质量 skill**，中文优先。不是编排框架，不是 skill 管理器 |
| D9 | 报告结构怎么确定？ | **三文件参考模型**：report-spines（骨架）+ section-archetypes（章节结构）+ writing-dna（风格锁定），借鉴 doc-to-sketch + Gamma + Quarto |
| D10 | tech-report 与 plugin 的关系？ | Plugin 是**建议填充者**，不是共同决策者。tech-report 通过调用契约（type/intent/format/insert_at）请求 plugin 填充，plugin 可失败但不能改报告结构 |
