# 现场演示与代码答辩说明（中文）

这份文档是答辩当天的实战版说明。
目标不是重新跑大实验，而是让你在老师要求“演示软件”或“打开代码看看”时，能稳、快、清楚地应对。

## 1. 总原则

### 原则一：先讲清，再演示
不要一上来直接跑命令。
先说一句：

“我先展示 dispatch demo 的运行入口和已有输出，再根据老师关注点切到关键代码文件。”

### 原则二：不现场重跑大实验
真实 benchmark 是正式主证据，但答辩现场不应该重跑大实验。
如果老师问 benchmark 代码，展示入口和关键函数即可。

### 原则三：先展示稳定输出，再解释代码
如果 demo 已经能打开，先展示：
- dashboard
- timeline
- contract gap 图

然后再讲代码逻辑。

## 2. 最安全的现场顺序

1. 完成 PPT 主讲
2. 老师要求演示时，先打开 demo 入口
3. 展示 dashboard 或已保存输出
4. 说明三种策略的差异
5. 再打开关键代码
6. 如果老师继续追问 benchmark，再切到正式实验入口

## 3. 最常用命令

### dispatch demo
```powershell
python .\osag_demo\run_visual_demo.py
python .\osag_demo\launch_visual_demo.py
```

### benchmark 代码入口（只展示，不重跑大实验）
```powershell
python .\scripts\run_all_real_experiments.py --help
```

## 4. 如果 demo 正常启动，先展示什么

### 第一步：dashboard 主界面
口头说法：

“这里重点不是某一个像素的分类结果，而是整个系统在预算和时限约束下如何服务不同合同。”

### 第二步：策略对比
重点对比：
- Random
- Contract-Priority
- OSAG

口头说法：

“这三者分别代表无治理、激进启发式和治理策略，最适合用来解释系统行为差异。”

### 第三步：timeline
口头说法：

“这张图能看到各策略在时间推进下的服务变化，尤其能看到 OSAG 的长期稳定性。”

### 第四步：contract gap 图
口头说法：

“这里能直观看到各合同最终和目标份额之间还有多少偏差。”

## 5. 如果老师说“给我看看代码”

### 先看 benchmark 代码时
顺序：

1. `scripts/run_all_real_experiments.py`
2. `scripts/reproduce_osag_real.py`
3. `build_contract_table_from_meta`
4. `compute_coverage_errors`

口头说法：

“我先展示正式实验的总入口，再展示合同构造和覆盖监控这两个最关键的治理环节。”

### 先看 demo 代码时
顺序：

1. `osag_demo/run_dispatch_demo.py`
2. `osag_demo/dispatch_demo_core.py`
3. `choose_observations`
4. `osag_demo/dispatch_demo_assets.py`

口头说法：

“这里是 demo 的入口；真正决定调度行为的是 choose_observations；最后这部分负责生成 dashboard 和图表。”

## 6. 如果老师问“OSAG 到底在代码里体现在哪里”
最稳的回答是：

1. 合同构造：`build_contract_table_from_meta`
2. 目标份额：同一个函数里计算 `target_weight`
3. 覆盖偏差：`compute_coverage_errors`
4. 调度分数：`choose_observations`

你可以直接说：

“OSAG 在代码里不是一个孤立函数名，而是一条完整治理链：合同构造、目标份额、调度/采样控制、覆盖监控。”

## 7. 如果运行慢了怎么办
不要硬等。
直接切换到保存好的输出，并说：

“我先展示已经保存的 dashboard 和 timeline 输出，再回到入口脚本解释它们是如何生成的。”

这比现场卡住更稳。

## 8. 如果路径或环境失败怎么办
安全处理顺序：

1. 先打开已保存的 HTML 和 PNG
2. 再展示入口脚本路径
3. 再说明正常情况下的运行命令

不要把现场时间浪费在修环境上。

## 9. 可以直接说出口的几句话

### 打开 demo 前
“我先展示 thesis 里 dispatch demo 的运行入口和保存输出，再解释关键调度逻辑。”

### 打开 dashboard 后
“这里的重点不是数据长什么样，而是有限预算下哪些合同被保障、哪些合同被漏掉。”

### 打开 `choose_observations` 后
“这段代码把 urgency、deadline pressure、coverage gap、uncertainty 和 priority 合成为调度分数。”

### 打开 benchmark 入口后
“如果老师关心正式实验链路，这里是统一入口；核心治理逻辑在 reproduce_osag_real.py 里。”

## 10. 最后提醒
现场最容易失误的不是不会写代码，而是顺序乱掉。

你只要记住这条顺序就够了：

1. 先展示结果
2. 再展示入口
3. 再展示关键函数
4. 最后再补细节
