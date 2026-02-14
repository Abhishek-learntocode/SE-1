#!/usr/bin/env python3
"""
collect_metrics.py — Unified Metrics Collector for Refactoring Lab

Collects all code metrics (CK, PMD, Checkstyle, Designite) and writes
structured output into two folders:
    {archive_dir}/system/system_metrics.csv   — one row, whole-repo aggregates
    {archive_dir}/class/class_metrics.csv     — one row per specified class

Also appends to unified history files:
    Refactoring_Lab/system_metrics_history.csv
    Refactoring_Lab/class_metrics_history.csv

Usage:
    python collect_metrics.py <archive_dir> <class_names_comma_separated> <phase> <refactoring_name>

Example:
    python collect_metrics.py "../data_archive/extract_method_1/before" \
        "org.apache.roller.weblogger.ui.rendering.model.PageModel,org.apache.roller.weblogger.business.jpa.JPAWeblogEntryManagerImpl" \
        "before" "extract_method_1"
"""

import pandas as pd
import numpy as np
import os
import sys
import datetime
import xml.etree.ElementTree as ET


# =============================================================================
# HELPERS
# =============================================================================

def ensure_dir(path):
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)


def safe_read_csv(filepath):
    """Read CSV safely, returning None on failure."""
    if not os.path.exists(filepath):
        print(f"   [MISSING] {os.path.basename(filepath)} not found.")
        return None
    try:
        df = pd.read_csv(filepath)
        if df.empty:
            print(f"   [WARN] {os.path.basename(filepath)} is empty.")
            return None
        return df
    except Exception as e:
        print(f"   [ERROR] Could not parse {os.path.basename(filepath)}: {e}")
        return None


# =============================================================================
# XML PARSERS — Checkstyle & PMD per-file violation counts
# =============================================================================

def parse_checkstyle_per_file(archive_dir):
    """
    Parse checkstyle_report.xml and return dict: { filepath: error_count }.
    Also returns total count.
    """
    xml_path = os.path.join(archive_dir, "checkstyle_report.xml")
    file_counts = {}
    total = 0

    if not os.path.exists(xml_path):
        print("   [MISSING] checkstyle_report.xml not found.")
        return file_counts, total

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        # Handle namespaces — iterate generically
        for file_node in root.iter():
            if file_node.tag.endswith('file') or file_node.tag == 'file':
                fname = file_node.get('name', '')
                if not fname:
                    continue
                count = 0
                for child in file_node:
                    if 'error' in child.tag:
                        count += 1
                if count > 0:
                    file_counts[fname] = count
                    total += count
        print(f"   [OK] Checkstyle: {total} errors across {len(file_counts)} files.")
    except Exception as e:
        print(f"   [ERROR] Checkstyle XML parse error: {e}")

    return file_counts, total


def parse_pmd_per_file(archive_dir):
    """
    Parse pmd_report.xml and return dict: { filepath: violation_count }.
    Also returns total count.
    """
    xml_path = os.path.join(archive_dir, "pmd_report.xml")
    file_counts = {}
    total = 0

    if not os.path.exists(xml_path):
        print("   [MISSING] pmd_report.xml not found.")
        return file_counts, total

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        for file_node in root.iter():
            if file_node.tag.endswith('file') or file_node.tag == 'file':
                fname = file_node.get('name', '')
                if not fname:
                    continue
                count = 0
                for child in file_node:
                    if 'violation' in child.tag:
                        count += 1
                if count > 0:
                    file_counts[fname] = count
                    total += count
        print(f"   [OK] PMD: {total} violations across {len(file_counts)} files.")
    except Exception as e:
        print(f"   [ERROR] PMD XML parse error: {e}")

    return file_counts, total


# =============================================================================
# CLASS MATCHER — Maps file paths from XML reports to CK class names
# =============================================================================

def filepath_to_classname(filepath):
    """
    Convert a Java source file path to a fully-qualified class name.
    e.g., '.../org/apache/roller/weblogger/Foo.java' -> 'org.apache.roller.weblogger.Foo'
    """
    # Normalize path separators
    fp = filepath.replace('\\', '/')

    # Find the 'org/' or 'com/' etc. prefix — look for common Java package roots
    for root in ['org/', 'com/', 'net/', 'io/', 'de/', 'fr/']:
        idx = fp.find(root)
        if idx != -1:
            rel = fp[idx:]
            # Remove .java extension
            if rel.endswith('.java'):
                rel = rel[:-5]
            return rel.replace('/', '.')

    # Fallback: use filename without extension
    basename = os.path.basename(filepath)
    if basename.endswith('.java'):
        basename = basename[:-5]
    return basename


