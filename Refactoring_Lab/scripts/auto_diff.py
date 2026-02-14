#!/usr/bin/env python3
"""
auto_diff.py — Automatically detect which classes changed between two snapshots.

Compares two CK `class.csv` files and reports:
  - ADDED classes   (present only in 'after')
  - REMOVED classes (present only in 'before')
  - CHANGED classes (present in both but with different metrics)

Usage:
    python auto_diff.py <before_dir> <after_dir> [--threshold 0] [--json] [--brief]

Output:
    By default prints a human-readable diff summary.
    With --brief, prints ONLY the list of class FQCNs that changed (one per line),
    suitable for piping into other scripts.
    With --json, prints structured JSON.

Exit codes:
    0 — success, differences found (or no differences)
    1 — error (missing files, etc.)
"""

import sys
import os
import json
import argparse
import pandas as pd
import numpy as np

# Metrics to compare
DIFF_METRICS = ['wmc', 'cbo', 'loc', 'lcom', 'rfc', 'dit',
                'totalMethodsQty', 'totalFieldsQty', 'nosi',
                'returnQty', 'loopQty', 'comparisonsQty',
                'tryCatchQty', 'stringLiteralsQty', 'variablesQty']

# Key metrics to display in the summary
KEY_METRICS = ['wmc', 'cbo', 'loc', 'lcom', 'rfc', 'dit']


def load_class_csv(snapshot_dir):
    """Load a class.csv from a snapshot directory."""
    class_csv_path = os.path.join(snapshot_dir, 'class.csv')
    if not os.path.exists(class_csv_path):
        raise FileNotFoundError(f"class.csv not found in {snapshot_dir}")
    
    df = pd.read_csv(class_csv_path)
    
    # Normalize column names to lowercase
    df.columns = [c.lower().strip() for c in df.columns]
    
    # Build a fully-qualified class name for matching
    if 'class' in df.columns:
        df['fqcn'] = df['class']
    else:
        raise ValueError("No 'class' column found in class.csv")
    
    return df


def compute_diff(before_df, after_df, threshold=0):
    """
    Compare two class DataFrames and return structured diff info.
    
    Args:
        before_df: DataFrame from before snapshot
        after_df: DataFrame from after snapshot
        threshold: minimum absolute change to count as 'changed' (default 0 = any change)
    
    Returns dict with keys: added, removed, changed, unchanged, summary
    """
    before_classes = set(before_df['fqcn'].unique())
    after_classes = set(after_df['fqcn'].unique())
    
    added_names = after_classes - before_classes
    removed_names = before_classes - after_classes
    common_names = before_classes & after_classes
    
    # For common classes, check which metrics actually changed
    changed = []
    unchanged = []
    
    for cls in sorted(common_names):
        before_row = before_df[before_df['fqcn'] == cls].iloc[0]
        after_row = after_df[after_df['fqcn'] == cls].iloc[0]
        
        deltas = {}
        has_change = False
        
        for metric in DIFF_METRICS:
            if metric in before_row.index and metric in after_row.index:
                try:
                    b_val = float(before_row[metric])
                    a_val = float(after_row[metric])
                    delta = a_val - b_val
                    if abs(delta) > threshold:
                        has_change = True
                    deltas[metric] = {
                        'before': b_val,
                        'after': a_val,
                        'delta': delta
                    }
                except (ValueError, TypeError):
                    pass
        
        if has_change:
            changed.append({'class': cls, 'deltas': deltas})
        else:
            unchanged.append(cls)
    
    # Build added class details
    added = []
    for cls in sorted(added_names):
        row = after_df[after_df['fqcn'] == cls].iloc[0]
        metrics = {}
        for m in KEY_METRICS:
            if m in row.index:
                try:
                    metrics[m] = float(row[m])
                except (ValueError, TypeError):
                    pass
        added.append({'class': cls, 'metrics': metrics})
    
    # Build removed class details
    removed = []
    for cls in sorted(removed_names):
        row = before_df[before_df['fqcn'] == cls].iloc[0]
        metrics = {}
        for m in KEY_METRICS:
            if m in row.index:
                try:
                    metrics[m] = float(row[m])
                except (ValueError, TypeError):
                    pass
        removed.append({'class': cls, 'metrics': metrics})
    
    # Summary statistics
    summary = {
        'total_before': len(before_classes),
        'total_after': len(after_classes),
        'added_count': len(added),
        'removed_count': len(removed),
        'changed_count': len(changed),
        'unchanged_count': len(unchanged),
        'affected_count': len(added) + len(removed) + len(changed)
    }
    
    return {
        'added': added,
        'removed': removed,
        'changed': changed,
        'unchanged': unchanged,
        'summary': summary
    }


