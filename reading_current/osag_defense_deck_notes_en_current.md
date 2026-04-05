# OSAG English Defense Deck Notes (Final Clean Version)

- Total estimated speaking time: 16.20 minutes
- Target duration inside 15-20 minutes: yes
- Slide count: 16
- Style goal: simple spoken English with one clear message per slide

## Slide 1. Title

**Key message**
Open formally with the thesis title and a calm first visual impression.

**What to say orally**
Good morning. My thesis is titled 'Governance-Aware Earth Observation Learning: Contract-Governed Training with Observed Service Agreement Graphs.' This work studies how to make EO training policy-aware at the contract level instead of optimizing only average accuracy.

**Emphasis words**
governance-aware EO training; contract-level service

**Transition**
I will begin with the motivation and the core research gap.

**Shortest interruption-safe answer**
The thesis is about explicit service allocation during EO training.

**Estimated time**
0.50 minutes

## Slide 2. Background and Motivation

**Key message**
Explain why average accuracy is not sufficient in policy-facing EO settings.

**What to say orally**
Earth observation has become a service infrastructure problem. In practice, users care not only about average accuracy, but also about which regions, classes, and semantic groups receive attention during training. That is why the thesis adds a governance layer on top of ordinary EO learning.

**Emphasis words**
accuracy is not enough; who is served

**Transition**
That motivation leads directly to the research gap and the thesis questions.

**Shortest interruption-safe answer**
The short answer is that the thesis makes hidden training allocation explicit.

**Estimated time**
1.05 minutes

## Slide 3. Research Gap and Questions

**Key message**
Move from motivation to the explicit questions that organize the thesis.

**What to say orally**
The central gap is that standard EO training does not represent service allocation explicitly. So the thesis asks how to formalize contracts, whether a lightweight governance layer can control exposure, what trade-offs appear on HSI and MSI benchmarks, and whether the same idea can be explained through a runnable defense artifact.

**Emphasis words**
research gap; explicit control; runnable artifact

**Transition**
Next, I will summarize the thesis contributions that answer those questions.

**Shortest interruption-safe answer**
The gap is lack of explicit policy control over training exposure.

**Estimated time**
1.00 minutes

## Slide 4. Thesis Contributions

**Key message**
Summarize the contribution layers without overstating novelty.

**What to say orally**
The thesis contributes conceptually, technically, empirically, and at the defense-artifact level. It reframes EO training as a governance problem, develops OSAG as a lightweight control layer, validates it through fresh reruns and scoped extensions, and packages the idea into a runnable defense artifact.

**Emphasis words**
conceptual; technical; empirical; artifact

**Transition**
With the contribution scope clear, I can now use Figure 1.1 as the map of the whole thesis.

**Shortest interruption-safe answer**
The novelty is mainly in the governance framing and control layer, not in a new backbone family.

**Estimated time**
0.95 minutes

## Slide 5. Figure 1.1 Method Overview

**Key message**
Use the thesis pipeline figure as the structural map for the defense.

**What to say orally**
Figure 1.1 is the high-level thesis map. EO inputs become contracts, policy targets specify intended service shares, the OSAG sampler injects that policy into training exposure, and the coverage monitor checks compliance. The key point is that OSAG wraps ordinary training rather than replacing the classifier backbone.

**Emphasis words**
contracts; target shares; sampler; monitor; feedback loop

**Transition**
To make that pipeline concrete, I will define the core terms next.

**Shortest interruption-safe answer**
OSAG is a governance loop around training, not a new backbone family.

**Estimated time**
1.20 minutes

## Slide 6. Core Concepts

**Key message**
Teach the minimum vocabulary needed for the results.

**What to say orally**
A contract is the service unit. The target service share says how much training attention it should receive. Empirical coverage says how much it actually receives. PrioCovErr measures the gap. Alpha controls how strongly the sampler follows the policy, and lambda_C adds extra fairness pressure in loss space.

**Emphasis words**
contract; target share; empirical coverage; PrioCovErr; alpha; lambda_C

**Transition**
Now I can show how the real benchmarks instantiate those concepts.

**Shortest interruption-safe answer**
PrioCovErr is the main governance metric because it measures policy misalignment directly.

**Estimated time**
1.10 minutes

## Slide 7. Benchmarks and Contract Design

**Key message**
Make the datasets, contract schemas, and target-share rule explicit.

**What to say orally**
The locked thesis uses corrected Indian Pines plus corrected Salinas for HSI and canonical EuroSAT MSI for multispectral data. The HSI setting realizes 44 contracts. EuroSAT uses 4 coarse contracts or 6 fine contracts. Target share is proportional to priority times contract size, so the policy mixes human priority with available evidence.

**Emphasis words**
Indian Pines; Salinas; EuroSAT MSI; 44; 4; 6

**Transition**
With the benchmark design fixed, I can now show the main fresh rerun evidence.

**Shortest interruption-safe answer**
EuroSAT fine is six realized contracts in the locked thesis.

**Estimated time**
1.10 minutes

## Slide 8. Main Benchmark Results

**Key message**
Show the governance effect clearly across both modalities.

**What to say orally**
Across both HSI and EuroSAT MSI, the OSAG family drives PrioCovErr close to zero while keeping useful overall accuracy and improving high-priority performance. The thesis claim is not that OSAG wins every metric at once. The claim is that it produces governance-faithful operating points with competitive utility.

**Emphasis words**
near-zero PrioCovErr; competitive utility; cross-modality pattern

**Transition**
The next slide explains why overall accuracy alone is not enough to tell this story.

**Shortest interruption-safe answer**
The main message is strong policy alignment with useful predictive performance.

**Estimated time**
1.55 minutes

