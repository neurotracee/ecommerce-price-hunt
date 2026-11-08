#!/usr/bin/env python3
"""Build the installable Skill zip (no third-party dependencies).

    python scripts/pack.py [version]

The archive contains a single top-level directory `ecommerce-price-hunt/` that
can be copied straight into an Agent's skills folder. GitHub/Gitee metadata
(.github/, CI, publishing scripts) is intentionally excluded.
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_arg_version = sys.argv[1].strip() if len(sys.argv) > 1 else ""
VERSION = _arg_version or (ROOT / "VERSION").read_text(encoding="utf-8").strip()
NAME = "ecommerce-price-hunt"
OUT_DIR = ROOT / "dist"
OUT_DIR.mkdir(exist_ok=True)
OUT = OUT_DIR / f"{NAME}-v{VERSION}.zip"

INCLUDE = [
    "SKILL.md",
    "README.md",
    "README.en.md",
    "LICENSE",
    "LICENSE-DOCS.md",
    "NOTICE.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "RELEASE_NOTES.md",
    "CITATION.cff",
    "VERSION",
]
INCLUDE_DIRS = [
    "references",
    "assets",
    "docs",
    "examples",
]

INSTALL_TXT = f"""ecommerce-price-hunt v{VERSION}
========================================

这是为 DSH go 做的一个附属功能的开源项目。
上游原仓库: https://github.com/ccch1mneyyy/dsh-go/
本项目不是 DSH go 的官方组件，不含上游代码，独立发布、独立授权。

安装（推荐：让 DSH 自己装）
----------------------------
1. 把压缩包文件本身直接发给 DSH（拖进对话框 / 作为附件上传），这一步最稳。
   也可以把下载链接发给 AI 让它自己取；能否顺利取到因宿主与网络而异
   （登录墙、跳转、限流、人机验证都可能卡住），卡住了就改为手动下载。
2. 对 AI 说这一句：
       帮我安装它到本地目录即可，我要把它添加进来。
   DSH 会自己解压并把 ecommerce-price-hunt/ 放进本地技能目录，装完回报路径。
3. 之后说「开始针对〈品牌 商品 规格〉做全网比价，出 HTML 报告，
   我收货地在〈省 市〉」即可触发本 Skill。

手动安装（换其它宿主时才需要）
--------------------------------
    mkdir -p ~/.dsh/skills
    cp -r ecommerce-price-hunt ~/.dsh/skills/
目录映射见 docs/portability.md。

免责声明（与 SKILL.md 一致）
----------------------------
本项目是一份「比价作业指导书」：只有提示词和操作手册，不含任何自动化脚本、
破解工具或接口逆向代码。仅供个人在自有设备上、用自己的账号、以人工浏览方式核对价格。
禁止用于群控、刷单、抢购、批量爬取、抓取个人信息、对外商业比价服务或价格宣传。
不绕过验证码、风控、应用锁或加密接口；遇到一律回到人工。

【药品专项】比价结果仅供个人参考；不得用于药品广告、价格宣传、诊疗建议，
也不得据此发布对外比价榜单。药品购买与使用请遵医嘱或药师指导。

本项目仅提供比价方法，不构成用药、购买或投资建议；价格信息具有时效性，
作者不对因使用本项目产生的任何直接或间接损失负责。仅供个人学习与研究，
不构成法律意见，商用前请咨询律师。

许可（任何二次开发、商用或借用均可，但必须署名）
----------------------------------------------
文档/提示词：CC BY-SA 4.0（允许商用；须署名并标注源仓库地址、注明是否修改、相同方式共享）。
代码/模板：MIT。

必须标注以下两个仓库地址，并说明二者由同一作者管理：
    https://github.com/neurotracee/ecommerce-price-hunt
    https://gitee.com/bio234/ecommerce-price-hunt
    （以上两个仓库由同一作者管理；GitHub 为主仓库，Gitee 为国内镜像）

协议 ≠ 用途：授权放开的是版权层面的使用方式，上面列出的用途限制依然有效，
不因允许商用而失效。完整条款见 NOTICE.md 与 LICENSE-DOCS.md。

作者与制作方式
--------------
作者创建本仓库时为初中生；Skill 提示词由 DSH GO 的 deepseek 作者自购 API 的
DeepSeek V4.1 Flash 1017 版，根据作者反馈与实际模型表现处理并正式优化，最终总结归纳生成；
开源编写与仓库构建由腾讯 WorkBuddy 的 Hy4 与 DeepSeek V4.1 Flash 1017 版分别负责
（部分工作有具体分工）；作者负责指令、监督、反馈与创意想法。
仓库首个构建日期：2026 年 11 月。
"""

files: list[Path] = []
for rel in INCLUDE:
    p = ROOT / rel
    if p.is_file():
        files.append(p)
for d in INCLUDE_DIRS:
    base = ROOT / d
    if base.is_dir():
        files.extend(sorted(p for p in base.rglob("*") if p.is_file()))

missing = [rel for rel in INCLUDE if not (ROOT / rel).is_file()]
if missing:
    raise SystemExit(f"打包失败，缺少文件: {missing}")

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for p in sorted(set(files)):
        z.write(p, f"{NAME}/{p.relative_to(ROOT).as_posix()}")
    z.writestr(f"{NAME}/INSTALL.txt", INSTALL_TXT.encode("utf-8"))

print(f"{OUT}  ({OUT.stat().st_size} bytes, {len(set(files)) + 1} files)")
