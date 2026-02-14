# ==============================================================================
# compare_snapshots.ps1 — Compare two recorded snapshots (auto-detect changes)
# ==============================================================================
#
# Automatically detects which classes changed between two snapshots and
# generates comparison plots + detailed analysis.
#
# Usage:
#   .\compare_snapshots.ps1 -Before "R1.2_before" -After "R1.2_after"
#
# You can also use full paths:
#   .\compare_snapshots.ps1 -Before "C:\...\data_archive\R1.2_before" -After "C:\...\data_archive\R1.2_after"
#
# Prerequisites:
#   Run record_snapshot.ps1 for both before and after first.
# ==============================================================================

param(
    [Parameter(Mandatory=$true)]
    [string]$Before,

    [Parameter(Mandatory=$true)]
    [string]$After
)

# ==============================================================================
# CONFIGURATION
# ==============================================================================

$SCRIPT_DIR   = Split-Path -Parent $MyInvocation.MyCommand.Path
$LAB_DIR      = Split-Path -Parent $SCRIPT_DIR
$DATA_ARCHIVE = Join-Path $LAB_DIR "data_archive"

$PATH_TO_AUTO_DIFF     = Join-Path $SCRIPT_DIR "auto_diff.py"
$PATH_TO_COLLECTOR     = Join-Path $SCRIPT_DIR "collect_metrics.py"
$PATH_TO_COMPARISON    = Join-Path $SCRIPT_DIR "generate_comparison.py"

# ==============================================================================
# RESOLVE SNAPSHOT PATHS
# ==============================================================================

# If the user passed just a name (not a full path), resolve relative to data_archive
function Resolve-SnapshotPath {
    param([string]$PathOrName)
    
    if (Test-Path $PathOrName) {
        return (Resolve-Path $PathOrName).Path
    }
    
    $resolved = Join-Path $DATA_ARCHIVE $PathOrName
    if (Test-Path $resolved) {
        return (Resolve-Path $resolved).Path
    }
    
    Write-Host "[ERROR] Snapshot not found: '$PathOrName'" -ForegroundColor Red
    Write-Host "        Looked in: $resolved" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Available snapshots in data_archive/:" -ForegroundColor Yellow
    Get-ChildItem $DATA_ARCHIVE -Directory | ForEach-Object {
        Write-Host "    - $($_.Name)" -ForegroundColor Gray
    }
    exit 1
}

$BEFORE_DIR = Resolve-SnapshotPath $Before
$AFTER_DIR  = Resolve-SnapshotPath $After

# Extract snapshot names (for display)
$BEFORE_NAME = Split-Path $BEFORE_DIR -Leaf
$AFTER_NAME  = Split-Path $AFTER_DIR -Leaf

# Output directory for comparison artifacts
$COMPARISON_DIR = Join-Path $AFTER_DIR "comparison"
if (Test-Path $COMPARISON_DIR) {
    Remove-Item $COMPARISON_DIR -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $COMPARISON_DIR | Out-Null

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  COMPARE SNAPSHOTS" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Before: $BEFORE_NAME  ($BEFORE_DIR)" -ForegroundColor White
Write-Host "  After:  $AFTER_NAME   ($AFTER_DIR)" -ForegroundColor White
Write-Host "  Output: $COMPARISON_DIR" -ForegroundColor White
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

# ==============================================================================
# VALIDATE SNAPSHOTS
# ==============================================================================

$beforeClassCsv = Join-Path $BEFORE_DIR "class.csv"
$afterClassCsv  = Join-Path $AFTER_DIR "class.csv"

if (-not (Test-Path $beforeClassCsv)) {
    Write-Host "[ERROR] Before snapshot missing class.csv: $beforeClassCsv" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path $afterClassCsv)) {
    Write-Host "[ERROR] After snapshot missing class.csv: $afterClassCsv" -ForegroundColor Red
    exit 1
}

# ==============================================================================
# STEP 1: AUTO-DETECT CHANGES
# ==============================================================================

Write-Host "[1/4] Auto-detecting changes between snapshots..." -ForegroundColor Yellow

