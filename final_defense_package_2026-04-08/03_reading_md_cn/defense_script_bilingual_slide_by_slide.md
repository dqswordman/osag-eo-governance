# 双语逐页答辩讲稿（个人练习版）

每一页先看英文口头讲法，再看中文理解说明，最后记关键词和过渡句。

## Slide 1. Title with Advisor Signature

### English oral script
Good morning, respected committee members. My thesis is titled 'Governance-Aware Earth Observation Learning: Contract-Governed Training with Observed Service Agreement Graphs.' Today I will present the motivation, the framework, the fresh benchmark evidence, the operational demo logic, and the software path that supports the defense.

### 中文理解与记忆
这一页的重点不是读题目，而是稳住开场：题目、身份、签字区都齐全，说明材料已经是正式答辩版。

### 要记住的关键词
governance-aware EO training; advisor signature area; final thesis state

### 预计时间
0.80 minutes

### 过渡句
I will begin with a short roadmap of the talk.

## Slide 2. Talk Roadmap

### English oral script
I will organize the presentation into five parts. First, the problem and motivation. Second, the OSAG framework and benchmark design. Third, the actual code path behind the framework. Fourth, the fresh rerun evidence and the dispatch demo. Fifth, the limitations, reproducibility scope, and final takeaways. The live demo and code questioning come after the slide presentation.

### 中文理解与记忆
这一页帮你把全场结构讲清楚，老师会更容易跟上，你自己也不容易慌。

### 要记住的关键词
problem; framework; code; evidence; boundaries

### 预计时间
0.50 minutes

### 过渡句
With that roadmap in place, I will begin with the motivation.

## Slide 3. Background and Motivation

### English oral script
Standard EO training is usually accuracy-driven. But many real EO tasks care about whether important regions, categories, or service groups are consistently served during training. That means the hidden allocation of training exposure becomes important. This is the motivation for a governance layer.

### 中文理解与记忆
背景页一定要讲到“accuracy 不等于服务被正确分配”，这是整篇 thesis 的问题意识。

### 要记住的关键词
accuracy is not enough; who gets served

### 预计时间
1.20 minutes

### 过渡句
That leads directly to the research gap and the thesis questions.

## Slide 4. Research Gap and Guiding Questions

### English oral script
The gap is that ordinary EO training does not represent service allocation explicitly. So the thesis asks four questions: how to formalize service over contracts, whether a lightweight governance layer can control it, what the utility-versus-governance trade-off looks like on HSI and MSI benchmarks, and whether this can be explained through a runnable operational artifact.

### 中文理解与记忆
这一页不要泛泛而谈，要把 thesis 想回答的四个问题直接讲成后面每一章的任务。

### 要记住的关键词
service allocation; explicit policy; four questions

### 预计时间
1.20 minutes

### 过渡句
Next, I will summarize the contributions that answer these questions.

## Slide 5. Thesis Contributions

### English oral script
The thesis contributes in four ways. Conceptually, it reframes EO training as a governance problem. Methodologically, it introduces OSAG as a lightweight contract-aware layer. Empirically, it provides fresh rerun benchmark evidence, ablation, runtime interpretation, and a scoped backbone extension. Finally, it adds a dispatch demo and a reproducibility appendix that make the work more inspectable and defensible.

### 中文理解与记忆
贡献页要把概念贡献、方法贡献、实证贡献和 artifact 贡献分开说。

### 要记住的关键词
conceptual; methodological; empirical; artifact-level

### 预计时间
1.10 minutes

### 过渡句
Now I will use Figure 1.1 as the map for the whole thesis.

## Slide 6. Figure 1.1 Method Overview

### English oral script
Figure 1.1 is the thesis map. EO inputs are converted into contracts, policy targets define how much service each contract should receive, the OSAG sampler injects that policy into training exposure, and the coverage monitor checks whether the observed exposure matches the target. The key idea is that OSAG wraps ordinary training rather than replacing the classifier.

