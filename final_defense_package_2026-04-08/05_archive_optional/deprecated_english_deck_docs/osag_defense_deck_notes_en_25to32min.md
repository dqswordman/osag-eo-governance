# OSAG English Defense Deck Notes (25-32 Minute Version)

- Total estimated main-deck time: 27.40 minutes
- Target time by section:
  - Opening and framing (Slides 1-5): about 5.20 minutes
  - Framework and benchmark design (Slides 6-10): about 7.20 minutes
  - Main benchmark evidence and extensions (Slides 11-15): about 7.90 minutes
  - Demo, boundaries, and close (Slides 16-21): about 7.10 minutes
- Main-deck timing inside 25-32 minutes: yes
- Live demo time is excluded from this estimate.
- The main deck alone is designed to satisfy the presentation-time requirement before demo and Q&A.

## Slide 1. Title with Advisor Signature

**Key message**
Open formally, show the thesis identity, and reserve advisor sign-off space.

**What to say orally**
Good morning. My thesis is titled 'Governance-Aware Earth Observation Learning: Contract-Governed Training with Observed Service Agreement Graphs.' Today I will present the problem, the framework, the fresh rerun evidence, and the operational demo logic. The advisor signature area is reserved on the printed defense copy.

**Emphasis words**
thesis title; governance-aware EO training; advisor signature area

**Transition to next slide**
I will begin with a short roadmap of the talk.

**Shortest interruption-safe answer**
This thesis is about making EO training policy-aware at the contract level.

**Estimated time**
0.90 minutes

## Slide 2. Talk Roadmap

**Key message**
Preview the structure of the longer defense so the committee can follow the argument.

**What to say orally**
I will organize the presentation into four parts. First, the problem and motivation. Second, the OSAG framework and the benchmark design. Third, the fresh rerun results, ablation, and robustness evidence. Fourth, the dispatch demo, the limitations, and the reproducibility scope. The live demo comes after the slides.

**Emphasis words**
problem; framework; evidence; demo and boundaries

**Transition to next slide**
With that roadmap in place, I will begin with the motivation.

**Shortest interruption-safe answer**
The structure is problem, method, evidence, and then demo plus boundaries.

**Estimated time**
0.60 minutes

## Slide 3. Background and Motivation

**Key message**
Explain why EO training needs an explicit governance layer.

**What to say orally**
Standard EO pipelines are usually accuracy-driven. But real deployments care about who gets served during training, especially rare or policy-critical contracts. That is why this thesis treats training exposure as a governance question rather than a hidden side effect of data frequency.

**Emphasis words**
accuracy is not enough; who is served

**Transition to next slide**
That leads to the research gap and the guiding questions.

**Shortest interruption-safe answer**
The short answer is that the thesis makes training exposure explicit instead of implicit.

**Estimated time**
1.20 minutes

## Slide 4. Research Gap and Guiding Questions

**Key message**
State the gap and the four questions clearly enough for the rest of the talk to feel structured.

**What to say orally**
The central gap is that ordinary EO training does not represent service allocation explicitly. So the thesis asks four questions: how to formalize service over contracts, whether a lightweight governance layer can control it, what the trade-off looks like on HSI and MSI benchmarks, and whether the idea can be explained through a runnable defense artifact.

**Emphasis words**
service allocation; explicit and measurable; four questions

**Transition to next slide**
Next, I summarize the thesis contributions that answer those questions.

**Shortest interruption-safe answer**
The gap is not lack of accuracy metrics. It is lack of explicit policy control over training exposure.

**Estimated time**
1.30 minutes

## Slide 5. Thesis Contributions

**Key message**
Separate the contribution types so the committee sees a thesis-sized package rather than a single experiment.

**What to say orally**
The contributions are fourfold. Conceptually, the thesis reframes EO training as governance-aware learning. Methodologically, it develops OSAG as a contract-aware layer. Empirically, it provides fresh reruns, ablation, runtime, and a scoped backbone extension. At the artifact level, it adds a dispatch demo and a reproducibility appendix.

**Emphasis words**
conceptual; methodological; empirical; artifact-level

**Transition to next slide**
Now I will show the full method overview that connects these contributions.

**Shortest interruption-safe answer**
The thesis is broader than a single benchmark table.

