#!/usr/bin/env python3
"""Validator for the google-ads skills pack.

Asserts the section skeleton every skill carries after the v2.2.0 deepening,
plus: every `../` relative path a skill cites resolves on disk (the false-pass
a section check alone would allow: a heading can exist while the helper it
points at does not).

This gate passes falsely if a section heading exists but its body is empty or
wrong - it checks presence and paths, not prose quality. Prose quality is the
grader's job, not this script's.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "## Use this skill when",
    "## Required input",
    "## Practical example",
    "## Output format",
    "### Route to next",
    "### Data gaps",
    "## Guardrails",
]
GUARD_LINE = "say which one you adjusted"

errors = []
skill_files = sorted(ROOT.glob("*/SKILL.md"))
for path in skill_files:
    rel = path.relative_to(ROOT)
    text = path.read_text()
    for section in REQUIRED:
        if section not in text:
            errors.append(f"{rel}: missing {section}")
    if "workflow" not in text.lower():
        errors.append(f"{rel}: no workflow section")
    if path.parent.name == "rsa-ad-copy-generator-google-ads":
        if "## Verification pass" not in text:
            errors.append(f"{rel}: missing ## Verification pass")
    else:
        if "## Decision rules" not in text:
            errors.append(f"{rel}: missing ## Decision rules")
    if GUARD_LINE not in text:
        errors.append(f"{rel}: missing threshold-adjustment guardrail")
    for ref in re.findall(r"\.\./[A-Za-z0-9_./-]+", text):
        target = (path.parent / ref.rstrip(").,`'\":;")).resolve()
        if not target.exists():
            errors.append(f"{rel}: broken relative reference {ref}")

if len(skill_files) != 20:
    errors.append(f"expected 20 skills, found {len(skill_files)}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: {len(skill_files)} skills validated")
