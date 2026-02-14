#!/usr/bin/env python3
"""
Simple Current-State Visualizations
Generates 6 clear plots showing what's wrong with your code RIGHT NOW

Usage: python simple_plots.py <latest_audit_directory>
Example: python simple_plots.py "../data_archive/2026-02-13_19-26"
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configuration
DPI = 150
FIGSIZE = (14, 8)

def load_data(archive_dir):
    """Load CK metrics"""
    class_csv = os.path.join(archive_dir, "class.csv")
    if not os.path.exists(class_csv):
        print(f"ERROR: Cannot find {class_csv}")
        sys.exit(1)
    return pd.read_csv(class_csv)

# ============================================================================
# PLOT 1: TOP 20 WORST CLASSES (Bar Chart)
# ============================================================================
def plot_worst_classes(df, output_dir):
    """Shows the 20 most complex classes - THESE ARE YOUR PROBLEMS"""
    print("   [1/6] Top 20 Most Complex Classes...")
    
    # Get top 20 by WMC
    worst = df.nlargest(20, 'wmc')[['class', 'wmc', 'cbo']].copy()
    worst['short_name'] = worst['class'].apply(lambda x: x.split('.')[-1])
    
    fig, ax = plt.subplots(figsize=FIGSIZE)
    
    # Create bars
    bars = ax.barh(range(len(worst)), worst['wmc'], color='#e74c3c', alpha=0.8)
    
    # Color code by severity
    for i, (idx, row) in enumerate(worst.iterrows()):
        if row['wmc'] > 150:
            bars[i].set_color('#c0392b')  # Dark red - CRITICAL
        elif row['wmc'] > 100:
            bars[i].set_color('#e74c3c')  # Red - HIGH
        elif row['wmc'] > 50:
            bars[i].set_color('#e67e22')  # Orange - MEDIUM
    
    # Add value labels
    for i, (idx, row) in enumerate(worst.iterrows()):
        ax.text(row['wmc'] + 2, i, f"{int(row['wmc'])} (CBO:{int(row['cbo'])})", 
                va='center', fontsize=9, fontweight='bold')
    
    ax.set_yticks(range(len(worst)))
    ax.set_yticklabels(worst['short_name'], fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel('WMC (Complexity)', fontsize=13, fontweight='bold')
    ax.set_title('TOP 20 MOST COMPLEX CLASSES → REFACTOR THESE FIRST', 
                 fontsize=15, fontweight='bold', pad=15)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#c0392b', label='CRITICAL (>150)'),
        Patch(facecolor='#e74c3c', label='HIGH (100-150)'),
        Patch(facecolor='#e67e22', label='MEDIUM (50-100)')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '1_worst_classes.png'), dpi=DPI, bbox_inches='tight')
    plt.close()

# ============================================================================
# PLOT 2: COUPLING vs COMPLEXITY SCATTER (All Classes)
# ============================================================================
def plot_coupling_complexity(df, output_dir):
    """Shows which classes have BOTH high complexity AND high coupling - DANGER ZONE"""
    print("   [2/6] Coupling vs Complexity (Danger Zones)...")
    
    fig, ax = plt.subplots(figsize=FIGSIZE)
    
    # Create scatter with color based on LOC
    scatter = ax.scatter(df['cbo'], df['wmc'], 
                        s=df['loc']*0.5,  # Size by LOC
                        c=df['wmc'], cmap='YlOrRd', 
                        alpha=0.6, edgecolors='black', linewidths=0.5)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('WMC (Complexity)', fontsize=11, fontweight='bold')
    
    # Mark danger zones
    danger_threshold_wmc = df['wmc'].quantile(0.9)  # Top 10%
    danger_threshold_cbo = df['cbo'].quantile(0.9)
    
    ax.axhline(y=danger_threshold_wmc, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Top 10% Complexity')
    ax.axvline(x=danger_threshold_cbo, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Top 10% Coupling')
    
    # Annotate worst class
    worst_idx = df['wmc'].idxmax()
    worst = df.loc[worst_idx]
    ax.annotate(worst['class'].split('.')[-1], 
                xy=(worst['cbo'], worst['wmc']),
                xytext=(10, 10), textcoords='offset points',
                fontsize=11, fontweight='bold', color='darkred',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    
    ax.set_xlabel('CBO (Coupling Between Objects)', fontsize=13, fontweight='bold')
    ax.set_ylabel('WMC (Weighted Methods per Class)', fontsize=13, fontweight='bold')
    ax.set_title('DANGER ZONE: Classes with High Complexity + High Coupling', 
                 fontsize=15, fontweight='bold', pad=15)
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(alpha=0.3, linestyle='--')
    
    # Add quadrant labels
    max_cbo = df['cbo'].max()
    max_wmc = df['wmc'].max()
    ax.text(danger_threshold_cbo*1.1, max_wmc*0.95, 'REFACTOR NOW!', 
            fontsize=12, fontweight='bold', color='darkred',
            bbox=dict(boxstyle='round', facecolor='#ffcccc', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '2_danger_zones.png'), dpi=DPI, bbox_inches='tight')
    plt.close()

# ============================================================================
# PLOT 3: PACKAGE COMPLEXITY DISTRIBUTION
# ============================================================================
def plot_package_complexity(df, output_dir):
    """Shows which packages have the most complexity - WHERE TO FOCUS"""
    print("   [3/6] Package Complexity Distribution...")
    
    # Extract package names
    df['package'] = df['class'].apply(lambda x: '.'.join(x.split('.')[:-2]) if x.count('.') >= 2 else 'root')
    
    # Group by package
    pkg_stats = df.groupby('package').agg({
        'wmc': 'sum',
        'cbo': 'mean',
        'loc': 'sum',
        'class': 'count'
    }).reset_index()
    pkg_stats.columns = ['package', 'total_wmc', 'avg_cbo', 'total_loc', 'class_count']
    
    # Sort and take top 15
    pkg_stats = pkg_stats.nlargest(15, 'total_wmc')
    pkg_stats['short_pkg'] = pkg_stats['package'].apply(lambda x: x.split('.')[-1] if '.' in x else x)
    
    fig, ax = plt.subplots(figsize=FIGSIZE)
    
    # Create bars
    bars = ax.bar(range(len(pkg_stats)), pkg_stats['total_wmc'], color='#3498db', alpha=0.8)
    
    # Color top 3 differently
    for i in range(min(3, len(bars))):
        bars[i].set_color('#e74c3c')
    
    # Add value labels
    for i, (idx, row) in enumerate(pkg_stats.iterrows()):
        ax.text(i, row['total_wmc'] + 50, 
                f"{int(row['total_wmc'])}\n({int(row['class_count'])} classes)", 
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    ax.set_xticks(range(len(pkg_stats)))
    ax.set_xticklabels(pkg_stats['short_pkg'], rotation=45, ha='right', fontsize=10)
    ax.set_ylabel('Total Complexity (Sum of WMC)', fontsize=13, fontweight='bold')
    ax.set_title('PACKAGE COMPLEXITY → Focus refactoring on RED packages', 
                 fontsize=15, fontweight='bold', pad=15)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '3_package_complexity.png'), dpi=DPI, bbox_inches='tight')
    plt.close()

# ============================================================================
# PLOT 4: COMPLEXITY DISTRIBUTION (Histogram)
# ============================================================================
def plot_complexity_distribution(df, output_dir):
    """Shows how many classes are in each complexity range - OVERALL HEALTH CHECK"""
    print("   [4/6] Complexity Distribution...")
    
    fig, ax = plt.subplots(figsize=FIGSIZE)
    
    # Create histogram with custom bins
    bins = [0, 10, 20, 30, 50, 75, 100, 150, 200, 300]
    counts, edges, patches = ax.hist(df['wmc'], bins=bins, color='#3498db', alpha=0.7, edgecolor='black')
    
    # Color code by severity
    colors = ['#27ae60', '#27ae60', '#2ecc71', '#f39c12', '#e67e22', '#e74c3c', '#c0392b', '#8b0000', '#4a0000']
    for patch, color in zip(patches, colors):
        patch.set_facecolor(color)
    
    # Add count labels on bars
    for i, (count, edge) in enumerate(zip(counts, edges[:-1])):
        if count > 0:
            ax.text(edge + (edges[i+1]-edge)/2, count + 2, 
                   f'{int(count)}', ha='center', va='bottom', 
                   fontsize=10, fontweight='bold')
    
    ax.set_xlabel('WMC (Complexity)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Number of Classes', fontsize=13, fontweight='bold')
    ax.set_title(f'COMPLEXITY DISTRIBUTION → {len(df[df["wmc"]>50])} classes need attention', 
                 fontsize=15, fontweight='bold', pad=15)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add statistics box
    stats_text = f'Total Classes: {len(df)}\n'
    stats_text += f'Low (0-30): {len(df[df["wmc"]<=30])} ({len(df[df["wmc"]<=30])/len(df)*100:.1f}%)\n'
    stats_text += f'Medium (31-75): {len(df[(df["wmc"]>30) & (df["wmc"]<=75)])} ({len(df[(df["wmc"]>30) & (df["wmc"]<=75)])/len(df)*100:.1f}%)\n'
    stats_text += f'High (76-150): {len(df[(df["wmc"]>75) & (df["wmc"]<=150)])} ({len(df[(df["wmc"]>75) & (df["wmc"]<=150)])/len(df)*100:.1f}%)\n'
    stats_text += f'CRITICAL (>150): {len(df[df["wmc"]>150])} ({len(df[df["wmc"]>150])/len(df)*100:.1f}%)'
    
    ax.text(0.98, 0.97, stats_text, transform=ax.transAxes,
            fontsize=11, verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '4_complexity_distribution.png'), dpi=DPI, bbox_inches='tight')
    plt.close()

# ============================================================================
# PLOT 5: GOD CLASSES (Bubble Chart)
# ============================================================================
def plot_god_classes(df, output_dir):
    """Shows god classes with multiple dimensions - SIZE MATTERS"""
    print("   [5/6] God Classes (Multi-Dimensional)...")
    
    # Define god class threshold (top 10% in both WMC and LOC)
    wmc_threshold = df['wmc'].quantile(0.90)
    loc_threshold = df['loc'].quantile(0.90)
    
    god_classes = df[(df['wmc'] > wmc_threshold) | (df['loc'] > loc_threshold)].copy()
    god_classes['short_name'] = god_classes['class'].apply(lambda x: x.split('.')[-1])
    
    fig, ax = plt.subplots(figsize=FIGSIZE)
    
    # Create bubble chart
    scatter = ax.scatter(god_classes['cbo'], god_classes['wmc'], 
                        s=god_classes['loc']*2,  # Bigger bubble = more lines
                        c=god_classes['lcom'], cmap='RdYlGn_r',
                        alpha=0.6, edgecolors='black', linewidths=2)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('LCOM (Lack of Cohesion)\nHigher = Worse', fontsize=11, fontweight='bold')
    
    # Annotate each god class
    for idx, row in god_classes.iterrows():
        ax.annotate(row['short_name'], 
                   xy=(row['cbo'], row['wmc']),
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=9, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    ax.set_xlabel('CBO (Coupling)', fontsize=13, fontweight='bold')
    ax.set_ylabel('WMC (Complexity)', fontsize=13, fontweight='bold')
    ax.set_title(f'GOD CLASSES ({len(god_classes)} found) → Bubble size = Lines of Code', 
                 fontsize=15, fontweight='bold', pad=15)
    ax.grid(alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '5_god_classes.png'), dpi=DPI, bbox_inches='tight')
    plt.close()

# ============================================================================
# PLOT 6: SUMMARY DASHBOARD (4-Panel)
# ============================================================================
def plot_summary_dashboard(df, output_dir):
    """Creates a 4-panel overview - THE BIG PICTURE"""
    print("   [6/6] Summary Dashboard...")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Panel 1: Complexity Categories (Pie)
    low = len(df[df['wmc'] <= 30])
    medium = len(df[(df['wmc'] > 30) & (df['wmc'] <= 75)])
    high = len(df[(df['wmc'] > 75) & (df['wmc'] <= 150)])
    critical = len(df[df['wmc'] > 150])
    
    sizes = [low, medium, high, critical]
    labels = [f'Low (≤30)\n{low} classes', f'Medium (31-75)\n{medium} classes', 
              f'High (76-150)\n{high} classes', f'CRITICAL (>150)\n{critical} classes']
    colors = ['#27ae60', '#f39c12', '#e67e22', '#c0392b']
    explode = (0, 0, 0.1, 0.2)  # Explode critical
    
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax1.set_title('Complexity Categories', fontsize=13, fontweight='bold', pad=10)
    
    # Panel 2: Top 10 Classes (Bar)
    top10 = df.nlargest(10, 'wmc')
    ax2.barh(range(len(top10)), top10['wmc'], color='#e74c3c', alpha=0.8)
    ax2.set_yticks(range(len(top10)))
    ax2.set_yticklabels([c.split('.')[-1] for c in top10['class']], fontsize=9)
    ax2.invert_yaxis()
    ax2.set_xlabel('WMC', fontsize=11, fontweight='bold')
    ax2.set_title('Top 10 Most Complex', fontsize=13, fontweight='bold', pad=10)
    ax2.grid(axis='x', alpha=0.3)
    
    # Panel 3: Coupling Distribution (Box Plot)
    ax3.boxplot([df['cbo']], vert=False, patch_artist=True,
                boxprops=dict(facecolor='#3498db', alpha=0.7),
                medianprops=dict(color='red', linewidth=2))
    ax3.set_xlabel('CBO (Coupling)', fontsize=11, fontweight='bold')
    ax3.set_title(f'Coupling Distribution (Median: {df["cbo"].median():.1f})', 
                  fontsize=13, fontweight='bold', pad=10)
    ax3.grid(axis='x', alpha=0.3)
    
    # Panel 4: Key Statistics (Text)
    ax4.axis('off')
    stats = f'''
    === KEY METRICS ===
    
    Total Classes: {len(df)}
    
    COMPLEXITY (WMC):
      • Average: {df["wmc"].mean():.1f}
      • Median: {df["wmc"].median():.1f}
      • Max: {df["wmc"].max():.0f}
      • Classes >100: {len(df[df["wmc"]>100])}
    
    COUPLING (CBO):
      • Average: {df["cbo"].mean():.1f}
      • Median: {df["cbo"].median():.1f}
      • Max: {df["cbo"].max():.0f}
    
    SIZE (LOC):
      • Average: {df["loc"].mean():.1f}
      • Total: {df["loc"].sum():.0f}
      • Largest: {df["loc"].max():.0f}
    
    REFACTORING PRIORITY:
      • Critical: {critical} classes
      • High: {high} classes
      • Total needing work: {critical + high}
    '''
    ax4.text(0.1, 0.9, stats, transform=ax4.transAxes,
            fontsize=12, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
    
    fig.suptitle('CODE QUALITY DASHBOARD', fontsize=18, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '6_summary_dashboard.png'), dpi=DPI, bbox_inches='tight')
    plt.close()

# ============================================================================
# MAIN
# ============================================================================
def main():
    if len(sys.argv) < 2:
        print("\nUsage: python simple_plots.py <audit_directory>")
        print("\nExample:")
        print('  python simple_plots.py "../data_archive/2026-02-13_19-26"')
        sys.exit(1)
    
    archive_dir = sys.argv[1]
    output_dir = os.path.join(archive_dir, 'simple_plots')
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "="*70)
    print("  SIMPLE CURRENT-STATE VISUALIZATIONS")
    print("="*70)
    print(f"\nReading data from: {archive_dir}")
    
    df = load_data(archive_dir)
    print(f"Loaded {len(df)} classes\n")
    
    print("Generating 6 plots...")
    plot_worst_classes(df, output_dir)
    plot_coupling_complexity(df, output_dir)
    plot_package_complexity(df, output_dir)
    plot_complexity_distribution(df, output_dir)
    plot_god_classes(df, output_dir)
    plot_summary_dashboard(df, output_dir)
    
    print("\n" + "="*70)
    print(f"✓ All plots saved to: {output_dir}")
    print("="*70)
    print("\nPlot Guide:")
    print("  1_worst_classes.png       → Which 20 classes to refactor first")
    print("  2_danger_zones.png        → Classes with high complexity + coupling")
    print("  3_package_complexity.png  → Which packages need most work")
    print("  4_complexity_distribution.png → Overall code health")
    print("  5_god_classes.png         → God classes that need splitting")
    print("  6_summary_dashboard.png   → Complete overview with statistics")
    print()

if __name__ == "__main__":
    main()