def match_violations_to_class(file_counts, class_name):
    """
    Given a dict {filepath: count} and a target class name,
    find the matching file and return its violation count.
    """
    # Normalize class name for matching
    class_parts = class_name.split('.')
    simple_name = class_parts[-1]

    for fpath, count in file_counts.items():
        mapped = filepath_to_classname(fpath)
        # Exact match
        if mapped == class_name:
            return count
        # Simple name match (for inner classes etc.)
        if mapped.split('.')[-1] == simple_name:
            return count

    return 0


# =============================================================================
# DESIGNITE PARSER — per-class smell counts
# =============================================================================

def parse_designite_for_class(archive_dir, class_name):
    """Return design smell count for a specific class from DesignSmells.csv."""
    design_file = os.path.join(archive_dir, "DesignSmells.csv")
    if not os.path.exists(design_file):
        return 0
    try:
        df = pd.read_csv(design_file)
        simple_name = class_name.split('.')[-1]
        # Designite uses 'Type Name' column typically
        for col in ['Type Name', 'Class Name', 'class']:
            if col in df.columns:
                matches = df[df[col].astype(str).str.contains(simple_name, case=False, na=False)]
                return len(matches)
        return 0
    except:
        return 0


def parse_designite_totals(archive_dir):
    """Return total smell counts from Designite CSVs."""
    arch_smells = 0
    design_smells = 0
    impl_smells = 0

    for fname, label in [
        ("ArchitectureSmells.csv", "Architecture"),
        ("DesignSmells.csv", "Design"),
        ("ImplementationSmells.csv", "Implementation")
    ]:
        fpath = os.path.join(archive_dir, fname)
        if os.path.exists(fpath):
            try:
                df = pd.read_csv(fpath)
                count = len(df)
                if "Architecture" in label:
                    arch_smells = count
                elif "Design" in label:
                    design_smells = count
                else:
                    impl_smells = count
                print(f"   [OK] Designite {label}: {count} smells.")
            except:
                pass
        else:
            print(f"   [MISSING] {fname}")

    return arch_smells, design_smells, impl_smells


# =============================================================================
# FIND CLASS IN CK DATA
# =============================================================================

def find_class_row(df, class_name):
    """Find a class in CK class.csv using flexible matching. Returns row or None."""
    # Exact match on 'class' column
    exact = df[df['class'] == class_name]
    if not exact.empty:
        return exact.iloc[0]

    # Ends-with match (package.ClassName)
    partial = df[df['class'].str.endswith(class_name, na=False)]
    if not partial.empty:
        return partial.iloc[0]

    # Simple name match
    simple_name = class_name.split('.')[-1]
    flexible = df[df['class'].str.endswith('.' + simple_name, na=False)]
    if not flexible.empty:
        return flexible.iloc[0]

    # Contains match (last resort)
    contains = df[df['class'].str.contains(simple_name, case=False, na=False)]
    if not contains.empty:
        return contains.iloc[0]

    return None


# =============================================================================
# SYSTEM-LEVEL METRICS COLLECTOR
# =============================================================================

