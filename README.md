# tech-report

<p align="center">
  <img src="./assets/cover.png" alt="tech-report cover" width="100%"/>
</p>

从代码、commit diff、文档链接、架构描述等技术输入，自动生成结构化中文技术报告的 AI Skill。

## 特性

- 📝 **报告排版 + 语言质量** — 不是通用 AI 编排框架，是专注写作质量的 skill
- 🔌 **插件增强** — 你本地安装的 skill 可以注册为插件，按能力自动补图表、配图或数据
- 📐 **三文件参考系统** — report-spines（骨架）+ section-archetypes（章节模板）+ writing-dna（风格锁定）
- 🎯 **`@report` 触发** — 统一的显式触发前缀

## 安装

```bash
npx skills add statefulai/tech-report -g
```

## 使用

```
@report 分析下 src/utils/feishuClientAuth.ts
@report 分析 commit fc2d575
@report https://xxx.feishu.cn/docx/xxx
@report 分析 src/auth/ 的架构
```

## 工作流程

<p align="center">
  <img src="./assets/architecture.svg" alt="工作流程" width="720"/>
</p>

## 报告类型

tech-report 根据输入内容自动选择报告骨架（spine），每种骨架有预定义的章节顺序：

| 类型 | 触发条件 | 章节结构 |
|------|---------|---------|
| `tech_analysis` | 输入含文件路径 | 概述 → 架构 → 核心逻辑 → 数据流 → 问题与建议 → 总结 |
| `bug_fix` | 含 commit + fix 类型 diff | 问题描述 → 根因分析 → 修复方案 → 影响范围 → 验证 → 总结 |
| `changelog` | 含 commit + 功能/重构 diff | 变更概览 → 变更清单 → 重点详解 → 兼容性 → 总结 |
| `architecture` | 含"架构""设计"关键词 | 系统定位 → 架构总览 → 组件说明 → 数据流 → 设计决策 → 总结 |
| `document_review` | 含 URL | 文档概述 → 结构评估 → 内容准确性 → 完整性 → 改进建议 → 总结 |

## 插件系统

tech-report 本身只负责报告的结构和文字质量。图表、配图、外部数据等增强能力来自**你本地已安装的其他 AI skill**。

在 `plugins.yaml` 中注册你想用的 skill：

```yaml
plugins:
  - your-diagram-skill      # 任何能生成 SVG/PNG 图表的 skill
  - your-illustration-skill  # 任何能生成配图的 skill
  - your-data-source-skill   # 任何能读取外部数据（飞书、Notion 等）的 skill
```

tech-report 会读取每个 skill 的 `SKILL.md`，自动推断其能力类型（`diagram` / `illustration` / `data_source` / `browser`），在报告生成时按需调用。

**不注册任何插件也能用** — 输出纯文字 Markdown 报告，不包含图表。

## 支持的宿主

| 宿主 | 安装路径 | 使用方式 |
|------|---------|------|
| Copilot CLI | `~/.agents/skills/` | `@report` |
| Claude Code | `~/.claude/skills/` | `@report` |
| Codex | `~/.codex/skills/` | `@report` |

## 项目结构

```
tech-report/
├── SKILL.md                    # 核心 skill 指令
├── plugins.yaml                # 插件注册表（用户配置）
├── references/
│   ├── report-spines.md        # 报告骨架定义（5 种）
│   ├── section-archetypes.md   # 章节 Markdown 模板（10 种）
│   └── writing-dna.md          # 写作风格锁定
├── scripts/
│   └── resolve-plugins.py      # 插件能力解析
├── assets/                     # 封面与示意图
└── package.json
```

## License

MIT
