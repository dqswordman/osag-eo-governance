# Simple Defense FAQ (English)

## 1. How to use this FAQ
Start with the short answer. If the committee asks for more detail, continue with the longer answer. Keep the limitation statements, because they increase credibility.

## 2. Top 10 most likely questions
1. **What is this thesis about?** Short: It is about making EO training policy-aware, not only accuracy-aware. Longer: The thesis asks whether important contracts are really being served during training, and OSAG is the lightweight governance layer used to control that service exposure.
2. **What is OSAG in one sentence?** Short: OSAG is a contract-aware governance layer that steers training exposure toward a target service policy. Longer: It wraps ordinary training with contract construction, target shares, policy-aware sampling, and coverage monitoring.
3. **Why is overall accuracy not enough?** Short: A model can score well overall while still underserving the contracts that matter most. Longer: Large or frequent groups can dominate training by default, so the thesis measures both utility and policy alignment.
4. **What is a contract?** Short: A contract is the service unit the policy cares about. Longer: It can include dataset identity, spatial cell, semantic group, or rarity flag.
5. **What is the main evidence?** Short: The main evidence is the fresh rerun benchmark, not the demo. Longer: The main tables come from fresh reruns on corrected Indian Pines plus Salinas and on EuroSAT MSI.
6. **What is the main empirical result?** Short: OSAG sharply reduces PrioCovErr while keeping competitive accuracy. Longer: On both HSI and EuroSAT MSI, Random leaves PrioCovErr around twenty-four points, while OSAG drives it near zero.
7. **Why is EuroSAT fine equal to 6?** Short: Because the locked rerun pipeline realizes six fine contracts for EuroSAT. Longer: In the final thesis, the fine design yields six realized contracts, not twelve.
8. **Why is there a demo?** Short: Because the demo shows time-stepped behavior that tables do not show clearly. Longer: The benchmark proves the scientific effect, while the demo shows budgets, deadlines, missed service, and stability over time.
9. **Is this a new backbone method?** Short: No. It is a governance layer around ordinary EO training. Longer: The thesis uses lightweight MLPs on purpose and adds only a small ResMLP robustness extension.
10. **How reproducible is the thesis?** Short: It is strongly reproducible at the script and artifact level, with a clear non-git boundary. Longer: Appendix A fixes the formal inputs, contract construction, fresh output paths, and artifact-generation scope.

## 3. Concept questions
- **What problem is the thesis solving?** Short: hidden service allocation during EO training. Longer: Standard learning tells us how well the model predicts, but not whether the right contracts were served in the right proportion.
- **What is target service share?** Short: the intended fraction of training exposure for each contract. Longer: It is proportional to contract priority times contract size.
- **What is empirical coverage?** Short: the fraction of observed training attention each contract actually gets. Longer: It lets us check whether the real training process follows the intended policy.
- **What is PrioCovErr?** Short: the contract-level policy mismatch score. Longer: It measures the L1 gap between target shares and empirical coverage.
- **What does governance mean here?** Short: controlling who gets served during training. Longer: It means making training exposure auditable, measurable, and steerable.
- **Why is EO a good setting?** Short: because EO often has rare, spatially uneven, and policy-critical strata. Longer: Some regions matter much more than their raw sample count suggests.

## 4. Method questions
- **What exactly is OSAG?** Short: a contract-aware sampling and monitoring framework. Longer: It combines contract construction, target shares, policy-aware sampling, and coverage monitoring.
- **Why is it called a graph?** Short: because the thesis models structured relations over the contract space. Longer: The graph idea is conceptual in the current implementation, not a full explicit graph optimizer.
- **Is OSAG mainly sampling or optimization?** Short: mainly a governance-aware sampling layer. Longer: The fairness-loss extension adds an optimization component, but the main benchmark is still driven by sampling and coverage tracking.
- **What does alpha do?** Short: it controls how strongly the sampler follows OSAG policy. Longer: Higher alpha means stronger governance control.
- **What does lambda_C do?** Short: it controls the strength of the fairness-loss term. Longer: It adds pressure when hard, high-priority contracts remain under-served in loss space.
- **Why can Uniform-Contract look good but still be weaker?** Short: because it can improve some utility metrics while still missing the intended policy target. Longer: Uniform treatment of contracts is not the same as policy-correct treatment.

