# 全部 291 篇 PRL 的图型与配色参考

已逐图查看保留文献中的 **1,022 张独立编号图件**，来自 286 篇论文；另外 5 篇没有编号图。扫描得到的 1,025 条记录中有 3 条重复图记录，已合并但保留原 ID。来源包括 235 篇正式出版 PDF 和 56 篇 CHORUS 录用稿，发表日期覆盖 2010–2026 年。

## 查找原图参考

```bash
python scripts/select_visual_references.py --family trajectory --limit 5
python scripts/select_visual_references.py --family heatmap --version publisher_pdf
python scripts/select_visual_references.py --pattern bar_comparison
python scripts/select_visual_references.py --paper P010 --verify-assets
python scripts/select_visual_references.py --query "反馈"
```

返回 DOI、图号、PDF 页码、裁切坐标、图型、配色含义和原始文件哈希。默认排除 25 篇既有留出集论文，优先返回正式出版版；`--include-holdout` 用于审计。`--verify-assets` 仅在本机原文存在时检查哈希；公开包没有原文也能检索来源位置。

[完整来源索引](visual-corpus-sources.json)包括所有论文的逐篇处理结果。开发目录的 `corpus/visual-prl-291-2026-11-14/index.html` 可筛选、查看原图，并打开 600 dpi 裁切；`paper-coverage.csv` 是逐篇清单。论文 PDF 和裁切不随公开包分发。

## 图型与配色如何使用

图型采用多标签：同一张图可以同时含示意图、曲线、热图和放大框。此批识别到现有 36 类配方中的 **34 类**，另记录柱形比较、饼图和响应矩阵三种观察形式。没有将普通矩阵误标为相关矩阵，也没有把柱形比较混入统计直方图。箱线／小提琴图、相关矩阵在本批没有确认的独立来源，仍是可用配方。

颜色分两层保存：所有图件均有测色结果和角色观察；经过角色选择的色卡进入[可调用配色库](prl-color-palettes.md)。渐变图的主要像素颜色不能直接当成类别色，透明误差带也不新增类别。没有可靠取色路径的连续图保留原图与测量，不臆造色标函数。

当前合并配色库有 **555 组**，来自 241 篇论文的 611 个不同“DOI＋图号”，保留 701 条跨批次取色记录。旧 133 组编号、色值和插值方式保持不变。全部色卡合并在同一个 [PDF](../reports/prl-colors-2025-2026/palette-atlas.pdf)。

## 范围

这是图型和用色的来源观察，不是整个 PRL 的频率统计，也不改变既有 100 篇写作研究。复核类型为 `agent_visual_review`；之前等待用户核验的流程图／示意图候选集仍保持原状态。

新归纳排除全部既有留出集。历史配色库有一篇与写作留出集交叠（DOI `10.1103/xs9l-1233`）；其旧配色保留，并在配色库的 `historical_holdout_overlap` 显式记录。这篇不能再作为独立配色评测来源。

维护入口：`extract_visual_corpus.py` → 逐图记录 `visual-review-notes.tsv` 与实际色条路径 `palette-specs.json` → `build_visual_corpus.py` → `build_prl_palettes.py` → `render_prl_palettes.py`。裁切修正有独立坐标记录，取色和复核绑定实际文件哈希。
