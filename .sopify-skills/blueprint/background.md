# 蓝图背景与目标

## tech-report 是什么

tech-report 是一个**报告排版与语言质量 Skill**。它的核心能力是：

> **将技术分析内容转化为结构清晰、语言专业的中文技术报告，并根据用户注册的本地 plugin 自动增强报告内容（图表、配图等）。**

### 核心价值

| 价值 | 说明 |
|------|------|
| **排版与语言** | tech-report 自身就是报告写作专家：结构化、专业术语、可读性 |
| **Plugin 注册制** | 用户在 plugins.yaml 中注册想用的 skill，不绑定任何具体 skill |
| **能力自动推断** | 读已注册 plugin 的 SKILL.md description，推断其能力类型 |
| **优雅降级** | 没装 plugin 也能输出纯文字报告；缺少的 plugin 末尾告知 |
| **一键触发** | 统一使用 `@report` 显式前缀触发，无需手动拆步骤 |

### 产品定位

tech-report **不是**：
- ❌ 报告编辑器 — 它只生成，不提供编辑能力
- ❌ Skill 分发平台 — 它消费已安装的 skill，不管理安装
- ❌ 图表生成器 — 图表能力来自用户注册的 plugin skill
- ❌ AI agent 框架 / 编排引擎 — 它是一个 Skill，不是框架
- ❌ 绑定特定 skill — SKILL.md 中不硬编码任何 plugin 名

tech-report **是**：
- ✅ 报告排版 + 语言质量 skill（中文优先）
- ✅ Plugin 增强层 — 注册的 plugin 存在则调用，不存在则跳过
- ✅ 降级层 — 缺什么能力就降级对应内容，末尾告知用户

## 使用场景

### 场景 1：即时分析报告
```
用户：@report 分析下 src/utils/feishuClientAuth.ts
→ 读代码 → 提炼分析 → 调用已注册的图表 plugin 生成架构图 → 组装报告
```

### 场景 2：Bug Fix 修复分析
```
用户：@report 分析 commit fc2d575
→ 读 commit diff → 识别 bug 根因 → 调用图表 plugin 生成前后对比图 → 输出修复分析报告
```

报告包含：问题现象、根因链路（配图：对比图/流程图）、修复内容、影响范围。

### 场景 3：Commit 变更分析
```
用户：@report 这个 commit 的变更报告
→ 读 diff → 分类变更（功能/修复/重构）→ 生成变更清单
```

### 场景 4：架构文档
```
用户：@report 分析 aiBridge 的架构
→ 代码分析 → 调用图表 plugin 生成架构图 + 数据流图 → 完整设计文档
```

### 场景 5：外部文档 → 完整报告（plugin 联动）
```
用户：@report <url>
→ 调用数据源 plugin 拉取文档内容
→ 分析内容结构，识别需要图表/配图的章节
→ 调用图表 plugin 生成技术架构图
→ 调用插画 plugin 生成封面/配图（如可用）
→ AI 写报告，在对应位置插入图片引用
→ 输出到 reports/ 文件夹（report.md + images/）
```

此场景展示 tech-report 的核心价值：用户只需一句话，tech-report 根据已注册且已安装的 plugin 自动编排多步骤生成。未安装的 plugin 自动跳过，报告末尾告知用户。

## 当前现实

截至 2026-05-21：

- **状态**：M1 骨架已落地，完整报告生成仍待实现
- **设计简化演进**：
  - 初版：config.yaml（registry + pipeline） + discover-capabilities.py + assemble-report.py + outline.json → 过度工程
  - 批判后精简：plugins.yaml（纯 skill 名列表） + SKILL.md 内置编排 + AI 直接写 Markdown
  - 核心认知：tech-report 的价值 = 报告 Recipe 可复用可分享 + 排版语言质量
- **前序分析结论**：
  - Skill 嵌套调用受限 → 解法：直接调用 plugin 的 `scripts/`
  - `npx skills add` 安装全能力（scripts/references/templates 全部拷贝）
  - 不同宿主无统一 slash → 解法：靠 SKILL.md description 关键词匹配
  - 不绑定具体 skill → 解法：plugins.yaml 注册制 + 能力自动推断

## 本蓝图的定位

- `background.md`（本文）：为什么做、核心价值、使用场景
- `design.md`：架构分层、能力注册、管线设计、宿主适配
- `tasks.md`：路线图 + 开放设计问题 + 延后项

## 非目标

- 不重新实现任何被依赖 skill 的核心能力
- 不做 skill 安装/分发/版本管理
- 不做报告在线编辑/协作
- 不绑定特定宿主（Copilot/Claude/Codex 均应可用）
- 不在蓝图阶段写实现代码
