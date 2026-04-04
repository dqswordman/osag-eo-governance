# OSAG English Defense Deck Notes (Final Code-Integrated Version)

- Total estimated main-deck time: 29.50 minutes
- Target time by section:
  - Opening and thesis framing (Slides 1-6): about 6.20 minutes
  - Governance logic and code path (Slides 7-14): about 9.80 minutes
  - Benchmark evidence and extensions (Slides 15-19): about 6.70 minutes
  - Demo, boundaries, and close (Slides 20-25): about 6.80 minutes
- Main-deck timing inside 28-33 minutes: yes
- Live demo time is excluded from this estimate.
- The main deck alone is intended to support the committee presentation before demo and Q&A.

## Slide 1. Title with Advisor Signature

**Key message**
Open formally, show the thesis identity, and keep the printed defense copy signature-ready.

**What to say orally**
Good morning, respected committee members. My thesis is titled 'Governance-Aware Earth Observation Learning: Contract-Governed Training with Observed Service Agreement Graphs.' Today I will present the motivation, the framework, the fresh benchmark evidence, the operational demo logic, and the software path that supports the defense.

**Emphasis words**
governance-aware EO training; advisor signature area; final thesis state

**Transition to next slide**
I will begin with a short roadmap of the talk.

**Shortest interruption-safe answer**
This thesis is about making EO training policy-aware at the contract level.

**Estimated time**
0.80 minutes

## Slide 2. Talk Roadmap

**Key message**
Preview the full argument so the committee knows the talk includes method, evidence, code, and boundaries.

**What to say orally**
I will organize the presentation into five parts. First, the problem and motivation. Second, the OSAG framework and benchmark design. Third, the actual code path behind the framework. Fourth, the fresh rerun evidence and the dispatch demo. Fifth, the limitations, reproducibility scope, and final takeaways. The live demo and code questioning come after the slide presentation.

**Emphasis words**
problem; framework; code; evidence; boundaries

**Transition to next slide**
With that roadmap in place, I will begin with the motivation.

**Shortest interruption-safe answer**
The structure is problem, method, code, evidence, and then boundaries.

**Estimated time**
0.50 minutes

## Slide 3. Background and Motivation

**Key message**
Explain why EO training needs an explicit governance layer rather than only a better accuracy target.

**What to say orally**
Standard EO training is usually accuracy-driven. But many real EO tasks care about whether important regions, categories, or service groups are consistently served during training. That means the hidden allocation of training exposure becomes important. This is the motivation for a governance layer.

**Emphasis words**
accuracy is not enough; who gets served

**Transition to next slide**
That leads directly to the research gap and the thesis questions.

**Shortest interruption-safe answer**
The thesis starts from the fact that training exposure is already a policy choice, even when it is not written down.

**Estimated time**
1.20 minutes

## Slide 4. Research Gap and Guiding Questions

**Key message**
State the gap and the four questions clearly enough that the later slides feel like direct answers.

**What to say orally**
The gap is that ordinary EO training does not represent service allocation explicitly. So the thesis asks four questions: how to formalize service over contracts, whether a lightweight governance layer can control it, what the utility-versus-governance trade-off looks like on HSI and MSI benchmarks, and whether this can be explained through a runnable operational artifact.

**Emphasis words**
service allocation; explicit policy; four questions

**Transition to next slide**
Next, I will summarize the contributions that answer these questions.

**Shortest interruption-safe answer**
The gap is not lack of models. The gap is lack of explicit training-governance control.

**Estimated time**
1.20 minutes

## Slide 5. Thesis Contributions

**Key message**
Separate the thesis contribution into conceptual, methodological, empirical, and artifact layers.

**What to say orally**
The thesis contributes in four ways. Conceptually, it reframes EO training as a governance problem. Methodologically, it introduces OSAG as a lightweight contract-aware layer. Empirically, it provides fresh rerun benchmark evidence, ablation, runtime interpretation, and a scoped backbone extension. Finally, it adds a dispatch demo and a reproducibility appendix that make the work more inspectable and defensible.

