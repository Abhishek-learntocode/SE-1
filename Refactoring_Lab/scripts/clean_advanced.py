"""
clean_advanced.py — The Macro View
Generates only the 2 essential context plots for the report.
"""
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from math import pi

# Configuration
plt.style.use('seaborn-v0_8-whitegrid')

def plot_god_class_quadrant(df, output_dir):
    """Context Plot 1: Where are the problems?"""
    print("   [1/2] Generating God Class Quadrant...")
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Filter valid data
    df_plot = df[(df['cbo'] > 0) & (df['wmc'] > 0)].copy()
    
    # Scatter Plot
    scatter = ax.scatter(
        df_plot['cbo'], 
        df_plot['wmc'], 
        s=df_plot['loc'], 
        c=df_plot['lcom'], 
        cmap='RdYlGn_r', 
        alpha=0.6, 
        edgecolors='black'
    )
    
    # Thresholds
    ax.axhline(y=47, color='red', linestyle='--', label='WMC Threshold (47)')
    ax.axvline(x=14, color='red', linestyle='--', label='CBO Threshold (14)')
    
    # Annotate Top 5 God Classes
    god_classes = df_plot[(df_plot['wmc'] > 47) & (df_plot['cbo'] > 14)].nlargest(5, 'wmc')
    for _, row in god_classes.iterrows():
        ax.annotate(
            row['class'].split('.')[-1],
            xy=(row['cbo'], row['wmc']),
            xytext=(10, 10),
            textcoords='offset points',
            fontsize=9,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
        )

    # Labels
    ax.set_xlabel('Coupling (CBO)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Complexity (WMC)', fontsize=12, fontweight='bold')
    ax.set_title('Target Identification: God Class Quadrant', fontsize=14, fontweight='bold')
    
    # Colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Lack of Cohesion (LCOM)', fontsize=10, fontweight='bold')
    
    ax.legend(loc='upper left')
    plt.savefig(os.path.join(output_dir, '01_context_quadrant.png'), dpi=150, bbox_inches='tight')
    plt.close()

def plot_project_radar(df, output_dir):
    """Context Plot 2: Did we maintain overall health?"""
    print("   [2/2] Generating Project Radar...")
    
    # Normalize metrics (capped at 100 for visualization)
    metrics = {
        'Complexity': min(100, (df['wmc'].mean() / 50) * 100),
        'Coupling': min(100, (df['cbo'].mean() / 20) * 100),
        'Cohesion': min(100, (df['lcom'].mean() / 100) * 100), # Adjusted divisor for LCOM
        'Size': min(100, (df['loc'].mean() / 500) * 100)
    }
    
    categories = list(metrics.keys())
    values = list(metrics.values())
    values += values[:1] # Close the loop
    
    angles = [n / float(len(categories)) * 2 * pi for n in range(len(categories))]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    
    # Draw Polygon
    ax.plot(angles, values, linewidth=2, linestyle='solid', color='#3498db')
    ax.fill(angles, values, color='#3498db', alpha=0.25)
    
    # Labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=11, fontweight='bold')
    ax.set_title('Overall Project Health', fontsize=14, fontweight='bold', pad=20)
    
    plt.savefig(os.path.join(output_dir, '02_project_radar.png'), dpi=150, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clean_advanced.py <archive_dir>")
        sys.exit(1)
        
    archive_dir = sys.argv[1]
    csv_path = os.path.join(archive_dir, "class.csv")
    
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        plot_god_class_quadrant(df, archive_dir)
        plot_project_radar(df, archive_dir)
        print("✅ Macro plots generated successfully.")
    else:
        print(f"❌ class.csv not found in {archive_dir}")