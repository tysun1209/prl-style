<div align="center">

<p><img src="assets/showcase/readme-hero.png" width="1440" alt="PRL Style — 科研绘图与中英文写作"></p>

<p><strong>让图更清晰，让论证更有力。</strong></p>

<p>为你的 AI agent 配备一套 PRL 风格的科研表达工具。<br>
从数据绘图、科学示意，到中英文写作、图注与审校。</p>

<p>可接入 <code>Codex</code> · <code>Claude Code</code> · <code>OpenCode</code> · <code>DeepSeek Harness</code></p>

<p>
  <a href="#一句话安装"><strong>一句话安装</strong></a> &nbsp;·&nbsp;
  <a href="#效果预览">看看效果</a> &nbsp;·&nbsp;
  <a href="https://github.com/tysun1209/prl-style/releases/latest">下载最新版</a> &nbsp;·&nbsp;
  <a href="#怎么使用">使用示例</a>
</p>

</div>

| <img src="assets/showcase/readme-stat-figures.png" width="180" alt="36 类图型"> | <img src="assets/showcase/readme-stat-palettes.png" width="180" alt="555 组配色"> | <img src="assets/showcase/readme-stat-visual-papers.png" width="180" alt="291 篇图形参考"> | <img src="assets/showcase/readme-stat-writing-papers.png" width="180" alt="100 篇写作参考"> |
| :---: | :---: | :---: | :---: |
| 数据图、场图与多面板组合 | 按数据含义选色，附文献来源 | 1,022 幅图件的构图与用色观察 | 英文表达与中文写作规则 |

PRL Style 从 *Physical Review Letters* 的真实论文中提炼绘图细节、配色与文章组织方式，将它们整理为 agent 可调用的规则、模板和脚本。交给它数据、草稿或研究思路，即可协助完成从图到文的表达：调整布局与图例，制作 Fig. 1，打磨中英文论证，并核对图件、图注与正文的一致性。

## 一句话安装

将下面这句话复制给 Codex、Claude Code、OpenCode、DeepSeek Harness 或其他支持 Agent Skills 的 agent，让它完成下载、安装和检查（需要联网及本地命令执行能力）：

```text
请从 https://github.com/tysun1209/prl-style 的最新 Release 下载完整发布包，确认当前 agent 的用户级 skills 目录，按 README 使用包内安装器安装 PRL Style 主 skill 和全部 8 个子 skill（没有对应的 --agent 选项时使用 --destination 指定目录），并验证文件完整性和当前 agent 能否发现这些 skill。
```

## 效果预览

### 同一批数据，使用前后

下面展示直方图、箱线图、热图与离散相图。左右使用相同数据和基础任务提示，完整原图按相同显示宽度呈现，原始物理尺寸标在图中。重点观察字体、图例、配色、留白和坐标轴的变化。

[![没用 skill 与用了 PRL Style 的四类图型对比](assets/showcase/skill-comparison.png)](assets/showcase/skill-comparison.png)

### 从 PRL 图件中提取的配色

555 组配色覆盖类别、顺序、发散、循环和多色相色标。下图为其中 9 组类别配色，每组保留配色 ID、色值及论文来源。绘图时可自动按数据含义选色，也可以指定喜欢的方案。

[![PRL 2025–2026 色卡节选：prl-025 至 prl-033](assets/showcase/palette-preview.png)](reports/prl-colors-2025-2026/palette-atlas.pdf)

[检索全部配色](reports/prl-colors-2025-2026/index.html) · [完整色卡 PDF · 555 组](reports/prl-colors-2025-2026/palette-atlas.pdf) · [配色选择与调用](references/prl-color-palettes.md)

已完成 **291 篇文献、1,022 张独立图件**的图型与用色提取，支持按图型、论文和稿件版本查找参考。所有新增色卡已并入上方 PDF。[完整文献覆盖与检索](references/visual-corpus.md) · [跨领域构图方式](references/crossfield-visual-design.md)。

### 更多图型

除了常见曲线和统计图，也支持轨迹、流线、时空场、三维曲面与网络等表达方式。点击图片可查看完整尺寸。

