# 简明答辩 FAQ（中文）

## 1. 怎么使用这份 FAQ
先背短答案。老师继续追问时，再补长一点的答案。不要把局限性藏起来，明确边界反而更稳。

## 2. 最可能被问到的 10 个问题
1. **你的论文到底在做什么？** 短：让遥感训练从“只看准确率”变成“也要看服务是否分配正确”。 长：OSAG 把训练服务分配变成可定义、可控制、可检查的治理问题。
2. **OSAG 一句话怎么解释？** 短：OSAG 是一个面向 contract 的训练治理层。 长：它不是新 backbone，而是包在普通训练流程外面的 policy-aware layer。
3. **为什么 overall accuracy 不够？** 短：平均准确率高，不代表关键合同真的被服务到了。 长：大类和密集区域天然更容易主导训练，所以还要看 policy alignment。
4. **contract 是什么？** 短：训练策略真正关心的服务单元。 长：它可以包含数据集身份、空间格网、语义组和稀有标记。
5. **论文最主要的证据是什么？** 短：是 fresh rerun benchmark，不是 demo。 长：dispatch demo 主要负责展示系统行为和解释性。
6. **最核心的实验结论是什么？** 短：OSAG 能把 PrioCovErr 压到接近 0，同时保持有竞争力的准确率。 长：在两个 benchmark 上都是这样。
7. **为什么 EuroSAT fine 是 6，不是 12？** 短：因为最终锁定版 rerun 管线里 realized contracts 就是 6。 长：答辩时必须统一说 6。
8. **既然有 benchmark，为什么还要做 demo？** 短：因为表格不直观展示预算、时限和漏服务过程。 长：demo 是补充，不是替代。
9. **这是不是一个新 backbone？** 短：不是。 长：论文主线一直是治理层，不是 backbone 竞争。
10. **这篇论文到底有多可复现？** 短：在脚本和产物层面较强，但 git provenance 不是完整闭环。 长：Appendix A 已把 formal inputs、contract rules、fresh outputs 和边界写清楚。

## 3. 概念问题
- **论文想解决什么问题？** 短：解决“训练时到底在服务谁”这个被隐藏的问题。 长：普通训练只告诉我们模型好不好，却不告诉我们关键合同有没有被按政策要求服务到。
- **target service share 是什么？** 短：每个 contract 理论上应该拿到多少训练服务份额。 长：论文里按 priority 乘 contract size 来分配。
- **empirical coverage 是什么？** 短：每个 contract 实际拿到了多少训练曝光。 长：它用来检查真实训练是否按目标在服务。
- **PrioCovErr 是什么？** 短：合同层面的政策偏差指标。 长：它衡量 target shares 和 observed coverage 之间的 L1 gap。
- **这篇论文里的 governance 是什么意思？** 短：控制训练服务怎么分配。 长：这里是训练过程里的可控、可审计、可度量的服务分配机制。
- **为什么 EO 特别适合做这个问题？** 短：因为 EO 常常存在稀有但重要的区域或语义组。 长：只看平均准确率很容易掩盖服务失衡。

## 4. 方法问题
- **OSAG 到底是什么？** 短：contract-aware 的 sampling 和 monitoring 框架。 长：它把 contract builder、policy targets、sampler 和 coverage monitor 串起来。
- **为什么叫 graph？** 短：因为论文把 contract space 当成有结构关系的空间来看。 长：当前实现里，graph 更多是 modeling view，不是完整显式 optimizer。
- **OSAG 更像 sampling 还是 optimization？** 短：当前主线更像 sampling。 长：fairloss 版本带一点优化补充，但主 benchmark 还是以 sampling 为主。
- **alpha 是做什么的？** 短：控制 sampler 跟随治理策略的强度。 长：alpha 越大，越强地往目标服务策略靠。
- **lambda_C 是做什么的？** 短：控制 fairness loss 的权重。 长：高优先级合同在 loss space 里更难学时，它会增加补偿压力。
- **为什么 Uniform-Contract 有时看起来也不错，但还是不够？** 短：因为平均对待所有合同不等于按政策正确服务。 长：如果合同优先级本来就不同，它就不是正确的治理目标。

