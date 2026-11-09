# Changelog

本项目版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。`SKILL.md` 的行为变更（新增闸门、修改口径、调整硬规则）视为功能变更。

本文件自 **1.1.0**（首个公开发布版本）起维护；更早的内部草稿未公开发布，不追溯记录。

## [1.4.0] - 2026-11-09

**功能版本：HTML 报告改为「随包技能驱动」，不再依赖宿主的 HTML 技能。**

### 文档修订（同版本内）· 屏幕视口不再写死，且**以安卓优先**

- **平台定位补正**：本技能主要给 DSH go / DeepSeek Harness 的**安卓手机端**用（无障碍读屏 + 手机浏览器），Windows / macOS / Linux **兼容保留**。`SKILL.md` 顶部、`README.md`（中英）、`docs/portability.md`（新增「平台优先顺序」表）同步写明。
- 删掉「手机 2.2:1 / 笔记本 1.5:1」与 `--desktop 1440x960 --mobile 1080x2376` 这类固定尺寸：**每个人的屏幕比例都不同，写死等于按作者自己的机器检查**。
- 改为**现场探测、安卓优先**：① 安卓 `adb shell wm size`（有 `Override size` 以 override 为准，分屏/挖孔/手势条会改可视区）+ `wm density`，**逻辑宽 = 物理宽 × 160 ÷ dpi**；无 adb 时读 `getprop ro.sf.lcd_density` 或用宿主无障碍/截图量可视区；② 桌面三平台兜底（Windows 主屏工作区 / `Win32_VideoController` ÷ 缩放、macOS `system_profiler`、Linux `xrandr`）；③ 按用户机型查资料（注意刘海/灵动岛/挖孔）；④ 都取不到才用保守缺省（安卓竖屏约 393×873、桌面约 1440×900），并在报告「局限」**明确注明是缺省视口、非用户真实设备**。
- **自检方式也按平台分**：安卓端一般跑不了 Playwright，改为真机自检——`python3 -m http.server` 起服务在手机浏览器打开，**竖屏看一遍 → 横屏/桌面版再看一遍**，`adb exec-out screencap -p` 留证；有 Chrome 远程调试时 `adb forward tcp:9222 localabstract:chrome_devtools_remote` 走 CDP 设视口截图。桌面/服务器有 Playwright 才跑随包 `shot.py`。
- 报告「局限」除自检方式外，还要写**实际用的两个视口 + 视口来源**（安卓探测 / 桌面探测 / 机型查询 / 缺省）。
- 断点说明里「避免 1440×960 被误判成竖屏」改为「避免宽而矮的桌面窗口（接近 3:2、4:3 的显示器）被误判成竖屏」。
- `scripts/validate.py` 新增防回退校验：`SKILL.md` 出现 `--desktop 1440x960` / `--mobile 1080x2376` / `--mobile 480x1056` / 「手机 2.2:1 与笔记本 1.5:1」任一即报错；必须含「逻辑分辨率」「缺省视口」「一律作废」；必须含安卓探测命令 `adb shell wm size`；且 **adb 必须排在 `Win32_VideoController` 之前**（防有人把桌面写回首位）。

### 新增 · 随包内置两个可视化 / HTML 技能（`vendor/`）

- `vendor/answer-visualization-preference/SKILL.md`：回答可视化偏好（该不该出图、出图形态、色块/进度条/箭头设计语言、移动端断点）。
- `vendor/html-visualization/html/`：单页 HTML 技能，含 `scripts/shot.py` 双屏自检脚本与 `references/`（前端设计、灵动报告、图表、Windows 兼容等）。
- `vendor/html-visualization/ai-visualization/`：图表/图解路由技能（ECharts、HTML-SVG、原图叠加、生成式配图等分支）。
- `vendor/README.md`：来源映射、相对路径约定、**不要就地修改**、第三方版权说明（`vendor/` 内容版权归原作者，本项目许可不覆盖）。

### 变更 · `SKILL.md`「交付：HTML 报告」

- 明确要求：**写 HTML 前必须同时完整读** `vendor/answer-visualization-preference/SKILL.md` 与 `vendor/html-visualization/html/SKILL.md`；报告含图表/图解时再加读 `vendor/html-visualization/ai-visualization/SKILL.md`（按需，不预读）。
- **路径只准用相对路径** `vendor/...`：严禁写死 `C://Users//...`、`%LOCALAPPDATA%\...`、`~/.dsh/skills/...`、`/mnt/...` 等环境专属路径。
- 双屏自检命令改为随包脚本：`python3 vendor/html-visualization/html/scripts/shot.py ...`（原为 `~/.dsh/skills/html/scripts/shot.py`）。
- `vendor/` 缺失时（只拷了 `SKILL.md` 等少数文件）：如实说明并降级到 `references/report-spec.md`，**不得假装读过**。
- 「按需加载」表、文件职责、顶部速览同步改写。

