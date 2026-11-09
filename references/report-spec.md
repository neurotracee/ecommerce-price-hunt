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

### 第一步：定视口（不写死比例，以实际为准）

**不要沿用任何固定像素或固定宽高比**——每个人的屏幕都不一样，照抄别人的尺寸等于没检查。按优先级取实际值：

1. **命令探测本机屏幕**：Windows 用 PowerShell 读主屏工作区（`System.Windows.Forms.Screen::PrimaryScreen.Bounds`）；要更细就读 `Get-CimInstance Win32_VideoController` 的分辨率，再按系统缩放百分比换算**逻辑分辨率**。macOS 用 `system_profiler SPDisplaysDataType`；Linux 用 `xrandr`。
2. **按机型查资料**：用户说了手机/电脑型号，就检索该型号的**逻辑分辨率与宽高比**（注意刘海屏/灵动岛、系统栏占用的可视区），别凭印象估。
3. **兜底**：都取不到时才用通用保守值（手机 ≈ `390x844`、桌面 ≈ `1440x900`），并**必须在报告「局限」里注明是缺省视口**。

手机档取**竖屏**，桌面档取**当前实际窗口或整屏的逻辑尺寸**；两档的宽高比就是设备真实比例，不做人为美化。

### 第二步：跑脚本

脚本随包提供，直接用相对路径调用（无需安装任何宿主技能）：

```bash
python3 vendor/html-visualization/html/scripts/shot.py <报告>.html --desktop <桌面宽>x<桌面高> --mobile <手机宽>x<手机高> --format-report summary
python3 vendor/html-visualization/html/scripts/shot.py <报告>.html --only mobile --mobile <手机宽>x<手机高> --outdir _shots --format-report summary
```

要求 error=0；`misalignedBlocks` 多为误报（子元素与 grid 宽度对比），横向溢出 `horizontalOverflow` 必须清零。

脚本跑不动时（缺 Playwright/Chromium 等依赖），用宿主截图能力，或手工把窗口调到上面定好的两档，逐节检查：横向溢出为 0、表格不挤成竖条、图表容器有高度、文字不被裁切；并在报告「局限」里注明**自检方式 + 实际用的两个视口 + 视口来源**（探测 / 机型查询 / 缺省）。移植说明见 `docs/portability.md`，随包技能说明见 `vendor/README.md`。

窄屏一律卡片列表、横屏才用表格；断点用 `(min-width: …) and (min-aspect-ratio: 5/4)`，避免**宽而矮的桌面窗口**（接近 3:2、4:3 的显示器）被误判成竖屏。

> 对**本地生成的 HTML 文件**做渲染自检属于交付质量检查，与对电商平台做自动采集是两回事；后者在本项目中被明确禁止。
