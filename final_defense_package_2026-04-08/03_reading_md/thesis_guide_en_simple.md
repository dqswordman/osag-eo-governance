# Simple Thesis Guide (English)

## 1. One-sentence thesis summary
This thesis studies how to make Earth Observation training policy-aware by adding a lightweight contract-governance layer that controls who gets served during training.

## 2. Short overall overview
The thesis starts from a simple observation: standard EO training is good at optimizing average predictive quality, but it is not designed to honor service priorities during training. In real remote-sensing settings, that matters. Some regions, semantic groups, or rare cases are more important than others. If training exposure follows data frequency by default, a model can look good overall and still be badly misaligned with the intended service policy.

The thesis answers this by defining contracts, target service shares, empirical coverage, and a policy mismatch metric called PrioCovErr. OSAG is the lightweight layer that turns those ideas into practice. The main evidence comes from fresh reruns on a joint HSI benchmark and on EuroSAT MSI. The thesis then adds a dispatch demo to show the same governance logic in a time-stepped operational setting. Appendix A strengthens the trust story by fixing the formal inputs, contract rules, rerun outputs, and provenance boundary.

## 3. The four research questions
- **RQ1**: How can EO training be reformulated as a service-allocation problem?
- **RQ2**: Can a lightweight governance layer control training exposure?
- **RQ3**: What is the trade-off between governance quality and predictive utility?
- **RQ4**: Can the thesis explain the governance behavior clearly in a runnable artifact?

## 4. Core concepts in plain language
- Contract: the service unit the policy cares about.
- Target service share: how much attention each contract should receive.
- Empirical coverage: how much attention each contract actually receives.
- PrioCovErr: the mismatch between target shares and empirical coverage.
- alpha: how strongly OSAG policy affects the sampler.
- lambda_C: how strongly the fairness-loss extension reacts to hard, high-priority contracts.
- OSAG: the main contract-aware governance layer.
- OSAG-FairLoss: OSAG plus an extra fairness penalty in loss space.
- Dispatch demo: the operational illustration of the same governance logic.
- Q_high: the final high-priority quality state in the demo, separate from K.

## 5. Chapter-by-chapter guide
- Chapter 1 explains why average accuracy is not enough when service priorities matter.
- Chapter 2 defines contracts and benchmark structure.
- Chapter 3 introduces target shares, empirical coverage, PrioCovErr, alpha, and lambda_C.
- Chapter 4 contains the dispatch demo as an operational explanation layer.
- Chapter 5 contains the fresh rerun benchmark, trade-off interpretation, ablation, runtime table, and scoped ResMLP extension.
- Chapter 6 closes the thesis and restates the contribution carefully.
- Appendix A is the trust anchor that fixes formal inputs, contract rules, fresh outputs, and provenance boundary.

## 6. Math intuition without too much density
Ordinary ERM minimizes average loss over samples. That is clean, but it is service-blind. Once the thesis defines a target share for each contract, training can be judged not only by loss and accuracy, but also by whether the exposure policy is being followed. Empirical coverage tells us the observed exposure. PrioCovErr measures the mismatch. Alpha is the control knob for policy strength. Lambda_C is the extra loss-space push for hard, high-priority contracts.

The graph idea should be explained carefully. In this thesis, it mainly contributes a structured modeling view over the contract space. The implementation is not yet a full explicit graph algorithm.

## 7. Experimental design explained simply
The HSI benchmark uses corrected Indian Pines and corrected Salinas because they give a joint hyperspectral setting with imbalance and spatial structure. EuroSAT MSI adds a second modality and supports coarse-versus-fine contract design. The main benchmark uses lightweight MLPs so that the governance effect is easier to isolate. The main tables are fresh five-seed reruns. The EuroSAT contract ablation is a fresh three-seed rerun. The ResMLP extension is a scoped robustness check.

## 8. Figure and table guide
- Figure 1.1: the thesis map. Learn it first.
- Table 2.1: benchmark and contract summary. Remember EuroSAT fine equals 6.
- Table 4.1: dispatch demo summary.
- Figure 4.2: the dispatch timeline and contract-gap behavior.
- Table 5.1: the main fresh rerun benchmark.
- Table 5.2: absolute percentage-point differences, not relative changes.
- Table 5.3: contract-design ablation.
- Table 5.4: runtime, read as comparable overhead.
- Table 5.5: scoped ResMLP extension.

## 9. Dispatch demo explained simply
The demo uses a 12 by 12 emergency grid over ten steps. It defines six contracts and limited budgets. Random is the unconstrained baseline. Contract-Priority is an aggressive heuristic. OSAG tries to stay aligned with service policy across time. The dashboard highlights five quantities: compliance, coverage error, missed service, Q_high, and reliability. Reliability is a summary, not the only metric. The demo adds operational intuition beyond the benchmark tables.

## 10. Novelty and what is inherited
The thesis inherits the conference-paper lineage, but strengthens it with a broader thesis framing, fresh reruns as the main evidence, a dispatch-style demo, and a stronger reproducibility appendix. The novelty is mainly conceptual and methodological in governance-aware EO training, not in backbone invention.

## 11. Likely confusion points
Do not confuse Q_high with K. Do not treat the demo as the main evidence. Do not call Table 5.2 a relative percentage table. Do not say EuroSAT fine has 12 contracts. Do not overstate the graph implementation. Do not overstate runtime. Do not forget the HSI split limitation.

## 12. Limitations and future work
The main limitations are clear. The HSI split is pixel-stratified rather than spatial-blocked. The graph is more explicit conceptually than algorithmically. The backbone scope is limited. Contracts are manually engineered policy units. Reproducibility is strong at the script and artifact level, but the local workspace is not backed by a full git ledger. Natural future work includes explicit graph algorithms, spatial-blocked HSI evaluation, broader backbone studies, and more adaptive contract design.

## 13. Defense preparation summary
The safest defense story is: this thesis is about governance-aware EO training; OSAG is a lightweight layer; the main evidence is the fresh rerun benchmark; the demo is an operational complement; the appendix strengthens trust.

## 14. Fast study route
If only 30 minutes remain, study Figure 1.1, Table 5.1, Table 5.2, Table 5.4, Table 5.5, Table 4.1, and the limitation slide. If only 10 minutes remain, memorize five facts: EuroSAT fine is 6, Table 5.2 is absolute percentage-point differences, the HSI split is pixel-stratified, the graph is a modeling view, and the demo is supportive rather than primary evidence.
