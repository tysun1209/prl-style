# PRL Style

面向支持 Agent Skills 的 AI 助手的科研绘图与中英文写作 skill。参考 *Physical Review Letters*（PRL）的图形表达和论文组织方式，帮助研究者把数据、图注与正文组织成清晰、紧凑的科学论证。

核心由 `SKILL.md`、参考资料、模板和 Python 脚本组成，可用于 Codex，也可接入 Claude Code、OpenCode 等支持该格式的 agent。目前工作流主要在 Codex 中验证，其他 agent 的完整执行效果尚未实测。

## 能做什么

使用主入口 `prl-style` 可以组合完成绘图、图注和写作；单项任务也可以直接调用对应的子 skill。下表和示例采用 Codex 的 `$` 调用写法，其他 agent 的写法见安装说明。

| 入口 | 功能 |
| --- | --- |
| `$prl-figures` | 根据数据绘图、修改已有绘图代码，调整多面板布局、配色、字体、坐标轴与图例，导出 PDF、PNG 和绘图代码。 |
| `$prl-writing-en` | 起草、润色、压缩和重组英文标题、摘要、引言、结果与结论，梳理整篇 Letter 的论证结构。 |
| `$prl-writing-zh` | 撰写和修改中文科研稿件，将紧凑的论证方式用于自然中文表达。 |
| `$prl-bilingual` | 中英互译与双语对照，核对术语、数值、单位、符号和结论含义。 |
| `$prl-captions` | 根据图片及实验或计算说明撰写中英文图注，核对面板、颜色、符号、误差定义与正文引用。 |
| `$prl-review` | 检查图件、图注、正文的一致性，以及成稿中的排版和表达问题，给出具体修改建议。 |
| `$prl-evidence` | 查询风格规则的文献依据，分析新的论文样例并维护参考库。 |

**绘图覆盖 36 类图型**，包括曲线、散点、误差棒与误差带、统计分布、相图、热图、标度坍缩、矢量场、粒子轨迹、时空图、频谱、能带、网络、示意图和多面板组合。详见[图型目录](references/figure-families.md)。

**配色库包含 117 组方案**，提取自 2025-01-01 至 2026-11-08 发表的 PRL 图件，覆盖类别色、顺序色标、发散色标和多色相色标，每组均附论文来源。可浏览[配色图册](reports/prl-colors-2025-2026/index.html)或下载[色卡 PDF](reports/prl-colors-2025-2026/palette-atlas.pdf)，再指定配色 ID 使用。

**写作参考库收录 100 篇 PRL 论文**，聚焦粒子运动、活性粒子和强化学习相关研究。写作强调明确的物理问题、紧凑的证据链和直接的结果表达；精简重复铺垫与空泛限定，同时保留实际适用条件和不确定性。

## 安装与接入

解压发布包，在包含 `install.py` 的目录运行以下任一命令（Python 3.10+）：

```bash
python3 install.py --agent codex
python3 install.py --agent claude-code
python3 install.py --agent opencode
```

每条命令为所选 agent 安装主入口和 7 个子 skill 的独立副本。安装后的 skill 文件不依赖原始解压目录；运行脚本的 Python 环境需单独保留。
默认用户目录分别为 `~/.codex/skills`、`~/.claude/skills` 和 `~/.config/opencode/skills`；
Codex 尊重 `CODEX_HOME`，OpenCode 尊重 `XDG_CONFIG_HOME`。可用 `--destination PATH` 指定其他父目录。
已有其他来源的同名 skill 时安装器会停止；更新本发布包安装的 skill 时会保留旧副本。

| Agent | 调用主入口 |
| --- | --- |
| Codex | `$prl-style` |
| [Claude Code](https://code.claude.com/docs/en/skills) | `/prl-style` |
| [OpenCode](https://opencode.ai/docs/skills) | `@prl-style` |

子 skill 沿用各平台的前缀，例如 `/prl-writing-en`。也可以让能够读取本地文件的 agent
直接读取解压目录中的 `SKILL.md`。绘图和检查需要文件读写、Python 执行及图像查看能力。
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

提供文件或内容，并说明希望得到的结果即可。绘图时说明数据列、单位和误差含义；写作时附上已有结果、参考文献和篇幅要求。可以指定字体、颜色、图尺寸、术语和修改范围。

**绘图、选色与图注一起完成：**

```text
$prl-style 根据 results.csv 绘制五组参数的曲线对比图。
从配色库中选择适合白底曲线的五色方案，输出单栏 PDF、PNG、绘图代码和英文图注。
各列含义、单位和误差定义见 data-notes.md。
```

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
- **输出：** 图件默认提供彩色 PDF 与 PNG；灰度版本按需生成。文字任务先交付正文，随后简要说明必要的修改或缺失信息。
- **写作：** 保留科学事实与证据强度，直接陈述有依据的结果，减少重复限定和无信息量的套话。

本项目是独立工具，以上为可调整的默认设置。中文写作用于科研工作稿；实际投稿的语言、篇幅与格式要求以 PRL 官方指南为准。

## 进一步使用

- [配色选择与 Python 调用](references/prl-color-palettes.md)
- [图型目录与示例生成](references/figure-families.md)
- [英文写作指南](references/writing-en.md) · [中文写作指南](references/writing-zh.md)
- [图注写作指南](references/caption-writing.md)
- [给代理使用的完整指令](SKILL.md)