**Emphasis words**
conceptual; methodological; empirical; artifact-level

**Transition to next slide**
Now I will use Figure 1.1 as the map for the whole thesis.

**Shortest interruption-safe answer**
The contribution is broader than one sampler trick or one table.

**Estimated time**
1.10 minutes

## Slide 6. Figure 1.1 Method Overview

**Key message**
Use the pipeline figure as the structural map for the whole defense.

**What to say orally**
Figure 1.1 is the thesis map. EO inputs are converted into contracts, policy targets define how much service each contract should receive, the OSAG sampler injects that policy into training exposure, and the coverage monitor checks whether the observed exposure matches the target. The key idea is that OSAG wraps ordinary training rather than replacing the classifier.

**Emphasis words**
contracts; policy targets; sampler; monitor; feedback loop

**Transition to next slide**
To see why the framework is needed, I first explain why standard ERM is service-blind.

**Shortest interruption-safe answer**
This figure is the easiest way to remember the whole thesis.

**Estimated time**
1.40 minutes

## Slide 7. Why Ordinary EO Training Is Service-Blind

**Key message**
Show why the thesis needs a governance formulation instead of just a different sampling heuristic.

**What to say orally**
The ordinary ERM objective optimizes average loss over a flat sample pool. That is mathematically clean, but it does not know which contracts are policy-critical, which ones are rare, or which ones deserve more sustained attention. In EO, that means training exposure follows data density by default. The governance layer makes those service choices explicit instead of accidental.

**Emphasis words**
ERM; flat sample pool; no policy target

**Transition to next slide**
With that intuition in place, I can define the core governance vocabulary.

**Shortest interruption-safe answer**
ERM is service-blind because it has no explicit contract-level policy target.

**Estimated time**
1.40 minutes

## Slide 8. Core Concepts and Control Logic

**Key message**
Teach the audience the minimum vocabulary needed for the results and the code explanation.

**What to say orally**
The key concepts are contract, target service share, empirical coverage, PrioCovErr, alpha, and lambda_C. A contract is the service unit. The target share says how much training exposure it should receive. Empirical coverage says how much it actually receives. PrioCovErr measures the gap. Alpha controls how strongly the sampler follows the policy, and lambda_C controls additional fairness pressure in loss space.

**Emphasis words**
contract; target share; empirical coverage; PrioCovErr; alpha; lambda_C

**Transition to next slide**
The next two slides show how this becomes a concrete benchmark design.

**Shortest interruption-safe answer**
PrioCovErr matters because it turns policy misalignment into a measurable training outcome.

**Estimated time**
1.50 minutes

## Slide 9. Benchmarks and Data Sources

**Key message**
Make the datasets, modalities, and formal input scope concrete.

**What to say orally**
The thesis uses two benchmark families. The HSI benchmark merges corrected Indian Pines and corrected Salinas after band alignment. The MSI benchmark uses canonical 13-band EuroSAT MSI. Appendix A fixes the formal inputs explicitly, which matters because the thesis evidence is supposed to come from the formal rerun pipeline rather than from notebook-only historical outputs.

**Emphasis words**
corrected HSI; canonical EuroSAT MSI; formal inputs

**Transition to next slide**
After the data sources, I will explain how contracts and target shares are built.

**Shortest interruption-safe answer**
These are the formal inputs behind the locked thesis evidence chain.

**Estimated time**
1.10 minutes

## Slide 10. Contract Construction and Target-Share Policy

**Key message**
Explain how contracts are realized and how the target policy is assigned.

**What to say orally**
Contract construction is part of the scientific design, not just preprocessing. In the locked rerun, HSI realizes 44 contracts, EuroSAT coarse uses 4, and EuroSAT fine uses 6. The target share is proportional to priority times contract size. So the governance target combines human policy intent with available evidence rather than ignoring either one.

**Emphasis words**
44; 4; 6; priority times contract size

**Transition to next slide**
With the benchmark design fixed, I can now show how the actual codebase implements the same logic.