### 同步修订

- `references/report-spec.md`：样式与自检来源改为随包技能，命令示例换成 `vendor/...` 相对路径。
- `docs/portability.md`：原「HTML 技能的替换」改为「随包内置，不再依赖宿主」；`docs/why-this-skill.md`、`examples/sample-session.md`、`CONTRIBUTING.md`、`README.md`（中英）同步。
- `scripts/pack.py`：`INCLUDE_DIRS` 增加 `vendor`，两个技能随 zip 分发。
- `scripts/validate.py`：新增校验——随包技能文件必须存在、`SKILL.md` 必须要求阅读这两个技能、必须写明「严禁写死」绝对路径、`SKILL.md` 不得出现 `AppData` / `.user_skills` 等本机路径。
- 版本号 1.3.0 → 1.4.0。

## [1.3.0] - 2026-11-08

**功能版本：Skill 自带版本自检与升级提示。** 比价方法本身未改动，新增的是「交付之后」的一小段收尾动作。

### 新增 · 版本自检与升级提示（`SKILL.md` 末尾）

- **结尾固定追加一行**：`📌 ecommerce-price-hunt v1.3.0 · 最新 vX.Y.Z（来源）· 已是最新 / 落后 N 个版本`，默认开启，只占一行。
- **顺序硬性规定**：先把比价任务做完、报告交付完，**再**反过来做版本检查，不占用采集与写作的 token。
- **检查链**：读本地 `VERSION` → **优先 Gitee**（`.../raw/main/VERSION`，302 需跟随）→ Gitee `releases/latest` 取 `tag_name` → GitHub `raw` 兜底（国内加 `ghproxy.net` 前缀）。**每级只试一次**，全失败写「未查到」，不猜、不循环重试。
- **落后时最多 3–5 行**：差距（`vX.Y.Z → vA.B.C`）+ 一两句话概括该版本主要修复/改动（读远端 `CHANGELOG.md`）+ 主动询问是否一键升级 + 两端 Release 直链。
- **结束语必须是追问**，不以陈述句收尾。
- **升级约定**：先改名备份原技能目录；自动下载**失败一次即停**并如实告知，把直链再给一次、由用户自行决定；升完核对 `VERSION`；**只有维护者本人或用户明确要求**时才同步两端页面（README 版本号与直链、CHANGELOG、RELEASE_NOTES、Release 正文与附件）。
- 版本号是否递增由维护者决定，Skill 不擅自改号。

### 文档修订（同版本内）

- 项目定位句去掉「药品」二字，改为「让 AI 自动完成商品全网比价」；另起一行说明**药品比价是其中的专项能力**，由作者与 DeepSeek 专项优化调试，重点是避免把「国药准字」买成食字号 / 妆字号 / 消字号 / 健字号 / 械字号产品（中英双语同步）。
- 「作者与制作方式」补充**维护节奏**：刚发布阶段可能较频繁更新与响应，之后转为低频维护（大约一两个月看一两次），不承诺即时响应；作者为初中生，具体原因不作解释（中英双语同步）。
- 两端仓库简介（About）同步改为「电商全网比价 Skill（含国药准字药品专项…）」。

### 新增 · 安全边界（`SKILL.md`「越界请求怎么答」）

- **防滥用清单**：群控/养号、刷单刷评刷量、抢购秒杀代抢、批量爬取商品评论用户、抓取或拼装个人信息、绕过验证码/风控/应用锁/加密参数/地区限制、代下单与自动支付、对外比价榜单与价格宣传、药品广告与诊疗建议——一律**不执行**。
- **不给降级方案**：不拆解「换个说法就能做」的步骤、不给绕过思路、不写半自动脚本；用户强调「自用/研究/只跑一次」也不放宽，只提供合规替代（人工核对、公开渠道、官方接口）。
- **拒绝必须附固定风险提示**：可能违反平台协议与相关法律（封号、限制提现、民事索赔，情节严重或涉行政/刑事责任），**后果由使用者自行承担，与本项目及作者无关**，并建议理性慎重评估。个人信息的处理、支付、账号安全一律 `handoff`。
- 被施压时原样重复风险提示，**不辩论、不追加细节、不承诺「下次可以」**；报告里只写「该项因合规限制未执行」。

### 新增 · 简版作者声明（`SKILL.md` 末尾）

