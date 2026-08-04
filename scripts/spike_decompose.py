#!/usr/bin/env python3
"""CPA spike decomposition for cpa-spike-diagnosis-google-ads.

Given a per-segment CSV with baseline and spike window columns, computes:
1. The CPC-vs-CVR decomposition of the blended CPA change.
2. The mix-shift test: spike-window CPA recomputed at baseline spend weights.
3. Per-segment contribution to the blended change, plus the unexplained residual.

Input CSV columns (one row per segment, e.g. campaign):
  segment, base_cost, base_clicks, base_conv, spike_cost, spike_clicks, spike_conv

Usage:
  python3 spike_decompose.py segments.csv

Exit codes: 0 ok, 2 could not read input.
"""
import argparse, csv, sys

def num(v):
    v = str(v or "").replace(",", "").replace("$", "").replace("%", "").strip()
    try:
        return float(v)
    except ValueError:
        return 0.0

def pick(header, cands):
    for h in header:
        if any(c == h.strip().lower() or c in h.strip().lower() for c in cands):
            return h
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csvfile")
    a = ap.parse_args()

    try:
        with open(a.csvfile, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
    except OSError as e:
        print(f"READ FAILED (not the same as no spike): {e}", file=sys.stderr)
        sys.exit(2)
    if not rows:
        print("CSV read fine but has zero rows - a finding about the export, not the account.")
        return

    header = list(rows[0].keys())
    cols = {}
    for key in ("base_cost", "base_clicks", "base_conv", "spike_cost", "spike_clicks", "spike_conv"):
        col = pick(header, [key, key.replace("_", " ")])
        if not col:
            sys.exit(f"missing column {key}. Header: {header}")
        cols[key] = col
    c_name = pick(header, ["segment", "campaign", "name"]) or header[0]

    segs = []
    for r in rows:
        s = {k: num(r.get(c, 0)) for k, c in cols.items()}
        s["name"] = r.get(c_name, "?")
        segs.append(s)

    B = {k: sum(s[k] for s in segs) for k in cols}
    if not B["base_conv"] or not B["spike_conv"]:
        print("Zero conversions in one window at the blended level - decomposition "
              "needs conversions in both windows. Verdict: needs_data.")
        return
    base_cpa = B["base_cost"] / B["base_conv"]
    spike_cpa = B["spike_cost"] / B["spike_conv"]
    base_cpc = B["base_cost"] / B["base_clicks"] if B["base_clicks"] else 0
    spike_cpc = B["spike_cost"] / B["spike_clicks"] if B["spike_clicks"] else 0
    base_cvr = B["base_conv"] / B["base_clicks"] if B["base_clicks"] else 0
    spike_cvr = B["spike_conv"] / B["spike_clicks"] if B["spike_clicks"] else 0

    print(f"Blended CPA: {base_cpa:,.2f} -> {spike_cpa:,.2f} "
          f"({(spike_cpa/base_cpa-1)*100:+.1f}%)")
    print(f"CPC:  {base_cpc:,.2f} -> {spike_cpc:,.2f} ({(spike_cpc/base_cpc-1)*100:+.1f}%)"
          if base_cpc else "CPC: no click data")
    print(f"CVR:  {base_cvr*100:.2f}% -> {spike_cvr*100:.2f}% "
          f"({(spike_cvr/base_cvr-1)*100:+.1f}%)" if base_cvr else "CVR: no click data")
    if base_cpc and base_cvr:
        # CPA = CPC / CVR; attribute log-change shares
        import math
        d_cpa = math.log(spike_cpa / base_cpa)
        d_cpc = math.log(spike_cpc / base_cpc)
        d_cvr = -math.log(spike_cvr / base_cvr)
        if d_cpa:
            print(f"Decomposition of the CPA change: CPC side {d_cpc/d_cpa*100:.0f}%, "
                  f"CVR side {d_cvr/d_cpa*100:.0f}% (log attribution)")

    # Mix-shift: spike CPA at baseline spend weights
    reweighted_num, reweighted_den = 0.0, 0.0
    for s in segs:
        w = s["base_cost"] / B["base_cost"] if B["base_cost"] else 0
        if s["spike_conv"] > 0:
            seg_cpa = s["spike_cost"] / s["spike_conv"]
            reweighted_num += w * seg_cpa
            reweighted_den += w
    if reweighted_den:
        mix_cpa = reweighted_num / reweighted_den
        print(f"\nMix-shift test: spike CPA at baseline spend weights = {mix_cpa:,.2f}")
        if abs(mix_cpa - base_cpa) < abs(spike_cpa - base_cpa) * 0.3:
            print("-> reweighted CPA is close to baseline: the spike is mostly MIX "
                  "(money moved to worse segments), not deterioration inside segments.")
        else:
            print("-> reweighted CPA still elevated: segments themselves deteriorated; "
                  "mix explains only part of the move.")

    print("\n| Segment | Base CPA | Spike CPA | Spend share (base->spike) | Contribution |")
    print("|---|---:|---:|---|---|")
    for s in sorted(segs, key=lambda s: -s["spike_cost"]):
        bc = s["base_cost"] / s["base_conv"] if s["base_conv"] else None
        sc = s["spike_cost"] / s["spike_conv"] if s["spike_conv"] else None
        wsb = s["base_cost"] / B["base_cost"] * 100 if B["base_cost"] else 0
        wss = s["spike_cost"] / B["spike_cost"] * 100 if B["spike_cost"] else 0
        note = ""
        if sc is None:
            note = "zero spike conv - check window/tracking before judging"
        elif bc and sc > bc * 1.2 and wss > wsb + 5:
            note = "worse AND absorbing more spend - primary contributor"
        elif bc and sc > bc * 1.2:
            note = "deteriorated in place"
        elif wss > wsb + 5:
            note = "mix: spend share grew"
        bc_s = f"{bc:,.2f}" if bc is not None else "-"
        sc_s = f"{sc:,.2f}" if sc is not None else "-"
        print(f"| {s['name']} | {bc_s} | {sc_s} | {wsb:.0f}% -> {wss:.0f}% | {note} |")
    print("\nDo not force causes to sum to 100%: name the residual. Cause "
          "attribution beyond arithmetic stays with the skill.")

if __name__ == "__main__":
    main()
