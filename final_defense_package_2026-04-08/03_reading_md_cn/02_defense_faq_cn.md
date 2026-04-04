# 答辩 FAQ（中文简明版）

这份 FAQ 只保留答辩最常见、最容易追问的问题，回答尽量短、稳、可直接说出口。

## 1. 你的论文到底在做什么？
短答：
这篇论文研究如何给遥感训练加入一层显式治理机制，让训练资源按合同级别的服务目标分配，而不是只看平均准确率。

稍长答：
传统训练主要优化整体损失或整体准确率，但现实任务往往更关心重点区域、稀有对象和高优先级服务对象是否真正被关注。我的 thesis 用 OSAG 把这种服务分配显式化，并在训练中持续监控是否和目标策略一致。

## 2. OSAG 一句话怎么解释？
短答：
OSAG 是一个面向合同的训练治理层。

稍长答：
它不是新 backbone，而是包在普通训练流程外面的一层 policy-aware 机制。它通过合同构造、目标服务份额、采样控制和覆盖监控来约束训练过程。

## 3. 为什么 overall accuracy 不够？
短答：
因为平均准确率高，不代表关键合同真的被服务到了。

稍长答：
如果数据分布不均，训练自然会偏向样本多、容易学的部分。这样模型的总体指标可能不错，但高优先级合同或稀有合同仍然可能被长期忽略。

## 4. contract 是什么？
短答：
contract 是治理真正关心的服务单位。

稍长答：
它不是简单的类别标签，而是根据数据集、空间位置、语义分组、稀有标记等信息构成的服务单元。训练治理就是围绕这些合同展开的。

## 5. target service share 是什么？
短答：
是每个合同理论上应获得的训练份额。

稍长答：
论文里采用的是“priority × contract size”后再归一化的规则，这样既考虑人为设定的优先级，也考虑合同本身的数据规模。

## 6. PrioCovErr 是什么？
短答：
是合同层面的策略偏差指标。

稍长答：
它衡量目标服务份额和实际训练覆盖之间的差距。值越小，说明治理越对齐。

## 7. 论文最主要的证据是什么？
短答：
主证据是 fresh rerun benchmark，不是 demo。

稍长答：
真实数据 benchmark 才是 thesis 的核心证据链。dispatch demo 的主要作用是展示系统行为和治理机制，不替代真实实验。

## 8. 主要实验结论怎么讲？
短答：
OSAG 家族能把 PrioCovErr 压到接近 0，同时保持有竞争力的整体准确率，并改善高优先级表现。

稍长答：
这个结论在 HSI 和 EuroSAT MSI 两条主线上都成立。论文并不声称 OSAG 在所有指标上都绝对第一，而是强调它能构造出更符合治理目标的 operating point。

## 9. 为什么 EuroSAT fine 是 6，不是 12？
短答：
因为当前锁定版 thesis 和 fresh rerun 管线中的 realized contracts 就是 6。

稍长答：
这一点已经在论文和审计中统一了，答辩时必须始终说 6。

## 10. demo 的作用是什么？
短答：
demo 用来展示治理行为，不是替代 benchmark。

稍长答：
表格能告诉我们结果如何，但不容易直观看到预算、时限、覆盖偏差和 missed service 的动态变化。dispatch demo 正好补上这部分。

## 11. 为什么只在 dashboard 里比较 Random / Contract-Priority / OSAG？
短答：
因为这三者最能代表“无治理、激进启发式、治理策略”三类行为。

稍长答：
如果主 dashboard 同时放太多策略，演示会变得嘈杂，不利于答辩讲解。完整 benchmark 里已经包含更多基线。

## 12. 这是不是只是 reweighted sampling？
短答：
当前主线确实以 sampling 为主，但 thesis 的重点不只是加权，而是完整治理回路。

稍长答：
论文关心的不只是“怎么采样”，还包括如何定义合同、如何定义目标份额、如何监控覆盖偏差，以及如何把这些量组织成一个可解释的治理框架。

## 13. graph 到底在哪里？
短答：
现在更多是 modeling view，不是完整显式 graph optimizer。

稍长答：
论文把 contract space 看成有结构关系的空间，这就是 graph 视角。但当前实现主要还是 contract-aware sampling 和 monitoring，完整显式图算法属于未来工作。

## 14. HSI split 有 spatial leakage 吗？
短答：
有这个风险。

稍长答：
当前 HSI split 是 pixel-stratified，不是 spatial-blocked，所以相邻像素可能跨 split。最稳的说法是：HSI 结果应理解为固定协议下的 comparative governance result。

## 15. runtime 应该怎么解释？
短答：
讲 comparable overhead，不讲 OSAG 更快。

稍长答：
runtime 表说明 OSAG 的额外代价处在可接受范围内，但 thesis 不应该被讲成“OSAG 本质上比 Random 更快”。

## 16. 为什么主 benchmark 用 lightweight MLP？
短答：
因为 thesis 的主线是治理层，不是 backbone 比赛。

稍长答：
用轻量 MLP 更容易隔离治理层本身的效果，避免老师觉得结果主要来自 backbone 复杂度差异。

## 17. ResMLP extension 的作用是什么？
短答：
是一个有限范围的鲁棒性补充。

稍长答：
它不是第二套主 benchmark，而是用来检查治理结论在稍强 backbone 下是否还能成立。结论是可以成立，但 thesis 仍然不是 backbone SOTA 研究。

## 18. 可复现性到底有多强？
短答：
在脚本和产物层面较强，但需要明确 non-git boundary。

稍长答：
Appendix A 已经明确 formal inputs、contract rules、fresh outputs 和 provenance boundary。也就是说，这篇 thesis 的复现链条是清楚的，但不是“完整 git ledger 闭环”。

## 19. 哪些话一定不能乱说？

1. 不要说 graph 已经是完整显式图算法。
2. 不要说 HSI split 完全没有 leakage。
3. 不要说 demo 是主证据。
4. 不要说 Table 5.2 是相对百分比变化。
5. 不要说 EuroSAT fine 是 12。
6. 不要说 thesis 是 backbone state of the art 研究。
