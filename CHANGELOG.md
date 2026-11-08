# Changelog

本项目版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。`SKILL.md` 的行为变更（新增闸门、修改口径、调整硬规则）视为功能变更。

本文件自 **1.1.0**（首个公开发布版本）起维护；更早的内部草稿未公开发布，不追溯记录。

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

### 说明

- 报告样式与双屏自检优先复用宿主自带 HTML 技能；`docs/portability.md` 给出无 HTML 技能时的替代做法，避免强绑定 DSH go 的本地路径。
- 文档采用 CC BY-NC-SA 4.0（含 NC 条款），代码/模板采用 MIT；因此本项目为源码公开 / 非商业自由使用，非 OSI 认证的开源软件。

[1.1.0]: https://github.com/neurotracee/ecommerce-price-hunt/releases/tag/v1.1.0
