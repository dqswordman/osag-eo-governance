# OSAG English Defense Deck Notes

- Total estimated main-deck time: 15.55 minutes
- Target time by section:
  - Opening and framing (Slides 1-5): about 3.45 minutes
  - Method and benchmark design (Slides 6-8): about 3.20 minutes
  - Main results and extensions (Slides 9-11): about 3.90 minutes
  - Demo and limitations (Slides 12-14): about 3.30 minutes
  - Reproducibility and close (Slides 15-17): about 1.70 minutes
- Main-deck timing inside 14-16 minutes: yes

## Slide 1. Title

**Key message**
State the thesis title, your identity, and the central theme in one breath.

**What to say orally**
Good morning. My thesis is titled 'Governance-Aware Earth Observation Learning: Contract-Governed Training with Observed Service Agreement Graphs.' In this work, I study how to make EO training policy-aware at the contract level rather than optimizing only aggregate accuracy.

**Emphasis words**
governance-aware EO training; contract-level service

**Transition to next slide**
I will start by explaining why this problem matters in the first place.

**Shortest interruption-safe answer**
It is about making EO training auditable at the contract level.

**Estimated time**
0.45 minutes

## Slide 2. Talk Roadmap

**Key message**
Preview the structure of the defense in one short slide so the talk feels easier to follow.

**What to say orally**
I will organize the talk into four parts. First, I will explain the problem and motivation. Second, I will summarize the OSAG framework and the benchmark setup. Third, I will present the fresh rerun results, the ablation, and the robustness checks. Finally, I will show the dispatch demo, the claim boundaries, and the reproducibility story.

**Emphasis words**
problem; framework; evidence; demo and boundaries

**Transition to next slide**
With that roadmap in place, I can begin with the motivation.

**Shortest interruption-safe answer**
The roadmap is simple: problem, method, evidence, and then demo plus boundaries.

**Estimated time**
0.30 minutes

## Slide 3. Background and Motivation

**Key message**
Explain why average accuracy alone is insufficient in policy-facing EO applications.

**What to say orally**
Standard EO pipelines are usually accuracy-driven. But in real deployments, decision makers also care about who gets served during training, such as rare crop types, vulnerable regions, or policy-critical semantic groups. This motivates adding a governance layer on top of ordinary EO learning.

**Emphasis words**
accuracy is not enough; who is served

**Transition to next slide**
That motivation leads directly to the research gap and the guiding questions.

**Shortest interruption-safe answer**
The short answer is that the thesis makes training exposure explicit rather than leaving it implicit.

**Estimated time**
0.90 minutes

## Slide 4. Research Gap and Guiding Questions

**Key message**
Move from motivation to the four questions that organize the thesis.

**What to say orally**
The central gap is that standard EO training does not represent service allocation explicitly. So the thesis asks four questions: how to formalize contract-level service, whether a lightweight governance layer can control it, what the empirical trade-off looks like on HSI and MSI benchmarks, and whether the idea can be communicated through a runnable defense artifact.

**Emphasis words**
service allocation; explicit and measurable; runnable demo

**Transition to next slide**
Next, I summarize the thesis contributions that answer those questions.

**Shortest interruption-safe answer**
The gap is not lack of accuracy metrics. It is lack of explicit policy control over training exposure.

**Estimated time**
1.00 minutes

## Slide 5. Thesis Contributions

**Key message**
Summarize conceptual, methodological, empirical, and artifact-level contributions without overstating novelty.

**What to say orally**
The thesis contributes at four levels. Conceptually, it reframes EO training as a governance problem. Methodologically, it develops OSAG as a contract-aware layer. Empirically, it provides fresh reruns, ablation, runtime, and a scoped robustness extension. At the artifact level, it adds a dispatch demo and a reproducibility appendix.

**Emphasis words**
conceptual; methodological; empirical; artifact-level

**Transition to next slide**
With that context, let me show the method overview that ties the thesis together.

**Shortest interruption-safe answer**
The novelty is mainly in the governance framing and the lightweight control layer, not in inventing a new backbone.

**Estimated time**
0.80 minutes

## Slide 6. Figure 1.1: Method Overview

**Key message**
Use the final pipeline figure as the structural anchor for the whole talk.

**What to say orally**
Figure 1.1 is the high-level thesis map. EO inputs are transformed into contracts, policy targets specify how much service each contract should receive, the OSAG sampler injects that policy into training exposure, and the coverage monitor checks whether observed exposure matches the target. The key point is that OSAG wraps a standard classifier rather than replacing it.