**Estimated time**
1.20 minutes

## Slide 6. Figure 1.1 Method Overview

**Key message**
Use the pipeline figure as the structural map for the entire talk.

**What to say orally**
Figure 1.1 is the high-level thesis map. EO inputs are transformed into contracts, policy targets specify how much service each contract should receive, the OSAG sampler injects that policy into training exposure, and the coverage monitor checks whether observed exposure matches the target. The key point is that OSAG wraps a standard classifier rather than replacing it.

**Emphasis words**
contracts; policy targets; OSAG sampler; coverage monitor

**Transition to next slide**
To see why this is needed, I will first explain why standard ERM is service-blind.

**Shortest interruption-safe answer**
It is a governance loop around training, not a new backbone.

**Estimated time**
1.40 minutes

## Slide 7. Why Ordinary EO Training Is Service-Blind

**Key message**
Show why the thesis needs a governance formulation rather than only a better sampler.

**What to say orally**
The standard ERM objective minimizes average loss over a flat sample pool. That is mathematically clean, but it has no explicit notion of contract priority or service obligations. In EO, that means training attention follows data density by default. The governance layer changes this by defining contracts, defining target shares, and monitoring observed exposure against those targets.

**Emphasis words**
ERM; flat sample pool; no explicit service target

**Transition to next slide**
With that intuition in place, I can define the key governance quantities.

**Shortest interruption-safe answer**
ERM is service-blind because it has no explicit contract-level policy target.

**Estimated time**
1.50 minutes

## Slide 8. Core Concepts and Control Logic

**Key message**
Teach the audience the minimum vocabulary needed to understand the results.

**What to say orally**
At the center of the framework are six ideas: contract, target service share, empirical coverage, PrioCovErr, alpha, and lambda_C. A contract is the service unit. The target share says how much training attention it should receive. Empirical coverage measures how much it actually receives. PrioCovErr measures the gap. Alpha controls how strongly the sampler follows policy, and lambda_C controls the additional fairness pressure.

**Emphasis words**
contract; target share; empirical coverage; PrioCovErr; alpha; lambda_C

**Transition to next slide**
The next two slides show how this becomes a concrete benchmark design.

**Shortest interruption-safe answer**
PrioCovErr is the main governance metric because it directly measures policy misalignment.

**Estimated time**
1.60 minutes

## Slide 9. Benchmarks and Data Sources

**Key message**
Make the datasets, modalities, and formal input scope concrete.

**What to say orally**
The thesis uses two benchmark families. The HSI benchmark merges corrected Indian Pines and corrected Salinas after band alignment. The MSI benchmark uses canonical 13-band EuroSAT MSI. Appendix A fixes the formal inputs explicitly, which matters because the current thesis evidence is supposed to come from the formal rerun pipeline rather than from notebook-only historical outputs.

**Emphasis words**
corrected HSI; canonical EuroSAT MSI; formal inputs

**Transition to next slide**
After the data sources, I will explain how the contracts and target shares are actually built.

**Shortest interruption-safe answer**
These are the formal inputs behind the locked thesis evidence chain.

**Estimated time**
1.20 minutes

## Slide 10. Contract Construction and Target-Share Policy

**Key message**
Explain how contracts are realized and how the target policy is assigned.

**What to say orally**
This slide is important because contract construction is part of the scientific design, not just preprocessing. In the current rerun, HSI realizes 44 contracts, EuroSAT coarse uses 4, and EuroSAT fine uses 6. The target share is proportional to priority times contract size. That means the governance target combines human policy intent with available evidence, instead of ignoring either one.

**Emphasis words**
44; 4; 6; priority times contract size

**Transition to next slide**
With the benchmark design fixed, I can now present the main HSI evidence first.

**Shortest interruption-safe answer**
EuroSAT fine is six realized contracts in the locked thesis.

**Estimated time**
1.50 minutes

## Slide 11. Main HSI Benchmark Results

**Key message**
Explain the HSI frontier slowly enough that the committee can see why governance is different from class balancing.

**What to say orally**
On HSI, Random gives strong overall accuracy, but it leaves PrioCovErr high at 23.49. Class-Balanced improves Acc_high, yet it makes PrioCovErr even worse. Uniform-Contract and Contract-Priority can look attractive on Acc_high alone, but they overserve some contracts badly. The OSAG family is different because it reduces policy misalignment sharply while still keeping useful accuracy, and OSAG-FairLoss reaches 91.15 on Acc_high with near-zero PrioCovErr.

