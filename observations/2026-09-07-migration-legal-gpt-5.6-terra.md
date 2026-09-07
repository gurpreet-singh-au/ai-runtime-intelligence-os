# GPT-5.6 Terra — Migration Legal Intelligence Observation

Date: 2026-09-07

Source project: `gurpreet-singh-au/migration-legal-intelligence-os`

Provider: OpenAI Responses API

Model: `gpt-5.6-terra`

Processing mode: Standard

Data class: synthetic / de-identified legal evaluation fixtures.

## Observed signal

Seven executable subclass 482 synthetic fixtures were completed across two controlled runs.

- completed: 7/7
- quality passes: 6/7
- quality failures: 1/7
- infrastructure errors: 0
- hard failures: 1
- issue/gap/escalation recall: 100% on every case
- prohibited-claim violations: 0
- weighted score: 100/100 on every case before hard-failure override

Failure: `CASE-482-004` produced `UNSUPPORTED_ESTABLISHED_FACT`, meaning the model treated a fact as established without evidence or human verification. Under the source project's legal evaluation standard this is a critical failure and overrides the aggregate score.

## Economics and latency

Observed totals:

- 6,071 input tokens
- 1,878 output tokens
- 7,949 total tokens
- mean latency approximately 3,899 ms
- median latency 3,869 ms
- latency range 3,276–4,998 ms

Using the portfolio-observed 2026-09-07 Standard pricing snapshot of US$2.00/1M input and US$12.00/1M output, estimated seven-case cost is approximately US$0.034678. Pricing is temporal and must be reverified before consequential decisions.

## Reusable interpretation

Terra is a strong lower-cost candidate but is **not currently promotable for the tested legal-analysis capability** because one critical evidence-grounding failure occurred. The appropriate next experiment is a targeted repeatability probe on the failing fixture rather than a full-suite rerun.

Do not generalise this result beyond the tested capability. Project-specific evaluation remains mandatory.
