# 代码讲解说明（中文）

这份文档的目标不是让你背所有代码，而是让你知道：

1. 项目里最重要的文件在哪
2. 老师如果要求看代码，应该先开什么
3. 每个关键函数大概在做什么
4. 哪些地方必须知道，哪些地方可以少讲

## 1. 先记住三条主线
整个项目可以分成三条线：

1. 真实 benchmark 重跑主线
2. dispatch demo 主线
3. 结果与答辩材料生成主线

答辩时不要一上来在目录里乱翻。只要按这三条主线讲，老师会觉得你对项目结构是清楚的。

## 2. 最重要的目录

### `scripts/`
放正式实验脚本和结果资产生成脚本。

### `osag_demo/`
放 dispatch demo 的运行入口、调度逻辑和图表输出逻辑。

### `results/`
放 fresh rerun 的结果表、图和 runtime 汇总。

### `reports/`
放讲稿、FAQ、审计说明、代码说明和答辩准备材料。

## 3. 最重要的文件

### 必须知道
- `scripts/run_all_real_experiments.py`
- `scripts/reproduce_osag_real.py`
- `osag_demo/run_visual_demo.py`
- `osag_demo/run_dispatch_demo.py`
- `osag_demo/dispatch_demo_core.py`
- `osag_demo/dispatch_demo_assets.py`

### 最好也知道
- `scripts/generate_real_result_assets.py`
- `osag_demo/launch_visual_demo.py`

## 4. 如果老师要看 benchmark 代码，按什么顺序开

### 第一步：`scripts/run_all_real_experiments.py`
这是一键总入口。
你可以先说：

“这是正式主实验的统一入口，负责按配置去调用真实 rerun 管线。”

### 第二步：`scripts/reproduce_osag_real.py`
这是核心实现文件。
绝大多数关键逻辑都在这里。

老师通常真正想看的，是下面几个点。

## 5. 关键逻辑分别在哪

### 5.1 contract construction
文件：
`scripts/reproduce_osag_real.py`

函数：
`build_contract_table_from_meta`

这部分做的事：
- 先根据若干字段拼出 `contract_key`
- 再给每个合同分配 `contract_id`
- 统计每个合同有多少样本
- 根据规则赋予 priority
- 计算 `raw_weight = priority * num_samples`
- 最后归一化成 `target_weight`

你可以口头这样讲：

“这一段把抽象的合同概念真正落到数据表里，后面的采样和覆盖监控都依赖这里生成的合同表。”

### 5.2 target service share
主 benchmark 里还是在 `build_contract_table_from_meta` 这条逻辑里完成。

本质上就是：
- 先定义合同
- 再根据优先级和合同规模算出目标份额

dispatch demo 里，对应的是 `osag_demo/dispatch_demo_core.py` 顶部的 `CONTRACTS` 常量。

你可以这样讲：

“benchmark 里 target share 是从数据统计出来的，demo 里 target share 是按场景直接定义的，但两边遵循的是同一套治理思想。”

### 5.3 OSAG sampler logic
文件：
`osag_demo/dispatch_demo_core.py`

函数：
`choose_observations`

这段逻辑把以下因素合成调度分数：
- urgency
- deadline pressure
- coverage gap
- uncertainty
- priority

你可以这样讲：

“OSAG 在 demo 里不是随机选格子，而是把紧急度、时限压力、覆盖缺口和优先级综合成一个调度分数。”

### 5.4 fairness loss
文件：
`scripts/reproduce_osag_real.py`

位置：
`run_one` 训练循环里 `osag_priority_fairloss` 的分支

这部分逻辑是：
- 分开看高优先级样本和低优先级样本的 loss
- 如果高优先级更难学，就增加 penalty
- `lambda_c` 控制 penalty 强度

你可以这样讲：

“fairness loss 不是单独一套模型，而是在已有训练循环里加一项补偿，避免高优先级合同长期更难学却得不到额外压力。”

### 5.5 coverage monitoring
文件：
`scripts/reproduce_osag_real.py`

函数：
`compute_coverage_errors`

作用：
- 根据 `contract_counts` 计算 observed coverage
- 和 `target_weight` 做比较
- 输出 PrioCovErr 等覆盖偏差指标

你可以这样讲：

“这部分是治理层里最关键的可观测量，没有它就无法判断训练是否真正按目标服务合同。”

## 6. demo 代码怎么看

### 入口文件
- `osag_demo/run_visual_demo.py`
- `osag_demo/run_dispatch_demo.py`

### 核心逻辑
- `osag_demo/dispatch_demo_core.py`

### 输出资产
- `osag_demo/dispatch_demo_assets.py`

最稳的讲法是：

1. 先展示入口
2. 再展示核心调度逻辑
3. 最后展示输出图和 dashboard

## 7. 如果老师让我“打开代码给我看”，最稳顺序

1. `scripts/run_all_real_experiments.py`
2. `scripts/reproduce_osag_real.py`
3. `build_contract_table_from_meta`
4. `compute_coverage_errors`
5. `osag_demo/run_dispatch_demo.py`
6. `osag_demo/dispatch_demo_core.py`
7. `choose_observations`

这个顺序好处是：
- 先让老师看到总入口
- 再看到核心合同和治理逻辑
- 最后再看 demo 如何把同样思想变成动态调度

## 8. 哪些文件是“必须知道”

### 必须知道
- `scripts/run_all_real_experiments.py`
- `scripts/reproduce_osag_real.py`
- `osag_demo/run_dispatch_demo.py`
- `osag_demo/dispatch_demo_core.py`

### 锦上添花
- `scripts/generate_real_result_assets.py`
- `osag_demo/dispatch_demo_assets.py`
- `osag_demo/launch_visual_demo.py`

## 9. 时间不够时不要过度展开什么

1. 不要现场讲完整训练循环的每一行。
2. 不要把所有 baseline 的实现细节都翻出来。
3. 不要把 deck/build 脚本讲成主线。
4. 不要在 demo 阶段陷进 HTML 细节。

最值得讲的永远是：

1. 合同怎么构造
2. 目标份额怎么得到
3. OSAG 如何根据这些信息影响采样/调度
4. 覆盖偏差怎么被监控出来

## 10. 最后一句话
如果老师突然说“给我看看代码”，你最稳的策略不是证明你会背所有实现，而是把代码讲成一条清楚的链：

“这里是实验入口，这里是合同构造，这里是治理控制，这里是覆盖监控，这里是 demo 调度入口。”