**Emphasis words**
HSI; class balancing is not governance; near-zero PrioCovErr

**Transition to next slide**
I will now show that the same governance effect also appears on EuroSAT MSI.

**Shortest interruption-safe answer**
The HSI story is that heuristic balancing can help some utility metrics while still breaking policy alignment.

**Estimated time**
1.80 minutes

## Slide 12. Main EuroSAT MSI Results

**Key message**
Use a second modality to show that the effect is not specific to the HSI benchmark.

**What to say orally**
EuroSAT shows the same governance pattern under a different sensing modality. Random keeps the strongest Acc_all, but its PrioCovErr is still high. Contract-Priority improves high-priority accuracy but distorts policy alignment badly. OSAG and OSAG-FairLoss again push PrioCovErr down to about 0.20 while improving high-priority performance. So the governance argument survives across both HSI and MSI.

**Emphasis words**
EuroSAT MSI; second modality; same governance effect

**Transition to next slide**
To connect the two benchmark slides, I next explain why overall accuracy alone is not enough.

**Shortest interruption-safe answer**
The MSI evidence supports the same governance conclusion under a different contract design.

**Estimated time**
1.80 minutes

## Slide 13. Why Accuracy Alone Is Not Enough

**Key message**
Interpret the trade-off correctly and carefully.

**What to say orally**
This slide is where Table 5.2 matters. The reported deltas are absolute percentage-point differences relative to Random, not relative percentage changes. On both benchmarks, OSAG gives up only about half a point of Acc_all, but it reduces PrioCovErr by about twenty-three points and improves Acc_high. That is why the thesis says average accuracy is important but insufficient.

**Emphasis words**
absolute percentage-point differences; trade-off; policy alignment

**Transition to next slide**
After the main tables, I will show how contract design itself changes governance cost.

**Shortest interruption-safe answer**
These are absolute point differences, not relative percentage changes.

**Estimated time**
1.30 minutes

## Slide 14. Contract-Design Ablation

**Key message**
Show that the contract schema itself changes the cost of governance.

**What to say orally**
The EuroSAT ablation asks a deeper question: does governance cost depend on how contracts are defined? The answer is yes. The fine contract design starts from a lower Random PrioCovErr baseline and retains more accuracy while still reaching near-zero policy error. That supports the thesis claim that contract design is a substantive part of governance, not an arbitrary preprocessing choice.

**Emphasis words**
contract design; governance cost; coarse versus fine

**Transition to next slide**
The next slide asks whether these governance gains come with unreasonable compute or disappear under a stronger backbone.

**Shortest interruption-safe answer**
The key claim is that better contract design makes governance cheaper.

**Estimated time**
1.40 minutes

## Slide 15. Runtime and Backbone Robustness

**Key message**
Address two natural objections: compute cost and backbone dependence.

**What to say orally**
The runtime table should be read as comparable-overhead evidence, not as a speed claim. OSAG is in the same practical runtime range as Random, and the apparently slower Random mean on HSI is driven mainly by one outlier seed. The ResMLP extension is intentionally scoped, but it is still useful because it shows the governance conclusion survives modest backbone strengthening.

**Emphasis words**
comparable overhead; not a speed claim; scoped ResMLP extension

**Transition to next slide**
With the benchmark evidence complete, I now move to the demo branch of the thesis story.

**Shortest interruption-safe answer**
The thesis is not claiming that OSAG is intrinsically faster or that it is a backbone study.

**Estimated time**
1.60 minutes

## Slide 16. Why the Dispatch Demo Is Needed

**Key message**
Explain why the presentation still needs a demo chapter even though the benchmark is the main evidence.

**What to say orally**
The benchmark chapter proves the scientific effect, but it does not naturally show the time-stepped operational behavior of the governance layer. The dispatch demo makes that behavior visible under budgets, deadlines, and missed-service events. In other words, it is an interpretability and communication artifact that complements the benchmark rather than replacing it.

**Emphasis words**
benchmark versus demo; operational complement

