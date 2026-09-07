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

### OpenAI Responses API

Model observed: `gpt-6-astra`

Processing mode: Standard

Current reusable signal as at 2026-09-07:

- `CASE-482-002` completed successfully;
- quality pass: yes;
- deterministic hard failures: 0;
- required-issue recall: 100%;
- required-gap recall: 100%;
- required-escalation recall: 100%;
- prohibited-claim violations: 0;
- weighted score: 100/100;
- latency: 10,797 ms;
- usage: 860 input tokens, 346 output tokens, 1,206 total tokens.

Interpretation: one-case smoke-test signal only. The remaining project benchmark is still required before comparative conclusions.

## Pricing observations — pending/temporal

The portfolio has observed current OpenAI pricing information on 2026-09-07 for GPT-6 Astra and GPT-5.6 Sol/Terra/Luna across Standard, Batch and data-residency processing modes. Because provider pricing changes, these observations must be verified against current official provider sources before a consequential cost or procurement decision.

Known portfolio principle from the observation:

- Standard is the current interactive baseline for the Migration Legal Intelligence benchmark;
- Batch can be evaluated for asynchronous regression/evaluation workloads where latency is non-critical;
- data-residency modes should be assessed separately when real client or regulated data is contemplated;
- model + processing mode must be optimised together rather than treating model selection alone as the decision.

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

This registry is evidence infrastructure, not a static model leaderboard.