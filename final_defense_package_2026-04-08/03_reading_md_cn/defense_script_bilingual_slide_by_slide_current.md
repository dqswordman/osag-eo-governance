# Defense Script: Bilingual Slide-by-Slide (Current Short Version)

This file is the main rehearsal script for the current short defense deck.

## Slide 1. Title

**English oral script**
Good morning. My thesis is titled 'Governance-Aware Earth Observation Learning: Contract-Governed Training with Observed Service Agreement Graphs.' This work studies how to make EO training policy-aware at the contract level instead of optimizing only average accuracy.

**中文理解与记忆**
开场先把题目和主线讲清楚：这篇论文不是在做新 backbone，而是在研究如何让遥感训练过程显式服从服务策略。

**Key terms**
governance-aware EO training; contract-level service

**Estimated time**
0.45 minutes

**Transition**
I will begin with a short roadmap of the talk.

## Slide 2. Talk Roadmap

**English oral script**
I will organize the talk into four parts: the problem and motivation, the OSAG framework and benchmark design, the results and robustness checks, and finally the demo, code orientation, and claim boundaries.

**中文理解与记忆**
这页就是路线图，让老师知道你不是散着讲，而是按问题、方法、证据、边界四段推进。

**Key terms**
roadmap; problem; framework; evidence; boundaries

**Estimated time**
0.35 minutes

**Transition**
With that structure in place, I can begin with the motivation.

## Slide 3. Background and Motivation

**English oral script**
Standard EO training is usually accuracy-driven. But real deployments also care about which regions, classes, or service groups are being served during training. That is why the thesis adds a governance layer on top of ordinary EO learning.

**中文理解与记忆**
核心意思是：模型平均上准，不代表重点对象真的被照顾到了，所以需要治理层。

**Key terms**
accuracy is not enough; who is served

**Estimated time**
1.10 minutes

**Transition**
That motivation leads directly to the research gap.

## Slide 4. Research Gap and Questions

**English oral script**
The central gap is that standard EO training does not represent service allocation explicitly. So the thesis asks how to formalize contracts, whether a lightweight governance layer can control exposure, what trade-offs appear on HSI and MSI benchmarks, and whether the idea can be communicated through a runnable defense artifact.

**中文理解与记忆**
这页要讲清楚：缺口不在于没有模型，而在于训练过程缺少显式的服务分配控制。

**Key terms**
research gap; explicit control; runnable artifact

**Estimated time**
1.00 minutes

**Transition**
Next, I will summarize the contributions that answer these questions.

## Slide 5. Figure 1.1 Method Overview

**English oral script**
Figure 1.1 is the thesis map. EO inputs become contracts, policy targets define intended service shares, the OSAG sampler injects that policy into training exposure, and the coverage monitor checks compliance. The key point is that OSAG wraps an ordinary classifier rather than replacing it.

**中文理解与记忆**
这页是全篇最重要的总览图。你要让老师记住：输入、合同、目标份额、采样器、覆盖监控，最后形成闭环。

**Key terms**
contracts; target shares; sampler; monitor; feedback loop

**Estimated time**
1.25 minutes

**Transition**
To make the framework concrete, I will define the core terms next.

## Slide 6. Core Concepts

**English oral script**
A contract is the service unit. The target service share says how much training attention it should receive. Empirical coverage says how much it actually receives. PrioCovErr measures the gap. Alpha controls how strongly sampling follows the policy, and lambda_C adds extra fairness pressure in loss space.

**中文理解与记忆**
这页是概念页。只要把 contract、target share、coverage、PrioCovErr、alpha、lambda_C 讲顺，后面实验就容易解释。

**Key terms**
contract; target share; empirical coverage; PrioCovErr; alpha; lambda_C

**Estimated time**
1.20 minutes

**Transition**
Now I can show how the benchmarks instantiate those concepts.

## Slide 7. Benchmark and Contract Design

**English oral script**
The locked thesis uses corrected Indian Pines plus corrected Salinas for HSI and canonical EuroSAT MSI for multispectral data. The HSI setting realizes 44 contracts. EuroSAT uses 4 coarse contracts or 6 fine contracts. Target share is proportional to priority times contract size, so the policy mixes human priority with available evidence.

**中文理解与记忆**
这一页要把数据集、合同构造和 44/4/6 这些关键数字讲准，尤其是 EuroSAT fine 一定是 6。

**Key terms**
Indian Pines; Salinas; EuroSAT MSI; 44; 4; 6

**Estimated time**
1.05 minutes

**Transition**
With the benchmark design fixed, I can now show the fresh rerun evidence.

## Slide 8. Main HSI Benchmark Results

**English oral script**
On HSI, Random keeps strong overall accuracy, but it leaves PrioCovErr high at 23.49. Class-Balanced helps some utility metrics but still makes policy alignment worse. The OSAG family is different because it pushes PrioCovErr toward zero while keeping useful accuracy, and OSAG-FairLoss reaches 91.15 on Acc_high with near-zero PrioCovErr.

**中文理解与记忆**
这页的重点是：随机采样不等于治理，类平衡也不等于治理。OSAG 的价值是把策略偏差压到接近 0。

**Key terms**
HSI; near-zero PrioCovErr; not just class balancing

**Estimated time**
1.35 minutes

**Transition**
The same governance pattern appears again on EuroSAT MSI.

## Slide 9. Main EuroSAT MSI Results

**English oral script**
EuroSAT shows the same pattern under a second sensing modality. Random keeps the strongest Acc_all, but its PrioCovErr is still high at 23.81. OSAG and OSAG-FairLoss again reduce policy error to about 0.20 while improving high-priority performance. So the governance claim is not tied to one dataset or one sensing modality.

