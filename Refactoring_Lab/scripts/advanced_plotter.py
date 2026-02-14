"""
Advanced Metrics Visualizer — Comprehensive Code Quality Analysis
Generates 14+ visualization types for deep insights into code structure
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import seaborn as sns
import xml.etree.ElementTree as ET
import os
import sys
from pathlib import Path
import squarify  # For treemap
from math import pi

# Configuration
plt.style.use('seaborn-v0_8-whitegrid')
FIGURE_DPI = 150
sns.set_palette("husl")

COLOR_SCHEMES = {
    'god_class': {'low': '#2ecc71', 'medium': '#f39c12', 'high': '#e74c3c'},
    'complexity': {'low': '#3498db', 'medium': '#9b59b6', 'high': '#e74c3c'},
    'quality': sns.color_palette("RdYlGn_r", 10)
}

def ensure_dir(path):
    """Create directory if it doesn't exist"""
    Path(path).mkdir(parents=True, exist_ok=True)

def load_ck_metrics(archive_dir):
    """Load CK metrics from class.csv"""
    ck_file = os.path.join(archive_dir, "class.csv")
    if not os.path.exists(ck_file):
        print(f"❌ CK metrics not found: {ck_file}")
        return None
    
    try:
        df = pd.read_csv(ck_file)
        # Clean class names
        df['class_simple'] = df['class'].apply(lambda x: x.split('.')[-1] if pd.notna(x) else 'Unknown')
        return df
    except Exception as e:
        print(f"❌ Error loading CK metrics: {e}")
        return None

def load_pmd_violations(archive_dir):
    """Load PMD violations from XML"""
    pmd_file = os.path.join(archive_dir, "pmd_report.xml")
    if not os.path.exists(pmd_file):
        return None
    
    violations = []
    try:
        tree = ET.parse(pmd_file)
        root = tree.getroot()
        for file_elem in root.findall('.//file'):
            for violation in file_elem.findall('violation'):
                violations.append({
                    'rule': violation.get('rule', 'Unknown'),
                    'priority': violation.get('priority', '3'),
                    'message': violation.text.strip() if violation.text else ''
                })
        return pd.DataFrame(violations)
    except Exception as e:
        print(f"⚠️ Could not parse PMD violations: {e}")
        return None

def load_history(history_file):
    """Load metrics history"""
    if not os.path.exists(history_file):
        return None
    try:
        df = pd.read_csv(history_file)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    except:
        return None

# ============================================================================
# CATEGORY 1: GOD CLASS & OOP STRUCTURAL ANALYSIS
# ============================================================================

def plot_god_class_quadrant(df, output_dir):
    """1. God Class Quadrant - CBO vs WMC with LOC size and LCOM color"""
    print("   [1/14] God Class Quadrant...")
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Filter valid data
    df_plot = df[(df['cbo'] > 0) & (df['wmc'] > 0) & (df['lcom'] >= 0)].copy()
    
    # Create scatter plot
    scatter = ax.scatter(
        df_plot['cbo'], 
        df_plot['wmc'],
        s=df_plot['loc'] * 2,  # Size by LOC
        c=df_plot['lcom'],      # Color by LCOM
        cmap='RdYlGn_r',        # Red = high LCOM (bad)
        alpha=0.6,
        edgecolors='black',
        linewidth=0.5
    )
    
    # Add threshold lines
    ax.axhline(y=47, color='red', linestyle='--', linewidth=2, alpha=0.5, label='WMC Threshold (47)')
    ax.axvline(x=14, color='red', linestyle='--', linewidth=2, alpha=0.5, label='CBO Threshold (14)')
    
    # Annotate God Classes
    god_classes = df_plot[(df_plot['wmc'] > 47) & (df_plot['cbo'] > 14)].nlargest(5, 'wmc')
    for _, row in god_classes.iterrows():
        ax.annotate(
            row['class_simple'],
            xy=(row['cbo'], row['wmc']),
            xytext=(10, 10),
            textcoords='offset points',
            fontsize=8,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', lw=1)
        )
    
    # Add quadrant labels
    ax.text(0.95, 0.95, 'GOD CLASS\nZONE', transform=ax.transAxes,
            fontsize=16, fontweight='bold', color='red', alpha=0.3,
            ha='right', va='top')
    
    ax.set_xlabel('Coupling Between Objects (CBO)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Weighted Methods per Class (WMC)', fontsize=12, fontweight='bold')
    ax.set_title('The "God Class" Quadrant\nSize = LOC | Color = Cohesion (LCOM)', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Lack of Cohesion (LCOM)\nHigher = Worse', fontsize=10, fontweight='bold')
    
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '01_god_class_quadrant.png'), dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close()

