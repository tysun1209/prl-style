# PRL 来源配色：选择、含义与调用

用这份资源为曲线、相图、场图、频谱、误差带或示意图挑选有真实论文来源的颜色。当前共 **555 组**：524 组类别色、16 组顺序色标、7 组发散色标、7 组多色相色标和 1 组循环色标。已完成[全部 291 篇保留文献](visual-corpus.md)的图型和颜色提取；入库配色来自其中经过角色选择的图件。来源版本、发表日期与用途逐项保留。

- [可搜索配色图册](../reports/prl-colors-2025-2026/index.html)：按名称、用途、DOI 和类型查询。
- [跨领域新增色卡 PNG 1](../assets/showcase/crossfield-palettes-1.png) / [PNG 2](../assets/showcase/crossfield-palettes-2.png)：16 组新增配色。
- [完整色卡 PDF · 555 组](../reports/prl-colors-2025-2026/palette-atlas.pdf)：47 页，原有配色与本次增补合并为同一份 PDF；VOR 表示正式出版版，AM 表示 CHORUS 录用稿。
- [机器可读配色库](../profiles/prl-color-palettes.json)：RGB、色序、采样路径、面板角色和来源哈希。
- [采样与复核报告](../reports/prl-colors-2025-2026/distillation-report.md)：实际数量、来源范围和验收记录。
- [调用示例](../reports/prl-colors-2025-2026/usage-examples.pdf)：合成数据演示，配有[独立图注](../reports/prl-colors-2025-2026/usage-examples-caption.md)。

## 选色顺序

先确定颜色表达什么，再选组合。普通绘图默认执行[按图型、数据含义和绘制方式自动选色](automatic-palette-selection.md)，无需用户额外提出“请调用配色库”。调用 `select_palette()`，将返回值真正用于 Artist；保存配色 ID、对象—颜色映射、色标方向与归一化。`categorical()` / `colormap()` 仍用于指定色卡；用户已有明确配色时保留其选择。

| 图中任务 | 选择方式 | 来源示例 |
|---|---|---|
| 2–7 个独立物理对象 | `categorical`，配点型或线型；整篇保持对象—颜色映射 | 玫红—钢蓝—芥黄、蓝紫玫红、六色输运分量 |
| 曲线及不确定度 | 深色线、同色浅填充；区间定义写在图注 | 储备池输出、同位素半径、模型区间 |
| 离散相区 | 柔和面积填色，边界/斜纹承担额外状态 | 浅绿—淡紫—珊瑚、奶黄—粉蓝—浅珊瑚、五相活性晶粒 |
| 强度、概率、密度 | `sequential`，说明色标范围；跨面板比较时共用归一化 | 深紫—蓝绿—黄、白—蓝、白—橙棕、白—紫 |
| 相对零点的正负量 | `diverging`；明确参考中心后配置 `TwoSlopeNorm` | 检测电流、波上做功 |
| 多条连续参数曲线 | 按参数值从色标取色，附同方向色标 | 蓝—青—绿速度、蓝—紫—玫红输入 |
| 离散数值分箱 | 保留 `stepped` 色标与分箱边界，使用 `BoundaryNorm` | 紫—浅色—浅绿十阶最优概率 |
| 示意图、光路、网络 | 以器件/过程/节点角色分色，同一角色复用 | 青紫器件、蓝红青光路、浅薄荷—浅粉节点 |

**浅填色与细线色用途不同。** 浅色相区可配黑边界；移用于白底细线前，先检查最终尺寸的可辨性。中性灰、黑、白可作为参照层，不能把坐标轴黑色自动计为一个数据类别。

## 从实际图件归纳出的做法