def collect_system_metrics(archive_dir):
    """
    Read all tool outputs and compute system-wide aggregate metrics.
    Returns a dict with all system-level metrics.
    """
    metrics = {}
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    metrics['Timestamp'] = timestamp

    # --- CK Metrics ---
    ck_file = os.path.join(archive_dir, "class.csv")
    df = safe_read_csv(ck_file)

    if df is not None:
        metrics['Total_Classes'] = len(df)
        metrics['Total_LOC'] = int(df['loc'].sum())
        metrics['God_Classes'] = int(len(df[(df['wmc'] > 47) & (df['cbo'] > 14)]))

        # WMC stats
        metrics['Max_WMC'] = int(df['wmc'].max())
        metrics['Avg_WMC'] = round(df['wmc'].mean(), 2)
        metrics['Median_WMC'] = round(df['wmc'].median(), 2)

        # CBO stats
        metrics['Max_CBO'] = int(df['cbo'].max())
        metrics['Avg_CBO'] = round(df['cbo'].mean(), 2)
        metrics['Median_CBO'] = round(df['cbo'].median(), 2)

        # Other averages
        metrics['Avg_LCOM'] = round(df['lcom'].mean(), 2) if 'lcom' in df.columns else 0
        metrics['Avg_RFC'] = round(df['rfc'].mean(), 2) if 'rfc' in df.columns else 0
        metrics['Avg_DIT'] = round(df['dit'].mean(), 2) if 'dit' in df.columns else 0

        # Complexity distribution buckets
        metrics['Classes_Low_WMC'] = int(len(df[df['wmc'] <= 10]))
        metrics['Classes_Med_WMC'] = int(len(df[(df['wmc'] > 10) & (df['wmc'] <= 30)]))
        metrics['Classes_High_WMC'] = int(len(df[(df['wmc'] > 30) & (df['wmc'] <= 47)]))
        metrics['Classes_Critical_WMC'] = int(len(df[df['wmc'] > 47]))

        print(f"   [OK] CK Metrics: {metrics['Total_Classes']} classes, "
              f"Max WMC={metrics['Max_WMC']}, God Classes={metrics['God_Classes']}")
    else:
        # Zero-fill CK metrics
        for key in ['Total_Classes', 'Total_LOC', 'God_Classes', 'Max_WMC', 'Avg_WMC',
                     'Median_WMC', 'Max_CBO', 'Avg_CBO', 'Median_CBO', 'Avg_LCOM',
                     'Avg_RFC', 'Avg_DIT', 'Classes_Low_WMC', 'Classes_Med_WMC',
                     'Classes_High_WMC', 'Classes_Critical_WMC']:
            metrics[key] = 0

    # --- Checkstyle ---
    _, checkstyle_total = parse_checkstyle_per_file(archive_dir)
    metrics['Checkstyle_Errors'] = checkstyle_total

    # --- PMD ---
    _, pmd_total = parse_pmd_per_file(archive_dir)
    metrics['PMD_Violations'] = pmd_total

    # --- Designite ---
    arch_smells, design_smells, impl_smells = parse_designite_totals(archive_dir)
    metrics['Architecture_Smells'] = arch_smells
    metrics['Design_Smells'] = design_smells
    metrics['Implementation_Smells'] = impl_smells

    return metrics


# =============================================================================
# CLASS-LEVEL METRICS COLLECTOR
# =============================================================================

