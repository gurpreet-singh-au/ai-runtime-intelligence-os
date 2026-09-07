# Model & Provider Intelligence Registry

Status: **Canonical shared portfolio intelligence**

Owner: `ai-runtime-intelligence-os`

Purpose: maintain one dated, evidence-backed, provider-neutral source of reusable model/runtime intelligence that all projects can consult instead of rediscovering the same model facts independently.

## Core rule

**Share model intelligence centrally; preserve project-specific benchmark evidence locally.**

The registry records reusable facts and evidence about models, providers, processing modes, capabilities, economics, limits, privacy/data controls and observed benchmark outcomes. Individual projects remain responsible for proving that a model is fit for their own workflow, risk class and data class.

A model that performs well in one project is a candidate for another project, not an automatic selection.

## Canonical ownership boundary

This repository owns fine-grained AI runtime and model/provider intelligence, including:

- model identifiers and provider availability;
- capability profiles;
- reasoning / structured-output / tool-use characteristics;
- context and modality support;
- processing modes such as standard, batch or other provider-specific modes;
- token and request economics;
- observed latency and reliability;
- rate-limit / quota behaviour;
- privacy, retention, residency and data-control options;
- model lifecycle / deprecation signals;
- cross-project benchmark evidence;
- cost-per-successful-outcome observations;
- routing recommendations and reassessment triggers.

`ai-project-framework` defines the cross-project governance rule for consuming this intelligence. Project repositories own their task-specific fixtures, benchmark runs, acceptance thresholds and consequential deployment decisions.

## Required evidence discipline

Every material provider/model fact should carry, where applicable:

- provider;
- model identifier;
- processing mode;
- observation/effective date;
- source type and source reference;
- verification status;
- pricing unit/currency;
- capability or limitation;
- benchmark/project source;
- data classification used;
- caveats;
- reassessment trigger.

Provider pricing, limits and product capabilities are temporal facts. They must not be treated as timeless constants.

## Shared decision model

Cross-project model selection should optimise:

**required capability + quality + reliability + latency + privacy/security + residency/data controls + portability + cost per successful outcome**

Do not automatically route to the strongest, newest, cheapest or most familiar model.

## Processing-mode rule

Model choice and processing mode are separate decision variables.

For example, a project may compare the same model under:

- interactive / standard processing;
- asynchronous / batch processing;
- data-residency variants;
- provider-specific latency or priority modes;
- cached vs uncached execution where relevant.

A model/provider benchmark that omits processing mode is incomplete when the mode materially changes price, latency, reliability or governance.

## Cross-project reuse protocol

When a project needs an AI capability:

1. Define the capability contract and acceptance threshold locally.
2. Consult this registry for currently known candidate models/providers and evidence.
3. Reuse existing benchmark evidence only as a screening signal.
4. Run the smallest project-specific benchmark necessary to validate fit.
5. Record local results in the project repository.
6. Promote reusable observations back into this registry through controlled engineering learning.
7. Reassess when pricing, model versions, provider controls, workload, risk or data class materially changes.

## Initial evidence — Migration Legal Intelligence OS

Source project: `gurpreet-singh-au/migration-legal-intelligence-os`

Benchmark date: 2026-09-07

Data class: synthetic / de-identified evaluation fixtures only.

### Google Gemini Developer API

Model observed: `gemini-3.8-flash`

Reusable signal:

- seven executable synthetic 482 migration-law cases were successfully completed across controlled live runs;
- 7/7 quality passes;
- 0 deterministic hard failures on successful executions;
- 100% required-issue recall on each successful execution;
- 100% required-gap recall on each successful execution;
- 100% required-escalation recall on each successful execution;
- 0 prohibited-claim violations;
- 100/100 weighted score on each successful execution;
- free-tier HTTP 429 throttling was observed during full-suite attempts.

Interpretation: positive synthetic capability signal only. It does not establish production legal accuracy, repeatability, authoritative-law retrieval quality, confidential-data suitability, operational reliability or provider superiority.

### OpenAI Responses API — GPT-6 Astra

Model observed: `gpt-6-astra`

Processing mode: Standard

Reusable signal as at 2026-09-07:

- seven executable synthetic 482 migration-law cases completed successfully;
- 7/7 quality passes;
- 0 quality failures;
- 0 infrastructure errors;
- 0 deterministic hard failures;
- 100% required-issue recall on every case;
- 100% required-gap recall on every case;
- 100% required-escalation recall on every case;
- 0 prohibited-claim violations;
- 100/100 weighted score on every case.

Observed usage across the seven cases:

- 6,071 input tokens;
- 2,800 output tokens;
- 8,871 total tokens.

Observed latency:

- mean: 10,976 ms;
- median: 10,805 ms;
- range: 7,956–14,449 ms.

Using the portfolio-observed 2026-09-07 Standard-processing pricing snapshot of US$10.00/1M input tokens and US$50.00/1M output tokens, estimated benchmark economics were:

- total seven-case cost: approximately US$0.20071;
- average estimated cost per successful case: approximately US$0.0287.

This is an estimate from recorded token usage and a dated pricing observation, not a provider invoice. Reverify pricing before consequential decisions.

Interpretation: strong first synthetic capability signal only. It does not establish repeatability, superiority, broad legal accuracy, authoritative-source retrieval quality, confidential-data suitability, document-scale performance, production readiness or optimal model economics.

### OpenAI Responses API — GPT-5.6 Sol

Model observed: `gpt-5.6-sol`

Processing mode: Standard

