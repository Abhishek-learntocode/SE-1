# Instance-Specific Visualization Guide

## Overview

The **instance visualization system** generates 4 plots for comparing **repository snapshots** before and after refactoring.

**What is an "Instance"?**
- An instance = **the entire repository state at a specific point in time**
- You compare TWO instances: BEFORE refactoring → AFTER refactoring
- Each audit run creates a snapshot of ALL classes, metrics, and violations
- Visualizations show the **full impact** of your refactoring on the entire codebase

### 4 Plots Generated:

1. **Coupling vs Complexity (Scatter)** - Shows the refactored class before/after with all other classes
2. **Package Treemap** - Visualizes complexity distribution across packages (target highlighted)
3. **Top 10 Violations (Bar Chart)** - Compares PMD violations before/after
4. **Slope Graph** - Shows metric improvements (WMC, CBO, LOC, RFC, LCOM)

## Usage Workflow

### Step 1: Baseline Audit (Before Refactoring)
```powershell
cd Refactoring_Lab\scripts
.\run_full_audit.ps1
```
**Note the timestamp directory created** (e.g., `2026-02-13_19-26`)

### Step 2: Perform Refactoring
Make your code changes for the instance (e.g., split JPAWeblogEntryManagerImpl)

### Step 3: Post-Refactoring Audit
```powershell
.\run_full_audit.ps1
```
**Note the new timestamp directory**

### Step 4: Generate Instance Visualizations
```powershell
.\run_instance_viz.ps1 `
    -InstanceName "Instance_1.1_JPAWeblogEntryManagerImpl" `
    -BeforeDir "../data_archive/2026-02-13_19-00" `
    -AfterDir "../data_archive/2026-02-13_19-26" `
    -TargetClass "JPAWeblogEntryManagerImpl"
```

**Or with auto-detection:**
```powershell
.\run_instance_viz.ps1 `
    -InstanceName "Instance_1.2_WeblogEntry" `
    -BeforeDir "../data_archive/2026-02-13_19-26" `
    -AfterDir "../data_archive/2026-02-14_10-15"
# Auto-detects class with biggest WMC reduction
```

## Output

Plots are saved in: `<AfterDir>/instance_plots/`
- `instance_01_coupling_complexity.png`
- `instance_02_package_treemap.png`
- `instance_03_top_violations.png`
- `instance_04_slope_graph.png`

## Example: Instance 1.1 (JPAWeblogEntryManagerImpl)

### Expected Improvements:
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **WMC** | 197 | ~120 | −77 (−39%) |
| **CBO** | 30 | 32 | +2 |
| **LOC** | 1394 | 1164 | −230 (−16.5%) |
| **Methods** | 44 | 44 (15 delegators) | 0 |

### Visualization Insights:
1. **Scatter Plot**: Shows JPAWeblogEntryManagerImpl moving from high-complexity zone to moderate zone
2. **Treemap**: Highlights `business.jpa` package complexity distribution
3. **Bar Chart**: Shows reduction in GodClass, ExcessiveImports, TooManyMethods violations
4. **Slope Graph**: Dramatic WMC and LOC reductions with slight CBO increase (acceptable trade-off)

## All 14 Instances

Run instance visualizations for each refactoring:

```powershell
# Instance 1.1: JPAWeblogEntryManagerImpl (Insufficient Modularization)
.\run_instance_viz.ps1 -InstanceName "Instance_1.1" -BeforeDir "<before>" -AfterDir "<after>" -TargetClass "JPAWeblogEntryManagerImpl"

# Instance 1.2: WeblogEntry (Insufficient Modularization)
.\run_instance_viz.ps1 -InstanceName "Instance_1.2" -BeforeDir "<before>" -AfterDir "<after>" -TargetClass "WeblogEntry"

# Instance 2.1: Blogroll (Deficient Encapsulation)
.\run_instance_viz.ps1 -InstanceName "Instance_2.1" -BeforeDir "<before>" -AfterDir "<after>" -TargetClass "Blogroll"

# ... and so on for all 14 instances
```

## Tips

1. **Always run audits before starting refactoring** to establish baseline
2. **Run audits immediately after refactoring** to capture changes
3. **Keep audit timestamps consistent** for tracking progress over time
4. **Use descriptive instance names** matching your refactoring plan
5. **Target class auto-detection** works best when you've made significant WMC reductions

## Integration with Reports

The instance plots can be embedded in your refactoring summary documents:

```markdown
## Visualization

![Coupling vs Complexity](../data_archive/2026-02-13_19-26/instance_plots/instance_01_coupling_complexity.png)
![Slope Graph](../data_archive/2026-02-13_19-26/instance_plots/instance_04_slope_graph.png)
```

## Troubleshooting

**Problem**: "Cannot find class in metrics"
- **Solution**: Check exact class name in `class.csv`; use fully qualified name

**Problem**: "PMD data not available"
- **Solution**: Ensure PMD runs in audit (may take time for large projects)

**Problem**: "No significant changes detected"
- **Solution**: Verify you're comparing correct before/after directories

## Architecture

```
run_full_audit.ps1          → Generate project-wide metrics
    ├─ CK Metrics
    ├─ Checkstyle
    ├─ PMD
    ├─ Designite
    ├─ metrics_plotter.py   → 5 basic trend charts
    ├─ advanced_plotter.py  → 14 advanced visualizations
    └─ report_generator.py  → HTML report

run_instance_viz.ps1        → Generate instance-specific comparisons
    └─ instance_plotter.py  → 4 before/after comparison plots
```

## Next Steps

After each refactoring instance:
1. ✅ Run post-refactoring audit
2. ✅ Generate instance visualizations
3. ✅ Update refactoring summary document
4. ✅ Commit changes with metrics in commit message
5. ✅ Move to next instance

---

**Last Updated**: February 13, 2026
**Version**: 1.0
