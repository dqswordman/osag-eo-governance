# 简明论文理解指南（中文）

## 1. 一句话总结
这篇论文研究的是：如何给遥感训练加上一层轻量的治理机制，让训练过程能按合同级别的服务策略来分配注意力。

## 2. 整体概览
论文的出发点很直接。传统遥感训练通常只关心平均预测效果，比如 overall accuracy。但现实任务里，我们更关心重点区域、稀有对象、重要语义组是否真的在训练中得到了应有的服务。也就是说，训练不是只有“学得准不准”的问题，还有“训练资源到底分给了谁”的问题。论文通过 contract、target service share、empirical coverage 和 PrioCovErr，把这个治理问题显式化，再通过 OSAG 把它放进训练流程里。

## 3. 四个研究问题
- RQ1：怎么把 EO 训练改写成 service-allocation 问题？
- RQ2：能不能只用一个轻量治理层来控制训练曝光？
- RQ3：治理质量和预测效果之间是什么关系？
- RQ4：能不能把这件事讲清楚，并做成可运行的答辩 artifact？

## 4. 核心概念的白话解释
- contract：策略真正关心的服务单元。
- target service share：某个合同理论上应得的训练份额。
- empirical coverage：它实际拿到的训练份额。
- PrioCovErr：目标份额和实际份额之间的偏差。
- alpha：治理采样强度旋钮。
- lambda_C：fairness loss 的强度旋钮。
- OSAG：核心治理层。
- OSAG-FairLoss：OSAG 加 loss-space 公平性压力。
- dispatch demo：展示动态治理行为的演示系统。
- Q_high：demo 中高优先级区域的最终质量指标，不等于 K。

## 5. 按章节理解论文
- Chapter 1：解释为什么 accuracy 不够。
- Chapter 2：定义 benchmark 和 contract 结构。
- Chapter 3：给出 target share、coverage、PrioCovErr、alpha、lambda_C。
- Chapter 4：用 dispatch demo 解释系统行为。
- Chapter 5：给出 fresh rerun benchmark、trade-off、ablation、runtime、ResMLP extension。
- Chapter 6：总结全文。
- Appendix A：固定 formal inputs、contract rules、fresh outputs 和 provenance boundary。

## 6. 数学直觉，尽量不堆公式
普通 ERM 做的是“在所有样本上把平均 loss 压低”。这在数学上很干净，但它并不知道哪些合同更重要。论文做的事，是先规定每个合同应该获得多少训练服务，再去观察真实训练是不是按这个目标执行。empirical coverage 就是观察值，PrioCovErr 就是误差。alpha 是治理强度旋钮，lambda_C 是 loss-space 的补充压力。graph 要谨慎讲：当前 thesis 里，它主要是一个结构化建模视角，不是完整显式的 graph algorithm。

## 7. 实验设计怎么简单解释
HSI 用 corrected Indian Pines 和 corrected Salinas，是因为这两个数据集合起来很适合展示稀有合同、空间结构和服务失衡。EuroSAT MSI 提供第二种模态，也支持 coarse vs fine contract design 的比较。主 benchmark 故意用 lightweight MLP，这样更容易把治理层效应隔离出来。主表是 five-seed fresh rerun，ablation 是 fresh three-seed rerun，ResMLP 是范围明确的 robustness extension。

## 8. 图表怎么读
- Figure 1.1：整篇论文的总结构图，最先背。
- Table 2.1：benchmark 和 contract summary，重点记住 EuroSAT fine = 6。
- Table 4.1：demo 总结表。
- Figure 4.2：看时间推进下的治理行为。
- Table 5.1：主 fresh rerun 结果表。
- Table 5.2：absolute percentage-point differences，不是 relative changes。
- Table 5.3：contract-design ablation。
- Table 5.4：runtime，讲 comparable overhead。
- Table 5.5：ResMLP 扩展。

## 9. Dispatch demo 怎么讲得简单
demo 是一个 12x12 的应急网格，持续 10 个时间步，一共有 6 个合同。每一步观测预算是 14，标注预算是 6。Random 是无约束基线，Contract-Priority 是激进启发式，OSAG 是治理策略。dashboard 看五个量：compliance、coverage error、missed service、Q_high 和 reliability。reliability 只是 summary，不是唯一指标。这个 demo 的价值，是把 benchmark 里看不见的动态服务行为展示出来。

## 10. 哪些是创新，哪些是继承
这篇 thesis 和 conference paper 有延续关系，但 thesis 版本做了几件强化：叙事更完整，主证据改成 fresh rerun，demo 升级成 dispatch 形式，Appendix A 也把可复现边界讲清楚了。创新重点在 governance-aware EO training 的概念和方法，不在 backbone 发明。

## 11. 最容易被质疑的点
不要把 Q_high 和 K 混在一起。不要把 demo 说成主证据。不要把 Table 5.2 说成相对百分比变化。不要把 EuroSAT fine 说成 12。不要把 graph 讲得过于强。不要把 runtime 讲成速度优势。不要回避 HSI split 的限制。

## 12. 局限性和未来工作
论文的局限性是明确的：HSI split 不是 spatial-blocked；graph 现在更多是建模视角；backbone 范围有限；contract 是人工设计的 policy unit；可复现性在脚本和产物层面较强，但没有完整 git ledger。未来工作可以沿着更显式的 graph algorithm、更严格的 spatial split、更广的 backbone study 和更自适应的 contract design 去扩展。

## 13. 答辩准备总结
最稳的答辩主线是：这篇论文讲的是 governance-aware EO training；OSAG 是一个轻量治理层；主证据来自 fresh rerun benchmark；dispatch demo 是 operational complement；Appendix A 是可信度支撑。

## 14. 快速复习路线
如果还剩 30 分钟，就先看 Figure 1.1、Table 5.1、Table 5.2、Table 5.4、Table 5.5、Table 4.1 和局限性。  
如果只剩 10 分钟，就死记五句话：EuroSAT fine 是 6；Table 5.2 是 absolute percentage-point differences；HSI split 是 pixel-stratified；graph 主要是 modeling view；demo 是补充证据，不是主证据。