**Emphasis words**
pipeline; contracts; policy targets; coverage monitor

**Transition to next slide**
To make that pipeline concrete, I will define the core concepts next.

**Shortest interruption-safe answer**
It is a governance loop around training, not a different EO backbone.

**Estimated time**
1.20 minutes

## Slide 7. Core Concepts

**Key message**
Teach the audience the six terms they need for the rest of the deck.

**What to say orally**
A contract is the service unit the policy cares about. The target service share tells us how much training attention each contract should receive. Empirical coverage tells us how much it actually receives. PrioCovErr measures the gap between the two. Alpha controls how strongly the sampler follows OSAG versus the baseline, and lambda_C controls the additional fairness penalty.

**Emphasis words**
contract; target share; empirical coverage; PrioCovErr; alpha; lambda_C

**Transition to next slide**
With those terms in place, I can now explain how the benchmarks instantiate contracts.

**Shortest interruption-safe answer**
PrioCovErr is the main governance metric because it measures policy misalignment directly.

**Estimated time**
1.00 minutes

## Slide 8. Benchmarks and Contract Construction

**Key message**
Show the actual data sources and the exact contract counts used in the locked thesis.

**What to say orally**
The main benchmarks are corrected Indian Pines plus corrected Salinas for HSI and canonical 13-band EuroSAT MSI for multispectral data. In the current rerun pipeline, the HSI benchmark produces 44 realized contracts. EuroSAT uses 4 coarse contracts or 6 fine contracts. Target shares are set proportional to priority times contract size, with the exact priority rules listed here from Appendix A.

**Emphasis words**
Indian Pines; Salinas; EuroSAT MSI; 44; 4; 6

**Transition to next slide**
After defining the benchmarks, the next step is the main fresh rerun evidence.

**Shortest interruption-safe answer**
EuroSAT fine is six contracts in the locked thesis, not twelve.

**Estimated time**
1.00 minutes

## Slide 9. Main Fresh Five-Seed Benchmark Results

**Key message**
Present the main evidence cleanly and make the governance effect visually obvious.

**What to say orally**
This slide summarizes the main fresh five-seed operating points. On both HSI and EuroSAT, the OSAG family drives PrioCovErr very close to zero while keeping Acc_all competitive and improving high-priority performance. The point is not that OSAG wins every metric at once. The point is that it creates governance-faithful operating points with useful predictive performance.

**Emphasis words**
fresh five-seed rerun; near-zero PrioCovErr; competitive Acc_all; stronger Acc_high

**Transition to next slide**
To see why that matters, the next slide explains why accuracy alone is not enough.

**Shortest interruption-safe answer**
The main message is strong policy alignment with competitive utility, not universal dominance on every number.

**Estimated time**
1.60 minutes

## Slide 10. Why Accuracy Alone Is Not Enough

**Key message**
Explain the trade-off and correctly interpret Table 5.2.

**What to say orally**
The trade-off figure shows why overall accuracy is not a sufficient governance metric. Table 5.2 reports absolute percentage-point differences relative to Random, not relative percentage changes. OSAG gives up only about half a point of Acc_all on both benchmarks, but reduces PrioCovErr by about twenty-three points and improves Acc_high. That is the governance-value argument of the thesis.

**Emphasis words**
absolute percentage-point differences; trade-off; policy alignment

**Transition to next slide**
The next slide asks whether contract design, compute cost, and backbone choice change that conclusion.

**Shortest interruption-safe answer**
These are absolute point differences, so please do not interpret them as relative percentages.

**Estimated time**
1.00 minutes

## Slide 11. Contract Design, Runtime, and Robustness

**Key message**
Cover the three extension checks honestly and compactly.

**What to say orally**
There are three extension checks. First, the fresh three-seed EuroSAT ablation shows that finer contracts reduce governance cost. Second, runtime stays in a comparable practical range; the thesis does not claim that OSAG is intrinsically faster than Random. Third, a scoped EuroSAT ResMLP extension shows that the governance conclusion survives modest backbone strengthening.

**Emphasis words**
three-seed ablation; comparable runtime; scoped ResMLP extension

**Transition to next slide**
After the benchmark evidence, I move to the dispatch demo and explain why it is needed.

**Shortest interruption-safe answer**
The runtime table is evidence of comparable overhead, not evidence of superior speed.