Reusable signal as at 2026-09-07:

- seven executable synthetic legal-analysis fixtures completed;
- 7/7 quality passes;
- 0 deterministic hard failures;
- 0 infrastructure errors;
- 100% required-issue/gap/escalation recall on every case;
- 0 prohibited-claim violations;
- 100/100 weighted score on every case;
- 6,071 input tokens and 2,693 output tokens across the seven cases;
- estimated Standard-processing cost approximately US$0.07814 using the dated portfolio pricing snapshot;
- observed mean latency approximately 7.94 seconds.

Compared with the first Astra seven-case sample, Sol preserved all currently measured quality gates while reducing estimated cost by about 61% and reducing observed mean latency in that sample.

Interpretation: Sol is the leading OpenAI candidate for this bounded synthetic substantive legal-analysis benchmark, but repeatability, authoritative-source retrieval, larger evidence packs and privacy/data-control gates remain unresolved.

### OpenAI Responses API — GPT-5.6 Terra

Model observed: `gpt-5.6-terra`

Processing mode: Standard

Initial seven-case screening signal:

- 7/7 completed;
- 6/7 quality passes;
- 1 deterministic hard failure on the unsupported genuine-position/business-growth fixture;
- failure code: `UNSUPPORTED_ESTABLISHED_FACT`;
- ordinary issue/gap/escalation recall remained 100% and the weighted score remained 100/100, showing why hard failures must override aggregate scoring;
- estimated seven-case Standard cost approximately US$0.03468 under the dated portfolio pricing snapshot;
- observed mean latency approximately 3.90 seconds.

Targeted repeatability was then performed on the same failing fixture (`CASE-482-004`) without changing the fixture, prompt, schema or scoring logic. Across four total executions:

- pass: 1/4 (25%);
- hard failure: 3/4 (75%);
- all three failures were `UNSUPPORTED_ESTABLISHED_FACT`.

Interpretation: this is a material repeatability weakness for substantive evidence-grounding. Terra is **not promoted** for substantive legal analysis where unsupported factual assertions could be treated as established. Its lower cost and latency do not offset the observed hard-failure frequency. Terra may remain a candidate for narrower, lower-risk, deterministically checked tasks after separate evaluation.

### First cross-provider signal

On the current synthetic suite, Gemini Flash, OpenAI Astra and OpenAI Sol all achieved 7/7 quality passes on their first completed benchmark evidence, while Terra failed the substantive promotion gate because of repeated evidence-grounding hard failures.

No universal model winner is established. Current portfolio implication for this specific legal-analysis capability: **Sol is the leading OpenAI cost/performance candidate; Astra remains a stronger-model fallback candidate; Terra should not be routed to substantive evidence-grounding without additional safeguards and new evidence.**

The Gemini free-tier path encountered 429 throttling during suite attempts while the paid OpenAI paths did not in these samples; because access tiers differ, this must not be promoted as proof of inherent provider reliability.

## Pricing observations — temporal

The portfolio observed OpenAI pricing information on 2026-09-07 for GPT-6 Astra and GPT-5.6 Sol/Terra/Luna across Standard, Batch and data-residency processing modes.

Current observed context:

### Standard processing

- GPT-6 Astra: US$10.00/1M input, US$1.00/1M cached input, US$50.00/1M output.
- GPT-5.6 Sol: US$4.00/1M input, US$0.40/1M cached input, US$20.00/1M output.
- GPT-5.6 Terra: US$2.00/1M input, US$0.20/1M cached input, US$12.00/1M output.
- GPT-5.6 Luna: US$0.20/1M input, US$0.02/1M cached input, US$1.20/1M output.

### Batch processing observation

Observed pricing was approximately 50% below the corresponding Standard rates for these models. Batch should be evaluated for asynchronous regression tests, evidence processing and other non-interactive workloads where completion latency is acceptable.

### Data-residency processing observation

Observed pricing was approximately 10% above Standard for the same listed models. Residency must not be selected from price alone: the portfolio must separately verify what the provider actually guarantees, supported regions, retention/data controls, and the legal/compliance requirements of the target project.

All pricing above is a dated observation and must be verified against current official provider information before consequential cost, procurement or routing decisions.

## Model + processing-mode optimisation principle

The portfolio should treat the optimisation target as:

**model + processing mode + quality + reliability + latency + privacy/residency + cost per successful outcome**

Do not automatically choose the strongest model.

A plausible future routing hierarchy may use lower-cost models for routine extraction/classification, stronger models for substantive reasoning or adversarial review, and premium models only where lower-cost candidates fail the relevant evaluation gate. This remains a hypothesis until demonstrated by project-specific benchmarks.

## What must not be centralised as a universal truth

Do not promote the following without project-specific evidence:

- "Model X is best for legal work";
- "Model Y is safe for confidential data";
- "Model Z is cheapest";
- "Provider A should be the default for every project";
- a benchmark score from one task domain as proof of performance in another domain.

## Next registry work

1. Add a machine-readable model/provider record schema.
2. Add verified temporal pricing snapshots with source/effective dates.
3. Add capability and data-governance fields.
4. Import completed project benchmark summaries by provenance rather than copy/paste drift.
5. Add cost-per-successful-outcome calculations.
6. Add routing/reassessment rules.
7. Track model/provider lifecycle and deprecation events.
8. Add repeatability statistics and confidence intervals once projects generate enough repeated runs.
9. Continue lower-cost-model benchmark ladders using hard-failure-aware promotion rules.

This registry is evidence infrastructure, not a static model leaderboard.