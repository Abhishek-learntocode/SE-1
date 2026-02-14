# ==============================================================================
# record_snapshot.ps1 - Record a metrics snapshot of your source code
# ==============================================================================
#
# Automatically scans the project's app/src directory with CK, Checkstyle,
# PMD, Designite and saves all raw data + system-level metrics + instance
# plots into: data_archive/<Name>/
#
# The source path is auto-derived from the project structure. No need to
# specify it manually.
#
# Usage:
#   .\record_snapshot.ps1 -Name "R1.2_before"
#   .\record_snapshot.ps1 -Name "R1.2_after"
#
# Optional: override auto-detected source path
#   .\record_snapshot.ps1 -Name "R1.2_before" -SourcePath "C:\...\other\src"
#
# Then compare two snapshots:
#   .\compare_snapshots.ps1 -Before "R1.2_before" -After "R1.2_after"
# ==============================================================================

param(
    [Parameter(Mandatory=$true)]
    [string]$Name,

    [Parameter(Mandatory=$false)]
    [string]$SourcePath
)

# ==============================================================================
# CONFIGURATION - derived relative to this script's location
# ==============================================================================

$SCRIPT_DIR   = Split-Path -Parent $MyInvocation.MyCommand.Path
$LAB_DIR      = Split-Path -Parent $SCRIPT_DIR
$PROJECT_ROOT = Split-Path -Parent $LAB_DIR

# Auto-derive source path if not provided
if (-not $SourcePath) {
    $SourcePath = Join-Path $PROJECT_ROOT "app\src"
}

$PATH_TO_CK_JAR     = Join-Path $LAB_DIR "bin\ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar"
$PATH_TO_CHECKSTYLE  = Join-Path $LAB_DIR "bin\checkstyle-13.2.0-all.jar"
$PATH_TO_PMD_BAT     = Join-Path $LAB_DIR "bin\pmd-bin\bin\pmd.bat"
$PATH_TO_DESIGNITE   = Join-Path $LAB_DIR "bin\DesigniteJava.jar"
$PATH_TO_SUN_CHECKS  = Join-Path $LAB_DIR "configs\sun_checks.xml"

$PATH_TO_COLLECTOR    = Join-Path $SCRIPT_DIR "collect_metrics.py"
$PATH_TO_SIMPLE_PLOTS = Join-Path $SCRIPT_DIR "simple_plots.py"

# ==============================================================================
# VALIDATE
# ==============================================================================

if (-not (Test-Path $SourcePath)) {
    Write-Host "[ERROR] Source path does not exist: $SourcePath" -ForegroundColor Red
    Write-Host "        Auto-detected from project root: $PROJECT_ROOT" -ForegroundColor Red
    Write-Host "        You can override with: -SourcePath 'C:\...\your\src'" -ForegroundColor Yellow
    exit 1
}

# ==============================================================================
# SETUP OUTPUT
# ==============================================================================

$DATA_ARCHIVE = Join-Path $LAB_DIR "data_archive"
$SNAPSHOT_DIR = Join-Path $DATA_ARCHIVE $Name

if (Test-Path $SNAPSHOT_DIR) {
    Write-Host "[WARN] Snapshot '$Name' already exists. Overwriting..." -ForegroundColor Yellow
    Remove-Item $SNAPSHOT_DIR -Recurse -Force
}

New-Item -ItemType Directory -Force -Path $SNAPSHOT_DIR | Out-Null
$SNAPSHOT_ABS = (Resolve-Path $SNAPSHOT_DIR).Path

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  RECORD SNAPSHOT: $Name" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Source:   $SourcePath"
Write-Host "  Output:   $SNAPSHOT_ABS"
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

# ==============================================================================
# STEP 1: RUN ANALYSIS TOOLS
# ==============================================================================

