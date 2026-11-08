# v1.1.0 · ecommerce-price-hunt

> **这是为 [DSH go](https://github.com/ccch1mneyyy/dsh-go/) 做的一个附属功能的开源项目。**
> 上游原仓库：<https://github.com/ccch1mneyyy/dsh-go/>
> 本项目**不是** DSH go 的官方组件，不隶属于上游项目，也不包含、不复制上游的任何代码；独立发布、独立授权。

首个公开发布版本。把「让 AI 自动完成商品/药品全网比价」沉淀为一份可复用的 Skill：品类闸门、统一单价口径、按需加载的读屏手册、药品专项规则，以及固定结构的双屏 HTML 报告。目标是减少 Agent 的返工、误判与不必要的上下文消耗。

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

1. **直接把压缩包下载下来**（`ecommerce-price-hunt-v1.1.0.zip`）：
   - GitHub：<https://github.com/neurotracee/ecommerce-price-hunt/releases/download/v1.1.0/ecommerce-price-hunt-v1.1.0.zip>
   - Gitee（国内更快）：<https://gitee.com/bio234/ecommerce-price-hunt/releases/download/v1.1.0/ecommerce-price-hunt-v1.1.0.zip>
2. **把下载到的 zip 文件本身直接发给 DSH**：拖进对话框，或作为附件上传。
   **不要把下载链接发给 AI，也不要让它跳转去下载**——链接不一定打得开，来回跳转和重试只会白白消耗时间与 token。**给文件，不给链接。**
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
- `README.md` / `README.en.md` / `NOTICE.md`：项目定位、DSH go 出处、完整免责声明、归属说明
- `docs/` / `examples/`：设计说明、宿主移植、FAQ、触发话术与流程示例
- 开源治理文件：CONTRIBUTING / CODE_OF_CONDUCT / SECURITY / CHANGELOG / CITATION.cff / Issue 与 PR 模板 / CI 校验

完整变更见 [CHANGELOG.md](CHANGELOG.md)。

## 许可

- 代码与模板（`assets/`、`scripts/`）：MIT
- 文档与提示词（`README*`、`SKILL.md`、`references/`、`docs/`、`examples/`）：CC BY-NC-SA 4.0（署名 - 非商业性使用 - 相同方式共享）；商业用途需另行获得书面授权
- 平台侧栏自动识别的 **MIT 仅覆盖代码与模板**；文档与提示词为非商业的 CC BY-NC-SA 4.0，以 `LICENSE-DOCS.md` 为准，请勿把侧栏的 MIT 当成整个项目的授权
- 因含 NC 条款，本项目为源码公开 / 非商业自由使用，而非 OSI 认证的开源软件

上游 DSH go 采用 AGPL-3.0；本项目为独立作品、独立授权，不含其代码，也不代表上游立场。

---

**仅供个人学习与研究。完整免责声明见仓库 `README.md` 开头与 `SKILL.md`。**