| 误差带 | 流线场 | 粒子轨迹 |
| :---: | :---: | :---: |
| [<img src="assets/showcase/uncertainty-band.png" width="240" alt="误差带图示例">](assets/showcase/uncertainty-band.png) | [<img src="assets/showcase/streamlines.png" width="240" alt="流线场示例">](assets/showcase/streamlines.png) | [<img src="assets/showcase/trajectory.png" width="240" alt="粒子轨迹示例">](assets/showcase/trajectory.png) |

| 时空图 | 三维曲面 | 网络图 |
| :---: | :---: | :---: |
| [<img src="assets/showcase/space-time.png" width="240" alt="时空图示例">](assets/showcase/space-time.png) | [<img src="assets/showcase/surface-3d.png" width="240" alt="三维曲面示例">](assets/showcase/surface-3d.png) | [<img src="assets/showcase/network.png" width="240" alt="网络图示例">](assets/showcase/network.png) |

对比图和图型示例使用合成数据；六张画廊图由随附绘图配方生成。[查看全部 36 类图型](references/figure-families.md)。

**Fig. 1：流程图与科学示意图**

[![内置图像模型生成的 Fig. 1 示例](assets/examples/model-first-schematic/fig1-model.png)](assets/examples/model-first-schematic/fig1-model.png)

先由内置绘图模型生成 PNG，再重建文字、形状、曲线与箭头可独立修改的 PPT。[下载可编辑示例](assets/examples/model-first-schematic/fig1.pptx) · [查看 PPT 实际渲染](assets/examples/model-first-schematic/fig1.preview.png) · [制作方法](references/schematic-image-pptx.md)。示例为原创概念图，不是实验或模拟结果。

## 能做什么

使用主入口 `prl-style` 可以组合完成绘图、图注和写作；单项任务也可以直接调用对应的子 skill。下表和示例采用 Codex 的 `$` 调用写法，其他 agent 的写法见安装说明。

| 入口 | 功能 |
| --- | --- |
| `$prl-figures` | 根据数据绘图、修改已有绘图代码，调整多面板布局、配色、字体、坐标轴与图例；默认保存 600 dpi PNG，按需导出 PDF、EPS、SVG 等格式。 |
| `$prl-schematics` | 用内置绘图模型生成 Fig. 1、模型／装置示意和流程图，再重建可编辑 PPT；包含量子线路、光路、散射顶点等跨领域构图指导。 |
| `$prl-writing-en` | 起草、润色、压缩和重组英文标题、摘要、引言、结果与结论，梳理整篇 Letter 的论证结构。 |
| `$prl-writing-zh` | 撰写和修改中文科研稿件，将紧凑的论证方式用于自然中文表达。 |
| `$prl-bilingual` | 中英互译与双语对照，核对术语、数值、单位、符号和结论含义。 |
| `$prl-captions` | 根据图片及实验或计算说明撰写中英文图注，核对面板、颜色、符号、误差定义与正文引用。 |
| `$prl-review` | 检查图件、图注、正文的一致性，以及成稿中的排版和表达问题，给出具体修改建议。 |
| `$prl-evidence` | 查询风格规则的文献依据，分析新的论文样例并维护参考库。 |

**绘图覆盖 36 类图型**，包括曲线、散点、误差棒与误差带、统计分布、相图、热图、标度坍缩、矢量场、粒子轨迹、时空图、频谱、能带、网络、示意图和多面板组合。详见[图型目录](references/figure-families.md)。

**Fig. 1 示意图子 skill**：从原有 100 篇中检查 96 张 Fig. 1，识别出 48 张示意或混合图；新增 50 篇跨领域图形参考，每篇保留具体观察与来源。默认采用“模型 PNG → 可编辑 PPT”，也保留六个 Python 示例供按需使用。详见[设计指南](references/prl-schematics.md)与[跨领域构图](references/crossfield-visual-design.md)。

**配色库包含 555 组方案**，在全部 291 篇文献的图件提取基础上，覆盖类别色、顺序、发散、循环和多色相色标，每组均附论文来源与用色含义。可浏览[最新配色图册](reports/prl-colors-2025-2026/index.html)，再指定配色 ID 使用。

**写作参考库收录 100 篇 PRL 论文**，聚焦粒子运动、活性粒子和强化学习相关研究。写作强调明确的物理问题、紧凑的证据链和直接的结果表达；精简重复铺垫与空泛限定，同时保留实际适用条件和不确定性。

