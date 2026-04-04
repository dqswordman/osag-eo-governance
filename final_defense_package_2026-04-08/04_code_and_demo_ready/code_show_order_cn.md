# 代码展示顺序（中文）

如果老师现场说“打开代码给我看”，最稳的顺序是：

1. `scripts/run_all_real_experiments.py`
   先说明这是正式真实实验的统一入口。

2. `scripts/reproduce_osag_real.py`
   再说明这是主 benchmark 的核心实现文件。

3. `build_contract_table_from_meta`
   解释合同如何从数据表里构造出来，以及 target weight 如何得到。

4. `compute_coverage_errors`
   解释 PrioCovErr 等治理指标是怎么从合同计数里算出来的。

5. `osag_demo/run_dispatch_demo.py`
   再切到 demo 入口，说明现场展示的是哪条链路。

6. `osag_demo/dispatch_demo_core.py`
   说明这里是真正的调度逻辑。

7. `choose_observations`
   最后讲 OSAG 如何把 urgency、deadline pressure、coverage gap、uncertainty 和 priority 合成调度分数。

## 一句话策略
先入口，再核心逻辑，再指标，再 demo。
不要一上来就在大文件里上下乱翻。