def plot_refactoring_target_map(df, output_dir):
    """2. Refactoring Target Map - LCOM vs WMC"""
    print("   [2/14] Refactoring Target Map...")
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    df_plot = df[(df['wmc'] > 0) & (df['lcom'] >= 0)].copy()
    
    scatter = ax.scatter(
        df_plot['lcom'],
        df_plot['wmc'],
        s=100,
        c=df_plot['cbo'],
        cmap='plasma',
        alpha=0.6,
        edgecolors='black',
        linewidth=0.5
    )
    
    # Add quadrant lines
    median_lcom = df_plot['lcom'].median()
    median_wmc = df_plot['wmc'].median()
    ax.axhline(y=median_wmc, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=median_lcom, color='gray', linestyle='--', alpha=0.5)
    
    # Add quadrant labels
    ax.text(0.75, 0.95, 'SPLIT CLASS\n(Unfocused + Complex)', 
            transform=ax.transAxes, fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='red', alpha=0.3))
    ax.text(0.05, 0.95, 'REFACTOR INTERNALS\n(Focused but Complex)', 
            transform=ax.transAxes, fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='orange', alpha=0.3))
    ax.text(0.05, 0.05, 'HEALTHY\n(Focused + Simple)', 
            transform=ax.transAxes, fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='green', alpha=0.3))
    
    ax.set_xlabel('Lack of Cohesion (LCOM)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Complexity (WMC)', fontsize=12, fontweight='bold')
    ax.set_title('Refactoring Target Map\nColor = Coupling (CBO)', 
                 fontsize=14, fontweight='bold', pad=20)
    
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Coupling (CBO)', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '02_refactoring_target_map.png'), dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close()

def plot_testing_nightmare(df, output_dir):
    """3. Testing Nightmare Chart - RFC vs WMC"""
    print("   [3/14] Testing Nightmare Chart...")
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    df_plot = df[(df['rfc'] > 0) & (df['wmc'] > 0)].copy()
    
    scatter = ax.scatter(
        df_plot['rfc'],
        df_plot['wmc'],
        s=df_plot['loc'],
        c=df_plot['cbo'],
        cmap='YlOrRd',
        alpha=0.6,
        edgecolors='black',
        linewidth=0.5
    )
    
    # Identify testing nightmares
    nightmares = df_plot[(df_plot['rfc'] > df_plot['rfc'].quantile(0.9)) & 
                         (df_plot['wmc'] > df_plot['wmc'].quantile(0.9))].nlargest(5, 'wmc')
    
    for _, row in nightmares.iterrows():
        ax.annotate(
            row['class_simple'],
            xy=(row['rfc'], row['wmc']),
            xytext=(10, 10),
            textcoords='offset points',
            fontsize=8,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='red', alpha=0.7),
            arrowprops=dict(arrowstyle='->', lw=1)
        )
    
    ax.set_xlabel('Response for Class (RFC)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Complexity (WMC)', fontsize=12, fontweight='bold')
    ax.set_title('The "Testing Nightmare" Chart\nHigh RFC + High WMC = Hard to Test\nSize = LOC | Color = Coupling', 
                 fontsize=14, fontweight='bold', pad=20)
    
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Coupling (CBO)', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '03_testing_nightmare.png'), dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close()

