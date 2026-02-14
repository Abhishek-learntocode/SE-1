#!/usr/bin/env python3
"""Detailed refactoring impact analysis"""
import pandas as pd
import os

base = r"c:\Users\Abhishek\IIITH\IITH\last_refactor\R6.1\6.1\roller-master\Refactoring_Lab\data_archive"

init = pd.read_csv(os.path.join(base, "inital", "class.csv")).rename(columns={"loc": "lines"})
r6 = pd.read_csv(os.path.join(base, "R6.1", "class.csv")).rename(columns={"loc": "lines"})

init_d = {row["class"]: row for _, row in init.iterrows()}
r6_d = {row["class"]: row for _, row in r6.iterrows()}

print("=" * 80)
print("  CLASSES THAT GOT SIGNIFICANTLY WORSE (dWMC > 5 or dLOC > 30)")
print("=" * 80)
worse = []
for c in set(init_d) & set(r6_d):
    dw = r6_d[c]["wmc"] - init_d[c]["wmc"]
    dl = r6_d[c]["lines"] - init_d[c]["lines"]
    dc = r6_d[c]["cbo"] - init_d[c]["cbo"]
    if dw > 5 or dl > 30:
        worse.append((c.split(".")[-1], int(dw), int(dl), int(dc), int(r6_d[c]["wmc"]), int(r6_d[c]["lines"]), int(r6_d[c]["cbo"])))
worse.sort(key=lambda x: -x[1])
for name, dw, dl, dc, wmc, loc, cbo in worse:
    print(f"  {name:>35}  dWMC={dw:>+4}  dLOC={dl:>+5}  dCBO={dc:>+3}  (now WMC={wmc}, LOC={loc}, CBO={cbo})")

print()
print("=" * 80)
print("  PRIMARY REFACTORING TARGETS - NET IMPACT")
print("=" * 80)
targets = [
    ("JPAWeblogEntryManagerImpl", "R1.1, R3.1"),
    ("WeblogEntry", "R1.2, R2.1"),
    ("Weblog", "R2.2, R6.1"),
    ("JPAWeblogManagerImpl", "R3.2"),
    ("EntryCollection", "R4.1"),
    ("RollerAtomHandler", "R4.1"),
    ("Subscription", "R4.2"),
    ("WeblogPageRequest", "R5.1"),
    ("MultiWeblogURLStrategy", "R5.2"),
]

for cls_short, rounds in targets:
    # Find full class name
    ic = None
    rc = None
    for c in init_d:
        if c.endswith("." + cls_short):
            ic = init_d[c]
            break
    for c in r6_d:
        if c.endswith("." + cls_short):
            rc = r6_d[c]
            break
    if ic is not None and rc is not None:
        dw = int(rc["wmc"] - ic["wmc"])
        dl = int(rc["lines"] - ic["lines"])
        dc = int(rc["cbo"] - ic["cbo"])
        dlc = int(rc["lcom"] - ic["lcom"])
        print(f"  {cls_short:>35}  [{rounds:>10}]  WMC: {int(ic['wmc']):>4}->{int(rc['wmc']):>4} ({dw:>+4})  CBO: {int(ic['cbo']):>3}->{int(rc['cbo']):>3} ({dc:>+3})  LOC: {int(ic['lines']):>5}->{int(rc['lines']):>5} ({dl:>+5})")

print()
print("=" * 80)
print("  NEWLY CREATED CLASSES (extracted during refactoring)")
print("=" * 80)
for c in sorted(set(r6_d) - set(init_d)):
    r = r6_d[c]
    short = c.split(".")[-1]
    print(f"  {short:>35}  WMC={int(r['wmc']):>4}  CBO={int(r['cbo']):>3}  LOC={int(r['lines']):>4}  LCOM={int(r['lcom']):>5}")

print()
print("=" * 80)
print("  UNTOUCHED HIGH-COMPLEXITY CLASSES (never refactored, WMC>50)")
print("=" * 80)

# Find classes with WMC>50 in R6.1 that barely changed
untouched = []
for c in r6_d:
    r = r6_d[c]
    if r["wmc"] <= 50:
        continue
    short = c.split(".")[-1]
    # Check if it changed much
    if c in init_d:
        ic = init_d[c]
        dw = abs(r["wmc"] - ic["wmc"])
        if dw <= 2:  # barely changed
            untouched.append((short, int(r["wmc"]), int(r["cbo"]), int(r["lines"]), int(r["lcom"]), int(r["rfc"])))
    else:
        # new class that's already complex
        pass

untouched.sort(key=lambda x: -x[1])
for name, wmc, cbo, loc, lcom, rfc in untouched:
    print(f"  {name:>35}  WMC={wmc:>4}  CBO={cbo:>3}  LOC={loc:>5}  LCOM={lcom:>6}  RFC={rfc:>4}")
print(f"\n  Total untouched high-WMC classes: {len(untouched)}")

# Net complexity budget
print()
print("=" * 80)
print("  COMPLEXITY BUDGET ANALYSIS")
print("=" * 80)
total_wmc_init = int(init["wmc"].sum())
total_wmc_r6 = int(r6["wmc"].sum())
total_loc_init = int(init["lines"].sum())
total_loc_r6 = int(r6["lines"].sum())
print(f"  Total WMC:  {total_wmc_init} -> {total_wmc_r6} ({total_wmc_r6 - total_wmc_init:+d})")
print(f"  Total LOC:  {total_loc_init} -> {total_loc_r6} ({total_loc_r6 - total_loc_init:+d})")

# Reduction in targeted classes
targeted_reduction = 0
for cls_short, _ in targets:
    for c in init_d:
        if c.endswith("." + cls_short):
            for c2 in r6_d:
                if c2.endswith("." + cls_short):
                    targeted_reduction += int(init_d[c]["wmc"] - r6_d[c2]["wmc"])
            break

# New classes added
new_wmc = sum(int(r6_d[c]["wmc"]) for c in set(r6_d) - set(init_d))
print(f"  WMC reduced in targets: {targeted_reduction}")
print(f"  WMC added by new classes: {new_wmc}")
print(f"  Net WMC change: {total_wmc_r6 - total_wmc_init:+d}")