**Estimated time**
1.30 minutes

## Slide 12. Why a Dispatch Demo Is Needed

**Key message**
Shift from scientific evidence to operational behavior.

**What to say orally**
The benchmark chapter is the scientific evidence chain, but it is not ideal for live defense. The dispatch demo turns the same governance idea into a time-stepped emergency scheduling system with budgets, deadlines, and missed-service consequences. That makes the behavioral mechanism visible in a way that tables alone cannot.

**Emphasis words**
benchmark versus demo; operational behavior; budgets and deadlines

**Transition to next slide**
Now I can show what the demo actually reports.

**Shortest interruption-safe answer**
The demo is supportive operational evidence; it does not replace the real benchmark.

**Estimated time**
0.80 minutes

## Slide 13. Dispatch Demo Results

**Key message**
Present the demo metrics and the bounded claim they support.

**What to say orally**
In the demo, OSAG reaches the strongest governance-oriented reliability, the best compliance, and the lowest coverage error. Contract-Priority looks attractive only on missed service alone. The sensitivity audit, computed from saved demo outputs only, shows that OSAG remains top-ranked around the thesis weighting and under several nearby perturbations. Reliability is therefore useful as a summary, but it is not the only metric.

**Emphasis words**
reliability; compliance; coverage error; missed service; Q_high

**Transition to next slide**
Before closing, I want to state the claim boundaries clearly.

**Shortest interruption-safe answer**
Q_high is not the same as K; reliability is a dashboard summary, not the only evaluation criterion.

**Estimated time**
1.30 minutes

## Slide 14. Limitations and Claim Boundaries

**Key message**
State the honest boundaries so the thesis sounds stronger, not weaker.

**What to say orally**
This slide makes the claim boundary explicit. The HSI split is pixel-stratified rather than spatial-blocked. The graph is a modeling view, not a full explicit graph optimizer. The main benchmark uses a lightweight MLP to isolate governance effects, and the ResMLP study is scoped. The demo is supportive evidence, and provenance relies on manifests, configs, logs, and stage reports rather than a git commit ledger.

**Emphasis words**
pixel-stratified; not leakage-free; graph as modeling view; not a backbone SOTA study

**Transition to next slide**
With those boundaries stated, I can summarize the reproducibility story briefly.

**Shortest interruption-safe answer**
The thesis is stronger because its limitations are explicit.

**Estimated time**
1.20 minutes

## Slide 15. Reproducibility and Public Release

**Key message**
Summarize the three reproducibility levels and the public release without turning the slide into a wall of text.

**What to say orally**
Appendix A makes the evidence chain auditable at three levels. The main HSI and EuroSAT tables are fully rerun over five seeds. The contract ablation and ResMLP extension are also freshly rerun within their stated scope. At the artifact level, the demo, thesis figures and tables, and thesis PDF can be regenerated. A companion public source release packages the cleaned scripts and the dispatch demo.

**Emphasis words**
fully rerun main benchmark; extensions; artifact-level reproducibility

**Transition to next slide**
I will end with three concise takeaways.

**Shortest interruption-safe answer**
The reproducibility story is script-driven and artifact-driven, even though the local thesis workspace itself is not a git repository.

**Estimated time**
0.80 minutes

## Slide 16. Final Takeaways

**Key message**
Land the three claims the committee should remember.

**What to say orally**
There are three final takeaways. First, the thesis contribution is governance-aware EO training. Second, OSAG sharply reduces policy misalignment on the current benchmarks while staying competitive in predictive utility. Third, the combination of fresh reruns, operational demo, and reproducibility appendix turns that contribution into a complete and defensible thesis story.

**Emphasis words**
governance-aware EO training; sharp reduction in misalignment; complete defense story

**Transition to next slide**
That concludes the main presentation. I welcome your questions.

**Shortest interruption-safe answer**
If you remember one sentence: EO training is also a service-allocation problem, and OSAG makes that allocation explicit.

**Estimated time**
0.70 minutes

## Slide 17. Closing / Q&A

**Key message**
Close formally and invite questions.

**What to say orally**
Thank you for your attention. I am happy to answer questions about the method, the rerun pipeline, the dispatch demo, or the limitations and future work.

**Emphasis words**
thank you; questions welcome

**Transition to next slide**
Move naturally into questions.

**Shortest interruption-safe answer**
I am happy to expand on any part of the benchmark, the demo, or the reproducibility appendix.

**Estimated time**
0.20 minutes