### 中文理解与记忆
Figure 1.1 是全篇总图。紧张时就回到这张图，按 inputs -> contracts -> policy -> sampler -> monitor 讲。

### 要记住的关键词
contracts; policy targets; sampler; monitor; feedback loop

### 预计时间
1.40 minutes

### 过渡句
To see why the framework is needed, I first explain why standard ERM is service-blind.

## Slide 7. Why Ordinary EO Training Is Service-Blind

### English oral script
The ordinary ERM objective optimizes average loss over a flat sample pool. That is mathematically clean, but it does not know which contracts are policy-critical, which ones are rare, or which ones deserve more sustained attention. In EO, that means training exposure follows data density by default. The governance layer makes those service choices explicit instead of accidental.

### 中文理解与记忆
这里要把普通 ERM 为什么 service-blind 讲明白，否则后面所有治理逻辑都会显得多余。

### 要记住的关键词
ERM; flat sample pool; no policy target

### 预计时间
1.40 minutes

### 过渡句
With that intuition in place, I can define the core governance vocabulary.

## Slide 8. Core Concepts and Control Logic

### English oral script
The key concepts are contract, target service share, empirical coverage, PrioCovErr, alpha, and lambda_C. A contract is the service unit. The target share says how much training exposure it should receive. Empirical coverage says how much it actually receives. PrioCovErr measures the gap. Alpha controls how strongly the sampler follows the policy, and lambda_C controls additional fairness pressure in loss space.

### 中文理解与记忆
这一页是术语页。只要 contract、target share、empirical coverage、PrioCovErr、alpha、lambda_C 讲顺，后面老师就容易接受结果。

### 要记住的关键词
contract; target share; empirical coverage; PrioCovErr; alpha; lambda_C

### 预计时间
1.50 minutes

### 过渡句
The next two slides show how this becomes a concrete benchmark design.

## Slide 9. Benchmarks and Data Sources

### English oral script
The thesis uses two benchmark families. The HSI benchmark merges corrected Indian Pines and corrected Salinas after band alignment. The MSI benchmark uses canonical 13-band EuroSAT MSI. Appendix A fixes the formal inputs explicitly, which matters because the thesis evidence is supposed to come from the formal rerun pipeline rather than from notebook-only historical outputs.

### 中文理解与记忆
这一页是数据与正式输入边界。要强调 corrected HSI、canonical EuroSAT MSI，以及 Appendix A 的 formal input role。

### 要记住的关键词
corrected HSI; canonical EuroSAT MSI; formal inputs

### 预计时间
1.10 minutes

### 过渡句
After the data sources, I will explain how contracts and target shares are built.

## Slide 10. Contract Construction and Target-Share Policy

### English oral script
Contract construction is part of the scientific design, not just preprocessing. In the locked rerun, HSI realizes 44 contracts, EuroSAT coarse uses 4, and EuroSAT fine uses 6. The target share is proportional to priority times contract size. So the governance target combines human policy intent with available evidence rather than ignoring either one.

### 中文理解与记忆
这一页一定要讲清楚 EuroSAT fine 是 6，不是 12。target share 是 priority 乘以 contract size。

### 要记住的关键词
44; 4; 6; priority times contract size

### 预计时间
1.30 minutes

### 过渡句
With the benchmark design fixed, I can now show how the actual codebase implements the same logic.

## Slide 11. Repository and Code Architecture

### English oral script
Before the results, I want to make the code path explicit. The repository has three practical branches. One is the real benchmark rerun pipeline. One is the dispatch-demo pipeline. One is the artifact-generation path for the defense materials. This structure matters because it makes the thesis easier to inspect under live questioning.

### 中文理解与记忆
代码架构页的目标是让老师相信你真的知道仓库怎么组织，不要只会讲论文。

### 要记住的关键词
real rerun path; demo path; artifact path

### 预计时间
1.00 minutes

### 过渡句
Now I will zoom in on the core functions that implement the contract policy.

## Slide 12. Code View: Contracts and Target Service Shares

