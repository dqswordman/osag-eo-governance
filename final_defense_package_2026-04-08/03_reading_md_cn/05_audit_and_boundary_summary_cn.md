# 审计与边界总结（中文）

这份文档的作用是把“这篇 thesis 现在到底完成到了什么程度”讲清楚。
它不是自我否定，而是帮助你在答辩时把边界说得稳、说得准。

## 1. 什么是 fresh rerun
这里的 fresh rerun 指的是：

- 从正式脚本入口出发
- 使用锁定的真实输入数据
- 在本地重新生成 logs、CSV、figures、runtime tables
- 最终把这些 fresh outputs 写回 thesis

所以 fresh rerun 不是“沿用以前的历史 CSV”，也不是“凭记忆重写表格”。

## 2. 当前 thesis 的主证据是什么
主证据是：

1. HSI 主 benchmark fresh five-seed rerun
2. EuroSAT MSI 主 benchmark fresh five-seed rerun
3. EuroSAT contract-design ablation fresh three-seed rerun
4. EuroSAT ResMLP scoped extension

dispatch demo 是补充性证据，不是主证据。

## 3. 现在还存在哪些边界

### HSI split 边界
当前 HSI split 是 pixel-stratified，不是 spatial-blocked。
这意味着相邻像素可能跨 train/test。

最稳说法：
“HSI 结果应理解为固定协议下的 comparative governance result，而不是严格部署条件下的最终绝对性能估计。”

### graph 边界
graph 在当前 thesis 中主要是 modeling view。
它帮助我们把 contract space 看成一个有结构关系的空间。

但当前实现仍然主要是：
- contract-aware sampling
- fairness loss
- coverage monitoring

最稳说法：
“当前实现不是完整显式 graph optimizer。”

### backbone 边界
主 benchmark 用的是 lightweight MLP。
这是为了隔离治理层效果，而不是为了做 backbone 比赛。

ResMLP 只是 scoped extension。
最稳说法：
“thesis 证明的是治理层结论，而不是 backbone state of the art。”

### runtime 边界
runtime 表能支持的说法是：
- OSAG 开销在可接受范围内
- 和 Random 属于同一实际量级

不能支持的说法是：
- OSAG 本质更快

最稳说法：
“runtime 应解释为 comparable overhead，而不是速度优势。”

### demo 边界
dispatch demo 用来展示系统行为和治理机制。
它不是替代真实 benchmark。

最稳说法：
“demo 是 operational complement，不是 main evidence chain。”

### provenance 边界
Appendix A 已经明确 formal inputs、contract construction details 和 fresh output locations。
但本地 thesis workspace 本身不是完整 git ledger。

最稳说法：
“这篇 thesis 在脚本和产物层面可审计，但 provenance 边界是明确存在的。”

## 4. 什么是这篇 thesis 已经做得比较强的地方

1. 主 benchmark 是 fresh rerun，不是历史结果拼接。
2. 论文正文、表格、图和 Appendix A 现在是一致的。
3. EuroSAT fine contract 数量、Table 5.2 表述、demo 指标命名等关键不一致都已经清理过。
4. dispatch demo、代码讲解材料和答辩包已经建立起来。

## 5. 哪些话不能讲过头

1. 不要说 graph 已经完整显式化。
2. 不要说 HSI split 没有 leakage。
3. 不要说 demo 比真实 benchmark 更重要。
4. 不要说 runtime 证明 OSAG 更快。
5. 不要说 thesis 是 backbone SOTA 研究。
6. 不要把 artifact-level reproducibility 讲成完整 git-level reproducibility。

## 6. 最稳的边界总结
如果老师直接问“你这篇 thesis 的边界是什么”，最稳的回答是：

这篇 thesis 的主贡献是治理层，而不是 backbone。它的主证据来自 fresh rerun 的真实 benchmark，dispatch demo 负责补充系统行为解释。当前实现把 graph 更多作为建模视角来使用，HSI 评估协议也仍是 pixel-stratified，因此这些边界都需要明确承认。但在这些边界之内，OSAG 对合同级服务偏差的改善结论是清晰而稳定的。
