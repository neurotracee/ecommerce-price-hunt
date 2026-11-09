# vendor/ · 随包内置的可视化技能

这里放的是**本技能写 HTML 报告时必须读取**的两个技能，随包分发，保证换机器、换宿主都能找到，不依赖任何绝对路径。

## 目录映射

| 本目录 | 来源（上游原始位置，仅供维护者追查） |
| --- | --- |
| `answer-visualization-preference/SKILL.md` | 用户级技能 `answer-visualization-preference`（个人回答可视化偏好） |
| `html-visualization/html/` | `HTML & Visualization（HTML与可视化）/html（网页）` |
| `html-visualization/ai-visualization/` | `HTML & Visualization（HTML与可视化）/ai-visualization（AI数据可视化）` |

> 上游原始路径**故意不写进本仓库**，也不允许任何技能文件写死：实际位置因机器、宿主而不同（如 `%LOCALAPPDATA%\...\.user_skills\...`、`~/.dsh/skills/...`、`/mnt/...` 各不相同）。**一律用相对路径 `vendor/...` 定位。**

## 使用约定

1. **写 HTML 前必须同时读** `vendor/answer-visualization-preference/SKILL.md` 与 `vendor/html-visualization/html/SKILL.md`；命中图表/图解分支时，再按 `vendor/html-visualization/ai-visualization/SKILL.md` 的路由加载它自己的 `references/` 文件（按需，不预读）。
2. **目录改名不改内容**：为跨平台与跨宿主稳定，`html（网页）` → `html`、`ai-visualization（AI数据可视化）` → `ai-visualization`。技能内部的相互引用都是相对路径（`references/...`、`assets/...`），改名不影响使用。
3. **不要就地修改这里的内容**：这些是上游技能的副本。要改就改上游、再重新打包，否则下次覆盖会丢失。
4. `html/scripts/shot.py` 是双屏自检脚本（截图 + 结构/溢出检查），跑不动（缺 Playwright 等依赖）时按技能内的降级方式处理。

## 版权与许可说明

- 本目录内容**版权归其原作者**，随本技能**原样分发**，未做内容修改（仅目录改名）。
- 各自的使用与再分发条件以对应 `SKILL.md` 及其所在上游仓库的声明为准；本项目的 CC BY-SA 4.0 / MIT **不覆盖** `vendor/` 下的第三方内容。
- `html/assets/vendor/acorn.cjs` 附带 `acorn.LICENSE`，请一并保留。