## Slide 9. Why Accuracy Alone Is Not Enough

**Key message**
Interpret the trade-off and use the correct wording for the delta table.

**What to say orally**
The trade-off figure shows why overall accuracy is not enough. Table 5.2 reports absolute percentage-point differences relative to Random, not relative percentage changes. On both benchmarks, OSAG gives up only about half a point of Acc_all, but reduces PrioCovErr by about twenty-three points and improves Acc_high.

**Emphasis words**
absolute percentage-point differences; trade-off; policy alignment

**Transition**
Next I will show what happens when contract design, compute scope, and backbone strength change.

**Shortest interruption-safe answer**
These are absolute point differences, not relative percentage changes.

**Estimated time**
1.05 minutes

## Slide 10. Contract Design, Runtime, and Robustness

**Key message**
Handle the three main extension checks honestly and compactly.

**What to say orally**
There are three extension checks. First, the EuroSAT ablation shows that finer contracts reduce governance cost. Second, runtime stays in a comparable practical range; the thesis does not claim that OSAG is intrinsically faster. Third, the scoped ResMLP extension shows that the governance conclusion survives modest backbone strengthening.

**Emphasis words**
ablation; comparable runtime; scoped ResMLP extension

**Transition**
After the benchmark evidence, I move to the demo branch of the thesis.

**Shortest interruption-safe answer**
The runtime result is comparable-overhead evidence, not a speed claim.

**Estimated time**
1.20 minutes

## Slide 11. Why the Demo Matters

**Key message**
Explain why the thesis still includes a demo after the benchmark chapter.

**What to say orally**
The benchmark chapter is the scientific evidence chain, but it does not naturally show time-stepped operational behavior. The dispatch demo turns the same governance idea into an emergency scheduling system with budgets, deadlines, missed service, and contract gaps. It is therefore a communication and interpretability artifact, not a replacement for the benchmark.

**Emphasis words**
benchmark versus demo; operational behavior

**Transition**
With that role clear, I can now show the engineered demo view used on defense day.

**Shortest interruption-safe answer**
The demo is a supportive operational complement, not the main evidence.

**Estimated time**
0.85 minutes

## Slide 12. Engineered Demo View

**Key message**
Show one strong defense-day demo view instead of turning the deck into a software manual.

**What to say orally**
This engineered demo view keeps the story readable in a live room. It leads with the primary KPIs, gives one side-by-side policy comparison, and keeps deeper evidence and code mapping available only when needed. The benchmark remains the formal evidence layer, and the engineered demo becomes the explanation layer.

**Emphasis words**
guided view; primary KPIs; offline support

**Transition**
After the demo view, I will show the repository and implementation path behind the thesis.

**Shortest interruption-safe answer**
This support package makes the same governance logic easier to present under live questioning.

**Estimated time**
1.00 minutes

## Slide 13. Code Architecture and Implementation Path

**Key message**
Orient the committee to the repository without dumping large raw code blocks.

**What to say orally**
The repository has three practical branches. One is the formal benchmark rerun path. One is the dispatch demo path. One is the defense-asset path that turns saved outputs into presentation materials. If the committee asks to inspect code, the safe route is entry script first, then contract and coverage logic, then the demo decision function.

**Emphasis words**
benchmark path; demo path; safe live inspection order

**Transition**
With the implementation path clear, I can state the claim boundaries directly.

**Shortest interruption-safe answer**
The committee usually needs a safe code path, not a large raw code dump.

**Estimated time**
0.95 minutes

## Slide 14. Limitations and Claim Boundaries

**Key message**
State the boundaries explicitly so the thesis sounds stronger, not weaker.

**What to say orally**
The HSI split is pixel-stratified rather than spatially blocked. The graph is a modeling and control view rather than a full explicit graph optimizer. The main benchmark uses a lightweight MLP to isolate governance effects. The reproducibility boundary is artifact-driven rather than an internal git ledger. These limits are stated directly so the main claim stays credible.

**Emphasis words**
pixel-stratified; graph as modeling view; lightweight MLP; reproducibility boundary

**Transition**
With those boundaries stated, I can summarize the reproducibility story and public release.

**Shortest interruption-safe answer**
The thesis is stronger because its limitations are explicit and bounded.

**Estimated time**
1.20 minutes

## Slide 15. Reproducibility and Public Release

**Key message**
Summarize the evidence chain, fresh outputs, and the companion public release.

**What to say orally**
Appendix A separates fully rerun main-benchmark evidence, fully rerun extension evidence, and artifact-level reproducibility. It also fixes the formal inputs, output locations, and environment used. Together with the companion public repository, this makes the thesis easier to inspect and reproduce.

**Emphasis words**
fully rerun main evidence; extension evidence; artifact-level reproducibility

**Transition**
I will close with three final takeaways.

**Shortest interruption-safe answer**
The reproducibility claim is strong at the script and artifact level, with a clear non-git boundary.

**Estimated time**
0.90 minutes

## Slide 16. Final Takeaways and Q&A

**Key message**
Land the three claims the committee should remember and invite questions.

**What to say orally**
There are three final takeaways. First, EO training is also a service-allocation problem. Second, OSAG sharply reduces policy misalignment on the current benchmarks while keeping useful utility. Third, the fresh reruns, demo support, implementation path, limitations, and Appendix A together make the thesis inspectable and defensible. Thank you. I welcome your questions.

**Emphasis words**
service-allocation problem; sharp policy-alignment gain; complete defense story

**Transition**
I am ready for questions.

**Shortest interruption-safe answer**
If you remember one sentence: OSAG makes training service allocation explicit and measurable.

**Estimated time**
0.60 minutes
