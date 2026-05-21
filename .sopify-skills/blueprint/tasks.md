# 蓝图路线图与待办

## 里程碑

### M0: Blueprint Finalization（当前）

完成蓝图三件套（background / design / tasks），闭合所有关键设计问题。

- 状态：进行中
- 交付物：background.md ✅ | design.md ✅ | tasks.md（本文） ✅
- 退出条件：所有开放设计问题有结论或明确延后

### M1: Skill Package MVP

最小可运行的 skill 包。tech-report 自身 = 报告排版 + 语言质量 skill，支持 plugins.yaml 注册外部 plugin。

- 前置：M0 ✅
- 状态：进行中
- 交付物：
  - `SKILL.md`（核心：排版+语言+编排逻辑+plugin调用指令）
  - `plugins.yaml`（用户配置：plugin 名列表，初始为空）
  - `scripts/resolve-plugins.py`（确定性逻辑：解析 plugins → 检查存在 → 推断能力 → 输出 JSON）
  - `references/report-spines.md`（输入类型 → 报告骨架）
  - `references/section-archetypes.md`（内容语义 → 章节结构）
  - `references/writing-dna.md`（写作风格锁定 + Markdown 规范）
  - `package.json`
  - `README.md`
- 退出条件：
  - 无 plugin 时：输入内容 → 输出纯 Markdown 报告（排版+语言质量达标）
  - 有 plugin 时：自动读 plugin SKILL.md 推断能力 → 调用 → 嵌入报告
  - 未安装的 plugin：跳过 + 报告末尾列出

### M2: 多宿主验证

在 Copilot CLI、Claude Code、Codex 上分别验证安装与触发流程。

- 前置：M1 ✅
- 状态：未开始
- 退出条件：至少 2 个宿主走通 install → trigger → report 全链路

### M3: 发布与文档

npm 包发布 + GitHub 仓库 + README + 使用文档。

- 前置：M1, M2 ✅
- 状态：未开始

## 开放项

### 设计问题（M0 已闭合 ✅）

| ID | 问题 | 决策 | 状态 |
|----|------|------|------|
| D1 | outline 生成后是否暂停确认？ | 默认不暂停，无 outline 中间产物 | ✅ 已确认 |
| D2 | 图表类型自动选择 vs 每次询问？ | 自动，按内容特征匹配规则表 | ✅ 已确认 |
| D3 | Session 回溯？ | 不做 session 回溯，只支持即时分析 | ✅ 已确认 |
| D4 | 报告模式是否允许用户自定义？ | 允许，references/ 下扩展 | ✅ 已确认 |
| D5 | 触发词风格？ | V1 只用 `@report` 前缀；自然语言触发留到 M2 | ✅ 已确认 |
| D6 | 降级信息展示方式？ | 终端 warn + 报告底部注脚 | ✅ 已确认 |
| D7 | 配置文件设计？ | 单一 plugins.yaml，纯 skill 名列表，能力自动推断 | ✅ 已确认 |
| D8 | tech-report 自身定位？ | 报告排版+语言质量 skill，中文优先 | ✅ 已确认 |
| D9 | 报告结构怎么确定？ | 三文件参考模型（spines + archetypes + writing-dna） | ✅ 已确认 |
| D10 | plugin 与 tech-report 关系？ | Plugin 是建议填充者，不改报告结构，调用契约驱动 | ✅ 已确认 |

### 技术验证（需在 M1 前完成）

| ID | 验证项 | 方法 |
|----|--------|------|
| V1 | 读 plugin SKILL.md description 推断能力可行性 | 测试 3-5 个不同 skill 的 description |
| V2 | 直接调用 plugin scripts/ 的兼容性 | 已验证 ✅（fireworks-tech-graph） |
| V3 | `npx skills add` 本地包安装 | 待验证 |

## 依赖关系

```
M0 (Blueprint)
 ↓
M1 (MVP: SKILL.md + plugins.yaml)
 ├── M2 (Multi-Host)
 └── M3 (Release)
```

## 明确延后项

| 项目 | 延后原因 | 复审触发 |
|------|---------|---------|
| HTML/PDF 输出格式 | MVP 只做 Markdown | 有用户需求时 |
| 报告在线编辑 | 不是 tech-report 的职责 | 永不 |
| 跨宿主 session 回溯 | 格式差异太大，成本高 | session 标准化协议出现时 |
| Skill 市场/分发 | 不是 tech-report 的职责 | 永不 |
| 多语言报告（i18n） | MVP 只做中文 | 有英文用户需求时 |
| CI/CD 集成（定时生成报告） | 需要 headless 运行支持 | 有自动化需求时 |
| 报告版本对比 | 需要 diff 机制 | M3 之后评估 |
| 能力映射配置（capability→skill） | 当前用推断足够 | 推断频繁失败时 |
| Pipeline 配置 | 编排逻辑内置于 SKILL.md | 用户有自定义管线需求时 |
| discover-capabilities 脚本 | 用 SKILL.md description 推断替代 | 推断机制不够用时 |