**Shortest interruption-safe answer**
EuroSAT fine is six realized contracts in the locked thesis.

**Estimated time**
1.30 minutes

## Slide 11. Repository and Code Architecture

**Key message**
Show the committee where the science lives in code so the software story feels concrete.

**What to say orally**
Before the results, I want to make the code path explicit. The repository has three practical branches. One is the real benchmark rerun pipeline. One is the dispatch-demo pipeline. One is the artifact-generation path for the defense materials. This structure matters because it makes the thesis easier to inspect under live questioning.

**Emphasis words**
real rerun path; demo path; artifact path

**Transition to next slide**
Now I will zoom in on the core functions that implement the contract policy.

**Shortest interruption-safe answer**
The repository is easy to explain if I separate rerun, demo, and artifact paths.

**Estimated time**
1.00 minutes

## Slide 12. Code View: Contracts and Target Service Shares

**Key message**
Connect the mathematical contract policy directly to the actual code.

**What to say orally**
This slide shows the first important implementation bridge. In the rerun pipeline, build_contract_table_from_meta materializes contract IDs, counts, priorities, and target weights. In the dispatch demo, the same idea appears in the fixed contract table with priorities, target weights, and deadlines. So both the benchmark and the demo are driven by explicit contract objects, not by hidden magic.

**Emphasis words**
contract table; target weight; same logic in benchmark and demo

**Transition to next slide**
With the contract table defined, I can now show how OSAG turns it into sampling and monitoring decisions.

**Shortest interruption-safe answer**
The code uses the same policy ingredients that the thesis defines mathematically.

**Estimated time**
1.20 minutes

## Slide 13. Code View: OSAG Sampler, Fairness, and Coverage Monitor

**Key message**
Show the committee the core operational logic without dumping too much code.

**What to say orally**
Here the governance layer becomes action. In the demo, choose_observations combines urgency, deadline pressure, coverage gap, uncertainty, and priority into the OSAG dispatch score. In the benchmark pipeline, the fairness-loss branch adds lambda_C only when high-priority contracts remain harder than low-priority ones. And the coverage monitor computes policy-alignment error from observed contract counts. That is the heart of OSAG in software.

**Emphasis words**
urgency; gap; uncertainty; lambda_C; monitor

**Transition to next slide**
After the core logic, I will show the execution path that I can safely demonstrate live if asked.

**Shortest interruption-safe answer**
The sampler, the fairness branch, and the monitor are the three implementation hooks to remember.

**Estimated time**
1.30 minutes

## Slide 14. Code View: Benchmark and Demo Execution Path

**Key message**
Explain how the committee can move from commands to outputs without getting lost in the repository.

**What to say orally**
The defense-day execution path is intentionally simple. For the benchmark, the clean entry is run_all_real_experiments.py, then reproduce_osag_real.py, then the generated tables and runtime summaries. For the demo, the clean entry is run_visual_demo.py, which delegates to run_dispatch_demo.py and then opens the dashboard. If the committee asks to inspect code, this slide gives the safest file order to open.

**Emphasis words**
entry points; safe file order; outputs

**Transition to next slide**
With the code path clear, I can return to the main evidence from the fresh reruns.

**Shortest interruption-safe answer**
This slide is the defense-day map for code questioning.

**Estimated time**
1.00 minutes

## Slide 15. Main HSI Benchmark Results

**Key message**
Explain the HSI frontier carefully enough that the committee sees why governance differs from class balancing.

**What to say orally**
On HSI, Random gives strong overall accuracy, but it leaves PrioCovErr high at 23.49. Class-Balanced improves high-priority accuracy somewhat, yet makes PrioCovErr worse. Uniform-Contract and Contract-Priority can look attractive on Acc_high alone, but they overserve some contracts badly. The OSAG family is different because it collapses policy misalignment while still keeping useful accuracy, and OSAG-FairLoss pushes Acc_high to 91.15 with near-zero PrioCovErr.

**Emphasis words**
HSI; class balancing is not governance; near-zero PrioCovErr