**中文理解与记忆**
这页是跨模态支撑：说明这个治理效应不是只在 HSI 上成立。

**Key terms**
EuroSAT MSI; second modality; same governance effect

**Estimated time**
1.35 minutes

**Transition**
That leads to the next question: why is overall accuracy alone not enough?

## Slide 10. Why Accuracy Alone Is Not Enough

**English oral script**
The trade-off figure shows why overall accuracy is insufficient. Table 5.2 reports absolute percentage-point differences relative to Random, not relative percentage changes. On both benchmarks, OSAG gives up only about half a point of Acc_all, but reduces PrioCovErr by about twenty-three points and improves Acc_high.

**中文理解与记忆**
这里一定要讲清楚：Table 5.2 不是相对百分比变化，而是绝对百分点差。

**Key terms**
absolute percentage-point differences; trade-off; policy alignment

**Estimated time**
1.05 minutes

**Transition**
Next I will show what happens when contract design and compute scope change.

## Slide 11. Contract Design, Runtime, and Robustness

**English oral script**
There are three extension checks. First, the EuroSAT ablation shows that finer contracts reduce governance cost. Second, runtime stays in a comparable practical range; the thesis does not claim that OSAG is intrinsically faster. Third, the scoped ResMLP extension shows the governance conclusion survives modest backbone strengthening.

**中文理解与记忆**
这页把扩展部分压缩成三句话：合同设计影响治理成本、运行时间是同量级、ResMLP 只是有限鲁棒性补充。

**Key terms**
ablation; comparable runtime; scoped ResMLP extension

**Estimated time**
1.20 minutes

**Transition**
After the benchmark evidence, I move to the demo branch of the thesis.

## Slide 12. Why the Demo Matters

**English oral script**
The benchmark chapter is the scientific evidence chain, but it does not naturally show time-stepped operational behavior. The dispatch demo turns the same governance idea into an emergency scheduling system with budgets, deadlines, and missed-service events. It is therefore a communication and interpretability artifact, not a replacement for the benchmark.

**中文理解与记忆**
要告诉老师：demo 不是主证据，而是为了把系统行为讲清楚。

**Key terms**
benchmark versus demo; operational behavior

**Estimated time**
0.85 minutes

**Transition**
With that role clear, I can now show the demo outputs.

## Slide 13. Dispatch Demo Results

**English oral script**
In the demo, OSAG reaches the strongest governance-oriented reliability, the best compliance, and the lowest coverage error. Contract-Priority looks attractive only if one over-focuses on missed service alone. The sensitivity audit from saved outputs keeps OSAG top-ranked around the thesis weighting, so the conclusion is stable near the chosen weights.

**中文理解与记忆**
这页主要讲行为稳定性：OSAG 不是所有单项都极端最好，但在治理导向的总体表现上最稳。

**Key terms**
reliability; compliance; coverage error; missed service; sensitivity

**Estimated time**
1.20 minutes

**Transition**
Before closing, I want to show where the committee can inspect the code safely.

## Slide 14. Repository and Code Architecture

**English oral script**
If the committee asks to inspect the implementation, this is the safe map. The formal benchmark path starts from run_all_real_experiments.py and moves into reproduce_osag_real.py. The dispatch path starts from run_visual_demo.py and moves into run_dispatch_demo.py and dispatch_demo_core.py. The live code discussion should focus on build_contract_table_from_meta, compute_coverage_errors, and choose_observations.

**中文理解与记忆**
这页不是让你读代码，而是让你知道“先开哪个文件、再看哪个函数、最后看哪个输出”。

**Key terms**
benchmark path; demo path; build_contract_table_from_meta; choose_observations

**Estimated time**
0.95 minutes

**Transition**
With the code path clear, I can now state the limitations directly.

## Slide 15. Limitations and Boundaries

**English oral script**
The HSI split is pixel-stratified rather than spatial-blocked, so absolute accuracy may be optimistic. The graph is a modeling view rather than a full explicit graph optimizer. The main benchmark uses a lightweight MLP to isolate governance effects, and the ResMLP study is scoped. The demo is supportive evidence, and reproducibility relies on scripts, manifests, logs, configs, and stage reports rather than a git commit ledger.

**中文理解与记忆**
这页一定要坦诚，但语气不能虚。要让老师感觉你知道边界，因此结论更可信。

**Key terms**
pixel-stratified; graph as modeling view; lightweight MLP; scoped extension; non-git provenance

**Estimated time**
1.25 minutes

**Transition**
With the boundaries stated, I can summarize the reproducibility story.

## Slide 16. Reproducibility and Public Release

**English oral script**
Appendix A separates fully rerun main benchmark evidence, rerun extensions, and artifact-level reproducibility. It fixes the formal inputs, contract construction rules, and fresh output locations. Together with the companion public repository, this makes the defense evidence much easier to inspect.

**中文理解与记忆**
这一页就是把“可复现”讲成三层：主实验 fresh rerun、扩展 fresh rerun、产物级可复现。

**Key terms**
fully rerun main benchmark; rerun extensions; artifact-level reproducibility

**Estimated time**
0.95 minutes

**Transition**
I will end with three concise takeaways.

## Slide 17. Final Takeaways

**English oral script**
There are three takeaways. First, the thesis contribution is governance-aware EO training. Second, OSAG sharply reduces policy misalignment on the current benchmarks while staying competitive in utility. Third, the benchmark, demo, code path, and Appendix A together form a complete and defensible defense package. Thank you. I am ready to move to live demo and questions.

**中文理解与记忆**
收尾时只保留三句：做的是什么、证据说明了什么、为什么这套答辩是完整的。

**Key terms**
governance-aware training; policy alignment; complete defense story

**Estimated time**
0.75 minutes

**Transition**
I am ready for your questions and the live demo.