def print_brief(diff_result):
    """Print just the list of affected class FQCNs, one per line."""
    names = []
    for item in diff_result['added']:
        names.append(item['class'])
    for item in diff_result['removed']:
        names.append(item['class'])
    for item in diff_result['changed']:
        names.append(item['class'])
    
    for name in sorted(set(names)):
        print(name)


def print_summary(diff_result):
    """Print a human-readable diff summary."""
    s = diff_result['summary']
    
    print()
    print("=" * 70)
    print("  AUTO-DIFF RESULTS")
    print("=" * 70)
    print(f"  Before: {s['total_before']} classes")
    print(f"  After:  {s['total_after']} classes")
    print(f"  ---")
    print(f"  Added:     {s['added_count']}")
    print(f"  Removed:   {s['removed_count']}")
    print(f"  Changed:   {s['changed_count']}")
    print(f"  Unchanged: {s['unchanged_count']}")
    print(f"  Total affected: {s['affected_count']}")
    print("=" * 70)
    
    # Added classes
    if diff_result['added']:
        print()
        print("  NEW CLASSES (added):")
        print("  " + "-" * 66)
        for item in diff_result['added']:
            short_name = item['class'].split('.')[-1] if '.' in item['class'] else item['class']
            metrics_str = ", ".join(f"{k.upper()}={int(v)}" for k, v in item['metrics'].items())
            print(f"    + {short_name}")
            if metrics_str:
                print(f"      {metrics_str}")
    
    # Removed classes
    if diff_result['removed']:
        print()
        print("  REMOVED CLASSES:")
        print("  " + "-" * 66)
        for item in diff_result['removed']:
            short_name = item['class'].split('.')[-1] if '.' in item['class'] else item['class']
            metrics_str = ", ".join(f"{k.upper()}={int(v)}" for k, v in item['metrics'].items())
            print(f"    - {short_name}")
            if metrics_str:
                print(f"      {metrics_str}")
    
    # Changed classes
    if diff_result['changed']:
        print()
        print("  CHANGED CLASSES:")
        print("  " + "-" * 66)
        for item in diff_result['changed']:
            short_name = item['class'].split('.')[-1] if '.' in item['class'] else item['class']
            print(f"    ~ {short_name}")
            for metric in KEY_METRICS:
                if metric in item['deltas']:
                    d = item['deltas'][metric]
                    delta = d['delta']
                    arrow = "▼" if delta < 0 else ("▲" if delta > 0 else "=")
                    color_hint = "(improved)" if (delta < 0 and metric in ['wmc', 'cbo', 'lcom']) else (
                        "(worsened)" if (delta > 0 and metric in ['wmc', 'cbo', 'lcom']) else ""
                    )
                    print(f"      {metric.upper():>6}: {int(d['before']):>6} -> {int(d['after']):>6}  ({delta:+.0f}) {arrow} {color_hint}")
    
    if s['affected_count'] == 0:
        print()
        print("  No differences detected. The snapshots are metrically identical.")
    
    print()
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description='Auto-detect class changes between two snapshots')
    parser.add_argument('before_dir', help='Path to the before snapshot directory')
    parser.add_argument('after_dir', help='Path to the after snapshot directory')
    parser.add_argument('--threshold', type=float, default=0,
                        help='Minimum absolute metric change to count (default: 0 = any)')
    parser.add_argument('--json', action='store_true', dest='output_json',
                        help='Output as JSON')
    parser.add_argument('--brief', action='store_true',
                        help='Output just affected class names (one per line)')
    
    args = parser.parse_args()
    
    try:
        before_df = load_class_csv(args.before_dir)
        after_df = load_class_csv(args.after_dir)
    except (FileNotFoundError, ValueError) as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    
    diff_result = compute_diff(before_df, after_df, threshold=args.threshold)
    
    if args.output_json:
        # Convert for JSON serialization
        output = {
            'summary': diff_result['summary'],
            'added': [item['class'] for item in diff_result['added']],
            'removed': [item['class'] for item in diff_result['removed']],
            'changed': [item['class'] for item in diff_result['changed']],
        }
        print(json.dumps(output, indent=2))
    elif args.brief:
        print_brief(diff_result)
    else:
        print_summary(diff_result)
    
    sys.exit(0)


if __name__ == '__main__':
    main()
