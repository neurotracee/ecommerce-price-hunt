# 比价报告章节与自检

样式、字体、断点、图表与交付规范一律遵循**随包内置**的两个技能（`vendor/answer-visualization-preference/SKILL.md`、`vendor/html-visualization/html/SKILL.md`，图表分支再加 `vendor/html-visualization/ai-visualization/SKILL.md`）；本文件只定「比价报告该有哪些节」。**路径一律用相对路径，不要写死任何机器或宿主专属路径。**

## 章节顺序
1. **结论 hero**：一个大数字（最低单价元/克）+ 3–4 条要点（最便宜、最稳妥、别买哪里、看单价）。
2. **指标条**：采集条数 / 单价区间 / 最高最低倍数。
3. **每平台最低价**：横向条形图，x 轴元/克，按阈值上色（低=绿、中=橙、高=红）。
4. **同平台价差区间**：每平台 min–max 价格带（custom series 或区间条），点出「同平台能差 2 倍」。
5. **最低价前 N 名**：表格/卡片，列 # / 店铺 / 标价 / 单件实付 / 发货地与快递 / 发货与送达。
6. **全量清单**：单价升序，列 平台 / 店铺 / 到手价 / 单价 / 销量 / 标签。
7. **平台活动标签卡**：每平台的价格带 + 标签 + 排序方式 + 在售条数。
8. **三种买法**：最便宜 / 最稳 / 要发票或售后。
9. **坑**：3–5 条实测教训（品牌错标、低价少销量、多盒折算、券后门槛）。
10. **数据说明与局限**：采集时间、方法、口径、读不到的部分。

## 自检
自检脚本随包提供，直接用相对路径调用（无需安装任何宿主技能）：

```bash
python3 vendor/html-visualization/html/scripts/shot.py <报告>.html --desktop 1440x960 --mobile 1080x2376 --format-report summary
python3 vendor/html-visualization/html/scripts/shot.py <报告>.html --only mobile --mobile 480x1056 --outdir _shots480 --format-report summary
```

要求 error=0；`misalignedBlocks` 多为误报（子元素与 grid 宽度对比），横向溢出 `horizontalOverflow` 必须清零。

脚本跑不动时（缺 Playwright/Chromium 等依赖），用宿主截图能力或手工把浏览器调到手机 2.2:1 与笔记本 1.5:1 两档，逐节检查：横向溢出为 0、表格不挤成竖条、图表容器有高度、文字不被裁切；并在报告「局限」里注明自检方式。移植说明见 `docs/portability.md`，随包技能说明见 `vendor/README.md`。

窄屏一律卡片列表、横屏才用表格；断点用 `(min-width: …) and (min-aspect-ratio: 5/4)`，避免 1440×960 被误判成竖屏。

> 对**本地生成的 HTML 文件**做渲染自检属于交付质量检查，与对电商平台做自动采集是两回事；后者在本项目中被明确禁止。
