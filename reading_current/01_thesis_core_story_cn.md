# 论文主线速读

## 1. 先用一句话概括
这篇论文研究的是：如何把遥感训练从“只优化平均准确率”的过程，改造成一个“能够显式控制服务分配”的治理过程。

## 2. 为什么这个问题重要
传统训练通常默认所有样本只是在一起优化损失。
这样做在数学上很干净，但现实任务里会有一个隐藏问题：

- 哪些区域被反复关注？
- 哪些类别被长期忽略？
- 哪些高优先级服务对象没有在训练中得到足够曝光？

也就是说，模型可能平均上表现不错，但关键合同、关键区域或关键语义组并没有真正被“服务到”。

## 3. 论文的核心想法是什么
论文给训练过程加了一层轻量治理机制，这层机制就是 OSAG。

它不是新 backbone，也不是要替代分类器本身。
它做的是三件事：

1. 先把数据组织成有意义的合同单元 `contract`
2. 再给每个合同定义目标服务份额 `target service share`
3. 再在训练过程中持续检查“实际服务”是否偏离目标

如果偏离太大，就通过 OSAG 的采样与控制逻辑把训练注意力往目标方向拉回去。

## 4. 论文里最重要的几个词

### contract
不是随便一堆样本，而是治理真正关心的服务单位。

### target service share
这个合同理论上应该得到多少训练资源。

### empirical coverage
这个合同实际上拿到了多少训练资源。

### PrioCovErr
目标份额和实际份额之间的偏差。这个指标越小，说明治理越对齐。

### alpha
控制采样时有多强地朝治理目标靠拢。

### lambda_C
控制 fairness loss 的强度，用来额外照顾高优先级且更难学的合同。

## 5. 论文的证据链怎么理解
这篇 thesis 不是只靠一个 demo，也不是只靠一张表。
它的证据链有三层：

1. 真实 benchmark fresh rerun
2. dispatch demo
3. Appendix A 的复现与边界说明

### 第一层：真实 benchmark
这是主证据。
主实验来自：

- corrected Indian Pines + corrected Salinas
- EuroSAT MSI

主结果表是 fresh five-seed rerun。
结论是：OSAG 家族可以把 PrioCovErr 压到接近 0，同时保持有竞争力的 Acc_all，并提升高优先级表现。

### 第二层：dispatch demo
这不是主证据，而是行为展示。
它回答的是：

- 在有限预算下，系统如何调度观察和标注资源？
- 哪些高优先级合同会被保障？
- 哪些策略会出现长期覆盖偏差？

所以 demo 的价值在于“把治理行为讲清楚”，不是替代 benchmark。

### 第三层：Appendix A
这一部分的作用是把可复现边界写清楚。
它明确了：

- formal input data
- contract construction details
- fresh output locations
- non-git provenance boundary

也就是说，论文不夸大“可复现性”，而是把已经做到的和还没做到的边界都讲明白。

## 6. 论文最核心的实验结论怎么说
最稳的讲法是：

1. OSAG 的主要价值不是追求最高平均准确率，而是显著降低合同级别的策略偏差。
2. 这种治理效果在 HSI 和 MSI 两条 benchmark 主线上都成立。
3. 当看高优先级表现和政策对齐时，OSAG 家族明显优于只看随机采样或简单平衡策略。

## 7. 哪些地方一定不能讲错

1. EuroSAT fine contract 数量是 6，不是 12。
2. Table 5.2 讲的是 absolute percentage-point differences，不是 relative percentage changes。
3. demo 里的 `Q_high` 不是 `K`。
4. HSI split 是 pixel-stratified，不是 spatial-blocked。
5. graph 在当前 thesis 里更多是 modeling view，不是完整显式 graph optimizer。
6. thesis 主线是治理层，不是 backbone SOTA。

## 8. 最后怎么收束这篇论文
如果老师问“你的 thesis 最终想表达什么”，最稳的回答是：

这篇论文的核心贡献，不是提出一个更强的遥感 backbone，而是把 EO 训练里的服务分配问题显式化、可控化、可审计化。OSAG 作为轻量治理层，让训练不再只是追求平均准确率，而是能够按合同目标去分配训练注意力，并用真实 benchmark、dispatch demo 和 Appendix A 共同支撑这个结论。
