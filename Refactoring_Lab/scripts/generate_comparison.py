#!/usr/bin/env python3
"""
generate_comparison.py — Before/After Refactoring Comparison Generator

Reads system and class metrics from before/after archives and generates
comparison plots organized into two output folders:
    {output_dir}/system/    — whole-repo impact plots
    {output_dir}/class/     — per-refactored-class impact plots

Usage:
    python generate_comparison.py <before_dir> <after_dir> <output_dir> <class_names>

Example:
    python generate_comparison.py \
        "../data_archive/extract_method_1/before" \
        "../data_archive/extract_method_1/after" \
        "../data_archive/extract_method_1/comparison" \
        "org.apache.roller.weblogger.ui.rendering.model.PageModel"
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from math import pi
import os
import sys
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# STYLING
# =============================================================================

try:
    plt.style.use('seaborn-v0_8-whitegrid')
except:
    plt.style.use('ggplot')

COLOR_BEFORE = '#e74c3c'   # Red
COLOR_AFTER  = '#27ae60'   # Green
COLOR_NEUTRAL = '#95a5a6'  # Gray
COLOR_WARN   = '#f39c12'   # Orange
DPI = 150


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


# =============================================================================
# DATA LOADERS
# =============================================================================

def load_system_metrics(archive_dir):
    """Load system_metrics.csv from {archive_dir}/system/"""
    path = os.path.join(archive_dir, "system", "system_metrics.csv")
    if not os.path.exists(path):
        print(f"   [ERROR] System metrics not found: {path}")
        return None
    try:
        df = pd.read_csv(path)
        return df.iloc[0].to_dict()
    except Exception as e:
        print(f"   [ERROR] Could not read system metrics: {e}")
        return None


def load_class_metrics(archive_dir):
    """Load class_metrics.csv from {archive_dir}/class/"""
    path = os.path.join(archive_dir, "class", "class_metrics.csv")
    if not os.path.exists(path):
        print(f"   [ERROR] Class metrics not found: {path}")
        return None
    try:
        return pd.read_csv(path)
    except Exception as e:
        print(f"   [ERROR] Could not read class metrics: {e}")
        return None


def load_full_ck(archive_dir):
    """Load the full class.csv for context scatter plots."""
    path = os.path.join(archive_dir, "class.csv")
    if not os.path.exists(path):
        return None
    try:
        return pd.read_csv(path)
    except:
        return None


def find_class_in_df(df, class_name):
    """Flexible class name matching in a DataFrame."""
    if df is None or 'class' not in df.columns:
        return None
    exact = df[df['class'] == class_name]
    if not exact.empty:
        return exact.iloc[0]
    simple = class_name.split('.')[-1]
    partial = df[df['class'].str.endswith('.' + simple, na=False)]
    if not partial.empty:
        return partial.iloc[0]
    contains = df[df['class'].str.contains(simple, case=False, na=False)]
    if not contains.empty:
        return contains.iloc[0]
    return None


# =============================================================================
# SYSTEM-LEVEL PLOTS
# =============================================================================

def plot_system_radar(before, after, output_dir):
    """
    System Radar: Before = 100% baseline, After shown as % of before.
    Lower = better for all axes (LCOM inverted label: higher LCOM = worse).
    """
    print("   [SYS 1/4] System Health Radar...")

    categories = ['Avg WMC\n(Complexity)', 'Avg CBO\n(Coupling)', 'Avg LCOM\n(Low Cohesion)',
                   'God Class %', 'PMD\nViolations', 'Checkstyle\nErrors']

    # Metric extraction
    total_b = max(before.get('Total_Classes', 1), 1)
    total_a = max(after.get('Total_Classes', 1), 1)

    metric_keys = [
        ('Avg_WMC', None),
        ('Avg_CBO', None),
        ('Avg_LCOM', None),
        ('God_Classes', lambda v, t: (v / t) * 100),  # as percentage
        ('PMD_Violations', None),
        ('Checkstyle_Errors', None),
    ]

    b_raw = []
    a_raw = []
    for key, transform in metric_keys:
        bv = float(before.get(key, 0))
        av = float(after.get(key, 0))
        if transform:
            bv = transform(bv, total_b)
            av = transform(av, total_a)
        b_raw.append(bv)
        a_raw.append(av)

    # Normalize: Before = 100% baseline, After = percentage of before
    b_vals = [100.0] * len(categories)
    a_vals = []
    for bv, av in zip(b_raw, a_raw):
        if bv > 0:
            a_vals.append((av / bv) * 100)
        else:
            a_vals.append(100 if av == 0 else 200)

    N = len(categories)
    angles = [n / N * 2 * pi for n in range(N)]
    angles += angles[:1]
    b_vals += b_vals[:1]
    a_vals += a_vals[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    ax.plot(angles, b_vals, color=COLOR_BEFORE, linewidth=2.5, linestyle='--', label='BEFORE (100%)')
    ax.fill(angles, b_vals, color=COLOR_BEFORE, alpha=0.08)
    ax.plot(angles, a_vals, color=COLOR_AFTER, linewidth=2.5, label='AFTER')
    ax.fill(angles, a_vals, color=COLOR_AFTER, alpha=0.15)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=9, fontweight='bold')
    ax.set_title('System Health Radar\n(Before = 100% baseline, lower = better)',
                 fontsize=13, fontweight='bold', pad=25)
    ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.1), fontsize=10)

    # Add percentage annotations on each axis
    for i, (angle, a_pct) in enumerate(zip(angles[:-1], a_vals[:-1])):
        delta = a_pct - 100
        color = COLOR_AFTER if delta <= 0 else COLOR_BEFORE
        ax.text(angle, a_pct + 8, f'{delta:+.1f}%', ha='center', va='center',
                fontsize=8, fontweight='bold', color=color)

    plt.savefig(os.path.join(output_dir, 'system_radar.png'), dpi=DPI, bbox_inches='tight')
    plt.close()


def plot_system_bar_comparison(before, after, output_dir):
    """
    Tornado/butterfly chart showing % change per metric.
    Each metric gets its own row so scale differences don't matter.
    Green bar = improvement (reduction), Red bar = regression (increase).
    """
    print("   [SYS 2/4] System Metric Changes (Tornado Chart)...")

    metrics = [
        ('God Classes',         'God_Classes'),
        ('Avg WMC',             'Avg_WMC'),
        ('Avg CBO',             'Avg_CBO'),
        ('Avg LCOM',            'Avg_LCOM'),
        ('Max WMC',             'Max_WMC'),
        ('PMD Violations',      'PMD_Violations'),
        ('Checkstyle Errors',   'Checkstyle_Errors'),
        ('Design Smells',       'Design_Smells'),
        ('Arch. Smells',        'Architecture_Smells'),
    ]

    labels = []
    pct_changes = []
    abs_labels = []

    for display_name, key in metrics:
        bv = float(before.get(key, 0))
        av = float(after.get(key, 0))
        if bv == 0 and av == 0:
            continue  # skip metrics with no data
        if bv > 0:
            pct = ((av - bv) / bv) * 100
        elif av > 0:
            pct = 100.0  # went from 0 to something
        else:
            pct = 0.0
        labels.append(display_name)
        pct_changes.append(pct)
        abs_labels.append(f'{int(bv)} -> {int(av)}')

    if not labels:
        print("   [SKIP] No non-zero metrics to compare.")
        return

    fig, ax = plt.subplots(figsize=(12, max(5, len(labels) * 0.7)))

    y_pos = np.arange(len(labels))
    colors = [COLOR_AFTER if p <= 0 else COLOR_BEFORE for p in pct_changes]

    bars = ax.barh(y_pos, pct_changes, color=colors, alpha=0.8, edgecolor='black', height=0.6)

    # Value labels
    for i, (bar, pct, abs_lbl) in enumerate(zip(bars, pct_changes, abs_labels)):
        # Percentage label at end of bar
        x_pos = pct + (1.5 if pct >= 0 else -1.5)
        ha = 'left' if pct >= 0 else 'right'
        ax.text(x_pos, bar.get_y() + bar.get_height()/2,
                f'{pct:+.1f}%', va='center', ha=ha, fontweight='bold', fontsize=10)
        # Absolute values on the left margin
        ax.text(-0.5, bar.get_y() + bar.get_height()/2,
                f'({abs_lbl})', va='center', ha='right', fontsize=8, color='gray',
                transform=ax.get_yaxis_transform())

    ax.axvline(x=0, color='black', linewidth=1.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=11, fontweight='bold')
    ax.set_xlabel('% Change (negative = improvement)', fontsize=11, fontweight='bold')
    ax.set_title('System Metrics: % Change After Refactoring',
                 fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)

    # Add legend
    legend_elements = [
        mpatches.Patch(facecolor=COLOR_AFTER, edgecolor='black', label='Improved (reduced)'),
        mpatches.Patch(facecolor=COLOR_BEFORE, edgecolor='black', label='Worsened (increased)'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)

    plt.savefig(os.path.join(output_dir, 'system_bar_comparison.png'), dpi=DPI, bbox_inches='tight')
    plt.close()


def plot_complexity_distribution_shift(before, after, output_dir):
    """
    Stacked bar showing complexity bucket distribution before vs after.
    Buckets: Low (≤10), Medium (11-30), High (31-47), Critical (>47)
    """
    print("   [SYS 3/4] Complexity Distribution Shift...")

    categories = ['Low (≤10)', 'Medium (11-30)', 'High (31-47)', 'Critical (>47)']
    b_vals = [
        before.get('Classes_Low_WMC', 0),
        before.get('Classes_Med_WMC', 0),
        before.get('Classes_High_WMC', 0),
        before.get('Classes_Critical_WMC', 0),
    ]
    a_vals = [
        after.get('Classes_Low_WMC', 0),
        after.get('Classes_Med_WMC', 0),
        after.get('Classes_High_WMC', 0),
        after.get('Classes_Critical_WMC', 0),
    ]

    x = np.arange(len(categories))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x - width/2, b_vals, width, label='BEFORE', color=COLOR_BEFORE, alpha=0.8, edgecolor='black')
    ax.bar(x + width/2, a_vals, width, label='AFTER', color=COLOR_AFTER, alpha=0.8, edgecolor='black')

    # Value labels
    for i, (b, a) in enumerate(zip(b_vals, a_vals)):
        ax.text(i - width/2, b + 0.5, str(int(b)), ha='center', fontsize=9, fontweight='bold')
        ax.text(i + width/2, a + 0.5, str(int(a)), ha='center', fontsize=9, fontweight='bold')

    ax.set_ylabel('Number of Classes', fontsize=12)
    ax.set_title('Complexity Distribution Shift: Before vs After', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3)

    plt.savefig(os.path.join(output_dir, 'complexity_distribution_shift.png'), dpi=DPI, bbox_inches='tight')
    plt.close()


def plot_system_summary_table(before, after, output_dir):
    """
    Render a table image showing all system metrics with before/after/delta.
    """
    print("   [SYS 4/4] System Summary Table...")

    rows = [
        ('Total Classes',       'Total_Classes'),
        ('Total LOC',           'Total_LOC'),
        ('God Classes',         'God_Classes'),
        ('Max WMC',             'Max_WMC'),
        ('Avg WMC',             'Avg_WMC'),
        ('Median WMC',          'Median_WMC'),
        ('Max CBO',             'Max_CBO'),
        ('Avg CBO',             'Avg_CBO'),
        ('Median CBO',          'Median_CBO'),
        ('Avg LCOM',            'Avg_LCOM'),
        ('Avg RFC',             'Avg_RFC'),
        ('Avg DIT',             'Avg_DIT'),
        ('PMD Violations',      'PMD_Violations'),
        ('Checkstyle Errors',   'Checkstyle_Errors'),
        ('Design Smells',       'Design_Smells'),
        ('Arch. Smells',        'Architecture_Smells'),
        ('Impl. Smells',        'Implementation_Smells'),
        ('Classes Low WMC',     'Classes_Low_WMC'),
        ('Classes Med WMC',     'Classes_Med_WMC'),
        ('Classes High WMC',    'Classes_High_WMC'),
        ('Classes Critical WMC','Classes_Critical_WMC'),
    ]

    table_data = []
    cell_colors = []

    for label, key in rows:
        b_val = before.get(key, 0)
        a_val = after.get(key, 0)
        try:
            b_num = float(b_val)
            a_num = float(a_val)
            delta = a_num - b_num
            pct = ((a_num - b_num) / b_num * 100) if b_num != 0 else 0
            delta_str = f"{delta:+.1f} ({pct:+.1f}%)" if delta != 0 else "—"
        except:
            delta_str = "—"
            delta = 0

        # Format values
        if isinstance(b_val, float):
            b_str = f"{b_val:.2f}"
            a_str = f"{float(a_val):.2f}"
        else:
            b_str = str(b_val)
            a_str = str(a_val)

        table_data.append([label, b_str, a_str, delta_str])

        # Color: green if improved (delta < 0 for most metrics), red if worsened
        # For "Classes Low WMC" more is better, for others less is better
        better_if_higher = key in ['Classes_Low_WMC', 'Total_Classes']
        if delta == 0:
            row_color = ['white', 'white', 'white', 'white']
        elif (delta < 0 and not better_if_higher) or (delta > 0 and better_if_higher):
            row_color = ['white', 'white', '#d4edda', '#d4edda']  # light green
        else:
            row_color = ['white', 'white', '#f8d7da', '#f8d7da']  # light red
        cell_colors.append(row_color)

    fig, ax = plt.subplots(figsize=(12, max(8, len(table_data) * 0.4)))
    ax.axis('off')

    table = ax.table(
        cellText=table_data,
        colLabels=['Metric', 'Before', 'After', 'Delta (% Change)'],
        cellColours=cell_colors,
        colColours=['#2c3e50'] * 4,
        loc='center',
        cellLoc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.0, 1.5)

    # Style header
    for j in range(4):
        table[0, j].set_text_props(color='white', fontweight='bold')

    ax.set_title('System Metrics Summary: Before vs After',
                 fontsize=14, fontweight='bold', pad=20)

    plt.savefig(os.path.join(output_dir, 'system_summary_table.png'), dpi=DPI, bbox_inches='tight')
    plt.close()


# =============================================================================
# CLASS-LEVEL PLOTS
# =============================================================================

def plot_class_slope(before_row, after_row, class_name, output_dir):
    """
    Horizontal bar chart showing % change per metric for a specific class.
    Each metric on its own row avoids the scale-mismatch problem
    (e.g. LCOM=4130 vs CBO=26 would make a slope graph unreadable).
    """
    short = class_name.split('.')[-1]
    print(f"   [CLS 1/4] Metric Changes: {short}...")

    metrics = ['wmc', 'cbo', 'rfc', 'lcom', 'loc']
    labels = ['Complexity (WMC)', 'Coupling (CBO)', 'Response (RFC)',
              'Cohesion (LCOM)', 'Size (LOC)']

    b_vals = [float(before_row.get(m, 0)) for m in metrics]
    a_vals = [float(after_row.get(m, 0)) for m in metrics]

    # Also include violations if available
    extra_metrics = ['checkstyle_errors', 'pmd_violations', 'design_smells']
    extra_labels = ['Checkstyle Errors', 'PMD Violations', 'Design Smells']
    for em, el in zip(extra_metrics, extra_labels):
        bv = float(before_row.get(em, 0))
        av = float(after_row.get(em, 0))
        if bv > 0 or av > 0:  # only show if non-zero
            metrics.append(em)
            labels.append(el)
            b_vals.append(bv)
            a_vals.append(av)

    # Calculate % changes
    pct_changes = []
    abs_labels = []
    for bv, av in zip(b_vals, a_vals):
        if bv > 0:
            pct_changes.append(((av - bv) / bv) * 100)
        elif av > 0:
            pct_changes.append(100.0)
        else:
            pct_changes.append(0.0)
        abs_labels.append(f'{bv:.0f} -> {av:.0f}')

    fig, ax = plt.subplots(figsize=(11, max(5, len(labels) * 0.8)))

    y_pos = np.arange(len(labels))
    colors = [COLOR_AFTER if p <= 0 else COLOR_BEFORE for p in pct_changes]

    bars = ax.barh(y_pos, pct_changes, color=colors, alpha=0.8, edgecolor='black', height=0.6)

    # Value labels
    for i, (bar, pct, abs_lbl) in enumerate(zip(bars, pct_changes, abs_labels)):
        x_pos = pct + (2 if pct >= 0 else -2)
        ha = 'left' if pct >= 0 else 'right'
        ax.text(x_pos, bar.get_y() + bar.get_height()/2,
                f'{pct:+.1f}%  ({abs_lbl})', va='center', ha=ha,
                fontweight='bold', fontsize=9)

    ax.axvline(x=0, color='black', linewidth=1.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=11, fontweight='bold')
    ax.set_xlabel('% Change (negative = improvement)', fontsize=11, fontweight='bold')
    ax.set_title(f'Refactoring Impact: {short}\n(Per-Metric % Change)',
                 fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)

    legend_elements = [
        Line2D([0], [0], color=COLOR_AFTER, lw=3, label='Improved'),
        Line2D([0], [0], color=COLOR_BEFORE, lw=3, label='Worsened / Trade-off')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)

    plt.savefig(os.path.join(output_dir, f'{short}_slope.png'), dpi=DPI, bbox_inches='tight')
    plt.close()


def plot_class_radar(before_row, after_row, class_name, output_dir):
    """
    Radar chart: Before = 100% baseline, After shown as % of before.
    """
    short = class_name.split('.')[-1]
    print(f"   [CLS 2/4] Radar Chart: {short}...")

    metrics = ['wmc', 'cbo', 'rfc', 'lcom', 'loc']
    labels = ['Complexity', 'Coupling', 'Response', 'Cohesion', 'Size']

    b_norm = [100] * len(metrics)
    a_norm = []
    for m in metrics:
        b_val = float(before_row.get(m, 0))
        a_val = float(after_row.get(m, 0))
        if b_val > 0:
            a_norm.append((a_val / b_val) * 100)
        else:
            a_norm.append(100 if a_val == 0 else 200)

    N = len(labels)
    angles = [n / N * 2 * pi for n in range(N)]
    angles += angles[:1]
    b_norm += b_norm[:1]
    a_norm += a_norm[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(projection='polar'))
    ax.plot(angles, b_norm, color=COLOR_BEFORE, linewidth=2, linestyle='--', label='Before (100%)')
    ax.fill(angles, b_norm, color=COLOR_BEFORE, alpha=0.05)
    ax.plot(angles, a_norm, color=COLOR_AFTER, linewidth=2.5, label='After')
    ax.fill(angles, a_norm, color=COLOR_AFTER, alpha=0.15)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10, fontweight='bold')
    ax.set_title(f'Metric Trade-offs: {short}\n(Before = 100% baseline)', fontsize=12, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.1), fontsize=10)

    plt.savefig(os.path.join(output_dir, f'{short}_radar.png'), dpi=DPI, bbox_inches='tight')
    plt.close()


def plot_class_detail_table(before_row, after_row, class_name, output_dir):
    """
    Table image showing all metrics for the class: before / after / delta.
    """
    short = class_name.split('.')[-1]
    print(f"   [CLS 3/4] Detail Table: {short}...")

    metric_labels = [
        ('WMC (Complexity)', 'wmc'),
        ('CBO (Coupling)', 'cbo'),
        ('LOC (Lines of Code)', 'loc'),
        ('LCOM (Cohesion)', 'lcom'),
        ('RFC (Response)', 'rfc'),
        ('DIT (Inheritance)', 'dit'),
        ('NOC (Children)', 'noc'),
        ('Total Methods', 'totalMethodsQty'),
        ('Public Methods', 'publicMethodsQty'),
        ('Checkstyle Errors', 'checkstyle_errors'),
        ('PMD Violations', 'pmd_violations'),
        ('Design Smells', 'design_smells'),
    ]

    table_data = []
    cell_colors = []

    for label, key in metric_labels:
        b_val = float(before_row.get(key, 0))
        a_val = float(after_row.get(key, 0))
        delta = a_val - b_val
        pct = ((delta) / b_val * 100) if b_val != 0 else 0

        b_str = f"{b_val:.0f}" if b_val == int(b_val) else f"{b_val:.2f}"
        a_str = f"{a_val:.0f}" if a_val == int(a_val) else f"{a_val:.2f}"
        d_str = f"{delta:+.0f} ({pct:+.1f}%)" if delta != 0 else "—"

        table_data.append([label, b_str, a_str, d_str])

        if delta == 0:
            row_color = ['white'] * 4
        elif delta < 0:
            row_color = ['white', 'white', '#d4edda', '#d4edda']
        else:
            row_color = ['white', 'white', '#f8d7da', '#f8d7da']
        cell_colors.append(row_color)

    fig, ax = plt.subplots(figsize=(10, max(5, len(table_data) * 0.45)))
    ax.axis('off')

    table = ax.table(
        cellText=table_data,
        colLabels=['Metric', 'Before', 'After', 'Delta (% Change)'],
        cellColours=cell_colors,
        colColours=['#2c3e50'] * 4,
        loc='center',
        cellLoc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.0, 1.5)

    for j in range(4):
        table[0, j].set_text_props(color='white', fontweight='bold')

    ax.set_title(f'Class Detail: {short} — Before vs After',
                 fontsize=13, fontweight='bold', pad=20)

    plt.savefig(os.path.join(output_dir, f'{short}_detail_table.png'), dpi=DPI, bbox_inches='tight')
    plt.close()


def plot_class_context_scatter(before_full_df, after_full_df, before_row, after_row,
                                class_name, output_dir):
    """
    CBO vs WMC scatter of ALL classes (gray dots), with the refactored class
    highlighted: before position (red) → after position (green) with arrow.
    """
    short = class_name.split('.')[-1]
    print(f"   [CLS 4/4] Context Scatter: {short}...")

    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot all classes from AFTER snapshot as gray background
    if after_full_df is not None:
        ax.scatter(after_full_df['cbo'], after_full_df['wmc'],
                   s=30, c=COLOR_NEUTRAL, alpha=0.3, label='All Classes (After)')

    # Thresholds
    ax.axhline(y=47, color='red', linestyle='--', alpha=0.4, linewidth=1)
    ax.axvline(x=14, color='red', linestyle='--', alpha=0.4, linewidth=1)

    # Before position
    b_cbo = float(before_row.get('cbo', 0))
    b_wmc = float(before_row.get('wmc', 0))
    # After position
    a_cbo = float(after_row.get('cbo', 0))
    a_wmc = float(after_row.get('wmc', 0))

    ax.scatter(b_cbo, b_wmc, s=200, c=COLOR_BEFORE, marker='o', edgecolors='black',
               linewidths=2, zorder=10, label=f'{short} BEFORE')
    ax.scatter(a_cbo, a_wmc, s=200, c=COLOR_AFTER, marker='o', edgecolors='black',
               linewidths=2, zorder=10, label=f'{short} AFTER')

    # Arrow from before to after
    ax.annotate('', xy=(a_cbo, a_wmc), xytext=(b_cbo, b_wmc),
                arrowprops=dict(arrowstyle='->', color='black', lw=2.5),
                zorder=9)

    # Labels at both positions
    ax.annotate(f'BEFORE\nWMC={b_wmc:.0f}\nCBO={b_cbo:.0f}',
                xy=(b_cbo, b_wmc), xytext=(-60, 20), textcoords='offset points',
                fontsize=9, fontweight='bold', color=COLOR_BEFORE,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=COLOR_BEFORE))
    ax.annotate(f'AFTER\nWMC={a_wmc:.0f}\nCBO={a_cbo:.0f}',
                xy=(a_cbo, a_wmc), xytext=(20, -30), textcoords='offset points',
                fontsize=9, fontweight='bold', color=COLOR_AFTER,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=COLOR_AFTER))

    ax.set_xlabel('Coupling (CBO)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Complexity (WMC)', fontsize=12, fontweight='bold')
    ax.set_title(f'Refactoring Context: {short} Movement in Code Landscape',
                 fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(alpha=0.3)

    plt.savefig(os.path.join(output_dir, f'{short}_context_scatter.png'), dpi=DPI, bbox_inches='tight')
    plt.close()


# =============================================================================
# ADDITIONAL ANALYSIS PLOTS
# =============================================================================

def plot_top_improved_classes(before_full_df, after_full_df, output_dir, top_n=10):
    """
    Show top N classes with the biggest improvements (WMC + CBO reduction).
    Filters out zero-change classes to avoid meaningless all-zero charts.
    """
    print(f"   [ANALYSIS 1/4] Top {top_n} Most Improved Classes...")
    
    if before_full_df is None or after_full_df is None:
        print("   [SKIP] Missing full class data for improvement analysis.")
        return
    
    # Merge before and after on class name
    merged = before_full_df[['class', 'wmc', 'cbo']].merge(
        after_full_df[['class', 'wmc', 'cbo']], 
        on='class', 
        suffixes=('_before', '_after')
    )
    
    # Calculate improvement score (weighted: 70% WMC, 30% CBO reduction)
    merged['wmc_reduction'] = merged['wmc_before'] - merged['wmc_after']
    merged['cbo_reduction'] = merged['cbo_before'] - merged['cbo_after']
    merged['improvement_score'] = 0.7 * merged['wmc_reduction'] + 0.3 * merged['cbo_reduction']
    
    # Filter out zero-change classes
    improved = merged[merged['improvement_score'] > 0.01]
    top_improved = improved.nlargest(top_n, 'improvement_score')
    
    if top_improved.empty:
        # Create informative "no changes" placeholder
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.6, 'No Measurable Improvements Detected', 
                ha='center', va='center', fontsize=18, fontweight='bold', color='#2c3e50')
        ax.text(0.5, 0.4, f'All {len(merged)} matched classes had identical WMC & CBO values.\n'
                'This is expected if no refactoring was applied between snapshots.',
                ha='center', va='center', fontsize=12, color='gray')
        ax.axis('off')
        plt.savefig(os.path.join(output_dir, 'analysis_top_improved.png'), dpi=DPI, bbox_inches='tight')
        plt.close()
        print("   [INFO] No changes detected - placeholder generated.")
        return
    
    # Plot
    fig, ax = plt.subplots(figsize=(12, max(5, len(top_improved) * 0.7)))
    
    y_pos = np.arange(len(top_improved))
    short_names = [c.split('.')[-1] for c in top_improved['class']]
    scores = top_improved['improvement_score'].values
    wmc_reds = top_improved['wmc_reduction'].values
    cbo_reds = top_improved['cbo_reduction'].values
    
    bars = ax.barh(y_pos, scores, color=COLOR_AFTER, edgecolor='black', alpha=0.8)
    
    # Value labels with breakdown
    for i, (bar, score, wr, cr) in enumerate(zip(bars, scores, wmc_reds, cbo_reds)):
        ax.text(score + 0.5, bar.get_y() + bar.get_height()/2, 
                f'{score:.1f}  (WMC:{wr:+.0f}, CBO:{cr:+.0f})',
                va='center', fontweight='bold', fontsize=9)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(short_names, fontsize=10)
    ax.set_xlabel('Improvement Score (WMC*0.7 + CBO*0.3 reduction)', fontsize=11, fontweight='bold')
    ax.set_title(f'Top {len(top_improved)} Most Improved Classes', fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    
    plt.savefig(os.path.join(output_dir, 'analysis_top_improved.png'), dpi=DPI, bbox_inches='tight')
    plt.close()


def plot_top_worsened_classes(before_full_df, after_full_df, output_dir, top_n=10):
    """
    Show top N classes that regressed (WMC + CBO increase).
    """
    print(f"   [ANALYSIS 2/4] Top {top_n} Most Worsened Classes...")
    
    if before_full_df is None or after_full_df is None:
        print("   [SKIP] Missing full class data for regression analysis.")
        return
    
    # Merge before and after on class name
    merged = before_full_df[['class', 'wmc', 'cbo']].merge(
        after_full_df[['class', 'wmc', 'cbo']], 
        on='class', 
        suffixes=('_before', '_after')
    )
    
    # Calculate regression score
    merged['wmc_increase'] = merged['wmc_after'] - merged['wmc_before']
    merged['cbo_increase'] = merged['cbo_after'] - merged['cbo_before']
    merged['regression_score'] = 0.7 * merged['wmc_increase'] + 0.3 * merged['cbo_increase']
    
    # Filter: only classes that actually got worse
    worsened = merged[merged['regression_score'] > 0.01]
    top_worsened = worsened.nlargest(top_n, 'regression_score')
    
    if top_worsened.empty:
        fig, ax = plt.subplots(figsize=(12, 6))
        total_changed = len(merged[(merged['wmc_increase'].abs() > 0) | (merged['cbo_increase'].abs() > 0)])
        if total_changed > 0:
            msg = f'No classes worsened!\n{total_changed} classes changed, all improved or stayed stable.'
            color = COLOR_AFTER
        else:
            msg = f'No regressions detected.\nAll {len(merged)} matched classes had identical metrics.'
            color = '#2c3e50'
        ax.text(0.5, 0.5, msg, ha='center', va='center', fontsize=16, fontweight='bold', color=color)
        ax.axis('off')
        plt.savefig(os.path.join(output_dir, 'analysis_top_worsened.png'), dpi=DPI, bbox_inches='tight')
        plt.close()
        return
    
    # Plot
    fig, ax = plt.subplots(figsize=(12, max(5, len(top_worsened) * 0.7)))
    
    y_pos = np.arange(len(top_worsened))
    short_names = [c.split('.')[-1] for c in top_worsened['class']]
    scores = top_worsened['regression_score'].values
    wmc_inc = top_worsened['wmc_increase'].values
    cbo_inc = top_worsened['cbo_increase'].values
    
    bars = ax.barh(y_pos, scores, color=COLOR_BEFORE, edgecolor='black', alpha=0.8)
    
    for i, (bar, score, wi, ci) in enumerate(zip(bars, scores, wmc_inc, cbo_inc)):
        ax.text(score + 0.5, bar.get_y() + bar.get_height()/2, 
                f'+{score:.1f}  (WMC:{wi:+.0f}, CBO:{ci:+.0f})',
                va='center', fontweight='bold', fontsize=9)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(short_names, fontsize=10)
    ax.set_xlabel('Regression Score (WMC*0.7 + CBO*0.3 increase)', fontsize=11, fontweight='bold')
    ax.set_title(f'Top {len(top_worsened)} Most Worsened Classes (Trade-offs)', fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    
    plt.savefig(os.path.join(output_dir, 'analysis_top_worsened.png'), dpi=DPI, bbox_inches='tight')
    plt.close()


def plot_god_class_transitions(before_full_df, after_full_df, output_dir):
    """
    God Class transition matrix: 2x2 grid showing stayed-god, exited, entered, stayed-normal.
    Also lists actual class names for transitions (much more useful than a pie chart
    that gets overwhelmed by 97% 'Stayed Normal').
    """
    print(f"   [ANALYSIS 3/4] God Class Status Transitions...")
    
    if before_full_df is None or after_full_df is None:
        print("   [SKIP] Missing full class data for god class analysis.")
        return
    
    # Identify god classes in each snapshot (don't modify originals)
    b_god = (before_full_df['wmc'] > 47) & (before_full_df['cbo'] > 14)
    a_god = (after_full_df['wmc'] > 47) & (after_full_df['cbo'] > 14)
    
    before_copy = before_full_df[['class']].copy()
    before_copy['is_god'] = b_god
    after_copy = after_full_df[['class']].copy()
    after_copy['is_god'] = a_god
    
    # Merge
    merged = before_copy.merge(after_copy, on='class', suffixes=('_before', '_after'))
    
    # Categorize
    stayed_god  = merged[(merged['is_god_before']) & (merged['is_god_after'])]
    exited_god  = merged[(merged['is_god_before']) & (~merged['is_god_after'])]
    entered_god = merged[(~merged['is_god_before']) & (merged['is_god_after'])]
    stayed_norm = merged[(~merged['is_god_before']) & (~merged['is_god_after'])]
    
    counts = {
        'Stayed God': len(stayed_god),
        'Fixed (Exited God)': len(exited_god),
        'Regressed (Entered God)': len(entered_god),
        'Stayed Normal': len(stayed_norm),
    }
    
    total_before_god = counts['Stayed God'] + counts['Fixed (Exited God)']
    total_after_god = counts['Stayed God'] + counts['Regressed (Entered God)']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7), gridspec_kw={'width_ratios': [1, 1.3]})
    
    # --- Left: 2x2 Transition Matrix ---
    matrix = np.array([
        [counts['Stayed God'], counts['Fixed (Exited God)']],
        [counts['Regressed (Entered God)'], counts['Stayed Normal']],
    ])
    
    cell_colors_matrix = [
        ['#f8d7da', '#d4edda'],  # [stayed-god=bad, exited=good]
        ['#fff3cd', '#f0f0f0'],  # [entered=warn, stayed-normal=neutral]
    ]
    
    ax1.axis('off')
    table = ax1.table(
        cellText=[
            [f'Stayed God\n{counts["Stayed God"]}', f'Fixed!\n{counts["Fixed (Exited God)"]}'],
            [f'Regressed\n{counts["Regressed (Entered God)"]}', f'Stayed Normal\n{counts["Stayed Normal"]}'],
        ],
        rowLabels=['Was God', 'Was Normal'],
        colLabels=['Still God (After)', 'Normal (After)'],
        cellColours=cell_colors_matrix,
        rowColours=['#f0f0f0', '#f0f0f0'],
        colColours=['#f0f0f0', '#f0f0f0'],
        loc='center',
        cellLoc='center',
    )
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.3, 2.5)
    
    # Bold the transition matrix header
    for key, cell in table.get_celld().items():
        cell.set_edgecolor('black')
        cell.set_linewidth(1.5)
    
    ax1.set_title(f'God Class Transition Matrix\nBefore: {total_before_god} god classes  |  After: {total_after_god} god classes',
                  fontsize=12, fontweight='bold', pad=15)
    
    # --- Right: List actual class names for key transitions ---
    ax2.axis('off')
    
    y = 0.95
    ax2.text(0.05, y, 'Key Transitions:', fontsize=13, fontweight='bold', va='top',
             transform=ax2.transAxes)
    y -= 0.07
    
    def list_classes(ax, label, classes_df, color, y_start, max_show=8):
        y = y_start
        ax.text(0.05, y, f'{label} ({len(classes_df)}):', fontsize=11, fontweight='bold',
                color=color, va='top', transform=ax.transAxes)
        y -= 0.05
        if classes_df.empty:
            ax.text(0.08, y, '(none)', fontsize=10, color='gray', va='top',
                    transform=ax.transAxes)
            y -= 0.04
        else:
            for i, cls in enumerate(classes_df['class'].values[:max_show]):
                short = cls.split('.')[-1]
                ax.text(0.08, y, f'- {short}', fontsize=9, va='top',
                        transform=ax.transAxes)
                y -= 0.04
            if len(classes_df) > max_show:
                ax.text(0.08, y, f'  ... and {len(classes_df) - max_show} more', 
                        fontsize=9, color='gray', va='top', transform=ax.transAxes)
                y -= 0.04
        return y - 0.03
    
    y = list_classes(ax2, 'Fixed (Exited God Class)', exited_god, COLOR_AFTER, y)
    y = list_classes(ax2, 'Regressed (Entered God Class)', entered_god, COLOR_BEFORE, y)
    y = list_classes(ax2, 'Stayed God Class', stayed_god, COLOR_WARN, y)
    
    ax2.set_title('Affected Classes', fontsize=12, fontweight='bold', pad=15)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'analysis_god_class_transitions.png'), dpi=DPI, bbox_inches='tight')
    plt.close()


def plot_overall_impact_score(sys_before, sys_after, before_full_df, after_full_df, output_dir):
    """
    Overall refactoring impact dashboard with semicircle gauge and component breakdown.
    Score of 0% when nothing changed is explicitly labeled as 'No Change Detected'.
    """
    print(f"   [ANALYSIS 4/4] Overall Refactoring Impact Score...")
    
    # Calculate weighted impact scores (each component 0 to its max weight)
    components = []  # list of (label, score, max_weight, before_val, after_val)
    
    if sys_before and sys_after:
        # 1. God class reduction (20 points)
        god_before = float(sys_before.get('God_Classes', 0))
        god_after = float(sys_after.get('God_Classes', 0))
        if god_before > 0:
            s = max(0, ((god_before - god_after) / god_before) * 20)
            components.append(('God Classes', s, 20, god_before, god_after))
        
        # 2. Average complexity reduction (25 points)
        wmc_before = float(sys_before.get('Avg_WMC', 0))
        wmc_after = float(sys_after.get('Avg_WMC', 0))
        if wmc_before > 0:
            s = max(0, ((wmc_before - wmc_after) / wmc_before) * 25)
            components.append(('Avg Complexity', s, 25, wmc_before, wmc_after))
        
        # 3. Average coupling reduction (20 points)
        cbo_before = float(sys_before.get('Avg_CBO', 0))
        cbo_after = float(sys_after.get('Avg_CBO', 0))
        if cbo_before > 0:
            s = max(0, ((cbo_before - cbo_after) / cbo_before) * 20)
            components.append(('Avg Coupling', s, 20, cbo_before, cbo_after))
        
        # 4. PMD violation reduction (15 points)
        pmd_before = float(sys_before.get('PMD_Violations', 0))
        pmd_after = float(sys_after.get('PMD_Violations', 0))
        if pmd_before > 0:
            s = max(0, ((pmd_before - pmd_after) / pmd_before) * 15)
            components.append(('PMD Issues', s, 15, pmd_before, pmd_after))
        
        # 5. Checkstyle error reduction (10 points)
        cs_before = float(sys_before.get('Checkstyle_Errors', 0))
        cs_after = float(sys_after.get('Checkstyle_Errors', 0))
        if cs_before > 0:
            s = max(0, ((cs_before - cs_after) / cs_before) * 10)
            components.append(('Checkstyle', s, 10, cs_before, cs_after))
        
        # 6. Complexity distribution shift (10 points)
        low_before = float(sys_before.get('Classes_Low_WMC', 0))
        low_after = float(sys_after.get('Classes_Low_WMC', 0))
        total = float(sys_before.get('Total_Classes', 1))
        s = max(0, min(10, ((low_after - low_before) / max(total, 1)) * 100))
        components.append(('Low WMC Classes', s, 10, low_before, low_after))
    
    total_score = sum(c[1] for c in components)
    total_possible = sum(c[2] for c in components) if components else 100
    score_pct = (total_score / total_possible * 100) if total_possible > 0 else 0
    
    # Determine if this is a no-change scenario
    any_change = any(c[3] != c[4] for c in components) if components else False
    
    # --- Build figure ---
    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.2, 1], hspace=0.35)
    
    # --- Top: Semicircle gauge ---
    ax_gauge = fig.add_subplot(gs[0])
    
    # Draw semicircle gauge
    theta_bg = np.linspace(pi, 0, 100)
    r_outer, r_inner = 1.0, 0.6
    
    # Background arc (gray)
    for i in range(len(theta_bg) - 1):
        t = i / (len(theta_bg) - 1)  # 0 to 1
        if t < 0.4:
            c = '#e74c3c'  # red zone (0-40%)
        elif t < 0.7:
            c = '#f39c12'  # orange zone (40-70%)
        else:
            c = '#27ae60'  # green zone (70-100%)
        ax_gauge.fill_between(
            [np.cos(theta_bg[i]) * r_outer, np.cos(theta_bg[i+1]) * r_outer,
             np.cos(theta_bg[i+1]) * r_inner, np.cos(theta_bg[i]) * r_inner],
            [np.sin(theta_bg[i]) * r_outer, np.sin(theta_bg[i+1]) * r_outer,
             np.sin(theta_bg[i+1]) * r_inner, np.sin(theta_bg[i]) * r_inner],
            alpha=0.15, color=c
        )
    
    # Draw colored arcs using wedges
    from matplotlib.patches import Wedge
    
    # Background arc
    bg_wedge = Wedge((0, 0), r_outer, 0, 180, width=r_outer-r_inner,
                     facecolor='lightgray', edgecolor='black', linewidth=1.5, alpha=0.3)
    ax_gauge.add_patch(bg_wedge)
    
    # Score arc (colored by score level)
    if score_pct >= 70:
        gauge_color = COLOR_AFTER
    elif score_pct >= 40:
        gauge_color = COLOR_WARN
    else:
        gauge_color = COLOR_BEFORE
    
    # The score fills from left (180 degrees) to the score position
    score_angle = 180 - (score_pct / 100) * 180
    if score_pct > 0.5:
        score_wedge = Wedge((0, 0), r_outer, score_angle, 180, width=r_outer-r_inner,
                            facecolor=gauge_color, edgecolor='black', linewidth=1.5, alpha=0.7)
        ax_gauge.add_patch(score_wedge)
    
    # Needle
    needle_angle = pi - (score_pct / 100) * pi
    needle_x = np.cos(needle_angle) * (r_inner - 0.05)
    needle_y = np.sin(needle_angle) * (r_inner - 0.05)
    ax_gauge.plot([0, needle_x], [0, needle_y], color='black', linewidth=3, zorder=10)
    ax_gauge.plot(0, 0, 'ko', markersize=8, zorder=11)
    
    # Score text in center
    if not any_change:
        label = 'No Change Detected'
    elif score_pct >= 70:
        label = 'Excellent!'
    elif score_pct >= 40:
        label = 'Good Progress'
    elif score_pct > 0:
        label = 'Needs More Work'
    else:
        label = 'No Improvement'
    
    ax_gauge.text(0, -0.15, f'{score_pct:.1f}%', ha='center', va='center',
                  fontsize=28, fontweight='bold', color=gauge_color if any_change else '#2c3e50')
    ax_gauge.text(0, -0.35, label, ha='center', va='center',
                  fontsize=14, fontweight='bold', color='gray')
    
    # Scale labels
    ax_gauge.text(-r_outer - 0.05, -0.05, '0%', ha='center', fontsize=10, color='gray')
    ax_gauge.text(r_outer + 0.05, -0.05, '100%', ha='center', fontsize=10, color='gray')
    ax_gauge.text(0, r_outer + 0.08, '50%', ha='center', fontsize=10, color='gray')
    
    ax_gauge.set_xlim(-1.4, 1.4)
    ax_gauge.set_ylim(-0.5, 1.3)
    ax_gauge.set_aspect('equal')
    ax_gauge.axis('off')
    ax_gauge.set_title('Overall Refactoring Impact Score', fontsize=16, fontweight='bold', pad=10)
    
    # --- Bottom: Component breakdown table ---
    ax_table = fig.add_subplot(gs[1])
    ax_table.axis('off')
    
    if components:
        table_data = []
        cell_colors = []
        for label, score, weight, bv, av in components:
            pct = (score / weight * 100) if weight > 0 else 0
            delta = av - bv
            delta_pct = ((av - bv) / bv * 100) if bv > 0 else 0
            
            table_data.append([
                label,
                f'{bv:.1f}',
                f'{av:.1f}',
                f'{delta_pct:+.1f}%' if delta != 0 else 'No change',
                f'{score:.1f} / {weight}',
                f'{pct:.0f}%',
            ])
            
            if delta == 0:
                row_color = ['white'] * 6
            elif delta < 0:  # improved
                row_color = ['white', 'white', '#d4edda', '#d4edda', '#d4edda', '#d4edda']
            else:  # worsened
                row_color = ['white', 'white', '#f8d7da', '#f8d7da', '#f8d7da', '#f8d7da']
            cell_colors.append(row_color)
        
        table = ax_table.table(
            cellText=table_data,
            colLabels=['Component', 'Before', 'After', 'Change', 'Score', 'Achievement'],
            cellColours=cell_colors,
            colColours=['#2c3e50'] * 6,
            loc='center',
            cellLoc='center',
        )
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.0, 1.6)
        
        for j in range(6):
            table[0, j].set_text_props(color='white', fontweight='bold')
        
        ax_table.set_title('Score Breakdown by Component', fontsize=13, fontweight='bold', pad=15)
    
    plt.savefig(os.path.join(output_dir, 'analysis_overall_impact.png'), dpi=DPI, bbox_inches='tight')
    plt.close()


# =============================================================================
# MAIN
# =============================================================================

def main():
    if len(sys.argv) < 4:
        print("Usage: python generate_comparison.py <before_dir> <after_dir> <output_dir> [<class_names>]")
        print("  <class_names>: comma-separated FQCNs, or 'NONE' to skip class plots (default: NONE)")
        sys.exit(1)

    before_dir = sys.argv[1]
    after_dir = sys.argv[2]
    output_dir = sys.argv[3]
    class_names_arg = sys.argv[4] if len(sys.argv) > 4 else "NONE"

    skip_class_plots = (class_names_arg.strip().upper() == "NONE")
    class_names = [] if skip_class_plots else [c.strip() for c in class_names_arg.split(',') if c.strip()]

    # Create output directories
    system_out = os.path.join(output_dir, "system")
    class_out = os.path.join(output_dir, "class")
    ensure_dir(system_out)
    if not skip_class_plots:
        ensure_dir(class_out)

    print("=" * 60)
    print("  REFACTORING COMPARISON GENERATOR")
    print("=" * 60)

    # --- Load Data ---
    print("\n--- Loading Data ---")
    sys_before = load_system_metrics(before_dir)
    sys_after = load_system_metrics(after_dir)
    cls_before_df = load_class_metrics(before_dir)
    cls_after_df = load_class_metrics(after_dir)
    full_ck_before = load_full_ck(before_dir)
    full_ck_after = load_full_ck(after_dir)

    # --- System-Level Plots ---
    if sys_before and sys_after:
        print("\n--- System-Level Plots ---")
        plot_system_radar(sys_before, sys_after, system_out)
        plot_system_bar_comparison(sys_before, sys_after, system_out)
        plot_complexity_distribution_shift(sys_before, sys_after, system_out)
        plot_system_summary_table(sys_before, sys_after, system_out)
        print(f"   [OK] 4 system plots saved to {system_out}")
    else:
        print("\n   [SKIP] System plots — missing before or after system metrics.")

    # --- Class-Level Plots ---
    if skip_class_plots:
        print("\n   [SKIP] Class plots — no class names specified (NONE).")
    elif cls_before_df is not None and cls_after_df is not None:
        print("\n--- Class-Level Plots ---")
        for class_name in class_names:
            short = class_name.split('.')[-1]
            print(f"\n   Processing class: {short}")

            # Find rows in class metrics
            b_match = cls_before_df[cls_before_df['class'].str.contains(short, case=False, na=False)]
            a_match = cls_after_df[cls_after_df['class'].str.contains(short, case=False, na=False)]

            if b_match.empty or a_match.empty:
                # Fallback: try from full CK data
                b_row = find_class_in_df(full_ck_before, class_name)
                a_row = find_class_in_df(full_ck_after, class_name)
                if b_row is None or a_row is None:
                    print(f"   [SKIP] Class '{short}' not found in before/after data.")
                    continue
            else:
                b_row = b_match.iloc[0]
                a_row = a_match.iloc[0]

            plot_class_slope(b_row, a_row, class_name, class_out)
            plot_class_radar(b_row, a_row, class_name, class_out)
            plot_class_detail_table(b_row, a_row, class_name, class_out)
            plot_class_context_scatter(full_ck_before, full_ck_after, b_row, a_row,
                                       class_name, class_out)
            print(f"   [OK] 4 class plots saved for {short}")
    else:
        print("\n   [SKIP] Class plots — missing before or after class metrics.")

    # --- Additional Analysis Plots ---
    print("\n--- Additional Analysis ---")
    plot_top_improved_classes(full_ck_before, full_ck_after, system_out, top_n=10)
    plot_top_worsened_classes(full_ck_before, full_ck_after, system_out, top_n=10)
    plot_god_class_transitions(full_ck_before, full_ck_after, system_out)
    plot_overall_impact_score(sys_before, sys_after, full_ck_before, full_ck_after, system_out)
    print(f"   [OK] 4 analysis plots saved to {system_out}")

    print(f"\n{'=' * 60}")
    print(f"  COMPARISON COMPLETE")
    print(f"  System plots: {system_out} (8 plots)")
    if not skip_class_plots:
        print(f"  Class plots:  {class_out} (4 plots per class x {len(class_names)} classes)")
    else:
        print(f"  Class plots:  skipped (no class names)")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
