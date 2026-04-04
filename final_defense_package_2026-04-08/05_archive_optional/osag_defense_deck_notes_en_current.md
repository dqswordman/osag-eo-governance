# OSAG Current English Defense Deck Notes

- Total estimated main-deck time: 17.30 minutes
- Section timing:
  - Opening and framing (Slides 1-4): about 2.90 minutes
  - Framework and benchmark design (Slides 5-7): about 3.50 minutes
  - Main evidence and extensions (Slides 8-11): about 4.90 minutes
  - Demo and code orientation (Slides 12-14): about 3.00 minutes
  - Boundaries and close (Slides 15-17): about 2.95 minutes
- Main-deck timing inside 15-20 minutes: yes
- Live demo time is excluded from this estimate.

## Slide 1. Title

**Key message**
Open formally and state the thesis theme in one sentence.

**What to say orally**
Good morning. My thesis is titled 'Governance-Aware Earth Observation Learning: Contract-Governed Training with Observed Service Agreement Graphs.' This work studies how to make EO training policy-aware at the contract level instead of optimizing only average accuracy.

**Emphasis words**
governance-aware EO training; contract-level service

**Transition**
I will begin with a short roadmap of the talk.

**Interruption-safe answer**
The thesis is about explicit service allocation during EO training.

**Estimated time**
0.45 minutes

## Slide 2. Talk Roadmap

**Key message**
Give the committee a short map so the talk feels easy to follow.

**What to say orally**
I will organize the talk into four parts: the problem and motivation, the OSAG framework and benchmark design, the results and robustness checks, and finally the demo, code orientation, and claim boundaries.

**Emphasis words**
roadmap; problem; framework; evidence; boundaries

**Transition**
With that structure in place, I can begin with the motivation.

**Interruption-safe answer**
The roadmap is problem, method, evidence, and then demo plus boundaries.

**Estimated time**
0.35 minutes

## Slide 3. Background and Motivation

**Key message**
Explain why average accuracy alone is not enough in policy-facing EO tasks.

**What to say orally**
Standard EO training is usually accuracy-driven. But real deployments also care about which regions, classes, or service groups are being served during training. That is why the thesis adds a governance layer on top of ordinary EO learning.

**Emphasis words**
accuracy is not enough; who is served

**Transition**
That motivation leads directly to the research gap.

**Interruption-safe answer**
The short answer is that the thesis makes hidden training allocation explicit.

**Estimated time**
1.10 minutes

## Slide 4. Research Gap and Questions

**Key message**
Move from motivation to the explicit research questions.

**What to say orally**
The central gap is that standard EO training does not represent service allocation explicitly. So the thesis asks how to formalize contracts, whether a lightweight governance layer can control exposure, what trade-offs appear on HSI and MSI benchmarks, and whether the idea can be communicated through a runnable defense artifact.

**Emphasis words**
research gap; explicit control; runnable artifact

**Transition**
Next, I will summarize the contributions that answer these questions.

**Interruption-safe answer**
The gap is lack of explicit policy control over training exposure.

**Estimated time**
1.00 minutes

## Slide 5. Figure 1.1 Method Overview

**Key message**
Use the final thesis pipeline figure as the map for the whole defense.

**What to say orally**
Figure 1.1 is the thesis map. EO inputs become contracts, policy targets define intended service shares, the OSAG sampler injects that policy into training exposure, and the coverage monitor checks compliance. The key point is that OSAG wraps an ordinary classifier rather than replacing it.

**Emphasis words**
contracts; target shares; sampler; monitor; feedback loop

**Transition**
To make the framework concrete, I will define the core terms next.

**Interruption-safe answer**
OSAG is a governance loop around training, not a new backbone family.

**Estimated time**
1.25 minutes

## Slide 6. Core Concepts

**Key message**
Teach the minimum vocabulary needed for the results.

**What to say orally**
A contract is the service unit. The target service share says how much training attention it should receive. Empirical coverage says how much it actually receives. PrioCovErr measures the gap. Alpha controls how strongly sampling follows the policy, and lambda_C adds extra fairness pressure in loss space.

