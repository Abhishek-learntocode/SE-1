#!/usr/bin/env python3
"""Quick analysis of current R6.1 metrics"""
import pandas as pd
import os

base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data_archive")

# Load R6.1 class.csv
r6 = pd.read_csv(os.path.join(base, "R6.1", "class.csv"))
init = pd.read_csv(os.path.join(base, "inital", "class.csv"))

# Rename 'loc' column to avoid pandas .loc conflict
r6 = r6.rename(columns={"loc": "lines"})
init = init.rename(columns={"loc": "lines"})

r6["short"] = r6["class"].apply(lambda x: x.split(".")[-1])
init["short"] = init["class"].apply(lambda x: x.split(".")[-1])

print("=" * 80)
print("  TOP 25 CLASSES BY WMC (R6.1 - Current State)")
print("=" * 80)
top = r6.nlargest(25, "wmc")[["short", "class", "wmc", "cbo", "lines", "lcom", "rfc"]].reset_index(drop=True)
for i, row in top.iterrows():
    print(f"  {i+1:>2}. WMC={int(row.wmc):>4}  CBO={int(row.cbo):>3}  LOC={int(row.lines):>5}  LCOM={int(row.lcom):>6}  RFC={int(row.rfc):>4}  {row.short}")

print()
print("=" * 80)
print("  CLASSES WITH WMC > 50 (Need Attention)")
print("=" * 80)
high = r6[r6["wmc"] > 50].sort_values("wmc", ascending=False)
for i, row in high.iterrows():
    print(f"  WMC={int(row.wmc):>4}  CBO={int(row.cbo):>3}  LOC={int(row.lines):>5}  LCOM={int(row.lcom):>6}  {row.short}")
print(f"\n  Total: {len(high)} classes with WMC > 50")

print()
print("=" * 80)
print("  HIGH COUPLING CLASSES (CBO > 20)")
print("=" * 80)
coupled = r6[r6["cbo"] > 20].sort_values("cbo", ascending=False)
for i, row in coupled.iterrows():
    print(f"  CBO={int(row.cbo):>3}  WMC={int(row.wmc):>4}  LOC={int(row.lines):>5}  {row.short}")
print(f"\n  Total: {len(coupled)} classes with CBO > 20")

print()
print("=" * 80)
print("  NEW/CHANGED CLASSES (in R6.1 but not in initial)")
print("=" * 80)
init_classes = set(init["class"].values)
r6_classes = set(r6["class"].values)
new_classes = r6_classes - init_classes
removed_classes = init_classes - r6_classes
for c in sorted(new_classes):
    row = r6[r6["class"] == c].iloc[0]
    print(f"  + {c.split('.')[-1]:>40}  WMC={int(row.wmc):>4}  CBO={int(row.cbo):>3}  LOC={int(row.lines):>4}")
print(f"\n  New: {len(new_classes)}, Removed: {len(removed_classes)}")
if removed_classes:
    for c in sorted(removed_classes):
        print(f"  - {c.split('.')[-1]}")

print()
print("=" * 80)
print("  GOD CLASS ANALYSIS (WMC>47 combined with LOC, CBO, LCOM)")
print("=" * 80)
# Standard god class: high WMC + high LCOM + large LOC
gods = r6[(r6["wmc"] > 47) & (r6["lines"] > 100)].sort_values("wmc", ascending=False)
print(f"  God class candidates (WMC>47 & LOC>100): {len(gods)}")
for i, row in gods.iterrows():
    flag = "***" if row.wmc > 100 else "  *" if row.wmc > 70 else "   "
    print(f"  {flag} WMC={int(row.wmc):>4}  CBO={int(row.cbo):>3}  LOC={int(row.lines):>5}  LCOM={int(row.lcom):>6}  {row.short}")

# Compare initial vs R6.1 for classes that existed in both
print()
print("=" * 80)
print("  METRICS CHANGES FOR REFACTORED CLASSES (Initial -> R6.1)")
print("=" * 80)
common = init_classes & r6_classes
changes = []
for c in common:
    i_row = init[init["class"] == c].iloc[0]
    r_row = r6[r6["class"] == c].iloc[0]
    dwmc = r_row.wmc - i_row.wmc
    dcbo = r_row.cbo - i_row.cbo
    dloc = r_row.lines - i_row.lines
    dlcom = r_row.lcom - i_row.lcom
    if abs(dwmc) > 0 or abs(dcbo) > 0 or abs(dloc) > 1:
        changes.append({
            "short": c.split(".")[-1],
            "wmc_before": int(i_row.wmc), "wmc_after": int(r_row.wmc), "dwmc": int(dwmc),
            "cbo_before": int(i_row.cbo), "cbo_after": int(r_row.cbo), "dcbo": int(dcbo),
            "loc_before": int(i_row.lines), "loc_after": int(r_row.lines), "dloc": int(dloc),
            "lcom_before": int(i_row.lcom), "lcom_after": int(r_row.lcom), "dlcom": int(dlcom),
        })
changes.sort(key=lambda x: x["dwmc"])
for c in changes:
    wmc_dir = "v" if c["dwmc"] < 0 else "^" if c["dwmc"] > 0 else "="
    print(f"  {wmc_dir} {c['short']:>45}  WMC: {c['wmc_before']:>4}->{c['wmc_after']:>4} ({c['dwmc']:>+4})  CBO: {c['cbo_before']:>3}->{c['cbo_after']:>3} ({c['dcbo']:>+3})  LOC: {c['loc_before']:>5}->{c['loc_after']:>5} ({c['dloc']:>+5})")
print(f"\n  Total changed classes: {len(changes)}")

# System level summary
print()
print("=" * 80)
print("  SYSTEM LEVEL: Initial vs R6.1")
print("=" * 80)
print(f"  Classes:   {len(init)} -> {len(r6)} ({len(r6)-len(init):+d})")
print(f"  Total LOC: {int(init.lines.sum())} -> {int(r6.lines.sum())} ({int(r6.lines.sum()-init.lines.sum()):+d})")
print(f"  Avg WMC:   {init.wmc.mean():.2f} -> {r6.wmc.mean():.2f} ({r6.wmc.mean()-init.wmc.mean():+.2f})")
print(f"  Max WMC:   {int(init.wmc.max())} -> {int(r6.wmc.max())} ({int(r6.wmc.max()-init.wmc.max()):+d})")
print(f"  Avg CBO:   {init.cbo.mean():.2f} -> {r6.cbo.mean():.2f} ({r6.cbo.mean()-init.cbo.mean():+.2f})")
print(f"  Avg LCOM:  {init.lcom.mean():.2f} -> {r6.lcom.mean():.2f} ({r6.lcom.mean()-init.lcom.mean():+.2f})")
print(f"  Avg RFC:   {init.rfc.mean():.2f} -> {r6.rfc.mean():.2f} ({r6.rfc.mean()-init.rfc.mean():+.2f})")
print(f"  WMC>100:   {len(init[init.wmc>100])} -> {len(r6[r6.wmc>100])}")
print(f"  WMC>50:    {len(init[init.wmc>50])} -> {len(r6[r6.wmc>50])}")
print(f"  CBO>20:    {len(init[init.cbo>20])} -> {len(r6[r6.cbo>20])}")
print(f"  LCOM>500:  {len(init[init.lcom>500])} -> {len(r6[r6.lcom>500])}")

