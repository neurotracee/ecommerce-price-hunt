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

for name, text in (("README.md", readme), ("NOTICE.md", notice), ("RELEASE_NOTES.md", release_notes)):
    require(DSH_GO_URL in text, f"{name} 缺少 DSH go 原仓库地址")
for name, text in (("README.md", readme), ("SKILL.md", skill), ("RELEASE_NOTES.md", release_notes)):
    require(DISCLAIMER_ZH in text, f"{name} 缺少药品专项用途限制（免责声明）")
require(DISCLAIMER_EN in readme, "README.md 英文部分缺少英文版免责声明")
require("附属" in readme[:1500], "README.md 开头未声明「DSH go 附属功能」")
require("ancillary" in readme, "README.md 英文部分未声明 ancillary project")
require("非官方" in notice or "不是" in notice, "NOTICE.md 缺少非官方/独立作品声明")
require("CC BY-SA 4.0" in readme, "README.md 缺少文档许可说明")
require("MIT" in readme, "README.md 缺少代码许可说明")


# ------------------------------------- 5a. dual-repo attribution (mandatory)
GH_REPO = "https://github.com/neurotracee/ecommerce-price-hunt"
GITEE_REPO = "https://gitee.com/bio234/ecommerce-price-hunt"
for name, text in (("README.md", readme), ("NOTICE.md", notice), ("RELEASE_NOTES.md", release_notes),
                   ("LICENSE-DOCS.md", read("LICENSE-DOCS.md"))):
    require(GH_REPO in text, f"{name} 缺少 GitHub 源仓库地址")
    require(GITEE_REPO in text, f"{name} 缺少 Gitee 源仓库地址")
# LICENSE 必须保持标准 MIT 原文，多余内容会让平台把许可识别成 NOASSERTION
require("github.com" not in read("LICENSE"), "LICENSE 不应写入额外内容（会破坏平台对 MIT 的自动识别）")
for name, text in (("README.md", readme), ("NOTICE.md", notice), ("RELEASE_NOTES.md", release_notes)):
    require("同一作者" in text or "same author" in text,
            f"{name} 未说明两个仓库由同一作者管理")
require("注明是否修改" in notice, "NOTICE.md 缺少「注明是否修改」要求")
require("ShareAlike" in notice or "相同方式共享" in notice, "NOTICE.md 缺少 ShareAlike 说明")


# ------------------------------------------- 5a2. author & build statement
for name, text in (("README.md", readme), ("RELEASE_NOTES.md", release_notes)):
    require("初中生" in text, f"{name} 缺少「作者创建仓库时为初中生」声明")
    require("2026 年 11 月" in text, f"{name} 缺少仓库首个构建日期（精确到月份）")
    require("DeepSeek V4.1 Flash 1017" in text, f"{name} 缺少提示词所用模型版本")
    require("Hy4" in text, f"{name} 缺少 WorkBuddy Hy4 贡献说明")
require("协议 ≠ 用途" in readme or "协议≠用途" in readme,
        "README.md 缺少「协议≠用途」提示")
require("协议 ≠ 用途" in skill or "协议≠用途" in skill,
        "SKILL.md 缺少「协议≠用途」提示")


# ------------------------------------------- 5a3. bilingual anchor layout
require("[English](#english)" in readme, "README.md 缺少 English 锚点跳转")
require("^# English" in readme or "\n# English" in readme, "README.md 英文部分缺少一级标题")
require(("\n# English" in readme) and ("[中文](#" in readme), "README.md 英文部分缺少回跳中文的锚点")
_en_idx = readme.find("\n# English")
require(_en_idx > len(readme) * 0.25,
        "README.md 英文部分应放在中文内容之后（中文在上、英文在下）")
require("允许商用" in readme, "README.md 未明确「允许商用」")
for _line in readme.splitlines():
    if "CC BY-NC-SA" in _line:
        require(("此前版本" in _line) or ("Earlier versions" in _line),
                "README.md 仍在用 CC BY-NC-SA 作为当前授权（应已改为 CC BY-SA 4.0）")


# ------------------------------------------- 5b. one-sentence install flow
INSTALL_PROMPT = "帮我安装它到本地目录即可，我要把它添加进来"
for name, text in (("README.md", readme), ("README.en.md", readme_en),
                   ("RELEASE_NOTES.md", release_notes)):
    require(INSTALL_PROMPT in text, f"{name} 缺少「一句话安装」提示词")
require(INSTALL_PROMPT in readme[:6000],
        "README.md 开头部分未给出「一句话安装」提示词")
require("给文件，不给链接" in readme, "README.md 缺少「给文件，不给链接」说明")
require("不要把下载链接发给 AI" in release_notes,
        "RELEASE_NOTES.md 缺少「不要把下载链接发给 AI」说明")
require(INSTALL_PROMPT in read("scripts/pack.py"),
        "pack.py 生成的 INSTALL.txt 缺少「一句话安装」提示词")
for name in ("docs/faq.md", "examples/prompt-examples.md", "docs/portability.md"):
    require(INSTALL_PROMPT in read(name), f"{name} 缺少「一句话安装」提示词")


# ------------------------------------------- 5c. license & upstream metadata
lic = read("LICENSE")
require(lic.startswith("MIT License"), "LICENSE 不是标准 MIT 文本，平台无法识别许可证")
require(lic.rstrip().endswith("SOFTWARE."),
        "LICENSE 末尾有多余内容，平台会把 MIT 误判为 Other")
require("CC BY-NC-SA" not in lic,
        "LICENSE 不应混入文档许可说明（会破坏平台对 MIT 的自动识别）")
require("代码与模板是 MIT" in readme, "README.md 缺少「代码与模板是 MIT」的双许可说明")
require("code and templates are MIT" in readme,
        "README.md 英文部分缺少「code and templates are MIT」说明")
require("CC BY-SA 4.0" in read("LICENSE-DOCS.md"), "LICENSE-DOCS.md 未声明 CC BY-SA 4.0")
require("Attribution-ShareAlike 4.0 International" in read("LICENSE-DOCS.md"),
        "LICENSE-DOCS.md 缺少 CC BY-SA 4.0 官方法律文本")
require("deepseek-harness" in read("CITATION.cff"),
        "CITATION.cff 缺少 deepseek-harness 关键词")
require("DeepSeek Harness" in notice, "NOTICE.md 缺少上游 DeepSeek Harness 说明")
require("deepseek-harness" in read("scripts/publish.sh"),
        "发布脚本默认标签缺少 deepseek-harness")


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