def collect_class_metrics(archive_dir, class_names):
    """
    For each specified class, extract CK metrics + violations + smells.
    Returns a list of dicts (one per class).
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    results = []

    # Load CK data
    df = safe_read_csv(os.path.join(archive_dir, "class.csv"))
    if df is None:
        print("   [ERROR] Cannot collect class metrics without class.csv")
        return results

    # Load violations maps
    checkstyle_map, _ = parse_checkstyle_per_file(archive_dir)
    pmd_map, _ = parse_pmd_per_file(archive_dir)

    ck_columns = ['wmc', 'cbo', 'loc', 'lcom', 'rfc', 'dit', 'noc',
                   'totalMethodsQty', 'publicMethodsQty', 'staticMethodsQty',
                   'totalFieldsQty', 'nosi', 'returnQty', 'loopQty',
                   'comparisonsQty', 'tryCatchQty', 'parenthesizedExpsQty',
                   'stringLiteralsQty', 'numbersQty', 'assignmentsQty',
                   'mathOperationsQty', 'variablesQty', 'maxNestedBlocksQty',
                   'anonymousClassesQty', 'innerClassesQty', 'lambdasQty',
                   'uniqueWordsQty']

    for class_name in class_names:
        class_name = class_name.strip()
        if not class_name:
            continue

        row = find_class_row(df, class_name)
        if row is None:
            print(f"   [WARN] Class '{class_name}' not found in class.csv — skipping.")
            continue

        record = {
            'Timestamp': timestamp,
            'class': row.get('class', class_name),
        }

        # Add all available CK metrics
        for col in ck_columns:
            if col in row.index:
                record[col] = row[col]
            else:
                record[col] = 0

        # Violations
        record['checkstyle_errors'] = match_violations_to_class(checkstyle_map, record['class'])
        record['pmd_violations'] = match_violations_to_class(pmd_map, record['class'])

        # Designite smells for this class
        record['design_smells'] = parse_designite_for_class(archive_dir, record['class'])

        results.append(record)
        short = record['class'].split('.')[-1]
        print(f"   [OK] Class '{short}': WMC={record['wmc']}, CBO={record['cbo']}, "
              f"LOC={record['loc']}, PMD={record['pmd_violations']}, "
              f"Checkstyle={record['checkstyle_errors']}")

    return results


# =============================================================================
# SAVE OUTPUTS
# =============================================================================

def save_system_metrics(metrics, archive_dir, history_file):
    """Save system metrics to archive folder and append to history."""
    system_dir = os.path.join(archive_dir, "system")
    ensure_dir(system_dir)

    df = pd.DataFrame([metrics])

    # Save snapshot in archive
    snapshot_path = os.path.join(system_dir, "system_metrics.csv")
    df.to_csv(snapshot_path, index=False)
    print(f"   [SAVED] {snapshot_path}")

    # Append to history
    if os.path.isfile(history_file):
        df.to_csv(history_file, mode='a', header=False, index=False)
    else:
        df.to_csv(history_file, index=False)
    print(f"   [SAVED] Appended to {history_file}")


def save_class_metrics(class_records, archive_dir, history_file):
    """Save class metrics to archive folder and append to history."""
    if not class_records:
        print("   [SKIP] No class metrics to save.")
        return

    class_dir = os.path.join(archive_dir, "class")
    ensure_dir(class_dir)

    df = pd.DataFrame(class_records)

    # Save snapshot in archive
    snapshot_path = os.path.join(class_dir, "class_metrics.csv")
    df.to_csv(snapshot_path, index=False)
    print(f"   [SAVED] {snapshot_path}")

    # Append to history
    if os.path.isfile(history_file):
        df.to_csv(history_file, mode='a', header=False, index=False)
    else:
        df.to_csv(history_file, index=False)
    print(f"   [SAVED] Appended to {history_file}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    if len(sys.argv) < 3:
        print("Usage: python collect_metrics.py <archive_dir> <class_names> [<phase>] [<refactoring_name>]")
        print("  <archive_dir>      : Path to archive folder containing class.csv, XML reports, etc.")
        print("  <class_names>      : Comma-separated FQCNs, or 'NONE' to skip class-level collection")
        print("  <phase>            : 'before', 'after', or 'snapshot' (default: 'snapshot')")
        print("  <refactoring_name> : Label for the refactoring instance (default: folder name)")
        sys.exit(1)

    archive_dir = sys.argv[1]
    class_names_arg = sys.argv[2]
    phase = sys.argv[3] if len(sys.argv) > 3 else "snapshot"
    refactoring_name = sys.argv[4] if len(sys.argv) > 4 else os.path.basename(os.path.normpath(archive_dir))

    # Parse class names — "NONE" means skip class-level
    skip_class_level = (class_names_arg.strip().upper() == "NONE")
    class_names = [] if skip_class_level else [c.strip() for c in class_names_arg.split(',') if c.strip()]

    # History files live in Refactoring_Lab/ (parent of scripts/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    lab_dir = os.path.dirname(script_dir)
    system_history = os.path.join(lab_dir, "system_metrics_history.csv")
    class_history = os.path.join(lab_dir, "class_metrics_history.csv")

    print("=" * 60)
    print(f"  METRICS COLLECTOR — {refactoring_name} [{phase.upper()}]")
    print("=" * 60)

    # --- System-level ---
    print(f"\n--- System-Level Metrics ---")
    system_metrics = collect_system_metrics(archive_dir)
    system_metrics['Phase'] = phase
    system_metrics['Refactoring'] = refactoring_name
    save_system_metrics(system_metrics, archive_dir, system_history)

    # --- Class-level (skip if NONE) ---
    if skip_class_level:
        print(f"\n--- Class-Level Metrics: SKIPPED (NONE) ---")
    else:
        print(f"\n--- Class-Level Metrics ({len(class_names)} class(es)) ---")
        class_records = collect_class_metrics(archive_dir, class_names)
        for rec in class_records:
            rec['Phase'] = phase
            rec['Refactoring'] = refactoring_name
        save_class_metrics(class_records, archive_dir, class_history)

    print(f"\n{'=' * 60}")
    print(f"  COLLECTION COMPLETE")
    print(f"  System: {os.path.join(archive_dir, 'system', 'system_metrics.csv')}")
    if not skip_class_level:
        print(f"  Class:  {os.path.join(archive_dir, 'class', 'class_metrics.csv')}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