1. **线与带共用色相。** 主曲线保留深色，区间使用同色浅填充。透明叠加后的混合色不新增类别。见 [量子储备池 Fig. 3](https://journals.aps.org/prl/abstract/10.1103/vp79-8t1l)。
2. **面积填色、边界和线型各负其责。** 相区颜色区分状态，边界区分区域，斜纹可表达另一属性。见 [旋转晶粒 Fig. 2](https://journals.aps.org/prl/abstract/10.1103/m3dy-53yc) 与 [管流转变 Fig. 3](https://journals.aps.org/prl/abstract/10.1103/46g3-n7cx)。
3. **同图可以同时使用类别色与连续色标。** 两种蓝色可以表示两个相区，橙色色标只描述另一相区内部的连续量；不要给整张图套同一个数值解释。见 [PRL Fig. 4](https://journals.aps.org/prl/abstract/10.1103/n7xg-dbfz)。
4. **色序要随物理量走。** 值升高可对应更亮，也可对应更暗；原图方向保存在 `sources[].direction`。调用反向色标时，数据归一化和标注也要一致。
5. **同色配不同标记/线型可以减少用色数量。** 颜色负责主比较，空实心或线型负责第二因素。见 [温度比较 Fig. 4](https://journals.aps.org/prl/abstract/10.1103/3mxj-ym4b)。

这些是带来源的可选设计做法，没有用便利样本估计整个 PRL 的采用比例。`notes` 保留特殊用法，例如原图用单向明度色序显示正负速度。全库复核补入一组来自明确相位色条的循环配色（G0283），保留负π至正π方向与近似闭合端点；普通彩虹条仍归多色相而非循环。

## Python 与命令行

在项目根目录运行；从已安装的子 skill 调用时先将脚本路径 `resolve()` 到规范位置。

```bash
.venv/bin/python scripts/prl_palette.py --kind categorical --min-colors 5
.venv/bin/python scripts/prl_palette.py --query 活性
.venv/bin/python scripts/prl_palette.py prl-001
```

```python
import sys
from pathlib import Path
skill = Path.cwd().resolve()
sys.path.insert(0, str(skill / 'scripts'))
from prl_palette import categorical, colormap, get_palette
from prl_figure import figure_context, new_figure
from matplotlib.colors import TwoSlopeNorm, BoundaryNorm

colors = categorical('prl-001', n=3)
# 在 figure_context 内：ax.plot(x, y, color=colors[0])
cmap = colormap('prl-110')
norm = TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)
# ax.imshow(field, cmap=cmap, norm=norm)

p = get_palette('prl-105')
step_cmap = colormap(p['id'])
step_norm = BoundaryNorm(p['bin_edges_normalized'], step_cmap.N)
# 实际物理区间不是 0–1 时，将归一化边界转换到该物理区间。

# 也可直接把库配色应用到局部绘图上下文，并把返回值写入 provenance：
with figure_context(palette_id='prl-070') as palette_info:
    fig, ax = new_figure()
    ax.plot([0, 1], [0, 1])  # 演示数据；实际使用时传入用户数据。
```

类别色不插值、不循环补齐。所需类别数超过配色长度时，另选足够长的方案。连续色图返回采样后的近似 sRGB 映射；`reverse=True` 可显式反向。辅助函数不修改全局 `rcParams`，不会改变 Times New Roman / 宋体、刻度朝内、默认无图内小字及默认不生成灰度图的设置。

## 数据与维护

每组配色包含 DOI、发表日期、图号/面板、角色、原图/PDF 的来源标识及 SHA-256；复核类型是 `agent_visual_review`。颜色是对应版本图件的提取近似值，不冒充作者源代码的 RGB 常量。类别色记录实际像素/局部色块；色标记录采样路径，分级色条保留分箱。原论文的数值数据没有由色图逆推。

完全相同的类别色集合合并来源。全库新增样本若与已有组合存在一一对应且最大 RGB 距离不超过 8，也合并为同一调用方案，逐来源保留实际 `source_colors`、对应索引及距离；这表示渲染近似，不表示颜色严格相同。连续色标保留方向。`near_alternatives` 提示相近类别色组合，采用 RGB 距离启发式，尚不是感知色差或色觉差异测试认证。原图含红绿组合时，应配标记/线型并检查最终图。

扩展配色时，先获取来源论文并复核实际图件，再记录 DOI、面板、用色角色、色序与分箱。发布包不含原论文或裁切图；已有色值和来源标识可直接使用。
