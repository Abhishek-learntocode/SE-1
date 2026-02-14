# CK Metrics Summary (Class-level)

This summary was generated from `ckclass.csv` (CK tool output).

## Summary Statistics (n=535 classes)
- **WMC** (Weighted Methods per Class): avg 18.73 (min 0, max 197), p90 43, p95 61, p99 108
- **CBO** (Coupling Between Objects): avg 6.74 (min 0, max 46), p90 15, p95 20, p99 31
- **RFC** (Response For a Class): avg 17.81 (min 0, max 190), p90 47, p95 62, p99 113
- **DIT** (Depth of Inheritance Tree): avg 1.58 (min 1, max 7), p90 3, p95 3, p99 4
- **NOC** (Number of Children): avg 0.22 (min 0, max 39), p90 0, p95 1, p99 4
- **LCOM** (Lack of Cohesion in Methods): avg 70.65 (min 0, max 4336), p90 135, p95 299, p99 1114

## Interpretation
- **WMC/RFC**: High tail values (p99 > 100) indicate classes with large method sets and complex behavior; good candidates for refactoring.
- **CBO**: Moderate average coupling with a long tail (p99 31) suggests some highly coupled classes needing decoupling or façade patterns.
- **DIT/NOC**: Low inheritance depth/children overall (p90 DIT=3, NOC=0) implies design favors composition over deep inheritance, which is generally maintainable.
- **LCOM**: Very high tail values indicate low cohesion in some classes, reinforcing refactoring targets.

## Files
- `Working/03-task2/ckclass.csv`
- `Working/03-task2/ckmethod.csv`
