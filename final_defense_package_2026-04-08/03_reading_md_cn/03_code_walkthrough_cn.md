# 代码走读说明（中文）

## 1. 先记住一句话
这套代码可以分成三条主线：真实 benchmark 重跑主线、dispatch demo 主线、答辩材料生成主线。答辩时不要一上来翻很多文件，按这三条主线讲就会很稳。

## 2. 项目目录怎么理解
- `scripts/`：正式实验脚本、结果表图生成脚本、答辩 deck 生成脚本。
- `osag_demo/`：dispatch demo 的核心逻辑、图表输出、dashboard 生成与启动入口。
- `results/`：真实重跑后的表、图、runtime 汇总。
- `deliverables/`：最终答辩 PPT/PDF。
- `reports/`：讲稿、FAQ、审计说明、代码讲解材料。
- `LaTeX_Thesis2026/LaTeX_Thesis2026/`：最终 thesis PDF 与其引用图表。

## 3. 哪些文件最重要
### 必须知道
- `scripts/run_all_real_experiments.py`
- `scripts/reproduce_osag_real.py`
- `osag_demo/run_dispatch_demo.py`
- `osag_demo/dispatch_demo_core.py`
- `osag_demo/dispatch_demo_assets.py`
- `osag_demo/launch_visual_demo.py`

### 最好也知道
- `scripts/generate_real_result_assets.py`
- `osag_demo/run_visual_demo.py`
- `osag_demo/run_osag_demo.py`

## 4. 关键逻辑分别在哪
### contract construction
主看：`scripts/reproduce_osag_real.py`
函数：`build_contract_table_from_meta`
作用：
- 组合出 `contract_key`
- 为每个 contract 分配 `contract_id`
- 统计 `num_samples`
- 生成 priority
- 计算 `raw_weight = priority * num_samples`
- 归一化成 `target_weight`

### target service share computation
benchmark 主线仍然是 `build_contract_table_from_meta`。
demo 里对应的是 `osag_demo/dispatch_demo_core.py` 顶部的 `CONTRACTS` 常量。
benchmark 是从数据统计出来，demo 是按场景直接定义，但两边逻辑都是“先有 contract，再有 target share”。

### OSAG sampler logic
demo 主看：`osag_demo/dispatch_demo_core.py`
函数：`choose_observations`
这个函数把 `urgency`、`deadline_pressure`、`coverage_gap`、`uncertainty` 和 `priority_norm` 合成调度分数。

### fairness loss
主看：`scripts/reproduce_osag_real.py`
位置：`run_one` 训练循环里的 `osag_priority_fairloss`
逻辑是：
- 高优先级样本与低优先级样本分别求 loss
- 如果高优先级更难，就加 penalty
- `lambda_c` 控制 penalty 强度

### coverage monitoring
主看：`scripts/reproduce_osag_real.py`
训练里累计 `contract_counts`，再把 observed coverage 和 target share 比较，得到 `PrioCovErr`。

### demo launch
- 生成 demo：`osag_demo/run_dispatch_demo.py`
- 简化入口：`osag_demo/run_visual_demo.py`
- 打开 dashboard：`osag_demo/launch_visual_demo.py`

### benchmark rerun entry
- 总入口：`scripts/run_all_real_experiments.py`
- 核心实现：`scripts/reproduce_osag_real.py`
- 结果资产生成：`scripts/generate_real_result_assets.py`

## 5. 老师要看代码时，先打开什么
最稳顺序：
1. `scripts/run_all_real_experiments.py`
2. `scripts/reproduce_osag_real.py`
3. `build_contract_table_from_meta`
4. `run_one` 里的 fairloss 分支
5. `osag_demo/run_dispatch_demo.py`
6. `osag_demo/dispatch_demo_core.py`
7. `choose_observations`

## 6. 哪些是 must know
- `build_contract_table_from_meta` 为什么关键
- `choose_observations` 为什么关键
- `lambda_c` 在哪里生效
- `PrioCovErr` 为什么是正式可计算的治理指标
- demo 的启动脚本和 dashboard 路径

## 7. 哪些是 nice to know
- 图表生成脚本的细节
- 旧 synthetic demo 代码
- 早期 deck 构建脚本的具体版式实现

## 8. 时间不够时不要过度展开什么
- 不要把整个训练循环逐行讲完
- 不要把 dashboard 前端细节讲太多
- 不要把所有 helper function 都打开
- 不要让代码展示喧宾夺主，主线还是 thesis 的治理逻辑
