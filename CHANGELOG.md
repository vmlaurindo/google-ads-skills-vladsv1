# Changelog

All notable changes to this pack are documented here. Format follows Keep a
Changelog, loosely.

## [2.2.0] - 2026-08-03

### Added
- `Decision rules` with unit-carrying thresholds in the five diagnostic skills
  that lacked them (anomaly detection, PMax diagnosis, conversion tracking
  audit, RSA review) and a mandatory `Verification pass` in the RSA generator
  (character recount, non-English length budgets, missing-input paths).
- `Route to next` and `Data gaps` sections in all skills - the routing graph is
  now bidirectional instead of v2-only.
- Load-bearing numbers promoted from Practical examples into the rules they
  belonged to: bidding volume floors and target-tightness, structure
  consolidation floors and migration mechanics, negation evidence floors with
  n-gram grouping, scaling cadence, waste expected-conversions formula.
- Method lines where judgment was previously unstated: weekly digest variance
  band, ROAS forecast band derivation, landing page default weight sets,
  quality score blank-components path, impression-share and auction-insights
  floored-value caveats, offline conversions enhanced-conversions fallback,
  shopping feed blocking threshold.
- 2026 platform context (AI Max auto-upgrade, call-only deprecation) in the
  skills most exposed: anomaly detection, PMax, both RSA skills, scaling.
- Deterministic helpers in `scripts/`: `anomaly_scan.py` (baselines, z-scores,
  severity tiers per campaign) and `spike_decompose.py` (CPC-vs-CVR split plus
  the mix-shift test at baseline spend weights). Both distinguish "read fine
  but empty" from "could not read".
- `scripts/validate-skills.py`: asserts the full section skeleton, the
  threshold-adjustment guardrail, and that every cited relative path resolves.
  Seen red before shipping (it caught seven real gaps on its first run).
- Threshold-adjustment guardrail backfilled to every skill, making the README's
  consistency claim true for the whole pack.

### Fixed
- Install command copies `scripts/` so helper paths cited by skills resolve.

## [2.1.0] - 2026-08-03

### Added
- MIT `LICENSE` (the pack was described as open source; now it formally is).
- `AGENTS.md` with durable guidance on how the pack behaves and composes.
- This changelog.

## [2.0.0] - 2026-07-22

### Added
- 10 new skills, doubling the pack to 20: entry-point account triage,
  Shopping feed QA, offline conversion import audit, Quality Score analysis,
  impression share gap finder, CPA spike diagnosis, landing page match
  scorer, competitor auction insights benchmark, ROAS forecast scenarios,
  and a weekly operator digest. The original 10 kept their names.

## [1.0.0] - 2026-05-06

### Added
- Initial public release: 10 Google Ads diagnostic skills.
