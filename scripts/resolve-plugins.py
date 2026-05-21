#!/usr/bin/env python3
import argparse
import json
import os
import re
from pathlib import Path


CAPABILITY_PATTERNS = [
    ("diagram", re.compile(r"\b(diagram|svg|chart|graph|flow|architecture|sequence)\b|图表|画图", re.I)),
    ("illustration", re.compile(r"\b(sketch|illustration|cover|image|pict|ppt)\b|配图|手绘|插画", re.I)),
    ("data_source", re.compile(r"\b(fetch|feishu|lark|notion|wiki|api|http|url)\b|文档|数据源", re.I)),
    ("browser", re.compile(r"\b(browser|screenshot|网页|截图|dom)\b", re.I)),
]


def load_plugin_names(path: Path) -> list[str]:
    if not path.exists():
        return []
    names: list[str] = []
    in_plugins = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if line.strip() == "plugins:":
            in_plugins = True
            continue
        if not in_plugins:
            continue
        match = re.match(r"^\s*-\s*(.+?)\s*$", line)
        if match:
            names.append(match.group(1))
    return names


def read_skill_description(skill_dir: Path) -> str:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return ""
    lines = skill_file.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return skill_file.read_text(encoding="utf-8")

    desc_lines: list[str] = []
    in_desc = False
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if in_desc:
            if line.startswith((" ", "\t")):
                desc_lines.append(line.strip())
                continue
            if not line.strip():
                continue
            in_desc = False
        if line.startswith("description:"):
            value = line.split(":", 1)[1].strip()
            if value in {">", ">-", "|", "|-"}:
                in_desc = True
                continue
            if value:
                desc_lines.append(value)
    return " ".join(desc_lines).strip()


def infer_capability(description: str) -> str | None:
    if not description:
        return None
    for capability, pattern in CAPABILITY_PATTERNS:
        if pattern.search(description):
            return capability
    return None


def resolve_skill_dir(name: str) -> Path | None:
    roots = [
        Path.home() / ".agents" / "skills",
        Path.home() / ".claude" / "skills",
        Path.home() / ".codex" / "skills",
    ]
    for root in roots:
        candidate = root / name
        if (candidate / "SKILL.md").exists():
            return candidate
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plugins-file", default="plugins.yaml")
    parser.add_argument("--skills-root", default=None, help="override skills root for tests")
    args = parser.parse_args()

    plugins_file = Path(args.plugins_file).expanduser().resolve()
    names = load_plugin_names(plugins_file)
    skills_root = Path(args.skills_root).expanduser().resolve() if args.skills_root else None

    available = []
    missing = []
    unknown = []

    for name in names:
        skill_dir = resolve_skill_dir(name) if skills_root is None else (skills_root / name if (skills_root / name / "SKILL.md").exists() else None)
        if skill_dir is None:
            missing.append(name)
            continue
        description = read_skill_description(skill_dir)
        capability = infer_capability(description)
        if capability is None:
            unknown.append(name)
            continue
        available.append({
            "name": name,
            "capability": capability,
            "path": str(skill_dir),
        })

    print(json.dumps({
        "available": available,
        "missing": missing,
        "unknown": unknown,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
