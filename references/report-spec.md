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

**不要沿用任何固定像素或固定宽高比**——每个人的屏幕都不一样，照抄别人的尺寸等于没检查。按优先级取实际值，**安卓优先**（本技能的主要宿主是手机端的 DSH go）：

1. **安卓（首选）**：`adb shell wm size` 拿物理尺寸（出现 `Override size` 时以 override 为准——分屏、挖孔、手势条都会改变可视区）；`adb shell wm density` 拿 dpi；**逻辑宽 = 物理宽 × 160 ÷ dpi**，逻辑高同理，这个逻辑尺寸才是浏览器视口。没有 adb 时读 `getprop ro.sf.lcd_density` 配合 `wm size`，或让宿主用自带的无障碍 / 截图能力直接量当前可视区。
2. **桌面三平台（兼容保留）**：Windows 读主屏工作区（`System.Windows.Forms.Screen::PrimaryScreen.Bounds`），要更细就读 `Get-CimInstance Win32_VideoController` 的分辨率 ÷ 系统缩放 = **逻辑分辨率**；macOS 用 `system_profiler SPDisplaysDataType`；Linux 用 `xrandr`。
3. **按机型查资料**：用户说了手机/电脑型号，就检索该型号的**逻辑分辨率与宽高比**（注意刘海屏 / 灵动岛 / 挖孔、系统栏占用的可视区），别凭印象估。
4. **兜底**：都取不到时才用通用保守值（安卓竖屏 ≈ `393x873`、桌面 ≈ `1440x900`），并**必须在报告「局限」里注明是缺省视口**。

手机档取**竖屏**且以真实安卓机为准；桌面档取**当前实际窗口或整屏的逻辑尺寸**；两档的宽高比就是设备真实比例，不做人为美化。报告可能被转发到电脑上看，所以桌面档不能省——但桌面尺寸同样要探测，不许套模板。

### 第二步：自检（安卓优先真机，桌面才跑脚本）

**安卓端一般没有 Playwright**，别硬跑 `shot.py`：

- 起本地服务打开报告：在报告目录执行 `python3 -m http.server 8000`，手机浏览器访问 `http://127.0.0.1:8000/<报告>.html`；或用 `content://`、宿主自带的文件预览打开。
- **竖屏看一遍 → 横屏 / 浏览器「桌面版」再看一遍**，重点看：横向溢出为 0、表格不挤成竖条、图表容器有高度、文字不被裁切。
- 留证：`adb exec-out screencap -p > shot.png`；有 Chrome 远程调试时可 `adb forward tcp:9222 localabstract:chrome_devtools_remote`，用 CDP 设视口后截图。
- 桌面 / 服务器上有 Playwright 时才跑随包脚本（命令见下），要求 error=0；`misalignedBlocks` 多为误报（子元素与 grid 宽度对比），横向溢出 `horizontalOverflow` 必须清零。

```bash
python3 vendor/html-visualization/html/scripts/shot.py <报告>.html --desktop <桌面宽>x<桌面高> --mobile <手机宽>x<手机高> --format-report summary
python3 vendor/html-visualization/html/scripts/shot.py <报告>.html --only mobile --mobile <手机宽>x<手机高> --outdir _shots --format-report summary
```

真机与脚本都跑不动时，用宿主截图能力或手工把窗口调到上面定好的两档，逐节检查同样四项；并在报告「局限」里注明**自检方式（真机 / shot.py / 手工）+ 实际用的两个视口 + 视口来源**（探测 / 机型查询 / 缺省）。移植说明见 `docs/portability.md`，随包技能说明见 `vendor/README.md`。

窄屏一律卡片列表、横屏才用表格；断点用 `(min-width: …) and (min-aspect-ratio: 5/4)`，避免**宽而矮的桌面窗口**（接近 3:2、4:3 的显示器）被误判成竖屏。

> 对**本地生成的 HTML 文件**做渲染自检属于交付质量检查，与对电商平台做自动采集是两回事；后者在本项目中被明确禁止。
