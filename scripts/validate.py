#!/usr/bin/env python3
"""Structure & compliance validation for the ecommerce-price-hunt Skill.

No third-party dependencies. Run from anywhere:

    python scripts/validate.py

It only checks repository structure and the presence of mandatory compliance
text. It never contacts any e-commerce platform and never collects data.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ERRORS: list[str] = []
WARNINGS: list[str] = []


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def warn(condition: bool, message: str) -> None:
    if not condition:
        WARNINGS.append(message)


# ---------------------------------------------------------------- 1. files
REQUIRED_FILES = [
    "README.md",
    "README.en.md",
    "SKILL.md",
    "LICENSE",
    "LICENSE-DOCS.md",
    "NOTICE.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "CITATION.cff",
    "RELEASE_NOTES.md",
    "VERSION",
    ".gitignore",
    ".gitattributes",
    ".editorconfig",
    "references/platform-playbooks.md",
    "references/screen-reading.md",
    "references/pricing-method.md",
    "references/report-spec.md",
    "assets/report-skeleton.html",
    "docs/why-this-skill.md",
    "docs/portability.md",
    "docs/faq.md",
    "examples/prompt-examples.md",
    "examples/sample-session.md",
    "scripts/validate.py",
    "scripts/pack.py",
    "scripts/pack.sh",
    "scripts/publish.sh",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/validate.yml",
]
for rel in REQUIRED_FILES:
    require((ROOT / rel).is_file(), f"缺少必需文件: {rel}")

if ERRORS:
    for e in ERRORS:
        print(f"ERROR  {e}")
    sys.exit(1)


# ------------------------------------------------- 2. SKILL.md frontmatter
skill = read("SKILL.md")
require(skill.startswith("---\n"), "SKILL.md 缺少 YAML frontmatter（必须是文件第一段）")
fm = skill.split("---", 2)[1] if skill.startswith("---\n") else ""
require(re.search(r"^name:\s*\S+", fm, re.M) is not None, "frontmatter 缺少 name")
require(re.search(r"^description:\s*\S+", fm, re.M) is not None, "frontmatter 缺少 description")


# -------------------------------------------- 3. referenced local files exist
refs = set()
for rel in re.findall(r"`([^`]+)`", skill):
    rel = rel.strip()
    if rel.startswith(("references/", "docs/", "assets/", "examples/")) and rel.endswith(
        (".md", ".html")
    ):
        refs.add(rel.split("#")[0])
    elif rel in ("README.md", "LICENSE", "LICENSE-DOCS.md", "NOTICE.md", "CHANGELOG.md"):
        refs.add(rel)
for rel in sorted(refs):
    require((ROOT / rel).is_file(), f"SKILL.md 引用了不存在的文件: {rel}")


# ------------------------------------------------- 4. markdown relative links
link_re = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
for md in sorted(ROOT.rglob("*.md")):
    rel_md = md.relative_to(ROOT).as_posix()
    if any(part in {".git", "dist", "node_modules"} for part in md.parts):
        continue
    text = md.read_text(encoding="utf-8")
    for target in link_re.findall(text):
        target = target.strip().split(" ")[0]
        if not target or target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target = target.split("#")[0]
        if not target:
            continue
        resolved = (md.parent / target).resolve()
        require(resolved.exists(), f"{rel_md} 中的相对链接失效: {target}")


# --------------------------------------------------- 5. mandatory compliance
DSH_GO_URL = "https://github.com/ccch1mneyyy/dsh-go/"
DISCLAIMER_ZH = "不得用于药品广告"
DISCLAIMER_EN = "medicine advertising"

readme = read("README.md")
readme_en = read("README.en.md")
notice = read("NOTICE.md")
release_notes = read("RELEASE_NOTES.md")

for name, text in (("README.md", readme), ("README.en.md", readme_en), ("NOTICE.md", notice)):
    require(DSH_GO_URL in text, f"{name} 缺少 DSH go 原仓库地址")
for name, text in (("README.md", readme), ("SKILL.md", skill), ("RELEASE_NOTES.md", release_notes)):
    require(DISCLAIMER_ZH in text, f"{name} 缺少药品专项用途限制（免责声明）")
require(DISCLAIMER_EN in readme_en, "README.en.md 缺少英文版免责声明")
require("附属" in readme[:1200], "README.md 开头未声明「DSH go 附属功能」")
require(("ancillary" in readme_en[:1200] or "附属" in readme_en[:1200]),
        "README.en.md 开头未声明 ancillary project")
require("非官方" in notice or "不是" in notice, "NOTICE.md 缺少非官方/独立作品声明")
require("CC BY-NC-SA 4.0" in readme, "README.md 缺少文档许可说明")
require("MIT" in readme, "README.md 缺少代码许可说明")


# ------------------------------------------------------- 6. sample data safety
skeleton = read("assets/report-skeleton.html")
require("虚构" in skeleton, "report-skeleton.html 未标注示例数据为虚构")
require("echarts.min.js" not in re.findall(r'<script[^>]+src="([^"]+)"', skeleton),
        "report-skeleton.html 仍引用了未捆绑的本地 echarts.min.js")
require("<head>" in skeleton and "</head>" in skeleton, "report-skeleton.html 缺少 head 段")


# ------------------------------------------------------------ 7. secret scan
secret_re = re.compile(r"\bghp_[A-Za-z0-9]{20,}\b|\bgitee_[A-Za-z0-9]{20,}\b")
for path in sorted(ROOT.rglob("*")):
    if not path.is_file():
        continue
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith((".git/", "dist/")) or path.suffix in {".zip", ".png", ".jpg", ".webp"}:
        continue
    try:
        body = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    require(secret_re.search(body) is None, f"{rel} 疑似包含明文访问令牌")


# --------------------------------------------------------------- 8. version
version = read("VERSION").strip()
require(re.fullmatch(r"\d+\.\d+\.\d+", version) is not None, "VERSION 不是 x.y.z 格式")
require(f"[{version}]" in read("CHANGELOG.md"), f"CHANGELOG.md 缺少 {version} 条目")
warn(f"v{version}" in release_notes or version in release_notes,
     "RELEASE_NOTES.md 未写出版本号")


# ------------------------------------------------------------------- report
for w in WARNINGS:
    print(f"WARN   {w}")
for e in ERRORS:
    print(f"ERROR  {e}")
if ERRORS:
    print(f"\n校验失败：{len(ERRORS)} 个错误。")
    sys.exit(1)
print(f"校验通过：{len(REQUIRED_FILES)} 个必需文件、{len(refs)} 个 Skill 引用、"
      f"版本 {version}，无错误。")
