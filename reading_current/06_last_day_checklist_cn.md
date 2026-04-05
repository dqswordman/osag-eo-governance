# 答辩前一天检查清单（中文）

这份清单只保留最实用的内容。答辩前一天不要再做大改动，重点是确认材料、路径、讲法和备选方案都稳。

## 1. 纸质和电子材料

### 纸质
- 论文最终 PDF 是否正确
- 封面和目录是否正常
- 参考文献是否无明显错误

### 电子
- 当前 official short deck 是否是最新版
- deck 的 PDF 预览是否能正常打开
- 最终 thesis PDF 是否能正常打开

## 2. 你要带什么文件

优先准备：
- thesis PDF
- 当前英文答辩 PPT
- bilingual slide-by-slide script
- 中文 FAQ
- 中文 code walkthrough
- demo quick commands

## 3. 你最先要会说的三句话

1. 我的 thesis 研究的是 governance-aware EO training。
2. OSAG 的作用是让训练过程按合同目标分配服务，而不是只看平均准确率。
3. 真实 benchmark 是主证据，dispatch demo 是行为解释补充。

## 4. 你最容易讲错的点

1. EuroSAT fine 是 6，不是 12。
2. Table 5.2 是 absolute percentage-point differences。
3. `Q_high` 不等于 `K`。
4. HSI split 是 pixel-stratified，不是 spatial-blocked。
5. runtime 只能讲 comparable overhead。

## 5. deck 检查

- 是否是当前短版 deck
- 字号是否足够大
- 首页是否干净
- Figure 1 是否是最新版本
- 是否没有旧的 15-minute wording
- 是否没有乱码或奇怪字符

## 6. demo 检查

- `run_visual_demo.py` 路径是否记得
- `launch_visual_demo.py` 路径是否记得
- `visual_outputs/` 下的 HTML 和 PNG 是否都在
- dashboard 是否能打开
- 如果打不开，是否知道先展示保存好的 PNG

## 7. 代码检查

最先记住这几个文件：

1. `scripts/run_all_real_experiments.py`
2. `scripts/reproduce_osag_real.py`
3. `osag_demo/run_dispatch_demo.py`
4. `osag_demo/dispatch_demo_core.py`

最先记住这几个函数或逻辑点：

1. `build_contract_table_from_meta`
2. `compute_coverage_errors`
3. `choose_observations`

## 8. 如果紧张，上台前先做什么

1. 不要再改文件
2. 先把 opening 三句话默念一遍
3. 再把目录和 slide 1 到 slide 3 过一遍
4. 记住你不需要背全文，只需要把主线讲顺

## 9. 如果老师现场突然追代码
你最稳的第一句话可以是：

“我先从正式实验入口开始，再展示合同构造、覆盖监控和 demo 调度逻辑。”

## 10. 如果老师现场突然追边界
你最稳的第一句话可以是：

“这篇 thesis 的边界我会直接说明：HSI split 不是 spatial-blocked，graph 目前主要是 modeling view，demo 是补充而不是主证据。”

## 11. 最后一句提醒
答辩前一天最重要的不是再加内容，而是保证你现在这套材料：

- 讲得顺
- 路径清楚
- 文件能打开
- 老师追问时你知道先看哪里