**Transition to next slide**
I will now show that the same pattern appears on EuroSAT MSI.

**Shortest interruption-safe answer**
The HSI story is that heuristic balancing can help utility while still breaking policy alignment.

**Estimated time**
1.50 minutes

## Slide 16. Main EuroSAT MSI Results

**Key message**
Use a second modality to show that the governance effect is not specific to HSI.

**What to say orally**
EuroSAT shows the same governance pattern under a second sensing modality. Random keeps the strongest Acc_all, but its PrioCovErr is still high at 23.81. Contract-Priority improves Acc_high, yet distorts policy alignment badly. OSAG and OSAG-FairLoss again drive PrioCovErr down to about 0.20 while improving high-priority performance. So the governance argument survives across both HSI and MSI.

**Emphasis words**
EuroSAT MSI; second modality; same governance effect

**Transition to next slide**
To connect these two benchmark slides, I next explain why overall accuracy alone is not enough.

**Shortest interruption-safe answer**
The MSI evidence supports the same conclusion under a different contract design.

**Estimated time**
1.50 minutes

## Slide 17. Why Accuracy Alone Is Not Enough

**Key message**
Interpret the trade-off carefully and mathematically correctly.

**What to say orally**
This is where Table 5.2 matters. The reported deltas are absolute percentage-point differences relative to Random, not relative percentage changes. On both benchmarks, OSAG gives up only about half a point of Acc_all, but reduces PrioCovErr by about twenty-three points and improves Acc_high. That is why the thesis says average accuracy is important but insufficient.

**Emphasis words**
absolute percentage-point differences; trade-off; policy alignment

**Transition to next slide**
After the main tables, I will show how contract design changes governance cost.

**Shortest interruption-safe answer**
These are absolute point differences, not relative percentage changes.

**Estimated time**
1.20 minutes

## Slide 18. Contract-Design Ablation

**Key message**
Show that contract design itself changes the cost of governance.

**What to say orally**
The EuroSAT ablation asks whether governance cost depends on how contracts are defined. The answer is yes. The fine contract design starts from a lower Random PrioCovErr baseline and retains more accuracy while still reaching near-zero policy error. That supports the claim that contract design is a substantive part of governance, not an arbitrary preprocessing choice.

**Emphasis words**
contract design; governance cost; coarse versus fine

**Transition to next slide**
The next slide addresses compute cost and modest backbone strengthening.

**Shortest interruption-safe answer**
The key claim is that better contract design can make governance cheaper.

**Estimated time**
1.20 minutes

## Slide 19. Runtime and Backbone Robustness

**Key message**
Address compute cost and backbone dependence honestly.

**What to say orally**
The runtime table should be read as comparable-overhead evidence, not as a speed claim. OSAG is in the same practical runtime range as Random, and the apparently slower Random mean on HSI is driven mainly by one outlier seed. The ResMLP extension is intentionally scoped, but it is still useful because the governance conclusion survives modest backbone strengthening.

**Emphasis words**
comparable overhead; not a speed claim; scoped ResMLP extension

**Transition to next slide**
With the benchmark evidence complete, I now move to the dispatch-demo branch of the thesis story.

**Shortest interruption-safe answer**
The thesis is not claiming that OSAG is intrinsically faster or that it is a backbone study.

**Estimated time**
1.30 minutes

## Slide 20. Why the Dispatch Demo Is Needed

**Key message**
Explain why the defense still includes a demo even though the benchmark is the main evidence.

**What to say orally**
The benchmark chapter proves the scientific effect, but it does not naturally show the time-stepped operational behavior of the governance layer. The dispatch demo makes that behavior visible under budgets, deadlines, and missed-service events. So it is an interpretability and communication artifact that complements the benchmark rather than replacing it.

**Emphasis words**
benchmark versus demo; operational complement

**Transition to next slide**
To make that concrete, the next slide defines the demo scenario.

**Shortest interruption-safe answer**
The demo is useful because it makes governance behavior visible.

**Estimated time**
0.90 minutes