### English oral script
This slide shows the first important implementation bridge. In the rerun pipeline, build_contract_table_from_meta materializes contract IDs, counts, priorities, and target weights. In the dispatch demo, the same idea appears in the fixed contract table with priorities, target weights, and deadlines. So both the benchmark and the demo are driven by explicit contract objects, not by hidden magic.

### 中文理解与记忆
这页把 thesis 数学定义和真实代码接起来，重点是 contract table 和 target_weight 真的是代码里的正式对象。

### 要记住的关键词
contract table; target weight; same logic in benchmark and demo

### 预计时间
1.20 minutes

### 过渡句
With the contract table defined, I can now show how OSAG turns it into sampling and monitoring decisions.

## Slide 13. Code View: OSAG Sampler, Fairness, and Coverage Monitor

### English oral script
Here the governance layer becomes action. In the demo, choose_observations combines urgency, deadline pressure, coverage gap, uncertainty, and priority into the OSAG dispatch score. In the benchmark pipeline, the fairness-loss branch adds lambda_C only when high-priority contracts remain harder than low-priority ones. And the coverage monitor computes policy-alignment error from observed contract counts. That is the heart of OSAG in software.

### 中文理解与记忆
这页是最核心的代码解释页，OSAG 真正的 sampler / fairness / coverage monitor 逻辑都在这里对应上。

### 要记住的关键词
urgency; gap; uncertainty; lambda_C; monitor

### 预计时间
1.30 minutes

### 过渡句
After the core logic, I will show the execution path that I can safely demonstrate live if asked.

## Slide 14. Code View: Benchmark and Demo Execution Path

### English oral script
The defense-day execution path is intentionally simple. For the benchmark, the clean entry is run_all_real_experiments.py, then reproduce_osag_real.py, then the generated tables and runtime summaries. For the demo, the clean entry is run_visual_demo.py, which delegates to run_dispatch_demo.py and then opens the dashboard. If the committee asks to inspect code, this slide gives the safest file order to open.

### 中文理解与记忆
这页告诉老师：如果现在要看代码，我知道从哪里进、会落到哪些输出，不是临场乱翻。

### 要记住的关键词
entry points; safe file order; outputs

### 预计时间
1.00 minutes

### 过渡句
With the code path clear, I can return to the main evidence from the fresh reruns.

## Slide 15. Main HSI Benchmark Results

### English oral script
On HSI, Random gives strong overall accuracy, but it leaves PrioCovErr high at 23.49. Class-Balanced improves high-priority accuracy somewhat, yet makes PrioCovErr worse. Uniform-Contract and Contract-Priority can look attractive on Acc_high alone, but they overserve some contracts badly. The OSAG family is different because it collapses policy misalignment while still keeping useful accuracy, and OSAG-FairLoss pushes Acc_high to 91.15 with near-zero PrioCovErr.

### 中文理解与记忆
HSI 结果页重点是 class balancing 不是 governance，heuristic baseline 不能保证 policy alignment。

### 要记住的关键词
HSI; class balancing is not governance; near-zero PrioCovErr

### 预计时间
1.50 minutes

### 过渡句
I will now show that the same pattern appears on EuroSAT MSI.

## Slide 16. Main EuroSAT MSI Results

### English oral script
EuroSAT shows the same governance pattern under a second sensing modality. Random keeps the strongest Acc_all, but its PrioCovErr is still high at 23.81. Contract-Priority improves Acc_high, yet distorts policy alignment badly. OSAG and OSAG-FairLoss again drive PrioCovErr down to about 0.20 while improving high-priority performance. So the governance argument survives across both HSI and MSI.

### 中文理解与记忆
EuroSAT 页要突出第二模态一致性，说明结果不是只在 HSI 里成立。

### 要记住的关键词
EuroSAT MSI; second modality; same governance effect

### 预计时间
1.50 minutes

### 过渡句
To connect these two benchmark slides, I next explain why overall accuracy alone is not enough.

## Slide 17. Why Accuracy Alone Is Not Enough

