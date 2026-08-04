#!/usr/bin/env python3
"""Anomaly scanner for anomaly-detection-google-ads.

Reads a daily per-campaign (or account-level) CSV, computes trailing and
same-weekday baselines, z-scores per metric, and the severity tiers from the
skill's Decision rules: within normal variance / investigate / significant.
Enforces the volume guards (no daily z-score for ratio metrics below ~5
conversions/day; no z-score at all without enough baseline points).

Usage:
  python3 anomaly_scan.py daily.csv --anomaly-days 1
  python3 anomaly_scan.py daily.csv --anomaly-days 3 --baseline-days 28 --no-weekday

Exit codes: 0 ok, 2 could not read input.
"""
import argparse, csv, math, sys
from datetime import datetime
from collections import defaultdict

def num(v):
    v = str(v or "").replace(",", "").replace("$", "").replace("%", "").strip()
    try:
        return float(v)
    except ValueError:
        return 0.0

def parse_date(s):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(str(s).strip()[:10], fmt)
        except ValueError:
            continue
    return None

def pick(header, cands):
    for h in header:
        if any(c in h.strip().lower() for c in cands):
            return h
    return None

def stats(vals):
    n = len(vals)
    if n < 2:
        return None, None
    m = sum(vals) / n
    sd = math.sqrt(sum((v - m) ** 2 for v in vals) / (n - 1))
    return m, sd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csvfile")
    ap.add_argument("--anomaly-days", type=int, default=1)
    ap.add_argument("--baseline-days", type=int, default=28)
    ap.add_argument("--no-weekday", action="store_true")
    ap.add_argument("--min-baseline-points", type=int, default=3)
    a = ap.parse_args()

    try:
        with open(a.csvfile, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
    except OSError as e:
        print(f"READ FAILED (not the same as a quiet account): {e}", file=sys.stderr)
        sys.exit(2)
    if not rows:
        print("CSV read fine but has zero rows - a finding about the export, not the account.")
        return

    header = list(rows[0].keys())
    c_date = pick(header, ["date", "day"])
    c_camp = pick(header, ["campaign"])
    c_cost = pick(header, ["cost", "spend"])
    c_clicks = pick(header, ["clicks"])
    c_conv = pick(header, ["conversions", "conv"])
    if not c_date or not c_cost:
        sys.exit(f"no date/cost columns found. Header: {header}")

    daily = defaultdict(lambda: defaultdict(dict))  # campaign -> date -> metrics
    for r in rows:
        d = parse_date(r[c_date])
        if not d:
            continue
        camp = r.get(c_camp, "ACCOUNT") if c_camp else "ACCOUNT"
        day = daily[camp].setdefault(d.date(), {})
        for key, col in (("cost", c_cost), ("clicks", c_clicks), ("conversions", c_conv)):
            if col:
                day[key] = day.get(key, 0.0) + num(r.get(col))

    for camp, days_map in sorted(daily.items(), key=lambda kv: -sum(d.get("cost", 0) for d in kv[1].values())):
        days = sorted(days_map)
        if len(days) < a.anomaly_days + 7:
            print(f"\n== {camp}: only {len(days)} days - needs_data")
            continue
        anom = days[-a.anomaly_days:]
        base = [d for d in days[:-a.anomaly_days]
                if (days[-1] - d).days <= a.baseline_days + a.anomaly_days]
        label = f"all days ({len(base)})"
        if not a.no_weekday and a.anomaly_days == 1:
            wd = [d for d in base if d.weekday() == anom[0].weekday()]
            if len(wd) >= a.min_baseline_points:
                base, label = wd, f"same-weekday ({len(wd)})"
        anom_conv = sum(days_map[d].get("conversions", 0) for d in anom)
        print(f"\n== {camp} | baseline: {label} | anomaly: {anom[0]}..{anom[-1]}")
        print("| Metric | Base mean | SD | Anomaly | Z | Verdict |")
        print("|---|---:|---:|---:|---:|---|")
        metrics = ["cost", "clicks", "conversions"]
        if c_conv:
            metrics.append("CPA")
        for m in metrics:
            def val(d):
                day = days_map[d]
                if m == "CPA":
                    return day.get("cost", 0) / day["conversions"] if day.get("conversions") else None
                return day.get(m, 0.0)
            if m == "CPA" and anom_conv < 5 * a.anomaly_days:
                print("| CPA | - | - | - | - | daily unreadable below ~5 conv/day; judge weekly [heuristic] |")
                continue
            bvals = [v for v in (val(d) for d in base) if v is not None]
            avals = [v for v in (val(d) for d in anom) if v is not None]
            mean, sd = stats(bvals)
            if mean is None or not avals or len(bvals) < a.min_baseline_points:
                print(f"| {m} | - | - | - | - | insufficient baseline |")
                continue
            av = sum(avals) / len(avals)
            z = (av - mean) / sd if sd else 0.0
            if abs(z) < 2:
                verdict = "within normal variance - monitor"
            elif abs(z) < 3:
                verdict = "investigate"
            else:
                verdict = "significant"
            print(f"| {m} | {mean:,.2f} | {sd:,.2f} | {av:,.2f} | {z:+.1f} | {verdict} |")
    print("\nA logged tracking/site/upgrade change in the window is 'significant' "
          "regardless of Z. The change-log check and attribution stay with the skill.")

if __name__ == "__main__":
    main()
