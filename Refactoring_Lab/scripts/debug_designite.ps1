# debug_designite.ps1

# 1. DEFINE PATHS (Relative to script location)
$_SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$_LAB_DIR    = Split-Path -Parent $_SCRIPT_DIR
$_PROJECT_ROOT = Split-Path -Parent $_LAB_DIR

$DESIGNITE_JAR = Join-Path $_LAB_DIR "bin\DesigniteJava.jar"
$SOURCE_CODE   = Join-Path $_PROJECT_ROOT "app\src"
$OUTPUT_DIR    = Join-Path $_LAB_DIR "data_archive\debug_test"

# 2. CREATE OUTPUT DIR
New-Item -ItemType Directory -Force -Path $OUTPUT_DIR | Out-Null

# 3. PRINT DIAGNOSTICS
Write-Host "--- DEBUG DIAGNOSTICS ---" -ForegroundColor Cyan
Write-Host "JAR Path: $DESIGNITE_JAR"
if (Test-Path $DESIGNITE_JAR) { Write-Host "   [OK] JAR found." -ForegroundColor Green } 
else { Write-Host "   [FAIL] JAR NOT FOUND!" -ForegroundColor Red }

Write-Host "Source Path: $SOURCE_CODE"
if (Test-Path $SOURCE_CODE) { Write-Host "   [OK] Source found." -ForegroundColor Green } 
else { Write-Host "   [FAIL] Source NOT FOUND!" -ForegroundColor Red }

Write-Host "Java Version:"
java -version

# 4. RUN DESIGNITE (NO SILENCING)
Write-Host "`n--- RUNNING DESIGNITE ---" -ForegroundColor Yellow
Write-Host "Command: java -jar $DESIGNITE_JAR -i $SOURCE_CODE -o $OUTPUT_DIR"

# Execute and capture both stdout and stderr
$ErrorActionPreference = "Continue"
Write-Host "`n--- OUTPUT STARTS ---" -ForegroundColor Magenta
java -jar "$DESIGNITE_JAR" -i "$SOURCE_CODE" -o "$OUTPUT_DIR" 2>&1 | ForEach-Object { Write-Host $_ }
Write-Host "--- OUTPUT ENDS ---" -ForegroundColor Magenta

# 5. CHECK IF OUTPUT FILES WERE CREATED
Write-Host "`n--- CHECKING OUTPUT FILES ---" -ForegroundColor Cyan
if (Test-Path "$OUTPUT_DIR\*.csv") {
    Write-Host "   [SUCCESS] CSV files generated:" -ForegroundColor Green
    Get-ChildItem "$OUTPUT_DIR\*.csv" | ForEach-Object { Write-Host "      - $($_.Name)" }
} else {
    Write-Host "   [FAIL] No CSV files found in output directory!" -ForegroundColor Red
}

Write-Host "`n--- END OF LOG ---" -ForegroundColor Cyan
