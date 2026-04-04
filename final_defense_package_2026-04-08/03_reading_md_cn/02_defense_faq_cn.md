# 中文答辩 FAQ（简明版）

## 怎么用
每个问题先记短答，再看稍长一点的答法。答辩时先短答，老师追问再展开。

## 最可能被问的 10 个问题
1. **这篇论文一句话讲什么？**
   - 短答：这篇论文研究的是如何把 EO 训练变成一个显式可控的服务治理问题，而不是只看平均准确率。
   - 稍长答：OSAG 用 contract、target share 和 coverage monitor 把训练服务分配显式化，并在真实 benchmark 上验证它能显著降低 policy misalignment。
2. **OSAG 是什么？**
   - 短答：OSAG 是一个 contract-aware 的轻量治理层。
   - 稍长答：它不是 backbone，而是包在普通训练外面的 policy-aware layer。
3. **为什么 accuracy 不够？**
   - 短答：因为 average accuracy 高，不代表关键 contract 被正确服务。
   - 稍长答：训练如果天然偏向大类或密集区域，就可能把高优先级 contract 挤掉，所以还需要看 policy alignment。
4. **contract 是什么？**
   - 短答：contract 是训练治理真正关心的服务单元。
   - 稍长答：它可以由数据集身份、空间格子、语义组或稀有标记组成。
5. **主证据是什么？**
   - 短答：是真实数据上的 fresh rerun benchmark，不是 demo。
   - 稍长答：HSI 和 EuroSAT MSI 的 fresh rerun 是主证据，dispatch demo 主要负责解释系统行为。
6. **最核心的实验结论是什么？**
   - 短答：OSAG family 能把 PrioCovErr 压到接近 0，同时保持有竞争力的准确率。
   - 稍长答：它最强的地方不是把所有 accuracy 都刷到最高，而是显著改善 policy alignment。
7. **为什么 EuroSAT fine 是 6？**
   - 短答：因为当前锁定版 thesis 和 rerun pipeline 里，EuroSAT fine contract 的 realized count 就是 6。
   - 稍长答：答辩时一定统一说 6，不要再说 12。
8. **为什么还要做 demo？**
   - 短答：因为 benchmark 表格不容易显示动态调度行为。
   - 稍长答：demo 补充了预算、deadline、missed service 和长期稳定性这些 benchmark 很难直观看到的内容。
9. **这是不是新 backbone？**
   - 短答：不是。
   - 稍长答：OSAG 的定位始终是治理层，不是 backbone 创新。
10. **这篇 thesis 可复现到什么程度？**
    - 短答：脚本和产物层面很强，但 git provenance 不是完整闭环。
    - 稍长答：Appendix A 已经把 formal inputs、contract construction、fresh outputs 和 non-git boundary 说明清楚。

## 15 条避坑提醒
1. 不要说 graph 已经完全显式实现。
2. 不要说 HSI split 没有 leakage。
3. 不要说 OSAG 在所有指标上都最好。
4. 不要说 demo 替代了 benchmark。
5. 不要把 Table 5.2 说成 relative changes。
6. 不要把 EuroSAT fine 说成 12。
7. 不要把 OSAG 说成新 backbone。
8. 不要把 runtime 说成速度优势。
9. 不要把 Q_high 和 K 混在一起。
10. 不要回避 reliability 的 hand-set 权重。
11. 不要把 5-seed 主结果和 3-seed 扩展结果混成一类。
12. 不要把高 Acc_high 的 heuristic baseline 直接说成治理更好。
13. 不要忘了 Appendix A。
14. 不要只讲 demo，不讲 benchmark。
15. 不要把 thesis 讲成 backbone SOTA 工作。
