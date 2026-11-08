# NOTICE · 授权与署名规范 / License & Attribution Notice

本文件是**授权条件的一部分**，不是建议。凡复制、分发、修改、二次开发或以任何方式使用本项目，
即视为接受下列条款。中文为准，英文摘要见文末。

---

## 一、授权（你可以做什么）

| 内容 | 许可 | 你可以 |
| --- | --- | --- |
| 文档与提示词（`README*`、`SKILL.md`、`references/`、`docs/`、`examples/`、本文件等所有非代码文本） | **CC BY-SA 4.0** | 复制、分发、修改、二次开发、**商业使用**，无需付费、无需申请、无需作者批准 |
| 代码与模板（`scripts/`、`assets/`） | **MIT** | 同上，限制更少 |

**任何二次开发、商用或借用均可**——这是明确允许的，不需要问作者（作者维护频率很低，问了也可能很久才回）。

## 二、必须做到的三条（硬要求）

### ① 署名，并标注两个源仓库地址，说明二者由同一作者管理

任何衍生作品、引用、转载、教程、二次开发版本，都必须**同时**写出下面两个地址，并说明二者是同一作者管理的两个仓库（不是互相抄的副本）：

```
https://github.com/neurotracee/ecommerce-price-hunt
https://gitee.com/bio234/ecommerce-price-hunt
（以上两个仓库由同一作者管理；GitHub 为主仓库，Gitee 为国内镜像）
```

可以直接整段复制这句，不要改写成只有其中一个地址。

### ② 注明是否修改

原样分发要说明出处；改过就要**明确写"已修改"**，并且不得暗示原作者为你的改动背书、认证或参与。

推荐写法：

> 本项目基于 https://github.com/neurotracee/ecommerce-price-hunt
> （镜像：https://gitee.com/bio234/ecommerce-price-hunt，两库同一作者管理）修改，
> 非原作者发布，原作者未参与本次修改。

### ③ 相同方式共享（ShareAlike）

如果你分发的是**基于本项目文档/提示词的衍生版本**，它必须同样以 **CC BY-SA 4.0**（或与之兼容的许可）发布。
这一条来自 CC BY-SA 4.0 本身，不是额外加码。

> 代码与模板（`scripts/`、`assets/`）是 MIT，不受 ShareAlike 约束，可以并入闭源项目，
> 但 MIT 要求保留版权声明与许可声明。

## 三、地址写在哪里算数

| 位置 | 是否算数 |
| --- | --- |
| 你的 README / 文档首屏 | ✅ 最省事 |
| 你的仓库 About 简介 | ✅ |
| 程序或网页的「关于」「页脚」「帮助」 | ✅ |
| 随附的 NOTICE / 第三方声明文件 | ✅ |
| 只埋在几百行开外的源码注释里 | ❌ 使用者正常操作时看不到，不算 |

## 四、不需要做的事

- ❌ 不需要付钱给作者
- ❌ 不需要发邮件、不需要等批准、不需要在 issue 里报备
- ❌ 自己改着自己用、不对外分发，**不需要公开任何东西**（CC BY-SA 与 MIT 只在分发时才产生义务）
- ❌ 不需要保留原作者的风格、结构或 bug，改得面目全非也行，只要署名和地址还在

## 五、许可 ≠ 用途：使用边界仍然有效

授权放开的是**版权层面的使用方式**（能不能改、能不能商用、能不能再分发），
**不是**对使用场景的免责。`SKILL.md` 与 `README.md` 中的用途限制依然有效，例如：

- 不得用于群控、刷单、抢购、批量爬取、抓取个人信息；
- 不得绕过验证码、风控、应用锁、加密接口；
- 比价结果不得用于药品广告、价格宣传、诊疗建议或对外发布的比价榜单。

也就是说：**协议允许你商用，但用途本身仍须合法合规**。这两件事互不替代。

## 六、与 DSH go 的关系

本项目是为 **[DSH go](https://github.com/ccch1mneyyy/dsh-go/)** 制作的**附属功能**开源项目：把「AI 自动全网比价」沉淀成一份可复用的 Skill。

- 上游原仓库：<https://github.com/ccch1mneyyy/dsh-go/>
- 上游简介：dsh-go — DeepSeek Harness 装进口袋：手机本机运行，也能遥控你的电脑。即上游是**基于 DeepSeek Harness 的二次开发方向**（其仓库标签含 `deepseek`、`deepseek-harness`）。
- 上游许可：AGPL-3.0。

**声明**：

1. 本项目**不是** DSH go 的官方组件、插件或分支，不隶属于上游项目，也不代表上游维护者的立场。
2. 本项目**不包含、不复制、不分发**上游的任何源代码或二进制文件；`SKILL.md` 中出现的 `~/.dsh/skills/...` 仅是**目录约定示例**，可由任意宿主替换（见 `docs/portability.md`）。
3. 本项目是独立作品、独立授权（文档 CC BY-SA 4.0 / 代码 MIT）；上游 AGPL-3.0 不适用于本项目文件。
4. 名称「DSH go」及其商标归各自权利人所有；此处仅为说明兼容性与出处而作指代性使用。

## 七、第三方组件、数据与免责

- `assets/report-skeleton.html` 预留图表挂载点，示例写法基于 **Apache ECharts**（Apache-2.0）。本项目**不捆绑** `echarts.min.js`，使用者自行引入时请遵守其许可。
- 各电商平台名称、界面元素名称仅用于说明操作路径，归各自权利人所有，不构成关联或背书。
- 仓库内所有商品、店铺、价格、批准文号示例均为**虚构占位或抽象描述**，不含真实采集数据、真实报价、真实个人信息。
- 本项目仅供学习与研究参考，不构成法律、用药、购买或投资建议；完整免责声明见 `README.md` 开头与 `SKILL.md`。

---

## English summary

This file forms part of the license terms. Using, copying, modifying or distributing this project
means you accept them.

**You may** use this project for anything, **including commercial use and forks**, free of charge and
without asking permission.

**You must** (hard requirements):

1. **Credit the author and cite BOTH repository URLs**, stating that the two repositories are managed
   by the same author (GitHub is the main repository, Gitee is the mainland-China mirror):
   - <https://github.com/neurotracee/ecommerce-price-hunt>
   - <https://gitee.com/bio234/ecommerce-price-hunt>
2. **State whether you changed it.** Modified versions must say so clearly and must not imply that
   the original author wrote, approved or endorses them.
3. **ShareAlike** for documentation/prompts: derivative documentation or prompts must be released
   under CC BY-SA 4.0 or a compatible license. Code and templates are MIT and are not subject to
   ShareAlike, but MIT requires keeping the copyright and permission notice.

**Where the attribution must appear:** your README or documentation front page, repository
description, an About/footer/help screen, or a bundled NOTICE file. Hiding it in a source comment
hundreds of lines down does not count.

**License is not permission for any use case.** The usage boundaries in `SKILL.md` and `README.md`
remain in force: no device farms, fake orders, flash-sale bots, bulk scraping or personal-data
harvesting; no bypassing CAPTCHAs, risk controls, app locks or encrypted endpoints; results must not
be used for medicine advertising, price promotion, treatment advice or published price rankings.

**Relationship to DSH go:** this is an ancillary, independently licensed project for
[DSH go](https://github.com/ccch1mneyyy/dsh-go/). It is not an official component, is not affiliated
with the upstream project, and contains no upstream code. "DSH go" and its marks belong to their
respective owners and are used here only to describe compatibility and provenance.