- 紧接正文之后加入**精简版**声明：DSH go 上游归属与非官方身份、作者建仓时为初中生、提示词由 DSH GO 的 deepseek 作者自购 API 的 DeepSeek V4.1 Flash 1017 版优化生成、开源编写与仓库构建由腾讯 WorkBuddy 的 Hy4 与 DeepSeek V4.1 Flash 1017 版分担、首个构建 2026 年 11 月、双许可与双地址署名要点。**刻意写短**，完整版仍在 `README.md` / `NOTICE.md`，避免每次加载都吃 token。

### 元数据与校验

- `SKILL.md` front-matter 增加 `version: 1.3.0`；正文顶部注明「本文件对应版本」。
- `scripts/validate.py` 增加两项防漂移校验：**`SKILL.md` 声明的版本必须与 `VERSION` 一致**、**`SKILL.md` 必须含两个仓库地址**；发版漏改会直接报错。
- 版本号 1.2.0 → 1.3.0：`VERSION`、`CITATION.cff`、README 安装直链、`RELEASE_NOTES.md` 同步；本次打包顺带带上 1.2.0 之后的两轮文档改动（Star/赞赏板块、安装说明去一刀切、`images/wechat-donate.png`）。

## 文档更新 · 2026-11-08（不改版本号）

- `README.md` 新增**「⭐ 支持本项目（点个 Star + 赞赏）」**板块（中英双语）：Star 引导为主、微信赞赏码为辅，并写明「赞赏是自愿打赏，不影响 CC BY-SA 4.0 / MIT 授权，商用与二次开发无需付费」。
- 安装三步之后加了一行 Star 提示（中英各一处），指向两个仓库。
- Star 引导补充**跨仓库互点**话术（中英双语）：说明两个仓库的 Star 数、搜索权重与推荐位相互独立，从任一端看到都建议到另一端也点一颗；同步改写「点一个就够」的旧表述。
- 新增 `images/wechat-donate.png`（微信赞赏码，560×560，22 KB）。**该图片不打进安装包**，因此 v1.2.0 技能包与 Release 附件无需重新打包，Release 正文亦不改动。
- **安装说明改为「不一刀切」的表述**：原文写死「不要把下载链接发给 AI／给文件，不给链接」，现改为「手动下载更稳、发链接也可以试」——说明能否取到取决于 AI 宿主能力与当时的网络环境（登录墙、跳转中转页、限流、人机验证、读不到页面等），卡住了就停止重试改手动下载。同步修改 `docs/faq.md`、`docs/portability.md`、`examples/prompt-examples.md` 与 `scripts/pack.py` 生成的 `INSTALL.txt` 文案；`scripts/validate.py` 改为**禁止**再出现该一刀切表述。

## [1.2.0] - 2026-11-08

**许可变更版本。** 授权方式、声明规范与文档结构均有调整，使用前请重读 `NOTICE.md`。

### 许可变更

- 文档与提示词由 **CC BY-NC-SA 4.0** 改为 **CC BY-SA 4.0**：**去掉非商业条款**，明确允许任何二次开发、商用与借用。
- 代码与模板继续使用 **MIT**；`LICENSE` 保持标准 MIT 全文（含两个仓库地址），保证平台自动识别。
- 新增 [`NOTICE.md`](NOTICE.md) 授权与署名规范：① 必须标注**两个**仓库地址（GitHub + Gitee）并说明由同一作者管理；② 必须注明是否修改、不得暗示原作者背书；③ 文档类衍生作品须以 CC BY-SA 4.0 共享（ShareAlike）。
- 明确 **「协议 ≠ 用途」**：授权允许商用，但 `SKILL.md` 的硬规则与药品专项限制仍然有效，不因商用授权而失效（按本次要求**全部保留**原有用途限制）。

### 文档结构

- `README.md` 合并为**单文件中英双语**：中文在上、英文在下，顶部 `[English](#english)` 锚点跳转、英文区 `[中文](#电商全网比价-skill)` 回跳；`README.en.md` 保留为指向英文小节的入口，避免旧链接失效。
- README 前半部分新增**「作者与制作方式（声明）」**与**「授权与声明规范」**：作者创建本仓库时为初中生；提示词由 DSH GO 的 deepseek 作者自购 API 的 DeepSeek V4.1 Flash 1017 版基于作者反馈与实际模型表现优化生成；开源编写与仓库构建由腾讯 WorkBuddy 的 Hy4 与 DeepSeek V4.1 Flash 1017 版分别负责（部分有具体分工）；作者负责指令、监督、反馈与创意；**仓库首个构建日期为 2026 年 11 月**。
- `RELEASE_NOTES.md` 同步改为中英双语，并把作者声明、授权规范前置。

### 其他

- `CITATION.cff`、README 徽章、目录结构说明同步新许可与版本号。
- 安装直链更新至 `v1.2.0`。

## [1.1.0] - 2026-11-08