# 1a. CK Metrics
if (Test-Path $PATH_TO_CK_JAR) {
    Write-Host "[1/4] Running CK Metrics..." -ForegroundColor Yellow
    $CK_OUT = Join-Path $SNAPSHOT_ABS " "
    $CK_OUT = $SNAPSHOT_ABS.TrimEnd('\') + '\'
    java -jar $PATH_TO_CK_JAR $SourcePath false 0 false $CK_OUT 2>&1 | Out-Null
    $classFile = Join-Path $SNAPSHOT_DIR "class.csv"
    if (Test-Path $classFile) {
        $classCount = (Import-Csv $classFile).Count
        Write-Host "      [OK] class.csv generated ($classCount classes)" -ForegroundColor Green
    }
    else {
        Write-Host "      [FAIL] class.csv NOT generated - aborting" -ForegroundColor Red
        exit 1
    }
}
else {
    Write-Host "[ERROR] CK jar not found: $PATH_TO_CK_JAR" -ForegroundColor Red
    exit 1
}

# 1b. Checkstyle
if (Test-Path $PATH_TO_CHECKSTYLE) {
    Write-Host "[2/4] Running Checkstyle..." -ForegroundColor Yellow
    if (Test-Path $PATH_TO_SUN_CHECKS) {
        $CONFIG = $PATH_TO_SUN_CHECKS
    }
    else {
        $CONFIG = "/sun_checks.xml"
    }
    Write-Host "      Config: $CONFIG" -ForegroundColor Gray
    $CS_OUTPUT = Join-Path $SNAPSHOT_ABS "checkstyle_report.xml"

    # Run checkstyle - capture ALL output so we can show errors
    $csResult = java -jar "$PATH_TO_CHECKSTYLE" -c "$CONFIG" -f xml -o "$CS_OUTPUT" "$SourcePath" 2>&1
    $csExit = $LASTEXITCODE

    $csFile = Join-Path $SNAPSHOT_DIR "checkstyle_report.xml"
    if (Test-Path $csFile) {
        Write-Host "      [OK] checkstyle_report.xml generated" -ForegroundColor Green
    }
    else {
        Write-Host "      [FAIL] Checkstyle report not generated!" -ForegroundColor Red
        Write-Host "      Exit code: $csExit" -ForegroundColor Red
        Write-Host "      Jar:    $PATH_TO_CHECKSTYLE" -ForegroundColor Gray
        Write-Host "      Config: $CONFIG" -ForegroundColor Gray
        Write-Host "      Output: $CS_OUTPUT" -ForegroundColor Gray
        Write-Host "      Source: $SourcePath" -ForegroundColor Gray
        Write-Host "      --- Error output ---" -ForegroundColor Yellow
        $csResult | ForEach-Object { Write-Host "      $_" -ForegroundColor Gray }
        Write-Host "      --- End error output ---" -ForegroundColor Yellow
    }
}
else {
    Write-Host "[SKIP] Checkstyle jar not found: $PATH_TO_CHECKSTYLE" -ForegroundColor DarkGray
}

# 1c. PMD
if (Test-Path $PATH_TO_PMD_BAT) {
    Write-Host "[3/4] Running PMD..." -ForegroundColor Yellow
    $PMD_OUTPUT = Join-Path $SNAPSHOT_ABS "pmd_report.xml"
    & $PATH_TO_PMD_BAT check -d $SourcePath -R rulesets/java/quickstart.xml -f xml -r $PMD_OUTPUT 2>&1 | Out-Null
    $pmdFile = Join-Path $SNAPSHOT_DIR "pmd_report.xml"
    if (Test-Path $pmdFile) {
        Write-Host "      [OK] pmd_report.xml generated" -ForegroundColor Green
    }
    else {
        Write-Host "      [WARN] PMD report not generated" -ForegroundColor DarkYellow
    }
}
else {
    Write-Host "[SKIP] PMD not found" -ForegroundColor DarkGray
}

# 1d. Designite
if (Test-Path $PATH_TO_DESIGNITE) {
    Write-Host "[4/4] Running Designite..." -ForegroundColor Yellow
    java -jar "$PATH_TO_DESIGNITE" -i "$SourcePath" -o "$SNAPSHOT_ABS" 2>&1 | Out-Null
    Write-Host "      [OK] Designite completed" -ForegroundColor Green
} else {
    Write-Host "[SKIP] Designite not found" -ForegroundColor DarkGray
}

# ==============================================================================
# STEP 2: COLLECT SYSTEM-LEVEL METRICS
# ==============================================================================

Write-Host ""
Write-Host "[COLLECT] Running metrics collector (system-level)..." -ForegroundColor Yellow
python "$PATH_TO_COLLECTOR" "$SNAPSHOT_ABS" "NONE" "snapshot" "$Name"

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Metrics collection failed!" -ForegroundColor Red
    exit 1
}

# ==============================================================================
# STEP 3: GENERATE INSTANCE PLOTS (current-state visualizations)
# ==============================================================================

if (Test-Path $PATH_TO_SIMPLE_PLOTS) {
    Write-Host ""
    Write-Host "[PLOTS] Generating snapshot visualizations..." -ForegroundColor Yellow
    python "$PATH_TO_SIMPLE_PLOTS" "$SNAPSHOT_ABS"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "      [OK] Instance plots generated" -ForegroundColor Green
    } else {
        Write-Host "      [WARN] Plot generation had issues" -ForegroundColor DarkYellow
    }
} else {
    Write-Host "[SKIP] simple_plots.py not found" -ForegroundColor DarkGray
}

# ==============================================================================
# STEP 4: PRINT SUMMARY
# ==============================================================================

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "  SNAPSHOT '$Name' RECORDED SUCCESSFULLY" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "  Location: $SNAPSHOT_ABS" -ForegroundColor White
Write-Host ""
Write-Host "  Contents:" -ForegroundColor White
Write-Host "    class.csv, method.csv       - CK metrics (raw)" -ForegroundColor Gray
Write-Host "    checkstyle_report.xml       - Checkstyle violations" -ForegroundColor Gray
Write-Host "    pmd_report.xml              - PMD violations" -ForegroundColor Gray
Write-Host "    system/system_metrics.csv   - Aggregated system metrics" -ForegroundColor Gray
Write-Host "    simple_plots/               - Current-state visualizations" -ForegroundColor Gray
Write-Host ""
Write-Host "  To compare with another snapshot:" -ForegroundColor Yellow
Write-Host ('    .\compare_snapshots.ps1 -Before "<other_name>" -After "' + $Name + '"') -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Green
