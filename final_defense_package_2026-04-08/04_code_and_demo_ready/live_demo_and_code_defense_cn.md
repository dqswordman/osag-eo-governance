# 现场演示与代码答辩说明（中文）

## 1. 防守型原则
现场演示不是重新做实验，也不是临场写代码。目标是让老师看到：
- 你知道系统从哪里启动
- 你知道关键逻辑在哪个文件
- 你知道输出该怎么看
- 即使运行慢或路径出问题，你也能稳住并切换到已有结果解释

## 2. 最安全的现场顺序
1. 先完成 PPT 主讲
2. 老师要求演示时，先说“我先展示 dispatch demo 的入口和输出，再看关键代码位置”
3. 先运行 demo 入口
4. 打开 dashboard 或现成输出
5. 再打开 `run_dispatch_demo.py`
6. 再跳到 `dispatch_demo_core.py` 的 `choose_observations`
7. 如果老师问 benchmark，再切到 `run_all_real_experiments.py` 和 `reproduce_osag_real.py`

## 3. 最常用命令
```powershell
python .\osag_demo\run_visual_demo.py
python .\osag_demo\launch_visual_demo.py
```

如果老师只想看 benchmark 入口，就展示：
```powershell
python .\scripts\run_all_real_experiments.py --help
```

现场不要真正重跑大实验。

## 4. 如果软件启动正常，先展示什么
推荐顺序：
1. dashboard 主界面
2. baseline 与 OSAG 的对照
3. timeline 图
4. contract gap 图
5. 再切回代码讲 `choose_observations`

## 5. 如果老师问 benchmark 代码看哪里
顺序：
1. `scripts/run_all_real_experiments.py`
2. `scripts/reproduce_osag_real.py`
3. `build_contract_table_from_meta`
4. `run_one`

## 6. 如果老师问 dispatch demo 代码看哪里
顺序：
1. `osag_demo/run_dispatch_demo.py`
2. `osag_demo/dispatch_demo_core.py`
3. `choose_observations`
4. `dispatch_demo_assets.py`

## 7. 如果运行慢，怎么办
不要死等。直接说：
- “我先展示已经保存好的 dashboard 和 timeline 输出，再回到入口脚本。”
- “这个系统的正式输出已经在 visual_outputs 里保存好了，我先从结果看，再回到代码解释。”

## 8. 如果路径失败，怎么办
安全做法：
1. 先展示已经存在的 HTML 和 PNG 输出
2. 再展示入口脚本的位置
3. 最后解释本来应该如何启动

## 9. 每一步可以怎么口头讲
- 打开 demo 前：`我先展示 thesis 里 dispatch demo 的实际运行入口和结果输出位置。`
- dashboard 打开后：`这里重点不是某一个格子的类别，而是服务覆盖、遗漏服务和长期稳定性。`
- 打开 `choose_observations`：`这段代码把 urgency、deadline pressure、coverage gap、uncertainty 和 priority 合成调度分数。`
- 打开 benchmark 入口：`如果老师关心正式实验链路，这里是总入口；再往下就是 contract 构造、训练循环和 coverage monitor。`