## 安装与接入

支持 Codex、Claude Code、OpenCode、DeepSeek Harness 等采用 Agent Skills 的助手。目前完整工作流主要在 Codex 中验证，其他 agent 已验证安装目录与脚本运行，完整交互流程尚未实测。

当前版本见 [VERSION](VERSION)。更新时，使用新发布包再次运行同一安装命令；继续使用 `$prl-style` 或原来的子 skill 名称。

解压发布包，在包含 `install.py` 的目录运行以下任一命令（Python 3.10+）：

```bash
python3 install.py --agent codex
python3 install.py --agent claude-code
python3 install.py --agent opencode
python3 install.py --agent deepseek-harness
```

每条命令为所选 agent 安装主入口和 8 个子 skill 的独立副本。安装后的 skill 文件不依赖原始解压目录；运行脚本的 Python 环境需单独保留。
默认用户目录分别为 `~/.agents/skills`、`~/.claude/skills`、`~/.config/opencode/skills` 和 `~/.dsh/skills`；
OpenCode 尊重 `XDG_CONFIG_HOME`，Harness 尊重 `DSH_HOME`。`CODEX_HOME` 不改变 Codex 的新默认目录。可用 `--destination PATH` 指定其他父目录。
已有其他来源的同名 skill 时安装器会停止；更新本发布包安装的 skill 时会保留旧副本。Codex 默认安装会将旧 `CODEX_HOME/skills`（默认 `~/.codex/skills`）中由本发布包管理的副本迁出扫描目录并备份，避免重复条目；不会移动其他来源的技能。