## 5. Experiment questions
- **Why Indian Pines plus Salinas?** Short: they give a joint corrected HSI benchmark with imbalance and spatial structure. Longer: The merged benchmark makes contract-level service questions visible.
- **Why EuroSAT MSI?** Short: it adds a second modality and supports contract-design ablation. Longer: It tests the same governance idea beyond HSI and compares coarse versus fine contracts.
- **Why use a lightweight MLP?** Short: to isolate the governance effect cleanly. Longer: The thesis wants to show that the governance layer itself matters.
- **Why five seeds for the main benchmark?** Short: because the main benchmark is the primary evidence chain. Longer: Five seeds give a more reliable estimate for the central tables.
- **What does the main result table mean?** Short: it shows the trade-off between utility and policy alignment. Longer: Acc_all and Acc_high measure utility, while PrioCovErr measures governance quality.
- **Why does Random sometimes have the best Acc_all?** Short: because the baseline is optimized for average accuracy, not policy alignment. Longer: This can happen together with poor service allocation.
- **Is the HSI split leakage-free?** Short: no. Longer: The HSI split is pixel-stratified, not spatial-blocked, so neighboring pixels can cross splits.
- **How should runtime be interpreted?** Short: as comparable-overhead evidence, not a speed claim. Longer: The runtime table shows that OSAG stays in the same practical range as Random.

## 6. Demo questions
- **Why only Random, Contract-Priority, and OSAG in the dashboard?** Short: to keep the dashboard readable while showing the most informative behaviors. Longer: That trio explains the operational story clearly.
- **What is Q_high?** Short: the final high-priority model-quality measure in the demo. Longer: It is not the same as the critical-capture term K.
- **What is missed service?** Short: service failures when deadlines or revisit needs are missed. Longer: It captures urgent operational failure directly.
- **What does the reliability score mean?** Short: a summary of several demo metrics. Longer: It helps summarize behavior, but it is not the only criterion.
- **Are the reliability weights hand-set?** Short: yes. Longer: That is why the thesis also reports a lightweight sensitivity audit from saved outputs.
- **Is OSAG still best if the weights change?** Short: around the thesis weighting, yes. Longer: Equal weights and several local perturbations still keep OSAG top-ranked.

## 7. Critical or skeptical questions
- **Is this just reweighted sampling with a fancy name?** Short: it is lightweight and sampling-centered, but not only ad hoc reweighting. Longer: The governance loop itself is the real contribution.
- **Where is the graph, really?** Short: mostly in the modeling view. Longer: The current implementation does not yet solve an explicit graph optimization problem.
- **Aren't contracts just hand-made bias?** Short: they are human-designed policy units, and that is part of the research question. Longer: The thesis studies how contract design affects governance cost.
- **Why trust the demo if the reliability weights are hand-set?** Short: because the demo is supportive evidence, not the main benchmark. Longer: The benchmark tables remain the primary scientific evidence.
- **Why not run a transformer study?** Short: because the thesis is about governance control, not backbone competition. Longer: The ResMLP extension is a scoped robustness check.
- **Is reproducibility complete if there is no git ledger?** Short: it is strong but not complete in that specific sense. Longer: The thesis gives script-level and artifact-level reproducibility, but not a full commit-history provenance chain.

## 8. 15 trap-avoidance reminders
1. Do not say the graph is fully explicit.
2. Do not say the HSI split is leakage-free.
3. Do not say OSAG wins every metric.
4. Do not say the demo replaces the benchmark.
5. Do not say Table 5.2 is a relative percentage table.
6. Do not say EuroSAT fine has 12 contracts.
7. Do not say OSAG is a new backbone.
8. Do not say runtime proves OSAG is faster.
9. Do not hide the hand-set reliability weights.
10. Do not blur Q_high and K.
11. Do not blur main five-seed reruns and smaller three-seed extensions.
12. Do not present heuristic baselines as governance-correct just because Acc_high looks high.
13. Do not ignore Appendix A when asked about reproducibility.
14. Do not turn the defense into only a demo story.
15. Do not oversell novelty beyond governance-aware EO training.

## 9. 20 rapid-response short answers
1. The thesis is about governance-aware EO training.
2. OSAG is a lightweight governance layer, not a new backbone.
3. A contract is the service unit the policy cares about.
4. Target share says how much service a contract should receive.
5. Empirical coverage says how much it actually receives.
6. PrioCovErr measures the mismatch between those two.
7. Lower PrioCovErr means better policy alignment.
8. The main evidence is the fresh rerun benchmark.
9. The demo is an operational complement.
10. HSI uses corrected Indian Pines plus corrected Salinas.
11. EuroSAT uses the canonical 13-band MSI version.
12. HSI realizes 44 contracts.
13. EuroSAT coarse uses 4 contracts.
14. EuroSAT fine uses 6 contracts.
15. The main tables use five seeds.
16. The ablation is a fresh three-seed rerun.
17. Runtime means comparable overhead, not speed superiority.
18. The graph is a modeling view in the current implementation.
19. The HSI split is pixel-stratified, not spatial-blocked.
20. Appendix A is the thesis trust and reproducibility anchor.
