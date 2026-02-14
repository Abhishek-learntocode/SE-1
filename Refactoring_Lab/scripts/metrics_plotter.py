"""
Metrics Plotter — Generates Trend Charts from Refactoring History
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import sys
from pathlib import Path

# Configuration
PLOT_STYLE = 'seaborn-v0_8-darkgrid'
FIGURE_DPI = 150
COLOR_PALETTE = {
    'god_classes': '#e74c3c',
    'complexity': '#e67e22', 
    'design_smells': '#3498db',
    'arch_smells': '#9b59b6',
    'pmd': '#16a085',
    'checkstyle': '#f39c12'
}

def ensure_dir(path):
    """Create directory if it doesn't exist"""
    Path(path).mkdir(parents=True, exist_ok=True)

def load_history(history_file):
    """Load metrics history CSV"""
    if not os.path.exists(history_file):
        print(f"❌ History file not found: {history_file}")
        return None
    
    try:
        df = pd.read_csv(history_file)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    except Exception as e:
        print(f"❌ Error loading history: {e}")
        return None

def plot_god_classes_trend(df, output_dir):
    """Plot God Classes over time"""
    plt.style.use(PLOT_STYLE)
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(df['Timestamp'], df['God_Classes (CK)'], 
            marker='o', linewidth=2, markersize=8,
            color=COLOR_PALETTE['god_classes'], label='God Classes')
    
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Count', fontsize=12, fontweight='bold')
    ax.set_title('God Classes Trend (WMC > 47 & CBO > 14)', 
                fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Annotate latest value
    latest = df.iloc[-1]
    ax.annotate(f"{int(latest['God_Classes (CK)'])}",
                xy=(latest['Timestamp'], latest['God_Classes (CK)']),
                xytext=(10, 10), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'god_classes_trend.png'), dpi=FIGURE_DPI)
    plt.close()
    print("   ✅ Generated: god_classes_trend.png")

def plot_complexity_trend(df, output_dir):
    """Plot Max Complexity over time"""
    plt.style.use(PLOT_STYLE)
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(df['Timestamp'], df['Max_Complexity (CK)'], 
            marker='s', linewidth=2, markersize=8,
            color=COLOR_PALETTE['complexity'], label='Max WMC')
    
    ax.axhline(y=50, color='red', linestyle='--', linewidth=1, alpha=0.5, label='Threshold (50)')
    
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('WMC (Weighted Methods per Class)', fontsize=12, fontweight='bold')
    ax.set_title('Maximum Complexity Trend', 
                fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Annotate latest value
    latest = df.iloc[-1]
    ax.annotate(f"{int(latest['Max_Complexity (CK)'])}",
                xy=(latest['Timestamp'], latest['Max_Complexity (CK)']),
                xytext=(10, 10), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'complexity_trend.png'), dpi=FIGURE_DPI)
    plt.close()
    print("   ✅ Generated: complexity_trend.png")

def plot_smells_comparison(df, output_dir):
    """Plot Design vs Architecture Smells"""
    plt.style.use(PLOT_STYLE)
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(df['Timestamp'], df['Design_Smells'], 
            marker='o', linewidth=2, markersize=8,
            color=COLOR_PALETTE['design_smells'], label='Design Smells')
    ax.plot(df['Timestamp'], df['Architecture_Smells'], 
            marker='^', linewidth=2, markersize=8,
            color=COLOR_PALETTE['arch_smells'], label='Architecture Smells')
    
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Count', fontsize=12, fontweight='bold')
    ax.set_title('Design & Architecture Smells (Designite)', 
                fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'smells_comparison.png'), dpi=FIGURE_DPI)
    plt.close()
    print("   ✅ Generated: smells_comparison.png")

def plot_violations_trend(df, output_dir):
    """Plot PMD & Checkstyle violations"""
    plt.style.use(PLOT_STYLE)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
    # PMD
    ax1.plot(df['Timestamp'], df['PMD_Issues'], 
            marker='o', linewidth=2, markersize=8,
            color=COLOR_PALETTE['pmd'], label='PMD Violations')
    ax1.set_ylabel('PMD Violations', fontsize=12, fontweight='bold')
    ax1.set_title('Code Quality Violations Trend', 
                 fontsize=14, fontweight='bold', pad=20)
    ax1.legend(loc='best', fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Checkstyle
    ax2.plot(df['Timestamp'], df['Checkstyle_Errors'], 
            marker='s', linewidth=2, markersize=8,
            color=COLOR_PALETTE['checkstyle'], label='Checkstyle Errors')
    ax2.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Checkstyle Errors', fontsize=12, fontweight='bold')
    ax2.legend(loc='best', fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'violations_trend.png'), dpi=FIGURE_DPI)
    plt.close()
    print("   ✅ Generated: violations_trend.png")