**Transition to next slide**
To make that concrete, the next slide defines the demo scenario itself.

**Shortest interruption-safe answer**
The demo is useful because it makes governance behavior visible, not because it replaces real experiments.

**Estimated time**
0.90 minutes

## Slide 17. Dispatch Demo Setup and Scenario

**Key message**
Walk the committee through the simulated operational setting before showing the results.

**What to say orally**
The dispatch demo models a 12 by 12 emergency grid over ten decision steps. It defines six contracts, of which the first three are high-priority and deadline-sensitive. The system has an observation budget of fourteen tiles and an annotation budget of six tiles per step. It compares Random, Contract-Priority, and OSAG, and it tracks five quantities: compliance, coverage error, missed service, Q_high, and reliability.

**Emphasis words**
12 by 12 grid; 10 steps; budgets; six contracts

**Transition to next slide**
With the setup clear, I can now show the end-of-run and timeline results.

**Shortest interruption-safe answer**
The demo is a small operational simulation with explicit budgets and deadlines.

**Estimated time**
1.30 minutes

## Slide 18. Dispatch Demo Results and Interpretation

**Key message**
Use the demo to explain behavior, not to replace the benchmark evidence.

**What to say orally**
In the demo, OSAG reaches the strongest governance-oriented reliability, the best compliance, and the lowest coverage error. Contract-Priority looks better only if the user focuses narrowly on missed service or critical capture. The timeline and contract-gap plots show why: OSAG is more stable in long-run service balance. The sensitivity note also matters here, because it shows the OSAG ranking is robust around the thesis weighting.

**Emphasis words**
reliability; compliance; coverage error; sensitivity note

**Transition to next slide**
After the demo, I will state the claim boundaries directly.

**Shortest interruption-safe answer**
Q_high is separate from K, and reliability is only a summary, not the only metric.

**Estimated time**
1.50 minutes

## Slide 19. Limitations and Claim Boundaries

**Key message**
State the boundaries explicitly so the claim remains defensible.

**What to say orally**
This thesis is careful about its boundaries. The HSI split is pixel-stratified rather than spatial-blocked, so absolute accuracy may be optimistic. The graph is a modeling view rather than a full explicit graph optimizer. The main benchmark uses a lightweight MLP to isolate governance effects, and the ResMLP study is scoped. The demo is supportive evidence, and reproducibility relies on manifests, configs, logs, and stage reports rather than a git commit ledger.

**Emphasis words**
pixel-stratified; graph as modeling view; scoped backbone; supportive demo

**Transition to next slide**
With those boundaries stated, I can summarize the reproducibility story briefly.

**Shortest interruption-safe answer**
The thesis is stronger because its limitations are explicit.

**Estimated time**
1.50 minutes

## Slide 20. Reproducibility and Public Release

**Key message**
Show that the thesis has a real evidence chain rather than a single final PDF.

**What to say orally**
Appendix A matters because it separates fully rerun main benchmark evidence, fully rerun extensions, and artifact-level reproducibility. It also records the formal input data, the contract construction rules, the fresh output locations, and the non-git provenance boundary. Together with the companion public source release, that makes the thesis much easier to inspect and defend.

**Emphasis words**
fully rerun main benchmark; extensions; artifact-level reproducibility

**Transition to next slide**
I will end with three short takeaways and then move to the live demo and questions.

**Shortest interruption-safe answer**
The reproducibility scope is strong at the script and artifact level, with a clear non-git boundary.

**Estimated time**
1.10 minutes

## Slide 21. Final Takeaways and Transition

**Key message**
Land the three claims the committee should remember and transition cleanly to the next defense stage.

**What to say orally**
There are three final takeaways. First, the thesis contribution is governance-aware EO training. Second, OSAG sharply reduces policy misalignment while keeping competitive utility on fresh reruns. Third, the benchmark, the demo slides, and Appendix A together form a complete and auditable defense story. This concludes the slide presentation. After this, I will move to the live demo and then to your questions.

**Emphasis words**
governance-aware EO training; sharp policy alignment gains; complete defense story

**Transition to next slide**
Move directly to the next slide.

**Shortest interruption-safe answer**
If you remember one sentence, it is that EO training is also a service-allocation problem, and OSAG makes that allocation explicit.

**Estimated time**
0.80 minutes
