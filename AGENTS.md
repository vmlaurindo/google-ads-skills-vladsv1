# AGENTS.md: Google Ads performance marketing skills

This repo is a pack of 20 Claude Skills for rigorous Google Ads work:
triage, wasted spend, structure, search terms, Quality Score, impression
share, conversion tracking, offline imports, Shopping feed QA, anomaly
diagnosis, RSA copy, Performance Max, bidding, landing page match,
competitive pressure, forecasting, scaling and reporting. Each skill is a
self-contained `SKILL.md` under its own folder, following the Agent Skills
standard, so the pack also runs in any other Agent Skills tool.

## How these skills behave

- **Data-first.** Every skill reads what you provide: Google Ads exports,
  search terms reports, auction insights, screenshots. If the input is
  missing, the skill says so and marks an assumption instead of guessing.
- **Human-in-the-loop.** Skills diagnose and recommend. They do not log into
  the account and they do not change campaigns, budgets or bids.
- **Honest about limits.** Every threshold inside a skill is a labeled
  heuristic, not a rule Google published. Confidence is stated.

## How the pack composes

- `account-triage-google-ads` is the entry point. It establishes what is
  broken and routes to the right deep-dive skill.
- Measurement skills (`conversion-tracking-audit-google-ads`,
  `offline-conversion-import-audit-google-ads`) come before efficiency and
  scaling skills. Bidding and scaling decisions on top of broken conversion
  tracking produce confident, wrong answers.
- The two RSA skills pair: `rsa-ad-copy-review-google-ads` grades what runs
  today, `rsa-ad-copy-generator-google-ads` drafts replacements.
- `weekly-operator-digest-google-ads` is the recurring summary skill; run it
  last.

## Verticals

Ecommerce accounts lean on Shopping feed QA, PMax diagnosis and ROAS
scenarios; lead gen accounts lean on search terms hygiene, offline
conversion imports and landing page match, and should rank on CRM-verified
lead value rather than platform conversions.