def plot_combined_dashboard(df, output_dir):
    """Create a comprehensive dashboard with all metrics"""
    plt.style.use(PLOT_STYLE)
    fig = plt.figure(figsize=(16, 12))
    
    # Create grid
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # 1. God Classes
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(df['Timestamp'], df['God_Classes (CK)'], 
            marker='o', linewidth=2, color=COLOR_PALETTE['god_classes'])
    ax1.set_ylabel('Count', fontsize=10, fontweight='bold')
    ax1.set_title('God Classes', fontsize=11, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # 2. Max Complexity
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(df['Timestamp'], df['Max_Complexity (CK)'], 
            marker='s', linewidth=2, color=COLOR_PALETTE['complexity'])
    ax2.set_ylabel('WMC', fontsize=10, fontweight='bold')
    ax2.set_title('Max Complexity', fontsize=11, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # 3. Design Smells
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(df['Timestamp'], df['Design_Smells'], 
            marker='o', linewidth=2, color=COLOR_PALETTE['design_smells'])
    ax3.set_ylabel('Count', fontsize=10, fontweight='bold')
    ax3.set_title('Design Smells', fontsize=11, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # 4. Architecture Smells
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.plot(df['Timestamp'], df['Architecture_Smells'], 
            marker='^', linewidth=2, color=COLOR_PALETTE['arch_smells'])
    ax4.set_ylabel('Count', fontsize=10, fontweight='bold')
    ax4.set_title('Architecture Smells', fontsize=11, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    # 5. PMD
    ax5 = fig.add_subplot(gs[2, 0])
    ax5.plot(df['Timestamp'], df['PMD_Issues'], 
            marker='o', linewidth=2, color=COLOR_PALETTE['pmd'])
    ax5.set_xlabel('Date', fontsize=10, fontweight='bold')
    ax5.set_ylabel('Violations', fontsize=10, fontweight='bold')
    ax5.set_title('PMD Issues', fontsize=11, fontweight='bold')
    ax5.grid(True, alpha=0.3)
    
    # 6. Checkstyle
    ax6 = fig.add_subplot(gs[2, 1])
    ax6.plot(df['Timestamp'], df['Checkstyle_Errors'], 
            marker='s', linewidth=2, color=COLOR_PALETTE['checkstyle'])
    ax6.set_xlabel('Date', fontsize=10, fontweight='bold')
    ax6.set_ylabel('Errors', fontsize=10, fontweight='bold')
    ax6.set_title('Checkstyle Errors', fontsize=11, fontweight='bold')
    ax6.grid(True, alpha=0.3)
    
    fig.suptitle('Code Quality Metrics Dashboard', 
                fontsize=16, fontweight='bold', y=0.995)
    
    plt.savefig(os.path.join(output_dir, 'dashboard.png'), dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close()
    print("   ✅ Generated: dashboard.png")

def generate_summary_stats(df, output_dir):
    """Generate summary statistics table"""
    latest = df.iloc[-1]
    
    if len(df) > 1:
        previous = df.iloc[-2]
        changes = {
            'God_Classes': latest['God_Classes (CK)'] - previous['God_Classes (CK)'],
            'Max_Complexity': latest['Max_Complexity (CK)'] - previous['Max_Complexity (CK)'],
            'Design_Smells': latest['Design_Smells'] - previous['Design_Smells'],
            'Architecture_Smells': latest['Architecture_Smells'] - previous['Architecture_Smells'],
            'PMD_Issues': latest['PMD_Issues'] - previous['PMD_Issues'],
            'Checkstyle_Errors': latest['Checkstyle_Errors'] - previous['Checkstyle_Errors']
        }
    else:
        changes = {k: 0 for k in ['God_Classes', 'Max_Complexity', 'Design_Smells', 
                                    'Architecture_Smells', 'PMD_Issues', 'Checkstyle_Errors']}
    
    summary = []
    summary.append("=" * 80)
    summary.append("SUMMARY STATISTICS")
    summary.append("=" * 80)
    summary.append(f"Latest Analysis: {latest['Timestamp']}")
    summary.append(f"Total Audits: {len(df)}")
    summary.append("")
    summary.append("CURRENT VALUES (Change from previous):")
    summary.append(f"  • God Classes:        {int(latest['God_Classes (CK)'])} ({changes['God_Classes']:+.0f})")
    summary.append(f"  • Max Complexity:     {int(latest['Max_Complexity (CK)'])} ({changes['Max_Complexity']:+.0f})")
    summary.append(f"  • Design Smells:      {int(latest['Design_Smells'])} ({changes['Design_Smells']:+.0f})")
    summary.append(f"  • Arch Smells:        {int(latest['Architecture_Smells'])} ({changes['Architecture_Smells']:+.0f})")
    summary.append(f"  • PMD Issues:         {int(latest['PMD_Issues'])} ({changes['PMD_Issues']:+.0f})")
    summary.append(f"  • Checkstyle Errors:  {int(latest['Checkstyle_Errors'])} ({changes['Checkstyle_Errors']:+.0f})")
    summary.append("=" * 80)
    
    summary_text = "\n".join(summary)
    
    with open(os.path.join(output_dir, 'summary.txt'), 'w') as f:
        f.write(summary_text)
    
    print("\n" + summary_text)
    print("   ✅ Generated: summary.txt")

def main():
    if len(sys.argv) < 2:
        print("Usage: python metrics_plotter.py <output_directory>")
        sys.exit(1)
    
    output_dir = sys.argv[1]
    ensure_dir(output_dir)
    
    history_file = "../metrics_history.csv"
    
    print("\n📊 GENERATING METRICS PLOTS...")
    
    df = load_history(history_file)
    if df is None or df.empty:
        print("❌ No history data available. Run an audit first.")
        sys.exit(1)
    
    print(f"   Loaded {len(df)} audit record(s)")
    
    # Generate all plots
    plot_god_classes_trend(df, output_dir)
    plot_complexity_trend(df, output_dir)
    plot_smells_comparison(df, output_dir)
    plot_violations_trend(df, output_dir)
    plot_combined_dashboard(df, output_dir)
    generate_summary_stats(df, output_dir)
    
    print(f"\n✅ All plots saved to: {output_dir}")

if __name__ == "__main__":
    main()