## Slide 21. Dispatch Demo Setup and Scenario

**Key message**
Walk the committee through the simulated operational setting before showing the result.

**What to say orally**
The dispatch demo models a 12 by 12 emergency grid over ten decision steps. It defines six contracts, of which the first three are high-priority and deadline-sensitive. The system has an observation budget of fourteen tiles and an annotation budget of six tiles per step. It compares Random, Contract-Priority, and OSAG, and it tracks five quantities: compliance, coverage error, missed service, Q_high, and reliability.

**Emphasis words**
12 by 12 grid; 10 steps; budgets; six contracts

**Transition to next slide**
With the setup clear, I can now show the end-of-run and timeline results.

**Shortest interruption-safe answer**
The demo is a small operational simulation with explicit budgets and deadlines.

**Estimated time**
1.20 minutes

## Slide 22. Dispatch Demo Results and Interpretation

**Key message**
Use the demo to explain behavior, not to replace the benchmark evidence.

**What to say orally**
In the demo, OSAG reaches the strongest governance-oriented reliability, the best compliance, and the lowest coverage error. Contract-Priority looks better only if the user focuses narrowly on missed service or critical capture. The timeline and contract-gap plots show why: OSAG is more stable in long-run service balance. The sensitivity note matters because it shows the OSAG ranking remains top around the thesis weighting.

**Emphasis words**
reliability; compliance; coverage error; sensitivity

**Transition to next slide**
After the demo, I will state the claim boundaries directly.

**Shortest interruption-safe answer**
Q_high is separate from K, and reliability is only a summary, not the only metric.

**Estimated time**
1.40 minutes

## Slide 23. Limitations and Claim Boundaries

**Key message**
State the boundaries explicitly so the claim remains defensible.

**What to say orally**
This thesis is careful about its boundaries. The HSI split is pixel-stratified rather than spatial-blocked, so absolute accuracy may be optimistic. The graph is a modeling view rather than a full explicit graph optimizer. The main benchmark uses a lightweight MLP to isolate governance effects, and the ResMLP study is scoped. The demo is supportive evidence, and reproducibility relies on scripts, manifests, logs, configs, and stage reports rather than a git commit ledger.

**Emphasis words**
pixel-stratified; graph as modeling view; scoped backbone; supportive demo

**Transition to next slide**
With those boundaries stated, I can summarize the reproducibility story.

**Shortest interruption-safe answer**
The thesis is stronger because its limitations are explicit.

**Estimated time**
1.40 minutes

## Slide 24. Reproducibility and Public Release

**Key message**
Show that the thesis has a real evidence chain rather than just a final PDF.

**What to say orally**
Appendix A matters because it separates fully rerun main benchmark evidence, fully rerun extensions, and artifact-level reproducibility. It records the formal input data, the contract construction rules, the fresh output locations, and the non-git provenance boundary. Together with the public source release, that makes the thesis easier to inspect and defend.

**Emphasis words**
fully rerun main benchmark; extensions; artifact-level reproducibility

**Transition to next slide**
I will end with three short takeaways and then move to the live demo and your questions.

**Shortest interruption-safe answer**
The reproducibility scope is strong at the script and artifact level, with a clear non-git boundary.

**Estimated time**
1.00 minutes

## Slide 25. Final Takeaways and Transition

**Key message**
Land the three claims the committee should remember and transition cleanly to the live part.

**What to say orally**
There are three final takeaways. First, the thesis contribution is governance-aware EO training. Second, OSAG sharply reduces policy misalignment while keeping competitive utility on fresh reruns. Third, the benchmark, the code path, the dispatch demo, and Appendix A together form a complete and auditable defense story. This concludes the slide presentation. After this, I will move to the live demo and then to your questions.

**Emphasis words**
governance-aware training; alignment gains; auditable defense story

**Transition to next slide**
Move directly to the next slide.

**Shortest interruption-safe answer**
If you remember one sentence, it is that EO training is also a service-allocation problem, and OSAG makes that allocation explicit.

**Estimated time**
0.90 minutes