**Emphasis words**
contract; target share; empirical coverage; PrioCovErr; alpha; lambda_C

**Transition**
Now I can show how the benchmarks instantiate those concepts.

**Interruption-safe answer**
PrioCovErr is the main governance metric because it measures policy misalignment directly.

**Estimated time**
1.20 minutes

## Slide 7. Benchmark and Contract Design

**Key message**
Make the datasets and realized contract counts explicit.

**What to say orally**
The locked thesis uses corrected Indian Pines plus corrected Salinas for HSI and canonical EuroSAT MSI for multispectral data. The HSI setting realizes 44 contracts. EuroSAT uses 4 coarse contracts or 6 fine contracts. Target share is proportional to priority times contract size, so the policy mixes human priority with available evidence.

**Emphasis words**
Indian Pines; Salinas; EuroSAT MSI; 44; 4; 6

**Transition**
With the benchmark design fixed, I can now show the fresh rerun evidence.

**Interruption-safe answer**
EuroSAT fine is six realized contracts in the locked thesis.

**Estimated time**
1.05 minutes

## Slide 8. Main HSI Benchmark Results

**Key message**
Show the governance effect clearly on HSI.

**What to say orally**
On HSI, Random keeps strong overall accuracy, but it leaves PrioCovErr high at 23.49. Class-Balanced helps some utility metrics but still makes policy alignment worse. The OSAG family is different because it pushes PrioCovErr toward zero while keeping useful accuracy, and OSAG-FairLoss reaches 91.15 on Acc_high with near-zero PrioCovErr.

**Emphasis words**
HSI; near-zero PrioCovErr; not just class balancing

**Transition**
The same governance pattern appears again on EuroSAT MSI.

**Interruption-safe answer**
The HSI result is about policy alignment with useful utility, not about winning every metric at once.

**Estimated time**
1.35 minutes

## Slide 9. Main EuroSAT MSI Results

**Key message**
Use a second modality to show the governance effect is not HSI-only.

**What to say orally**
EuroSAT shows the same pattern under a second sensing modality. Random keeps the strongest Acc_all, but its PrioCovErr is still high at 23.81. OSAG and OSAG-FairLoss again reduce policy error to about 0.20 while improving high-priority performance. So the governance claim is not tied to one dataset or one sensing modality.

**Emphasis words**
EuroSAT MSI; second modality; same governance effect

**Transition**
That leads to the next question: why is overall accuracy alone not enough?

**Interruption-safe answer**
The MSI benchmark supports the same governance conclusion under a different contract design.

**Estimated time**
1.35 minutes

## Slide 10. Why Accuracy Alone Is Not Enough

**Key message**
Interpret the trade-off and describe Table 5.2 correctly.

**What to say orally**
The trade-off figure shows why overall accuracy is insufficient. Table 5.2 reports absolute percentage-point differences relative to Random, not relative percentage changes. On both benchmarks, OSAG gives up only about half a point of Acc_all, but reduces PrioCovErr by about twenty-three points and improves Acc_high.

**Emphasis words**
absolute percentage-point differences; trade-off; policy alignment

**Transition**
Next I will show what happens when contract design and compute scope change.

**Interruption-safe answer**
These are absolute point differences, not relative percentage changes.

**Estimated time**
1.05 minutes

## Slide 11. Contract Design, Runtime, and Robustness

**Key message**
Handle the three main extension checks honestly.

**What to say orally**
There are three extension checks. First, the EuroSAT ablation shows that finer contracts reduce governance cost. Second, runtime stays in a comparable practical range; the thesis does not claim that OSAG is intrinsically faster. Third, the scoped ResMLP extension shows the governance conclusion survives modest backbone strengthening.

**Emphasis words**
ablation; comparable runtime; scoped ResMLP extension

**Transition**
After the benchmark evidence, I move to the demo branch of the thesis.

**Interruption-safe answer**
The runtime result is comparable-overhead evidence, not a speed claim.

**Estimated time**
1.20 minutes

## Slide 12. Why the Demo Matters

**Key message**
Explain why the thesis still includes a demo after the benchmark.

