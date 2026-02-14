# ==================================================
# Generate Simple Plots for Current Repository State
# ==================================================
# Shows 6 clear visualizations of what's wrong NOW
# No comparisons, no HTML, just straightforward charts
# ==================================================

param(
    [Parameter(Mandatory=$false)]
    [string]$ArchiveDir = ""
)

$PATH_TO_PYTHON = "python"
$_SP_SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$_SP_LAB_DIR    = Split-Path -Parent $_SP_SCRIPT_DIR
$PATH_TO_SIMPLE_PLOTS = Join-Path $_SP_SCRIPT_DIR "simple_plots.py"

Write-Host "`n=========================================="
Write-Host "   SIMPLE CURRENT-STATE PLOTS"
Write-Host "==========================================" -ForegroundColor Cyan

# If no directory specified, use the latest VALID one
if ($ArchiveDir -eq "") {
    # Find all audit directories with actual data (class.csv exists)
    $ValidDirs = Get-ChildItem (Join-Path $_SP_LAB_DIR "data_archive") -Directory | Where-Object { 
        $_.Name -match '^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}$' -and 
        (Test-Path "$($_.FullName)\class.csv")
    } | Sort-Object Name -Descending
    
    if ($ValidDirs.Count -gt 0) {
        $LatestDir = $ValidDirs | Select-Object -First 1
        $ArchiveDir = $LatestDir.FullName
        Write-Host "[*] Using latest valid audit: $($LatestDir.Name)" -ForegroundColor Yellow
        Write-Host "[*] Found $($ValidDirs.Count) valid audit(s) total" -ForegroundColor Gray
    } else {
        Write-Host "[ERROR] No valid audit directories found. Run .\run_full_audit.ps1 first" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "[*] Using specified directory: $ArchiveDir" -ForegroundColor Gray
    # Validate it has data
    if (-not (Test-Path "$ArchiveDir\class.csv")) {
        Write-Host "[ERROR] Directory exists but has no class.csv file" -ForegroundColor Red
        Write-Host "[*] Run .\run_full_audit.ps1 to generate fresh data" -ForegroundColor Yellow
        exit 1
    }
}

& $PATH_TO_PYTHON $PATH_TO_SIMPLE_PLOTS $ArchiveDir

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[OK] Plots generated successfully!" -ForegroundColor Green
    Write-Host "[*] Location: $ArchiveDir\simple_plots" -ForegroundColor Cyan
} else {
    Write-Host "`n[ERROR] Failed to generate plots" -ForegroundColor Red
    exit 1
}

Write-Host ""
