# Simple Plots Guide - Understanding Your Code Quality

## 🎯 What This Shows

These 6 plots show the **CURRENT state** of your repository - what's wrong RIGHT NOW and what needs fixing.

**No comparisons, no complexity - just clear answers to:**
- Which classes are the worst?
- Where should I focus my refactoring?
- How healthy is my codebase overall?

---

## 📊 The 6 Plots Explained

### 1️⃣ **1_worst_classes.png** - YOUR TO-DO LIST
**What it shows:** The 20 most complex classes ranked by WMC (complexity score)

**How to read it:**
- **Dark Red bars**: CRITICAL - Refactor these FIRST
- **Red bars**: HIGH priority - Refactor these NEXT
- **Orange bars**: MEDIUM priority - Keep an eye on these
- Numbers show: `WMC (CBO:X)` = Complexity (Coupling:X)

**Action:** Focus your refactoring on the top 3-5 classes

---

### 2️⃣ **2_danger_zones.png** - WORST OFFENDERS
**What it shows:** All classes plotted as Coupling (x) vs Complexity (y)

**How to read it:**
- Each dot = one class
- Bigger dots = more lines of code
- Red color = higher complexity
- **Top-right corner** = DANGER ZONE (high complexity + high coupling)
- Red dashed lines = top 10% threshold

**Action:** Classes in the danger zone (top-right) need urgent attention

---

### 3️⃣ **3_package_complexity.png** - WHERE TO FOCUS
**What it shows:** Which packages (folders) have the most total complexity

**How to read it:**
- Each bar = one package
- **Red bars** = Top 3 worst packages
- Blue bars = Other packages
- Numbers show: `Total Complexity (X classes)`

**Action:** Focus refactoring efforts on RED packages first

---

### 4️⃣ **4_complexity_distribution.png** - OVERALL HEALTH CHECK
**What it shows:** How many classes fall into each complexity category

**How to read it:**
- Green = Good (low complexity)
- Orange/Red = Problem areas (high complexity)
- Dark Red = Critical problems

**Stats box shows:**
- How many classes are "Low", "Medium", "High", "CRITICAL"
- What percentage of your codebase needs work

**Action:** Goal is to have most classes in green/yellow, minimize red

---

### 5️⃣ **5_god_classes.png** - CLASSES THAT DO TOO MUCH
**What it shows:** God classes (classes that do everything)

**How to read it:**
- Each bubble = one god class
- **Bubble size** = Lines of code (bigger = more LOC)
- **Position (x,y)** = Coupling vs Complexity
- **Color** = LCOM (lack of cohesion - red is bad)
- Labels show class names

**Action:** These classes need to be split into smaller, focused classes

---

### 6️⃣ **6_summary_dashboard.png** - THE BIG PICTURE
**What it shows:** 4-panel overview of everything

**Panels:**
1. **Pie Chart** (top-left): Percentage breakdown by complexity category
2. **Bar Chart** (top-right): Top 10 most complex classes
3. **Box Plot** (bottom-left): Coupling distribution across all classes
4. **Statistics** (bottom-right): Key numbers and metrics

**Action:** Share this with your team to show overall code quality

---

## 🚀 How to Use

### Generate plots for CURRENT state:
```powershell
cd Refactoring_Lab\scripts
.\run_simple_plots.ps1
```

### Generate plots for SPECIFIC audit:
```powershell
.\run_simple_plots.ps1 "..\data_archive\2026-02-13_19-26"
```

---

## 📈 What the Metrics Mean

### **WMC (Weighted Methods per Class)**
- **What:** Complexity score - sum of cyclomatic complexity of all methods
- **Good:** 0-30 (simple class)
- **Medium:** 31-75 (moderate complexity)
- **Bad:** 76-150 (very complex)
- **Critical:** 150+ (god class, needs refactoring NOW)

### **CBO (Coupling Between Objects)**
- **What:** How many other classes this class depends on
- **Good:** 0-10 (loosely coupled)
- **Medium:** 11-20 (moderate coupling)
- **Bad:** 20+ (tightly coupled, changes break many things)

### **LOC (Lines of Code)**
- **What:** Total lines in the class
- **Good:** 0-200 (focused class)
- **Medium:** 201-500 (getting large)
- **Bad:** 500+ (probably doing too much)

### **LCOM (Lack of Cohesion)**
- **What:** How well methods in a class work together
- **Good:** Low values (cohesive - methods use same data)
- **Bad:** High values (not cohesive - class does unrelated things)

---

## 🎯 Typical Refactoring Priority

Based on these plots, tackle issues in this order:

1. **Start with plot #1** - Pick top 3-5 worst classes
2. **Check plot #2** - Prioritize classes in danger zone (top-right)
3. **Check plot #5** - Confirm which are god classes
4. **Check plot #3** - Make sure you're working in high-impact packages
5. **Track plot #4** - Watch distribution shift left (toward green) as you refactor
6. **Use plot #6** - Report progress to stakeholders

---

## 💡 Example Interpretation

Looking at **JPAWeblogEntryManagerImpl**:
- ✅ Plot #1: Shows it's the 2nd worst class (WMC=155)
- ✅ Plot #2: It's in the danger zone (high complexity + high coupling)
- ✅ Plot #3: It's in the "jpa" package which has highest complexity
- ✅ Plot #5: It appears as a god class bubble
- ✅ **Decision:** This class is a top refactoring priority ← And we already refactored it! ✓

---

## 🔄 Tracking Progress

Run these plots:
- **Before starting refactoring** → Save plots as baseline
- **After each major refactoring** → Compare visually to see impact
- **Weekly/Sprint basis** → Track overall improvement trend

Watch for:
- Red bars shrinking in plot #1
- Danger zone emptying in plot #2
- Distribution shifting left (green) in plot #4
- Stats improving in plot #6

---

## ⚠️ Common Patterns

### Pattern 1: "Top-Heavy Distribution"
- Plot #4 shows most classes in red/orange range
- **Means:** Codebase has widespread complexity issues
- **Action:** Systematic refactoring needed across many classes

### Pattern 2: "A Few Bad Apples"
- Plot #4 mostly green/yellow, but plot #1 shows some critical classes
- **Means:** Generally healthy code with a few problem areas
- **Action:** Focus refactoring on the worst 5-10 classes

### Pattern 3: "Package Hotspot"
- Plot #3 shows one package way above others
- **Means:** One module/package has accumulated technical debt
- **Action:** Consider architectural refactoring of that entire package

---

## 📝 Quick Reference Card

| Plot | Answers | Look For | Action |
|------|---------|---------|---------|
| #1 Worst Classes | Which classes first? | Top 5 bars | Refactor these |
| #2 Danger Zones | Which are most critical? | Top-right quadrant | Urgent fixes |
| #3 Package Complexity | Which packages? | Red bars | Focus area |
| #4 Distribution | Overall health? | Color shift | Track progress |
| #5 God Classes | What to split? | Large bubbles | Split into smaller classes |
| #6 Dashboard | How are we doing? | All numbers | Team report |

---

**Generated by:** Refactoring Lab Simple Visualization System  
**Last Updated:** February 13, 2026  
**Version:** 1.0