**What to say orally**
The benchmark chapter is the scientific evidence chain, but it does not naturally show time-stepped operational behavior. The dispatch demo turns the same governance idea into an emergency scheduling system with budgets, deadlines, and missed-service events. It is therefore a communication and interpretability artifact, not a replacement for the benchmark.

**Emphasis words**
benchmark versus demo; operational behavior

**Transition**
With that role clear, I can now show the demo outputs.

**Interruption-safe answer**
The demo is a supportive operational complement, not the main evidence.

**Estimated time**
0.85 minutes

## Slide 13. Dispatch Demo Results

**Key message**
Use the demo to show behavior, not to replace the benchmark.

**What to say orally**
In the demo, OSAG reaches the strongest governance-oriented reliability, the best compliance, and the lowest coverage error. Contract-Priority looks attractive only if one over-focuses on missed service alone. The sensitivity audit from saved outputs keeps OSAG top-ranked around the thesis weighting, so the conclusion is stable near the chosen weights.

**Emphasis words**
reliability; compliance; coverage error; missed service; sensitivity

**Transition**
Before closing, I want to show where the committee can inspect the code safely.

**Interruption-safe answer**
Q_high is not the same as K, and reliability is only a summary score.

**Estimated time**
1.20 minutes

## Slide 14. Repository and Code Architecture

**Key message**
Orient the committee to the repository without dumping raw code.

**What to say orally**
If the committee asks to inspect the implementation, this is the safe map. The formal benchmark path starts from run_all_real_experiments.py and moves into reproduce_osag_real.py. The dispatch path starts from run_visual_demo.py and moves into run_dispatch_demo.py and dispatch_demo_core.py. The live code discussion should focus on build_contract_table_from_meta, compute_coverage_errors, and choose_observations.

**Emphasis words**
benchmark path; demo path; build_contract_table_from_meta; choose_observations

**Transition**
With the code path clear, I can now state the limitations directly.

**Interruption-safe answer**
The committee usually needs a safe code path, not a large raw code dump.

**Estimated time**
0.95 minutes

## Slide 15. Limitations and Boundaries

**Key message**
State the boundaries explicitly so the claims stay credible.

**What to say orally**
The HSI split is pixel-stratified rather than spatial-blocked, so absolute accuracy may be optimistic. The graph is a modeling view rather than a full explicit graph optimizer. The main benchmark uses a lightweight MLP to isolate governance effects, and the ResMLP study is scoped. The demo is supportive evidence, and reproducibility relies on scripts, manifests, logs, configs, and stage reports rather than a git commit ledger.

**Emphasis words**
pixel-stratified; graph as modeling view; lightweight MLP; scoped extension; non-git provenance

**Transition**
With the boundaries stated, I can summarize the reproducibility story.

**Interruption-safe answer**
The thesis is stronger because its limitations are explicit and bounded.

**Estimated time**
1.25 minutes

## Slide 16. Reproducibility and Public Release

**Key message**
Summarize the evidence chain and the public companion release.

**What to say orally**
Appendix A separates fully rerun main benchmark evidence, rerun extensions, and artifact-level reproducibility. It fixes the formal inputs, contract construction rules, and fresh output locations. Together with the companion public repository, this makes the defense evidence much easier to inspect.

**Emphasis words**
fully rerun main benchmark; rerun extensions; artifact-level reproducibility

**Transition**
I will end with three concise takeaways.

**Interruption-safe answer**
The reproducibility claim is strong at the script and artifact level, with a clear non-git boundary.

**Estimated time**
0.95 minutes

## Slide 17. Final Takeaways

**Key message**
Land the three claims the committee should remember.

**What to say orally**
There are three takeaways. First, the thesis contribution is governance-aware EO training. Second, OSAG sharply reduces policy misalignment on the current benchmarks while staying competitive in utility. Third, the benchmark, demo, code path, and Appendix A together form a complete and defensible defense package. Thank you. I am ready to move to live demo and questions.

**Emphasis words**
governance-aware training; policy alignment; complete defense story

**Transition**
I am ready for your questions and the live demo.

**Interruption-safe answer**
The short answer is that OSAG makes training service allocation explicit and measurable.

**Estimated time**
0.75 minutes