def plot_inheritance_depth(df, output_dir):
    """4. Inheritance Tree Depth Distribution"""
    print("   [4/14] Inheritance Depth Distribution...")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    df_plot = df[df['dit'] >= 0].copy()
    
    # Create histogram
    counts, bins, patches = ax.hist(df_plot['dit'], bins=range(0, int(df_plot['dit'].max()) + 2),
                                     color='skyblue', edgecolor='black', alpha=0.7)
    
    # Color bars > 5 in red
    for i, patch in enumerate(patches):
        if bins[i] > 5:
            patch.set_facecolor('red')
            patch.set_alpha(0.8)
    
    ax.axvline(x=5, color='red', linestyle='--', linewidth=2, label='Danger Zone (DIT > 5)')
    
    ax.set_xlabel('Depth of Inheritance Tree (DIT)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Classes', fontsize=12, fontweight='bold')
    ax.set_title('Inheritance Tree Depth Distribution\nDIT > 5 = Over-Abstracted Code', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    
    # Add statistics
    stats_text = f"Mean: {df_plot['dit'].mean():.1f}\nMax: {int(df_plot['dit'].max())}\nClasses with DIT>5: {len(df_plot[df_plot['dit'] > 5])}"
    ax.text(0.95, 0.95, stats_text, transform=ax.transAxes,
            fontsize=10, verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '04_inheritance_depth.png'), dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close()

# ============================================================================
# CATEGORY 2: ARCHITECTURAL HEALTH
# ============================================================================

def plot_hot_package_treemap(df, output_dir):
    """7. Hot Package Treemap"""
    print("   [5/14] Hot Package Treemap...")
    
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Extract package names
    df['package'] = df['class'].apply(lambda x: '.'.join(x.split('.')[:-1]) if pd.notna(x) else 'Unknown')
    
    # Aggregate by package
    package_stats = df.groupby('package').agg({
        'loc': 'sum',
        'wmc': 'sum',
        'cbo': 'mean'
    }).reset_index()
    
    # Filter top packages
    package_stats = package_stats.nlargest(20, 'loc')
    
    # Normalize CBO for color mapping
    norm = plt.Normalize(vmin=package_stats['cbo'].min(), vmax=package_stats['cbo'].max())
    colors = [plt.cm.RdYlGn_r(norm(value)) for value in package_stats['cbo']]
    
    # Create treemap
    squarify.plot(
        sizes=package_stats['loc'],
        label=[f"{pkg.split('.')[-1]}\nLOC:{int(loc)}\nWMC:{int(wmc)}" 
               for pkg, loc, wmc in zip(package_stats['package'], package_stats['loc'], package_stats['wmc'])],
        color=colors,
        alpha=0.7,
        text_kwargs={'fontsize': 8, 'weight': 'bold'},
        ax=ax
    )
    
    ax.set_title('Hot Package Treemap\nSize = Total LOC | Color = Average Coupling (CBO)\nRed = High Coupling', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.axis('off')
    
    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap=plt.cm.RdYlGn_r, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Average Coupling (CBO)', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '05_hot_package_treemap.png'), dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close()

# ============================================================================
# CATEGORY 3: QUALITY & MAINTAINABILITY
# ============================================================================

def plot_technical_debt_pyramid(df, output_dir):
    """8. Technical Debt Pyramid"""
    print("   [6/14] Technical Debt Pyramid...")
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    total_loc = df['loc'].sum()
    total_wmc = df['wmc'].sum()
    # Estimate technical debt (simple heuristic: 1 min per WMC point)
    technical_debt_hours = total_wmc / 60
    
    # Pyramid layers (normalized)
    layers = [
        ('Lines of Code', total_loc / 1000, 'lightblue'),
        ('Complexity', total_wmc / 100, 'orange'),
        ('Tech Debt (hrs)', technical_debt_hours, 'red')
    ]
    
    pyramid_width = 1.0
    y_position = 0
    
    for label, value, color in layers:
        width = pyramid_width * (value / max([v for _, v, _ in layers]))
        height = 0.3
        x_center = 0.5 - width / 2
        
        rect = Rectangle((x_center, y_position), width, height, 
                         facecolor=color, edgecolor='black', linewidth=2, alpha=0.7)
        ax.add_patch(rect)
        
        # Add label
        ax.text(0.5, y_position + height/2, f"{label}\n{value:.1f}",
                ha='center', va='center', fontsize=12, fontweight='bold')
        
        y_position += height + 0.05
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.2)
    ax.axis('off')
    ax.set_title('Technical Debt Pyramid\nWider Top = More Expensive Code', 
                 fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '06_technical_debt_pyramid.png'), dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close()

def plot_rule_violation_pareto(pmd_df, output_dir):
    """9. Rule Violation Pareto Chart"""
    print("   [7/14] Rule Violation Pareto...")
    
    if pmd_df is None or pmd_df.empty:
        print("      ⚠️ No PMD data available")
        return
    
    fig, ax1 = plt.subplots(figsize=(14, 8))
    
    # Count violations by rule
    violation_counts = pmd_df['rule'].value_counts().head(15)
    
    # Calculate cumulative percentage
    cumulative_percent = violation_counts.cumsum() / violation_counts.sum() * 100
    
    # Bar chart
    ax1.bar(range(len(violation_counts)), violation_counts.values, 
            color='steelblue', alpha=0.7, edgecolor='black')
    ax1.set_xlabel('Violation Type', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Frequency', fontsize=12, fontweight='bold', color='steelblue')
    ax1.set_xticklabels(violation_counts.index, rotation=45, ha='right', fontsize=9)
    ax1.set_xticks(range(len(violation_counts)))
    ax1.tick_params(axis='y', labelcolor='steelblue')
    
    # Line chart (cumulative)
    ax2 = ax1.twinx()
    ax2.plot(range(len(violation_counts)), cumulative_percent.values, 
             color='red', marker='o', linewidth=2, markersize=8)
    ax2.set_ylabel('Cumulative %', fontsize=12, fontweight='bold', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.axhline(y=80, color='red', linestyle='--', alpha=0.5, label='80% Line')
    ax2.set_ylim(0, 105)
    
    ax1.set_title('PMD Violation Pareto Chart\n80/20 Rule: Fix Top Issues First', 
                  fontsize=14, fontweight='bold', pad=20)
    ax1.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '07_rule_violation_pareto.png'), dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close()

def plot_cognitive_complexity_distribution(df, output_dir):
    """10. Cognitive Complexity Distribution"""
    print("   [8/14] Cognitive Complexity Distribution...")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Use WMC as proxy for cognitive complexity
    df_plot = df[df['wmc'] > 0]['wmc']
    
    # Violin plot
    parts = ax.violinplot([df_plot], positions=[0], widths=0.7, 
                          showmeans=True, showextrema=True, showmedians=True)
    
    for pc in parts['bodies']:
        pc.set_facecolor('skyblue')
        pc.set_alpha(0.7)
    
    # Add box plot overlay
    ax.boxplot([df_plot], positions=[0], widths=0.3, 
               boxprops=dict(color='darkblue', linewidth=2),
               medianprops=dict(color='red', linewidth=2))
    
    ax.set_ylabel('Complexity (WMC)', fontsize=12, fontweight='bold')
    ax.set_title('Cognitive Complexity Distribution\nHealthy = Fat Bottom, Thin Top\nInconsistent = Dumbbell Shape', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks([])
    ax.grid(axis='y', alpha=0.3)
    
    # Add statistics
    stats_text = f"Mean: {df_plot.mean():.1f}\nMedian: {df_plot.median():.1f}\nStd Dev: {df_plot.std():.1f}\n90th %ile: {df_plot.quantile(0.9):.1f}"
    ax.text(0.5, 0.95, stats_text, transform=ax.transAxes,
            fontsize=11, verticalalignment='top', horizontalalignment='center',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '08_cognitive_complexity_distribution.png'), dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close()

# ============================================================================
# CATEGORY 4: EVOLUTION (BEFORE/AFTER)
# ============================================================================

def plot_smell_reduction_stacked_bar(history_df, output_dir):
    """12. Smell Reduction Stacked Bar Chart"""
    print("   [9/14] Smell Reduction Chart...")
    
    if history_df is None or len(history_df) < 2:
        print("      ⚠️ Need at least 2 audit runs for trend analysis")
        return
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Prepare data
    timestamps = history_df['Timestamp'].dt.strftime('%Y-%m-%d %H:%M')
    
    # Stack data
    god_classes = history_df['God_Classes (CK)']
    design_smells = history_df['Design_Smells']
    arch_smells = history_df['Architecture_Smells']
    
    x = range(len(timestamps))
    
    ax.bar(x, arch_smells, label='Architecture Smells', color='#e74c3c', alpha=0.8)
    ax.bar(x, design_smells, bottom=arch_smells, label='Design Smells', color='#f39c12', alpha=0.8)
    ax.bar(x, god_classes, bottom=arch_smells+design_smells, label='God Classes', color='#e67e22', alpha=0.8)
    
    ax.set_xlabel('Audit Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Count', fontsize=12, fontweight='bold')
    ax.set_title('Smell Reduction Progress\nLower Bars = Better Code', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(timestamps, rotation=45, ha='right')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '09_smell_reduction.png'), dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close()

# ============================================================================
# CATEGORY 5: MANAGEMENT DASHBOARD
# ============================================================================

def plot_project_radar(df, pmd_df, output_dir):
    """13. Project Radar Chart"""
    print("   [10/14] Project Radar Chart...")
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    # Calculate metrics (normalized 0-100)
    metrics = {
        'Complexity': min(100, (df['wmc'].mean() / 50) * 100),
        'Coupling': min(100, (df['cbo'].mean() / 20) * 100),
        'Cohesion': min(100, (df['lcom'].mean() / 1.0) * 100),
        'Inheritance': min(100, (df['dit'].mean() / 5) * 100),
        'Size': min(100, (df['loc'].mean() / 500) * 100),
        'God Classes': min(100, (len(df[(df['wmc'] > 47) & (df['cbo'] > 14)]) / len(df)) * 200)
    }
    
    # Add PMD violations if available
    if pmd_df is not None and not pmd_df.empty:
        metrics['Style Violations'] = min(100, (len(pmd_df) / 2000) * 100)
    
    categories = list(metrics.keys())
    values = list(metrics.values())
    
    # Close the plot
    values += values[:1]
    
    # Calculate angles
    angles = [n / float(len(categories)) * 2 * pi for n in range(len(categories))]
    angles += angles[:1]
    
    # Plot
    ax.plot(angles, values, 'o-', linewidth=2, color='steelblue', label='Current State')
    ax.fill(angles, values, alpha=0.25, color='steelblue')
    
    # Add ideal state (all 20%)
    ideal = [20] * (len(categories) + 1)
    ax.plot(angles, ideal, 'o--', linewidth=2, color='green', alpha=0.5, label='Ideal State')
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=8)
    ax.set_title('Project Quality Radar\nSmaller Shape = Better Quality', 
                 fontsize=14, fontweight='bold', pad=30)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '10_project_radar.png'), dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close()

def plot_bus_factor(df, output_dir):
    """14. Bus Factor Analysis"""
    print("   [11/14] Bus Factor Analysis...")
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Get top 15 most complex classes
    top_classes = df.nlargest(15, 'wmc')[['class_simple', 'wmc', 'cbo', 'loc']]
    
    # Create horizontal bar chart
    y_pos = range(len(top_classes))
    colors = plt.cm.Reds(np.linspace(0.4, 0.9, len(top_classes)))
    
    bars = ax.barh(y_pos, top_classes['wmc'], color=colors, edgecolor='black', linewidth=1.5)
    
    # Add value labels
    for i, (idx, row) in enumerate(top_classes.iterrows()):
        ax.text(row['wmc'] + 2, i, f"WMC:{int(row['wmc'])} | LOC:{int(row['loc'])}", 
                va='center', fontsize=9, fontweight='bold')
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(top_classes['class_simple'], fontsize=10)
    ax.set_xlabel('Complexity (WMC)', fontsize=12, fontweight='bold')
    ax.set_title('Bus Factor Analysis\nTop 15 Critical Classes\nIf these developers leave, project dies', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3)
    
    # Add warning box
    ax.text(0.98, 0.02, '⚠️ HIGH RISK CLASSES\nDocument & Refactor ASAP', 
            transform=ax.transAxes, fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='red', alpha=0.7),
            ha='right', va='bottom', color='white')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '11_bus_factor.png'), dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close()

