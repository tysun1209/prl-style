# 按图型与数据含义自动选色

默认先判断颜色表达的物理含义，再结合图型、对象数、绘制方式和背景，从现有 555 组色卡中筛选。用户指定的颜色优先；同一论文中已经确定的对象—颜色映射直接复用。

| 颜色承担的任务 | 默认做法 |
|---|---|
| 独立类别曲线、散点、误差棒 | 选择与背景对比充足、彼此可辨的类别色；实际类别数决定取色数，配合线型/点型。 |
| 误差带 | 主曲线与带共用色相，带使用透明度；不把同一组拆成两种类别色。 |
| 离散相区、箱线与小提琴分组 | 使用较柔和的面积色，细边界、黑色中位线帮助阅读；同组在不同面板同色。 |
| 强度、概率、密度、速率 | 使用明暗基本单向变化的顺序色标，保留数据范围与方向。 |
| 连续参数扫描 | 按真实参数值取色并共享归一化、色条；白底曲线避开过浅的部分，记录实际采用的源色标区间。 |
| 相对指定参考点的正负偏离 | 使用发散色标，明确中心；不因为数据出现负数就自行推断参考点。 |
| 周期相位、方向 | 明确颜色编码周期变量时使用端点近似闭合的循环色标；极坐标图、相图不自动等同于周期色标。 |
| 离散数值区间 | 显式选择阶梯色标，保留原分箱，或提供真实边界；不插值为连续色条。 |

图型建议覆盖全部 36 类。单幅图可以同时有类别、强度和相位等不同编码，应分别选色。可辨性不够时减少同时比较的对象或分面，不重复循环少量颜色来冒充更多类别。多面板的同一量还需共用范围、参考点和单位；共享色卡并不等于共享数值尺度。

## 简单调用

```bash
python scripts/prl_palette.py --recommend --family line_comparison --n-colors 3
python scripts/prl_palette.py --recommend --family phase_discrete --n-colors 5
python scripts/prl_palette.py --recommend --family heatmap --kind diverging
```

脚本路径位于已安装 skill 的 `scripts/` 中；使用已经满足 `requirements.txt` 的 Python 环境。

```python
from prl_figure import figure_context, new_figure, export_figure

with figure_context(family='line_comparison', objects=['control', 'treatment']) as plan:
    fig, ax = new_figure()
    ax.plot(x, control, color=plan['object_colors']['control'], label='Control')
    ax.plot(x, treatment, color=plan['object_colors']['treatment'], ls='--', label='Treatment')
    # 添加真实坐标、单位、图例；export_figure 默认写出 600 dpi PNG 和检查记录。
    export_figure(fig, 'response', {'palette': plan, 'data_file': 'measurements.csv'})
```

`figure_context(..., palette_id='prl-070')` 使用指定色卡；`colors=['#4477AA', '#CC6677']` 使用自定义类别颜色。跨图复用 `plan['object_colors']`，不要在每个子集上重新编号。

```python
from palette_selection import select_palette, plan_colormap, plan_norm

plan = select_palette('heatmap', role='diverging')
cmap = plan_colormap(plan)
norm = plan_norm(plan, vmin=-2, vmax=6, center=0)
# im = ax.imshow(field, cmap=cmap, norm=norm)
# fig.colorbar(im, ax=ax, label='明确的物理量与单位')
# 导出时记录 plan 及 {'vmin': -2, 'vmax': 6, 'center': 0}。
```

实际数据的范围由绘图者提供。常数场、空数据或未知参考点不会被自动编造为一个尺度。阶梯色标用 `plan_norm(plan, boundaries=真实边界)`；若沿用原分箱比例，可显式给出 `vmin`、`vmax`。

## 筛选依据与复核

类别色按背景对比、RGB 色间距离、明暗和饱和程度筛选；填色与细线采用不同标准。连续色标检查明暗方向，发散色标检查参考点附近的中性与两侧明暗，循环色标检查端点衔接。来源中同图型的非留出图件提供辅助依据；来源匹配是图级先例，不表示该图每个面板都使用了所选色卡。

这些是可复现的本地设计启发式，不是整个 PRL 的频率统计或色觉无障碍认证。保持原始色卡不变，自动类别取色仅选择原有颜色；顺序参数曲线使用的色标区间会写入 `sample_interval`。发散和循环色标保留中心及完整周期，细线中的浅色位置可用描边或标记补足，不为提高对比而截断物理含义。结果包含色卡 ID、色值、对象映射、选择理由、候选方案和非留出 DOI。

最终查看实际 PNG：细线是否可见、相邻区域是否分得清、背景上的比例尺是否清楚、带与曲线是否同色、图例/色条是否与实际绘图一致。源色卡的角色正确只是起点，实际画出的图才是验收对象。