### English oral script
This is where Table 5.2 matters. The reported deltas are absolute percentage-point differences relative to Random, not relative percentage changes. On both benchmarks, OSAG gives up only about half a point of Acc_all, but reduces PrioCovErr by about twenty-three points and improves Acc_high. That is why the thesis says average accuracy is important but insufficient.

### 中文理解与记忆
这一页要明确 Table 5.2 是 absolute percentage-point differences，不是 relative changes。

### 要记住的关键词
absolute percentage-point differences; trade-off; policy alignment

### 预计时间
1.20 minutes

### 过渡句
After the main tables, I will show how contract design changes governance cost.

## Slide 18. Contract-Design Ablation

### English oral script
The EuroSAT ablation asks whether governance cost depends on how contracts are defined. The answer is yes. The fine contract design starts from a lower Random PrioCovErr baseline and retains more accuracy while still reaching near-zero policy error. That supports the claim that contract design is a substantive part of governance, not an arbitrary preprocessing choice.

### 中文理解与记忆
ablation 页的重点是 contract design 本身就会改变治理成本。

### 要记住的关键词
contract design; governance cost; coarse versus fine

### 预计时间
1.20 minutes

### 过渡句
The next slide addresses compute cost and modest backbone strengthening.

## Slide 19. Runtime and Backbone Robustness

### English oral script
The runtime table should be read as comparable-overhead evidence, not as a speed claim. OSAG is in the same practical runtime range as Random, and the apparently slower Random mean on HSI is driven mainly by one outlier seed. The ResMLP extension is intentionally scoped, but it is still useful because the governance conclusion survives modest backbone strengthening.

### 中文理解与记忆
runtime 和 backbone 页的重点是诚实：不是说 OSAG 更快，也不是说 thesis 在比 backbone SOTA。

### 要记住的关键词
comparable overhead; not a speed claim; scoped ResMLP extension

### 预计时间
1.30 minutes

### 过渡句
With the benchmark evidence complete, I now move to the dispatch-demo branch of the thesis story.

## Slide 20. Why the Dispatch Demo Is Needed

### English oral script
The benchmark chapter proves the scientific effect, but it does not naturally show the time-stepped operational behavior of the governance layer. The dispatch demo makes that behavior visible under budgets, deadlines, and missed-service events. So it is an interpretability and communication artifact that complements the benchmark rather than replacing it.

### 中文理解与记忆
这一页是为 demo 正名：demo 是 operational complement，不是替代 benchmark。

### 要记住的关键词
benchmark versus demo; operational complement

### 预计时间
0.90 minutes

### 过渡句
To make that concrete, the next slide defines the demo scenario.

## Slide 21. Dispatch Demo Setup and Scenario

### English oral script
The dispatch demo models a 12 by 12 emergency grid over ten decision steps. It defines six contracts, of which the first three are high-priority and deadline-sensitive. The system has an observation budget of fourteen tiles and an annotation budget of six tiles per step. It compares Random, Contract-Priority, and OSAG, and it tracks five quantities: compliance, coverage error, missed service, Q_high, and reliability.

### 中文理解与记忆
这页把 dispatch demo 的格子、时间步、预算、合同全部讲明白，后面结果才有语境。

### 要记住的关键词
12 by 12 grid; 10 steps; budgets; six contracts

### 预计时间
1.20 minutes

### 过渡句
With the setup clear, I can now show the end-of-run and timeline results.

## Slide 22. Dispatch Demo Results and Interpretation

### English oral script
In the demo, OSAG reaches the strongest governance-oriented reliability, the best compliance, and the lowest coverage error. Contract-Priority looks better only if the user focuses narrowly on missed service or critical capture. The timeline and contract-gap plots show why: OSAG is more stable in long-run service balance. The sensitivity note matters because it shows the OSAG ranking remains top around the thesis weighting.

### 中文理解与记忆
demo 结果页要提醒自己：reliability 是 summary，不是唯一指标；Q_high 不等于 K。

### 要记住的关键词
reliability; compliance; coverage error; sensitivity

### 预计时间
1.40 minutes

### 过渡句
After the demo, I will state the claim boundaries directly.