| Agent | 调用主入口 |
| --- | --- |
| Codex | `$prl-style` |
| [Claude Code](https://code.claude.com/docs/en/skills) | `/prl-style` |
| [OpenCode](https://opencode.ai/docs/skills) | `@prl-style` |
| [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md) | `/prl-style` |

子 skill 沿用各平台的前缀，例如 `/prl-writing-en`。

**DeepSeek Harness：** 在实际运行 Harness 的机器上执行。默认安装到 `~/.dsh/skills`（设置了 `DSH_HOME` 时使用其下的 `skills` 目录）；另一台机器上的 Codex 安装不会自动同步：

```bash
python3 install.py --agent deepseek-harness
python3 install.py --agent deepseek-harness --check
```

安装后在 DeepSeek Harness 中输入 `/prl-style`，或 `/prl-figures`、`/prl-writing-zh` 等子 skill 名称。自定义了技能目录时，使用配置中的实际路径；其目录发现和调用方式见 [Skills 文档](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md)与[调用说明](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/tool-skill/README.md)。

**安装后验证：** 在 Codex 中运行 `/skills` 或输入 `$prl`，应能选到 `$prl-style` 及 8 个子 skill；Harness 中输入 `/prl-style`。主入口名称是 `prl-style`，没有独立的 `prl` 别名。若未出现，重启 agent，并确认运行机器、用户和安装目录一致。技能入口使用普通文件，安装器不创建 `SKILL.md` 文件软链接。

**其他 agent：** 支持 Agent Skills 时，用 `--destination PATH` 指向该 agent 的技能父目录，安装器会创建 9 个独立 skill 文件夹并携带完整资源。安装后在目标 agent 中确认能发现并加载 `prl-style`；`--check` 只检查已安装文件。没有自动发现功能时，可让 agent 直接读取解压目录中的 `SKILL.md` 和相关资料。

绘图和检查需要文件读写、Python 执行及图像查看能力。
示意图／流程图默认还需要宿主内置图像生成工具；PPT 重建使用 python-pptx，实际渲染核对可用 PowerPoint 或 LibreOffice。
上面的命令适用于 Linux/macOS；Windows 可将 `python3` 换成 `python -X utf8`，该系统尚未实测。

需要绘图或运行检查脚本时，在发布包根目录准备 Python 环境：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

在 agent 中运行脚本时使用这个环境的 Python。Windows 对应命令为 `.venv\Scripts\python.exe -X utf8`。
纯文字起草、润色和翻译不需要绘图库、字体或 LaTeX；编译论文 PDF 需要相应的 LaTeX 引擎及模板依赖。

可检查包完整性与已安装内容：

```bash
python3 scripts/verify_package.py
python3 install.py --agent codex --check
```

发布包包含规则、来源索引和原创示例。论文原文与原图通过 DOI 单独获取；字体文件不随包分发。

## 怎么使用

例如：`使用 $prl-schematics，根据下面的模型与方法画论文 Fig. 1，生成 PNG 和可编辑 PPT，附简洁图注。` 随后提供物理对象、相互作用或流程步骤即可；也可直接说“画模型示意图”，默认走内置绘图模型。宿主需要具备图像生成工具；重建 PPT 需 Python 和 python-pptx，实际渲染核对可用 PowerPoint 或 LibreOffice。

提供文件或内容，并说明希望得到的结果即可。绘图时说明数据列、单位和误差含义；写作时附上已有结果、参考文献和篇幅要求。可以指定字体、颜色、图尺寸、术语和修改范围。

**绘图、选色与图注一起完成：**

```text
$prl-style 根据 results.csv 绘制五组参数的曲线对比图。
从配色库中选择适合白底曲线的五色方案，输出单栏 PNG、绘图代码和英文图注。
各列含义、单位和误差定义见 data-notes.md。
```

数据图不指定格式时保存 **600 dpi PNG**。需要其他格式时直接补充“同时保存 PDF”或“只导出 EPS”；也可指定其他 dpi。脚本对应参数为 `--formats png pdf`、`--formats eps` 和 `--dpi 1200`。示意图／流程图默认另交付可编辑 PPTX；生成 PNG 的实际分辨率按原生像素核查。

**修改英文稿件：**

```text
$prl-writing-en 修改 draft.tex，使摘要和结果部分更紧凑、直接。
保留数值、引用和结论的适用范围，返回修改稿并简要说明主要结构调整。
```

**撰写中文稿件：**

```text
$prl-writing-zh 根据 results.md 和 figures/ 中的图件撰写中文结果部分。
围绕物理发现组织段落，避免逐图流水账，使用自然中文表达。
```

**根据图片生成图注：**

```text
$prl-captions 根据 figure1.pdf 和 methods.md 撰写中英文图注。
说明各面板、线型和误差带的含义；缺少的信息列在图注后供我补充。
```

**中英对照检查：**

```text
$prl-bilingual 对照 manuscript-zh.md 与 manuscript-en.tex，
修正术语、数值、条件和结论含义不一致的地方，并润色英文表达。
```

仅有图片时，可以先生成基于可见内容的图注草稿；样本量、误差定义和实验条件需要作者提供。绘图示例使用合成数据，实际研究任务请提供自己的数据。

## 默认风格

- **字体：** 英文和数字使用 Times New Roman，中文使用宋体（SimSun）。指定字体的图件与文档导出需要本机具备对应字体；聊天和 Markdown 的显示字体由客户端决定。
- **图面：** 刻度朝内；保留坐标、单位、图例、色标和面板编号，解释性小字放在独立图注或正文中。
- **图例与布局：** 图例优先放在不遮挡数据的图内空白处；多面板按实际绘图区对齐，压缩不必要的间距，为色标单独预留空间。
- **配色与刻度：** 未指定颜色时，结合图型、数据含义、对象数量与背景，从 555 组来源配色中自动选择：曲线清晰可辨、相区柔和填色、连续量有序渐变、正负量围绕指定中心发散；同一对象跨面板保持同色。也可指定色卡或自定义颜色。上侧、右侧刻度逐面板选择。
- **输出：** 数据图默认 600 dpi PNG；示意图先由模型生成 PNG，再重建可编辑 PPTX，保留原生像素并核查有效分辨率。PDF、EPS、SVG 和灰度图按需生成。文字任务先交付正文，再简述必要修改。
- **写作：** 保留科学事实与证据强度，直接陈述有依据的结果，减少重复限定和无信息量的套话。

本项目是独立工具，以上为可调整的默认设置。中文写作用于科研工作稿；实际投稿的语言、篇幅与格式要求以 PRL 官方指南为准。

## 进一步使用

- [配色选择与 Python 调用](references/prl-color-palettes.md)
- [图型目录与示例生成](references/figure-families.md)
- [英文写作指南](references/writing-en.md) · [中文写作指南](references/writing-zh.md)
- [图注写作指南](references/caption-writing.md)
- [给代理使用的完整指令](SKILL.md)
