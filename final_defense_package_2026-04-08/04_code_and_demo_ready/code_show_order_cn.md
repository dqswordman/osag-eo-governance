# Code Show Order (中文)

1. 先开 `scripts/run_all_real_experiments.py`，说明正式实验总入口。
2. 再开 `scripts/reproduce_osag_real.py`，说明 contract 和训练治理逻辑。
3. 再开 `osag_demo/run_dispatch_demo.py`，说明 demo 产物生成入口。
4. 最后开 `osag_demo/dispatch_demo_core.py` 的 `choose_observations`，解释 OSAG 调度分数。
