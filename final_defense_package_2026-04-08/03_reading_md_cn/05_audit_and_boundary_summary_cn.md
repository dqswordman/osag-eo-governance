# 审计与边界总结（中文）

## 什么是 freshly rerun 的
当前 thesis 的主证据链来自真实脚本链路重新生成的结果，主要包括 HSI 主 benchmark、EuroSAT MSI 主 benchmark、runtime 汇总、合同设计 ablation 和 scoped ResMLP extension。

## 什么不是主证据
- dispatch demo 不是主 benchmark 证据
- reliability score 不是唯一评价标准
- 历史 conference-version 结果不是当前 thesis 的 fully rerun 主证据

## reproducibility 在这里是什么意思
当前 thesis 的 reproducibility 主要是：
- formal input data 固定
- contract construction rules 固定
- fresh output locations 固定
- scripts / manifests / logs / configs / stage reports 可追踪

## graph 到底是什么意思
应该说：graph 是 structured contract space 的 modeling view。
不应该说：当前实现已经是 full explicit graph optimizer。

## HSI split 的边界
当前 HSI split 是 pixel-stratified，不是 spatial-blocked。
所以最好把 HSI 结果理解成 comparative governance evidence，而不是 leakage-free deployment estimate。

## runtime 表能说明什么
能说明：
- OSAG 和 Random 在实际训练开销上属于同一量级
- fairness penalty 会增加一点成本，但仍在可接受范围

不能说明：
- OSAG 天生更快
- runtime 已经足以证明工程最优实现

## backbone scope 的边界
主 benchmark 用 lightweight MLP，是为了隔离治理效应。ResMLP extension 的作用是做 scoped robustness check，不是 backbone SOTA 对比。
