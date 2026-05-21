---
name: tech-report
description: 从代码、commit diff、文档链接、架构描述等技术输入，自动生成结构化中文技术报告。Trigger on: "@report".
---

# tech-report

## 作用

将技术输入转换为结构清晰、语言专业的中文技术报告。

## 执行约定

- 仅在输入以 `@report` 开头时激活。
- 先运行 `scripts/resolve-plugins.py` 解析 `plugins.yaml`，得到 `available / missing / unknown`。
- 再按输入类型选 `report-spines.md`，用 `section-archetypes.md` 套模板；`writing-dna.md` 始终全程生效，不是最后一步。
- `diagram` 和 `illustration` 只有在能力可用且内容确实需要时才使用。
- 缺少能力就降级：省略对应 slot，继续输出纯 Markdown 报告；`missing` 和 `unknown` 只在生成信息里列出。
- 报告默认写入 `reports/{YYYY-MM-DD}_{spine_type}_{slug}/report.md`，图片放同目录 `assets/`。
- 不要求用户安装特定 skill 名，`plugins.yaml` 只写已注册 skill 名。

## 参考

- `references/report-spines.md`
- `references/section-archetypes.md`
- `references/writing-dna.md`
