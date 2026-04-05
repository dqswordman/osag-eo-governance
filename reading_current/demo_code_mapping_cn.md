# Demo V2 与代码映射说明

## 1. 这套 Demo V2 和真实项目代码是什么关系
它不是独立乱写的前端玩具，而是把当前项目里已经存在的治理逻辑重新组织成一个更适合答辩展示的工程层。

## 2. 最重要的真实文件
### benchmark / thesis logic
- `scripts/run_all_real_experiments.py`
- `scripts/reproduce_osag_real.py`

### dispatch logic
- `osag_demo/run_dispatch_demo.py`
- `osag_demo/dispatch_demo_core.py`

### Demo V2 builder
- `scripts/build_engineered_demo_package_v2.py`

## 3. 如果老师要看代码，最稳的顺序
1. 先开 `scripts/build_engineered_demo_package_v2.py`
2. 再开 `osag_demo/dispatch_demo_core.py`
3. 再回到 `scripts/reproduce_osag_real.py`

## 4. 和 thesis benchmark evidence 的关系
- thesis 的正式证据仍然来自 locked benchmark rerun
- Demo V2 只是把同样的治理思想做成更容易解释的工程化演示
- 它帮助理解 thesis，不替代 thesis
