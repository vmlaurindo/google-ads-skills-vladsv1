# Google Ads Performance Marketing Skills

A pack of 10 production-ready Claude Skills that help agencies, freelancers, and in-house performance marketers run rigorous Google Ads diagnostics — wasted spend, account structure, search terms hygiene, conversion tracking, anomaly detection, RSA copy review and generation, Performance Max diagnosis, bidding sanity checks, and budget scaling.

Each skill is a self-contained `SKILL.md` with explicit triggers, required inputs, analysis workflow, decision rules, a practical example, output format, and guardrails. Drop them into Claude and they activate automatically when their use case matches the conversation.

## What's inside

| # | Skill | Folder | Purpose |
|---|-------|--------|---------|
| 1 | Wasted Spend Finder | `wasted-spend-finder-google-ads` | Find segments that spend without converting — search terms, devices, dayparts, geos, demographics |
| 2 | Account Structure Audit | `account-structure-audit-google-ads` | Map structure, flag under-volume / fragmented / duplicated campaigns, propose consolidation |
| 3 | Search Terms Hygiene | `search-terms-hygiene-google-ads` | Build a layered negative keyword plan from search terms reports |
| 4 | Conversion Tracking Audit | `conversion-tracking-audit-google-ads` | Audit Google Ads tracking using GA4 + GTM data; deduplication, primary vs secondary, attribution windows |
| 5 | Anomaly Detection | `anomaly-detection-google-ads` | Z-score baseline detection across CPA, ROAS, CVR, CTR, CPC, conversion volume |
| 6 | RSA Ad Copy Review | `rsa-ad-copy-review-google-ads` | Score existing RSAs for intent match, asset diversity, compliance, landing page alignment |
| 7 | RSA Ad Copy Generator | `rsa-ad-copy-generator-google-ads` | Produce 15 headlines + 4 descriptions matched to brand voice, intent, and offer |
| 8 | PMax Performance Diagnosis | `pmax-performance-diagnosis-google-ads` | Diagnose Performance Max — asset groups, audience signals, search insights, cannibalization |
| 9 | Bidding Strategy Sanity Check | `bidding-strategy-sanity-check-google-ads` | Match bid strategy to conversion volume, tracking quality, budget, and account stage |
| 10 | Scaling Planner | `scaling-planner-google-ads` | Decide where to add budget, hold, reduce, or pause — with reallocation and monitoring plan |

## How to install

### Option A — Claude Code (recommended)

1. Clone or download this repository.
2. Copy the skill folders into your project's `.claude/skills/` directory, or into the user-level skills directory at `~/.claude/skills/`.
3. Start a new Claude Code session in that project. Skills will activate automatically when their description matches the conversation.

### Option B — Other Claude environments

The skills are plain Markdown with YAML frontmatter and work anywhere Claude can read files. Paste the relevant `SKILL.md` content into context when you want to use it.

## How to use

Once installed, just describe what you want in natural language. Skills self-trigger on the patterns documented in their `## Use this skill when` section.

Examples:

- "Find wasted spend in this Google Ads account, here are the CSV exports from the last 60 days." → activates Wasted Spend Finder.
- "Why did CPA spike yesterday in the lead gen account?" → activates Anomaly Detection.
- "Generate 15 RSA headlines for emergency furnace repair, brand voice is trustworthy and urgent." → activates RSA Ad Copy Generator.

## Bring your data

Every skill is data-first. They work best when you provide actual exports — search terms reports, performance CSVs, asset reports, conversion action lists. Each `SKILL.md` documents exactly which exports it expects under `## Required input`.

For users with the Google Ads MCP server connected, skills can pull live data directly. For everyone else, CSV exports from Google Ads UI or Google Ads Editor work fine.

## License & attribution

Free to use, modify, and redistribute for personal and commercial work. If you ship something built on top of these skills, a credit is appreciated but not required.

Built and maintained by [AdLume](https://adlume.co) — performance marketing infrastructure for AI-native agencies.

Read the full guide on AdLume blog → https://blog.adlume.co/google-ads-claude-skills/
