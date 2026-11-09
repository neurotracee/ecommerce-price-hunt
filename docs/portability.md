# 移植到其他 Agent 宿主

`SKILL.md` 原本在 DSH go 环境下写成，少量路径与命令带有宿主印记。开源版的原则是：**能力要求写清楚，宿主细节可替换**。上游仓库见 <https://github.com/ccch1mneyyy/dsh-go/>。

## 1. 宿主需要提供的最小能力

| 能力 | 用途 | 没有时的替代做法 |
| --- | --- | --- |
| 读屏幕结构（无障碍树 / 屏幕树） | 找按钮、读价格、读标签 | 只能靠截图读图，精度下降、轮次变多，需在报告「局限」里写明 |
| 读图 | 图片渲染的详情页、价格角标 | 该平台标「读不到」，不猜数字 |
| 点击 / 滚动 / 返回 | 切页签、进详情、滚屏 | 无 UI 操作能力时本 Skill 不适用 |
| 交还用户（`handoff`） | 登录、验证码、应用锁、支付 | 必须明确停止，不能自行尝试绕过 |
| 生成并预览单文件 HTML | 交付报告 | 输出结构化 Markdown 表格，但需说明未做双屏自检 |

`SKILL.md` 里的 `screen`、`scroll`、`tap_xy`、`handoff` 都是**能力占位名**，不是某个平台的专有 API；按宿主自己的工具名映射即可。

## 2. 技能目录映射

用 DSH go 时不需要手动映射：把下载到的技能包 zip **文件本身**直接发给 DSH（更稳的做法；也可以先发下载链接让 AI 自己取，取不到再手动下载），再说「帮我安装它到本地目录即可，我要把它添加进来」，由 DSH 自己解压并放进本地技能目录。下表只在换宿主或自己动手时才用得上。

| 宿主 | 建议位置 | 说明 |
| --- | --- | --- |
| DSH go / `~/.dsh/skills` 约定 | `~/.dsh/skills/ecommerce-price-hunt/` | 原始形态，直接可用 |
| Claude Code | 项目的 `.claude/skills/ecommerce-price-hunt/` 或用户级 skills 目录 | 保留 `SKILL.md` frontmatter 的 `name` / `description` |
| WorkBuddy / 其他支持 Skill 的客户端 | 按各自 skills 目录约定 | 目录名保持 `ecommerce-price-hunt` |
| 无技能机制的自定义 Agent | 把 `SKILL.md` 作为系统提示词 | `references/*.md` 按「按需加载」表由编排层注入 |

> 若宿主对 frontmatter 有严格校验，只保留 `name` 与 `description` 两个字段，不要添加自定义字段。

## 3. HTML 技能：随包内置，不再依赖宿主

从 v1.4.0 起，HTML 与可视化能力**随本技能一起分发**，换宿主、换机器都一样：

- 必读：`vendor/answer-visualization-preference/SKILL.md`、`vendor/html-visualization/html/SKILL.md`；
- 按需：`vendor/html-visualization/ai-visualization/SKILL.md`（命中图表/图解分支时）；
- 自检脚本：`vendor/html-visualization/html/scripts/shot.py`（相对路径调用）。

宿主自带 HTML 技能（DSH go 的 `html` 等）仍然可以叠加使用，但**不再是前提**。`vendor/` 缺失（有人只拷了 `SKILL.md`）时的降级做法：

- 按 `references/report-spec.md` 自己实现，至少满足：
  - 单文件自包含、语义化标题、非 `index.html` 文件名；
  - 窄屏卡片列表、宽屏表格；断点用 `(min-width: …) and (min-aspect-ratio: 5/4)`，避免 1440×960 被误判成竖屏；
  - 手机 2.2:1 与笔记本 1.5:1 各检查一遍，横向溢出必须为 0；
  - 图表可选：`assets/report-skeleton.html` 预留了挂载点，需要图表时自行内联 ECharts（Apache-2.0），本项目不捆绑该文件。

随包的 `shot.py` 依赖 Playwright/Chromium；跑不起来就用宿主截图能力或手工在两个窗口尺寸下看一遍，并在报告「局限」注明自检方式。**任何情况下都写相对路径 `vendor/...`，不要写死个人机器上的绝对路径。**

> 说明：对**本地生成的 HTML 文件**做渲染自检，与对**电商平台**做自动采集是两回事。前者是交付质量检查，后者是本项目明确禁止的行为。

## 4. 平台清单的差异

`references/platform-playbooks.md` 记录的是 2026-11 某一台设备上的六个平台入口。换设备后：

1. 先看应用清单确认有哪些 App；闪购/外卖类 App 不等于综合电商；
2. 缺 App 时用手机浏览器网页版，并在报告写明「网页版读数、无 App 客服」；
3. 平台改版后，把新的入口/排序/标签位置补进 playbook，并注明实测月份。

数量少（只有 2–3 条链接）要如实说明「这个平台就这么多」，不要拿别的平台数据补齐。

## 5. 保持边界不变

移植时**不要**改动以下内容，它们是 Skill 的合规前提：

- 第 0 步品类判定与药品专项闸门、用途限制；
- 硬规则（禁止高频/批量、禁止绕过、禁止越权用途、最小采集、只做人工级浏览）；
- 「不猜数据」「推断与实测分开写」「结算页不提交订单」；
- `README.md` 开头的免责声明与 DSH go 出处。

如果宿主环境无法遵守其中任何一条，就不要在该环境启用本 Skill。

## 6. 校验

改动 `SKILL.md` 或增删文件后运行：

```bash
python scripts/validate.py
```

它只检查结构完整性（frontmatter、按需加载表引用的文件、免责声明、示例文件是否标注虚构），不检查任何平台可达性。