# ============================================================================
# ADDITIONAL SPECIALIZED PLOTS
# ============================================================================

def plot_complexity_heatmap(df, output_dir):
    """Bonus: Complexity Heatmap by Package"""
    print("   [12/14] Complexity Heatmap...")
    
    df['package'] = df['class'].apply(lambda x: '.'.join(x.split('.')[:-1]) if pd.notna(x) else 'Unknown')
    
    # Get top packages
    top_packages = df['package'].value_counts().head(20).index
    df_filtered = df[df['package'].isin(top_packages)]
    
    # Create pivot table
    pivot = df_filtered.pivot_table(
        values='wmc',
        index='package',
        aggfunc='mean'
    ).sort_values('wmc', ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 12))
    
    # Create heatmap
    sns.heatmap(pivot, annot=True, fmt='.1f', cmap='YlOrRd', 
                cbar_kws={'label': 'Average Complexity (WMC)'},
                linewidths=0.5, ax=ax)
    
    ax.set_title('Package Complexity Heatmap\nRed = High Average Complexity', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('')
    ax.set_ylabel('Package', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '12_complexity_heatmap.png'), dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close()

def plot_metric_correlation_matrix(df, output_dir):
    """Bonus: Metric Correlation Matrix"""
    print("   [13/14] Metric Correlation Matrix...")
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Select metrics
    metrics = ['wmc', 'cbo', 'rfc', 'lcom', 'loc', 'dit', 'noc']
    df_corr = df[metrics].corr()
    
    # Create heatmap
    sns.heatmap(df_corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={'label': 'Correlation'},
                ax=ax)
    
    ax.set_title('Metric Correlation Matrix\nRed = Positive Correlation | Blue = Negative', 
                 fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '13_metric_correlation.png'), dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close()

def plot_top_issues_summary(df, pmd_df, output_dir):
    """Bonus: Top Issues Summary Dashboard"""
    print("   [14/14] Top Issues Summary...")
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    # 1. Top God Classes
    ax1 = fig.add_subplot(gs[0, 0])
    god_classes = df[(df['wmc'] > 47) & (df['cbo'] > 14)].nlargest(10, 'wmc')
    ax1.barh(range(len(god_classes)), god_classes['wmc'], color='red', alpha=0.7)
    ax1.set_yticks(range(len(god_classes)))
    ax1.set_yticklabels(god_classes['class_simple'], fontsize=8)
    ax1.set_xlabel('WMC')
    ax1.set_title('Top 10 God Classes', fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    # 2. Complexity Distribution
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.hist(df['wmc'], bins=50, color='orange', alpha=0.7, edgecolor='black')
    ax2.axvline(df['wmc'].median(), color='red', linestyle='--', linewidth=2, label=f"Median: {df['wmc'].median():.1f}")
    ax2.set_xlabel('WMC')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Complexity Distribution', fontweight='bold')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    # 3. Coupling vs Cohesion
    ax3 = fig.add_subplot(gs[1, 0])
    scatter = ax3.scatter(df['cbo'], df['lcom'], s=df['wmc'], alpha=0.5, c=df['wmc'], cmap='viridis')
    ax3.set_xlabel('Coupling (CBO)')
    ax3.set_ylabel('Cohesion (LCOM)')
    ax3.set_title('Coupling vs Cohesion (size=WMC)', fontweight='bold')
    plt.colorbar(scatter, ax=ax3, label='WMC')
    ax3.grid(alpha=0.3)
    
    # 4. PMD Top Violations
    ax4 = fig.add_subplot(gs[1, 1])
    if pmd_df is not None and not pmd_df.empty:
        top_violations = pmd_df['rule'].value_counts().head(10)
        ax4.barh(range(len(top_violations)), top_violations.values, color='purple', alpha=0.7)
        ax4.set_yticks(range(len(top_violations)))
        ax4.set_yticklabels(top_violations.index, fontsize=8)
        ax4.set_xlabel('Count')
        ax4.set_title('Top 10 PMD Violations', fontweight='bold')
        ax4.grid(axis='x', alpha=0.3)
    else:
        ax4.text(0.5, 0.5, 'No PMD Data', ha='center', va='center', fontsize=14)
        ax4.axis('off')
    
    fig.suptitle('Top Issues Summary Dashboard', fontsize=16, fontweight='bold')
    
    plt.savefig(os.path.join(output_dir, '14_top_issues_summary.png'), dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close()

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python advanced_plotter.py <archive_directory>")
        sys.exit(1)
    
    archive_dir = sys.argv[1]
    ensure_dir(archive_dir)
    
    print("\n" + "="*80)
    print(" 📊 ADVANCED METRICS VISUALIZATION SUITE")
    print("="*80)
    
    # Load data
    print("\n📂 Loading data...")
    ck_df = load_ck_metrics(archive_dir)
    if ck_df is None:
        print("❌ Cannot proceed without CK metrics")
        sys.exit(1)
    
    pmd_df = load_pmd_violations(archive_dir)
    history_df = load_history("../metrics_history.csv")
    
    print(f"   ✅ Loaded {len(ck_df)} classes from CK metrics")
    if pmd_df is not None:
        print(f"   ✅ Loaded {len(pmd_df)} PMD violations")
    if history_df is not None:
        print(f"   ✅ Loaded {len(history_df)} historical audits")
    
    print("\n🎨 Generating visualizations...")
    
    # Category 1: God Class & OOP Analysis
    plot_god_class_quadrant(ck_df, archive_dir)
    plot_refactoring_target_map(ck_df, archive_dir)
    plot_testing_nightmare(ck_df, archive_dir)
    plot_inheritance_depth(ck_df, archive_dir)
    
    # Category 2: Architectural Health
    plot_hot_package_treemap(ck_df, archive_dir)
    
    # Category 3: Quality & Maintainability
    plot_technical_debt_pyramid(ck_df, archive_dir)
    plot_rule_violation_pareto(pmd_df, archive_dir)
    plot_cognitive_complexity_distribution(ck_df, archive_dir)
    
    # Category 4: Evolution
    plot_smell_reduction_stacked_bar(history_df, archive_dir)
    
    # Category 5: Management Dashboard
    plot_project_radar(ck_df, pmd_df, archive_dir)
    plot_bus_factor(ck_df, archive_dir)
    
    # Bonus plots
    plot_complexity_heatmap(ck_df, archive_dir)
    plot_metric_correlation_matrix(ck_df, archive_dir)
    plot_top_issues_summary(ck_df, pmd_df, archive_dir)
    
    print("\n" + "="*80)
    print(f"✅ Generated 14 advanced visualizations in: {archive_dir}")
    print("="*80)
    print("\nPlot Index:")
    print("  [01] God Class Quadrant")
    print("  [02] Refactoring Target Map")
    print("  [03] Testing Nightmare Chart")
    print("  [04] Inheritance Depth Distribution")
    print("  [05] Hot Package Treemap")
    print("  [06] Technical Debt Pyramid")
    print("  [07] Rule Violation Pareto")
    print("  [08] Cognitive Complexity Distribution")
    print("  [09] Smell Reduction (Timeline)")
    print("  [10] Project Radar Chart")
    print("  [11] Bus Factor Analysis")
    print("  [12] Complexity Heatmap")
    print("  [13] Metric Correlation Matrix")
    print("  [14] Top Issues Summary Dashboard")
    print()

if __name__ == "__main__":
    main()
