# 论文核心故事（中文速读版）

这篇 thesis 真正讲的不是谁的 backbone 更强，也不是单纯追求更高的 average accuracy。它讲的是：在 Earth Observation 训练里，训练资源本身就是一种服务分配。既然训练资源会分给不同区域、不同语义组、不同优先级对象，那么这个分配过程就应该被显式建模、显式控制、显式审计。

传统训练默认把样本看成一个大池子，优化的是平均损失。这样做在数学上很自然，但现实任务经常不是平均主义的。某些区域、某些稀有但关键的对象、某些高优先级服务目标，本来就比普通区域更重要。如果训练过程天然偏向样本量大的部分，那模型即使 overall accuracy 很高，也可能在真正重要的服务目标上分配失衡。

thesis 的做法是先定义 contract。contract 就是训练治理真正关心的服务单元。然后为每个 contract 定义 target service share，也就是“理论上应该分到多少训练关注”。接着统计 empirical coverage，也就是“训练过程中实际分到了多少”。两者之间的偏差用 PrioCovErr 来衡量。OSAG 的作用，就是把这个治理目标注入训练过程。

很重要的一点是：OSAG 不是一个新 backbone。它是一个轻量治理层。它包裹在普通训练流程外面，主要通过 contract-aware sampling、coverage monitoring，以及在扩展版本里加入 fairness loss 来改变训练关注分配。这样做的好处是，thesis 想证明的是治理逻辑本身，而不是靠更复杂的 backbone 把所有东西都盖过去。

thesis 的主证据是 fresh rerun benchmark，而不是 demo。真实 benchmark 包括 corrected Indian Pines + corrected Salinas 的联合 HSI benchmark，以及 canonical 13-band EuroSAT MSI benchmark。两条 benchmark 共同回答一个问题：当训练被看成一个 contract-governed service allocation 问题后，是否真的能在不同模态下把 policy misalignment 压下去，同时保持有竞争力的预测性能。

最核心的结果不是“OSAG 在所有指标上都最好”，而是：OSAG family 可以把 PrioCovErr 从二十多个点压到接近 0，同时 overall accuracy 只付出很小代价，而且 high-priority performance 仍然保持竞争力。这意味着 thesis 证明的不是“更高 accuracy”，而是“更好的治理对齐”。

benchmark 是科学证据，但 benchmark 表格不容易直观看出预算、deadline、missed service 和长期稳定性是怎么变化的。所以 thesis 又加了 dispatch demo。这个 demo 的作用不是替代真实实验，而是让老师能看到治理层在一个时间推进场景里是怎么工作的。

最后一定要记住 thesis 的边界：HSI split 是 pixel-stratified，不是 spatial-blocked；graph 在当前实现里更多是 modeling view，不是 full explicit graph optimizer；主 benchmark 用 lightweight MLP 是为了隔离治理效应；ResMLP 只是 scoped robustness extension；reproducibility 很强，但主要是脚本和产物层面的，不是完整 git provenance ledger。