# Run the auto_diff tool to show the full summary
python "$PATH_TO_AUTO_DIFF" "$BEFORE_DIR" "$AFTER_DIR"

# Now get just the class names (brief mode) for feeding into comparisons
$diffOutput = python "$PATH_TO_AUTO_DIFF" "$BEFORE_DIR" "$AFTER_DIR" --brief 2>&1
$changedClasses = @()

if ($diffOutput) {
    $changedClasses = $diffOutput | Where-Object { $_.ToString().Trim() -ne "" } | ForEach-Object { $_.ToString().Trim() }
}

if ($changedClasses.Count -eq 0) {
    Write-Host ""
    Write-Host "[INFO] No class-level changes detected between '$BEFORE_NAME' and '$AFTER_NAME'." -ForegroundColor Yellow
    Write-Host "       System-level comparison will still be generated." -ForegroundColor Gray
    $classNamesArg = "NONE"
} else {
    Write-Host ""
    Write-Host "[INFO] Detected $($changedClasses.Count) affected class(es):" -ForegroundColor Green
    foreach ($cls in $changedClasses) {
        $shortName = $cls.Split('.')[-1]
        Write-Host "       - $shortName" -ForegroundColor Gray
    }
    
    # Join class names with comma for CLI argument
    $classNamesArg = $changedClasses -join ","
}

# ==============================================================================
# STEP 2: COLLECT CLASS-LEVEL METRICS FOR CHANGED CLASSES
# ==============================================================================

Write-Host ""
Write-Host "[2/4] Collecting class-level metrics for before snapshot..." -ForegroundColor Yellow
python "$PATH_TO_COLLECTOR" "$BEFORE_DIR" "$classNamesArg" "before" "$AFTER_NAME"

Write-Host "[2/4] Collecting class-level metrics for after snapshot..." -ForegroundColor Yellow
python "$PATH_TO_COLLECTOR" "$AFTER_DIR" "$classNamesArg" "after" "$AFTER_NAME"

# ==============================================================================
# STEP 3: GENERATE COMPARISON PLOTS
# ==============================================================================

Write-Host ""
Write-Host "[3/4] Generating comparison plots..." -ForegroundColor Yellow
python "$PATH_TO_COMPARISON" "$BEFORE_DIR" "$AFTER_DIR" "$COMPARISON_DIR" "$classNamesArg"

if ($LASTEXITCODE -ne 0) {
    Write-Host "[WARN] Comparison plot generation had issues (exit code: $LASTEXITCODE)" -ForegroundColor DarkYellow
} else {
    Write-Host "      [OK] Comparison plots generated" -ForegroundColor Green
}

# ==============================================================================
# STEP 4: SUMMARY
# ==============================================================================

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "  COMPARISON COMPLETE" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "  Before: $BEFORE_NAME" -ForegroundColor White
Write-Host "  After:  $AFTER_NAME" -ForegroundColor White
Write-Host "  Changes detected: $($changedClasses.Count) class(es)" -ForegroundColor White
Write-Host ""
Write-Host "  Output directory:" -ForegroundColor White
Write-Host "    $COMPARISON_DIR" -ForegroundColor Cyan
Write-Host ""

# List generated files
$plotFiles = Get-ChildItem $COMPARISON_DIR -Recurse -File -ErrorAction SilentlyContinue
if ($plotFiles.Count -gt 0) {
    Write-Host "  Generated files:" -ForegroundColor White
    $systemPlots = $plotFiles | Where-Object { $_.DirectoryName -like "*system*" }
    $classPlots  = $plotFiles | Where-Object { $_.DirectoryName -like "*class*" }
    $analyPlots  = $plotFiles | Where-Object { $_.DirectoryName -like "*analysis*" }
    
    if ($systemPlots.Count -gt 0) {
        Write-Host "    System plots:   $($systemPlots.Count) files" -ForegroundColor Gray
    }
    if ($classPlots.Count -gt 0) {
        Write-Host "    Class plots:    $($classPlots.Count) files" -ForegroundColor Gray
    }
    if ($analyPlots.Count -gt 0) {
        Write-Host "    Analysis plots: $($analyPlots.Count) files" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Green
