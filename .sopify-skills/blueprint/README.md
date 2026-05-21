# 蓝图索引

状态: M1 骨架阶段
项目: tech-report — 报告排版与语言质量 Skill

## 当前目标

- 维护已落地的骨架与执行口径
- 收敛残留矛盾，补齐实现前的最小约束

## 当前焦点

- 蓝图三件套：background ✅ | design ✅ | tasks ✅
- 参考文件已落地：report-spines / section-archetypes / writing-dna
- 继续修正文档口径与脚本边界，避免前后矛盾

## 核心设计方向

- **定位**：报告排版 + 语言质量 skill（中文优先），不是编排框架
- **配置**：单一 plugins.yaml（纯 skill 名列表），不绑定任何具体 skill
- **推断**：读已注册 plugin 的 SKILL.md description 自动推断能力类型
- **降级**：未安装 plugin 跳过 + 报告末尾告知
- **脚本**：`scripts/resolve-plugins.py` 只负责插件解析，编排逻辑仍在 SKILL.md 中

## 阅读入口

- [背景与目标](./background.md) — 为什么做、核心价值、使用场景
- [架构与契约](./design.md) — 插件注册、能力推断、宿主适配、输出规范
- [路线图与待办](./tasks.md) — 里程碑 M0-M3、D1-D8 决策表、延后项