## Slide 23. Limitations and Claim Boundaries

### English oral script
This thesis is careful about its boundaries. The HSI split is pixel-stratified rather than spatial-blocked, so absolute accuracy may be optimistic. The graph is a modeling view rather than a full explicit graph optimizer. The main benchmark uses a lightweight MLP to isolate governance effects, and the ResMLP study is scoped. The demo is supportive evidence, and reproducibility relies on scripts, manifests, logs, configs, and stage reports rather than a git commit ledger.

### 中文理解与记忆
局限性页不是自我否定，而是告诉老师你知道自己的结论边界在哪里。

### 要记住的关键词
pixel-stratified; graph as modeling view; scoped backbone; supportive demo

### 预计时间
1.40 minutes

### 过渡句
With those boundaries stated, I can summarize the reproducibility story.

## Slide 24. Reproducibility and Public Release

### English oral script
Appendix A matters because it separates fully rerun main benchmark evidence, fully rerun extensions, and artifact-level reproducibility. It records the formal input data, the contract construction rules, the fresh output locations, and the non-git provenance boundary. Together with the public source release, that makes the thesis easier to inspect and defend.

### 中文理解与记忆
这一页把可复现性边界讲清楚，尤其是 fully rerun、artifact-level reproducibility 和 non-git provenance boundary。

### 要记住的关键词
fully rerun main benchmark; extensions; artifact-level reproducibility

### 预计时间
1.00 minutes

### 过渡句
I will end with three short takeaways and then move to the live demo and your questions.

## Slide 25. Final Takeaways and Transition

### English oral script
There are three final takeaways. First, the thesis contribution is governance-aware EO training. Second, OSAG sharply reduces policy misalignment while keeping competitive utility on fresh reruns. Third, the benchmark, the code path, the dispatch demo, and Appendix A together form a complete and auditable defense story. This concludes the slide presentation. After this, I will move to the live demo and then to your questions.

### 中文理解与记忆
结论页只留三句话：问题是什么、结果证明了什么、整套 defense story 为什么完整。

### 要记住的关键词
governance-aware training; alignment gains; auditable defense story

### 预计时间
0.90 minutes

### 过渡句
按问答需要切换到下一页。

## Slide 26. Backup: Where Is the Graph Really?

### English oral script
If asked where the graph is, the safe answer is that the current thesis uses the graph mainly as a structured view over the contract space. The implementation itself is still mostly a contract-aware sampling and monitoring layer. Explicit graph algorithms are future work.

### 中文理解与记忆
backup 图页用于处理 graph 质疑：讲 modeling view，不要讲成 full explicit graph optimizer。

### 要记住的关键词
graph as structured contract space

### 预计时间
Backup slide / on demand

### 过渡句
按问答需要切换到下一页。

## Slide 27. Backup: HSI Split and Spatial Leakage Boundary

### English oral script
If asked about leakage, the answer is yes: the HSI split is pixel-stratified rather than spatial-blocked, so neighboring pixels can cross splits. The safest interpretation of the HSI results is therefore comparative governance evidence under a fixed protocol.

### 中文理解与记忆
backup HSI split 页用于处理 leakage 质疑：直接承认 pixel-stratified，不要硬辩。

### 要记住的关键词
pixel-stratified; comparative governance result

### 预计时间
Backup slide / on demand

### 过渡句
按问答需要切换到下一页。

## Slide 28. Backup: Demo Metrics, Reliability, Q_high, and Sensitivity

### English oral script
If asked about the demo metrics, clarify that reliability is a hand-set summary score, Q_high is distinct from K, and the sensitivity note was computed from saved outputs only. The primitive metrics still matter more than the composite score by itself.

### 中文理解与记忆
backup demo metrics 页用于处理 reliability/Q_high/K/sensitivity 的追问，记住 primitive metrics 更重要。

### 要记住的关键词
reliability; Q_high versus K; sensitivity

### 预计时间
Backup slide / on demand

### 过渡句
按问答需要切换到下一页。