## 5. 实验问题
- **为什么选 Indian Pines + Salinas？** 短：它们适合构造 joint HSI governance benchmark。 长：能更明显展示稀有合同、空间结构和训练服务不均衡。
- **为什么选 EuroSAT MSI？** 短：它提供第二种模态，也支持 contract-design ablation。 长：这样可以验证治理效应不只在 HSI 上成立。
- **为什么主 benchmark 用 lightweight MLP？** 短：因为这样更容易看清 governance effect。 长：避免老师觉得结果主要来自 backbone 差异。
- **为什么主表是 5 seeds，而 ablation 是 3 seeds？** 短：主表是主证据链，需要更稳。 长：ablation 是范围更窄的扩展项。
- **主结果表到底在表达什么？** 短：它表达 utility 和 governance 之间的关系。 长：Acc_all 和 Acc_high 看预测效果，PrioCovErr 看政策对齐程度。
- **为什么 Random 有时 Acc_all 最高？** 短：因为它天然更贴近 average-accuracy 目标。 长：这不代表它在政策服务上做得对。
- **HSI split 有泄漏吗？** 短：有这个风险。 长：当前 split 是 pixel-stratified，不是 spatial-blocked。
- **runtime 应该怎么讲？** 短：讲 comparable overhead，不讲 OSAG 更快。 长：它只能说明 OSAG 处在和 Random 相近的实用范围内。

## 6. Demo 问题
- **为什么 dashboard 里只放 Random、Contract-Priority 和 OSAG？** 短：因为这样最容易讲清三种代表性行为。 长：三者已经足够表达无治理、激进启发式和治理策略之间的差别。
- **Q_high 是什么？** 短：demo 里高优先级区域的最终质量指标。 长：它不是 reliability 公式里的 K。
- **missed service 是什么？** 短：没按时服务到的次数。 长：它反映 deadline 或 revisit pressure 下的失败事件。
- **reliability score 是什么？** 短：多个 demo 指标的汇总分数。 长：它方便比较，但不能替代原始指标。
- **reliability 的权重是不是手工设的？** 短：是。 长：所以 thesis 也补了 lightweight sensitivity audit。
- **如果权重变了，OSAG 还最好吗？** 短：在 thesis 设定附近，基本还是。 长：equal weights 和若干局部扰动下，OSAG 仍是第一。

## 7. 尖锐问题
- **这不就是 reweighted sampling 吗？** 短：它确实是轻量、以 sampling 为主，但不只是随便重加权。 长：真正的新意在于整套 governance loop。
- **graph 到底在哪里？** 短：主要在建模视角里。 长：当前 benchmark 实现不是完整显式 graph optimization。
- **contract 不就是人为造 bias 吗？** 短：是人为设计的 policy unit，但这正是论文研究对象。 长：论文专门分析了 contract design 如何影响 governance cost。
- **手工权重的 demo 凭什么可信？** 短：因为 demo 不是主证据。 长：主证据仍然是 benchmark，demo 只是补充解释。
- **为什么不做 transformer？** 短：因为论文主线不是 backbone 比赛。 长：ResMLP extension 已经足够说明治理结论在稍强模型下还能成立。
- **没有 git ledger，还能说可复现吗？** 短：可以说较强可复现，但要把边界讲清楚。 长：论文在脚本、manifest、config、logs、artifacts 层面是清楚的。

## 8. 15 条避坑提醒
1. 不要说 graph 已经完全显式实现。
2. 不要说 HSI split 没有 leakage。
3. 不要说 OSAG 所有指标都赢。
4. 不要说 demo 代替了 benchmark。
5. 不要把 Table 5.2 说成 relative percentage。
6. 不要把 EuroSAT fine 说成 12。
7. 不要把 OSAG 说成新 backbone。
8. 不要把 runtime 讲成 OSAG 更快。
9. 不要回避 reliability weights 是 hand-set。
10. 不要把 Q_high 和 K 混在一起。
11. 不要把 main five-seed 和 three-seed extension 混讲。
12. 不要因为 Acc_high 高就说 heuristic baseline 是 governance-correct。
13. 不要忘记 Appendix A。
14. 不要把答辩讲成只有 demo 的故事。
15. 不要把创新夸大成 backbone SOTA。

## 9. 20 条超短答法
1. 这篇论文研究的是 governance-aware EO training。
2. OSAG 是治理层，不是 backbone。
3. contract 是策略关心的服务单元。
4. target share 是应得服务份额。
5. empirical coverage 是实际服务份额。
6. PrioCovErr 是两者之间的偏差。
7. PrioCovErr 越小，policy alignment 越好。
8. 主证据是 fresh rerun benchmark。
9. demo 是 operational complement。
10. HSI 用 corrected Indian Pines 和 corrected Salinas。
11. EuroSAT 用 canonical 13-band MSI。
12. HSI 一共 44 个 realized contracts。
13. EuroSAT coarse 是 4。
14. EuroSAT fine 是 6。
15. 主表是 five seeds。
16. ablation 是 fresh three-seed rerun。
17. runtime 只能讲 comparable overhead。
18. graph 目前更多是 modeling view。
19. HSI split 是 pixel-stratified。
20. Appendix A 是答辩可信度的关键支撑。