首个公开发布版本，同步至 GitHub 与 Gitee，附带可直接安装的技能包 Release。

### 新增 · Skill 本体

- `SKILL.md`：品类判定（普通商品 / 药品 / 化妆品 / 保健食品 / 医疗器械）作为第 0 步闸门。
- 采集流程：每平台 3–5 屏、价格与销量双排序、筛选面板标签、详情页继续滚动、结算页兜底看规格（**不提交订单**）。
- 统一口径：单价 = 实付 ÷ 净含量；实付 = 标价 + 运费 − 可叠加券；不同规格绝不混算。
- 药品专项：国药准字 + OTC/RX + 剂型三条件闸门，默认排除妆/食/健/消/械字号；用途限制与免责。
- 最低价前 N 名（默认 3）深挖发货地、快递、时效与客服原话。
- 硬规则：禁止高频/批量、禁止绕过、禁止越权用途、最小采集、只做人工级浏览。
- 按需加载表与交付检查清单，避免一次性把所有手册塞进上下文。

### 新增 · 参考手册

- `references/platform-playbooks.md`：六平台入口、排序、活动标签位置与通用坑位（实测于 2026-11）。
- `references/screen-reading.md`：读屏快路、坑与对策表、误点防护、数据落地格式。
- `references/pricing-method.md`：单价换算、券与运费、用量/疗程估算、风险标记。
- `references/report-spec.md`：报告 10 章节、双屏断点、自检要求。
- `assets/report-skeleton.html`：只含比价章节的 HTML 骨架，示例数据全部虚构。

### 新增 · 开源项目配套

- README 开头明确「本项目为 DSH go 附属功能」并附上游仓库地址 <https://github.com/ccch1mneyyy/dsh-go/>。
- README（中/英）与 Release 正文完整收录 `SKILL.md` 的用途声明与药品专项免责声明。
- `NOTICE.md` 澄清非官方、非上游代码、独立授权关系。
- `CONTRIBUTING.md` / `CODE_OF_CONDUCT.md` / `SECURITY.md` / `CITATION.cff` / `.editorconfig` / `.gitattributes` / `.gitignore`。
- `.github/` Issue 与 PR 模板、CI 结构校验工作流。
- `docs/`（设计说明、宿主移植、FAQ）与 `examples/`（触发话术、任务流程示例）。
- `scripts/validate.py`、`scripts/pack.sh`、`scripts/publish.sh`：结构校验、打包、一键双端同步发布。

### 文档修订 · 2026-11-08（同版本内，不改变 Skill 行为）

- README（中/英）、Release 正文、安装包 `INSTALL.txt`、FAQ、话术示例、宿主移植文档统一改为三步安装：**下载 zip → 把文件本身直接发给 DSH → 说「帮我安装它到本地目录即可，我要把它添加进来」**。
- 明确「不要把下载链接发给 AI、不要让它跳转去下载」，避免多余的跳转、重试与 token 消耗；不再要求 clone 仓库或敲命令。
- 同步到 GitHub 与 Gitee 的仓库首页、简介、Release 正文与附件。

### 文档修订 · 2026-11-08（标签与许可证元数据）

- 上游关系补全：DSH go 是基于 **DeepSeek Harness** 的二次开发方向，其仓库标签含 `deepseek` / `deepseek-harness`；已写入 README（中英）、NOTICE、CITATION.cff 关键词与仓库简介。
- 两端仓库标签同步为 10 个（含 `deepseek`、`deepseek-harness`）；发布脚本改为**读取现有标签后合并去重**，不再覆盖使用者在网页端手动新增的 topics。
- `LICENSE` 恢复为**标准 MIT 全文**（去掉末尾自定义尾注）：此前平台自动识别把 MIT 判成 `Other` / 空。现在 GitHub 侧栏显示 MIT License、Gitee 仓库显示 MIT。双许可说明移到 `NOTICE.md`、`LICENSE-DOCS.md`、README 与 Release 正文。
- README（中英）顶部新增**纯文字许可声明**，避免 shields.io 徽章图片加载不出来时看不到协议；并明确「平台侧栏的 MIT 仅覆盖代码与模板，文档与提示词是 CC BY-NC-SA 4.0 非商业」。

### 说明

- 报告样式与双屏自检优先复用宿主自带 HTML 技能；`docs/portability.md` 给出无 HTML 技能时的替代做法，避免强绑定 DSH go 的本地路径。
- 文档采用 CC BY-NC-SA 4.0（含 NC 条款），代码/模板采用 MIT；因此本项目为源码公开 / 非商业自由使用，非 OSI 认证的开源软件。

[1.1.0]: https://github.com/neurotracee/ecommerce-price-hunt/releases/tag/v1.1.0
