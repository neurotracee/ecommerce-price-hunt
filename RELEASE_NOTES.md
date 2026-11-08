# v1.3.0 · ecommerce-price-hunt

**中文** | [English](#english)

> **这是为 [DSH go](https://github.com/ccch1mneyyy/dsh-go/) 做的一个附属功能的开源项目。**
> 上游原仓库：<https://github.com/ccch1mneyyy/dsh-go/>
> 本项目**不是** DSH go 的官方组件，不隶属于上游项目，也不包含、不复制上游的任何代码；独立发布、独立授权。

## 本次发布：技能自带版本自检与升级提示

- `SKILL.md` 末尾新增**「版本自检与升级提示」**：每次比价任务**交付完成之后**，自动查一次远端版本，并在输出结尾固定追加一行版本状态（当前版本 · 远端最新 · 是否最新）。
- 检查顺序固定：**先完成任务 → 再读本地 `VERSION` → 优先查 Gitee**（`VERSION` raw，失败回退 `releases/latest`）→ GitHub 兜底；每级只试一次，查不到就写「未查到」，不猜、不循环重试。
- 落后时只多说 3–5 行：**版本差距** + **一到两句话说明本次主要改了什么**（依据 `CHANGELOG.md`）+ **主动问是否一键升级**，并同时给出两端 Release 下载直链。
- 升级约定：先改名**备份**原技能目录；自动下载失败一次即停、把决定权交回用户；升完核对 `VERSION`；只有维护者本人或用户明确要求时才同步远端页面。
- `SKILL.md` 新增**「越界请求怎么答（安全边界）」**：群控、刷单、抢购、批量爬取、抓取个人信息、绕过验证码/风控/应用锁、代下单等一律**拒绝执行**，只给合规替代，**不提供任何变通方案**；拒绝时固定附一句风险提示（可能违反平台协议与法律，后果由使用者自行承担，**与本项目及作者无关**），并建议理性慎重评估。
- `SKILL.md` 末尾新增**简版作者声明**（上游归属、作者身份、提示词与仓库构建分工、首个构建月份、双许可要点），用最少 token 承载合规信息；完整版仍在 `README.md` / `NOTICE.md`。
- 本轮不改变比价方法与任何用途限制；文档/提示词仍为 CC BY-SA 4.0、代码/模板仍为 MIT，「协议 ≠ 用途」继续有效。

## 作者与制作方式

- **作者在创建本仓库时为初中生。**
- **Skill 提示词**由 **DSH GO 的 deepseek 作者自购 API 的 DeepSeek V4.1 Flash 1017 版**，根据作者的反馈与实际模型表现处理并正式优化，最终总结归纳生成。
- **开源编写与仓库构建**：由 **腾讯 WorkBuddy 的 Hy4** 与 **DeepSeek V4.1 Flash 1017 版** 分别负责（部分工作有具体分工）。
- **作者负责**：指令、监督、反馈与创意想法。
- **仓库首个构建日期：2026 年 11 月。**
- **维护节奏**：刚发布阶段可能较频繁更新与响应，之后转为**低频维护**（大约一两个月看一两次），不承诺即时响应；作者为初中生，具体原因不作解释。
- **药品专项**：由作者与 DeepSeek 专项优化调试，重点是避免把「国药准字」的正规药品买成食字号 / 妆字号 / 消字号 / 健字号 / 械字号产品。

## 授权与署名规范（硬要求）

**两个仓库地址（同一作者管理，转载/衍生必须两个都写）：**

```
https://github.com/neurotracee/ecommerce-price-hunt
https://gitee.com/bio234/ecommerce-price-hunt
（以上两个仓库由同一作者管理；GitHub 为主仓库，Gitee 为国内镜像）
```

1. **必须署名并标注上述两个仓库地址**，并说明二者由同一作者管理；
2. **必须注明是否修改**，且不得暗示原作者为你的版本背书；
3. 文档类衍生作品须以 **CC BY-SA 4.0**（或兼容许可）发布（ShareAlike）。

> ⚠️ **协议 ≠ 用途。** 授权允许商用，但下文用途限制与 `SKILL.md` 硬规则**依然有效**，不因商用授权而失效。

## ⚠️ 免责声明（与 `SKILL.md` 一致，原文收录）

> **用途声明**
> 本项目是一份「比价作业指导书」：**只有提示词和操作手册，不含任何自动化脚本、破解工具或接口逆向代码**。设计给个人在自有设备上、用自己的账号、以人工浏览的方式核对价格使用。**禁止**用于群控、刷单、抢购、批量爬取、抓取个人信息、对外商业比价服务或价格宣传。本项目**不绕过**验证码、风控、应用锁或加密接口；遇到这些一律回到人工。仅供学习与个人研究，**不构成法律意见**，商用或大范围传播前请自行咨询律师。

> **【药品专项】用途限制**（摘自 `SKILL.md`，目标为药品时强制生效）
> - 比价结果仅供个人参考；**不得用于药品广告、价格宣传、诊疗建议，也不得据此发布对外比价榜单**。
> - 本技能的输出仅供个人参考：**不得用于药品广告、价格宣传、诊疗建议或对外发布的比价榜单**；药品购买与使用请遵医嘱或药师指导。
> - 闸门三条件：国药准字 + 字母 + 8 位数字；有 OTC 或 RX 标识；剂型与通用名对得上。三者齐全才进表；查不到文号写「未核实」，不编造。

> 本项目仅提供比价方法，不构成用药、购买或投资建议；价格信息具有时效性，作者不对因使用本项目产生的任何直接或间接损失负责。请遵守各平台用户协议与相关法律法规。

## 安装：下载压缩包 → 直接发给 DSH → 一句话装好

**不用 clone 仓库，不用敲命令，也不用翻到别的页面或章节找说明。**

1. **直接把压缩包下载下来**（`ecommerce-price-hunt-v1.3.0.zip`）：
   - GitHub：<https://github.com/neurotracee/ecommerce-price-hunt/releases/download/v1.3.0/ecommerce-price-hunt-v1.3.0.zip>
   - Gitee（国内更快）：<https://gitee.com/bio234/ecommerce-price-hunt/releases/download/v1.3.0/ecommerce-price-hunt-v1.3.0.zip>
2. **把 zip 交给 DSH**：最稳的是把下载到的文件本身拖进对话框或作为附件上传；也可以直接把下载链接发给它、让它自己去取。
   能不能顺利取到**取决于宿主能力和网络环境**（登录墙、跳转中转页、限流、人机验证都可能卡住，反复重试会白花时间与 token），卡住了就停下改手动下载——因人而异，不做一刀切。
3. 对它说这一句（可直接复制）：

   > 帮我安装它到本地目录即可，我要把它添加进来。

DSH 会自己解压、把 `ecommerce-price-hunt/` 放进本地技能目录，装完把路径告诉你。之后直接说「开始针对〈品牌 商品 规格〉做全网比价，出 HTML 报告，我收货地在〈省 市〉」即可触发。

手动安装（一般用不到，换其它宿主时才需要）：

```bash
mkdir -p ~/.dsh/skills
cp -r ecommerce-price-hunt ~/.dsh/skills/
```

## 包含内容

- `SKILL.md`：品类判定、采集流程、口径、药品专项、硬规则、按需加载表、交付检查
- `references/`：平台实录、读屏坑与对策、单价/实付口径、报告章节与双屏自检
- `assets/report-skeleton.html`：只含比价章节的 HTML 骨架（示例数据全部虚构）
- `README.md`（中英双语，中文在上）/ `README.en.md`（指向英文段）/ `NOTICE.md`（授权与署名规范）
- `LICENSE`（MIT）/ `LICENSE-DOCS.md`（CC BY-SA 4.0 全文）
- `docs/` / `examples/`：设计说明、宿主移植、FAQ、触发话术与流程示例
- 开源治理文件：CONTRIBUTING / CODE_OF_CONDUCT / SECURITY / CHANGELOG / CITATION.cff / Issue 与 PR 模板 / CI 校验

完整变更见 [CHANGELOG.md](CHANGELOG.md)。

## 许可

| 内容 | 许可 |
| --- | --- |
| 文档与提示词（`README*`、`SKILL.md`、`references/`、`docs/`、`examples/`、`NOTICE.md`） | **CC BY-SA 4.0**（署名 + 标明修改 + 相同方式共享，允许商用） |
| 代码与模板（`scripts/`、`assets/`） | **MIT** |

- 平台侧栏自动识别的 **MIT 仅覆盖代码与模板**，请勿当成整个项目的授权。
- 必须标注两个仓库地址并说明同一作者管理，写法见 `NOTICE.md`。
- 上游 DSH go 采用 AGPL-3.0；本项目为独立作品、独立授权，不含其代码，也不代表 upstream 立场。

---

**仅供学习与研究参考。完整免责声明见仓库 `README.md` 开头与 `SKILL.md`。**

---

# English

[中文](#v130--ecommerce-price-hunt) | **English**

> **This is an open-source project for an ancillary feature built for [DSH go](https://github.com/ccch1mneyyy/dsh-go/).**
> Upstream repository: <https://github.com/ccch1mneyyy/dsh-go/>
> This is **not** an official DSH go component, is not affiliated with the upstream project, and contains or copies **no upstream code**. Independently published, independently licensed.

## This release: the Skill now checks its own version and tells you about updates

- `SKILL.md` gains a **"version self-check"** section at the end: **after the comparison task is delivered**, it checks the remote version once and appends a single fixed line to the output (current version · latest version · up to date or not).
- Fixed order: **finish the task → read the local `VERSION` → check Gitee first** (`VERSION` raw, falling back to `releases/latest`) → GitHub as a last resort. One attempt per source; if all fail it says "not checked" instead of guessing or looping.
- When out of date it adds only 3–5 lines: **the version gap**, **one or two sentences on what changed** (from `CHANGELOG.md`), and **an offer to upgrade**, together with the direct Release download links for both platforms.
- Upgrade rules: **back up** the existing skill folder by renaming first; stop after the first failed automatic download and leave the decision to the user; verify `VERSION` afterwards; sync remote pages only when the maintainer themselves or the user explicitly asks.
- `SKILL.md` gains an **"out-of-scope requests" (safety boundary) section**: device farms, fake orders, flash-sale grabbing, bulk scraping, harvesting personal data, bypassing CAPTCHAs / risk controls / app locks, and placing orders on someone's behalf are **refused**, with compliant alternatives only and **no workarounds of any kind**. Every refusal carries a fixed risk notice (possible breach of platform terms and the law; the user bears the consequences, **unrelated to this project or its author**) and advises a calm, careful decision.
- A **condensed author statement** is appended to `SKILL.md` (upstream provenance, author identity, how prompts and the repository were produced, first build month, dual-license essentials) — the full version stays in `README.md` / `NOTICE.md`.
- The comparison method and every usage restriction are unchanged; docs/prompts remain CC BY-SA 4.0, code/templates MIT, and "a license is not permission for any use case" still holds.

## Author & how it was made

- **The author was a junior high school student when this repository was created.**
- **The Skill prompts** were processed and formally optimised by **the DeepSeek V4.1 Flash 1017 build, using an API key purchased by the DSH GO deepseek author**, based on the author's feedback and the model's actual behaviour, then summarised and consolidated.
- **Open-source writing and repository construction**: handled respectively by **Hy4 on Tencent WorkBuddy** and **DeepSeek V4.1 Flash 1017** (the roles were partly and specifically divided).
- **The author was responsible for** instructions, supervision, feedback and creative input.
- **First repository build date: November 2026.**
- **Maintenance pace**: frequent updates right after the initial release, then **low-frequency maintenance** (roughly one or two looks a month), with no promise of a fast reply. The author was a junior high school student; the specific circumstances are not explained.
- **Medicine specialisation**: optimised and debugged by the author together with DeepSeek, focusing on not buying a food-, cosmetic-, hygiene-, supplement- or device-licence product when a proper 国药准字 medicine is what was intended.

## License & attribution (hard requirements)

**Both repository URLs — mandatory in any redistribution or derivative (same author manages both):**

```
https://github.com/neurotracee/ecommerce-price-hunt
https://gitee.com/bio234/ecommerce-price-hunt
(both repositories are managed by the same author; GitHub is the main repo, Gitee the mainland-China mirror)
```

1. **Credit the author and cite both URLs above**, stating that one author manages them;
2. **State whether you modified it**, and never imply the original author endorses your version;
3. Derivative documentation must be released under **CC BY-SA 4.0** (or a compatible license) — ShareAlike.

> ⚠️ **A license is not permission for any use case.** Commercial use is licensed, but the usage restrictions below and the hard rules in `SKILL.md` **remain in force**.

## ⚠️ Disclaimer (mirrors `SKILL.md`; the Chinese text there is authoritative)

> **Statement of purpose**
> This project is a **comparison work instruction**: prompts and operating playbooks only, with **no automation scripts, no cracking tools and no reverse-engineered API code**. It is designed for an individual using their own device, their own account, and human-paced browsing. **Do not** use it for device farms, fake orders, flash-sale bots, bulk scraping, harvesting personal data, commercial price-comparison services, or price advertising. It does **not** bypass CAPTCHAs, risk controls, app locks or encrypted endpoints — hand control back to the user instead. For learning and personal research only; **not legal advice**. Consult a lawyer before commercial use or wide distribution.

> **Medicine-specific use restriction** (from `SKILL.md`, mandatory when the target is a medicine)
> - Results are **for personal reference only**; **they must not be used for medicine advertising, price promotion, diagnostic or treatment advice, or for publishing public price-comparison rankings**.
> - Purchasing and using medicines must follow a physician's or pharmacist's guidance.
> - Gate: an NMPA approval number (国药准字 + letter + 8 digits), an OTC/RX marking, and a dosage form matching the generic name — all three must be present; unverifiable approval numbers are recorded as "unverified", never invented.

> This project provides a method only. It is not medical, purchasing or investment advice. Prices are time-sensitive; the author accepts no liability for any loss arising from its use. Comply with each platform's terms of service and applicable law.

## Install: download the zip → hand it to DSH → one sentence

1. **Download the zip** (`ecommerce-price-hunt-v1.3.0.zip`):
   - GitHub: <https://github.com/neurotracee/ecommerce-price-hunt/releases/download/v1.3.0/ecommerce-price-hunt-v1.3.0.zip>
   - Gitee (faster in mainland China): <https://gitee.com/bio234/ecommerce-price-hunt/releases/download/v1.3.0/ecommerce-price-hunt-v1.3.0.zip>
2. **Hand the zip to DSH** — the safest route is to drag the downloaded file into the chat or attach it; you can also paste the download link and let it fetch the file.
   Whether that works **depends on the host and the network** (login walls, redirect interstitials, rate limits and human-verification checks can all stall it, and retries then burn time and tokens). If it stalls, stop and download manually — it varies, so no blanket rule.
3. Say this one line:

   > 帮我安装它到本地目录即可，我要把它添加进来。

Manual install (rarely needed, only for other hosts):

```bash
mkdir -p ~/.dsh/skills
cp -r ecommerce-price-hunt ~/.dsh/skills/
```

## What is inside

`SKILL.md` (category gate, collection flow, pricing rules, medicine gate, hard rules, on-demand loading),
`references/` (platform playbooks, screen reading, pricing math, report spec), `assets/report-skeleton.html`
(fictional sample data only), `README.md` (bilingual), `NOTICE.md` (license & attribution rules),
`LICENSE` (MIT), `LICENSE-DOCS.md` (CC BY-SA 4.0 full text), `docs/`, `examples/`, and the usual
governance files (CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, CHANGELOG, CITATION.cff, issue/PR templates, CI).

See [CHANGELOG.md](CHANGELOG.md) for the full change list.

## License

| Content | License |
| --- | --- |
| Documentation and prompts (`README*`, `SKILL.md`, `references/`, `docs/`, `examples/`, `NOTICE.md`) | **CC BY-SA 4.0** (attribution + indicate changes + share-alike; commercial use allowed) |
| Code and templates (`scripts/`, `assets/`) | **MIT** |

- The **MIT** label shown in the platform sidebar covers **code and templates only**; it is not the license of the whole project.
- Citing both repository URLs and stating that one author manages them is mandatory — wording in `NOTICE.md`.
- Upstream DSH go is AGPL-3.0. This project is an independent work under its own license, contains none of its code, and does not speak for the upstream project.

---

For learning and research reference only. Full disclaimer at the top of `README.md` and in `SKILL.md`.
