# PowerShell script to run Nation Wants to Guess app
# Run this in PowerShell and follow the prompts

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host " Nation Wants to Guess - Scoring System" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python from https://www.python.org/" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check dependencies
Write-Host "`nChecking dependencies..." -ForegroundColor Yellow

$dependencies = @('kivy', 'fastapi', 'uvicorn', 'sqlalchemy', 'requests')
$missing = @()

foreach ($pkg in $dependencies) {
    try {
        python -c "import $pkg" 2>&1 | Out-Null
        Write-Host "  ✓ $pkg" -ForegroundColor Green
    } catch {
        Write-Host "  ✗ $pkg (missing)" -ForegroundColor Red
        $missing += $pkg
    }
}

if ($missing.Count -gt 0) {
    Write-Host "`nInstalling missing packages..." -ForegroundColor Yellow
    pip install $missing
}

# Start app
Write-Host "`nStarting Nation Wants to Guess..." -ForegroundColor Green
Write-Host "(The backend server will start automatically)`n" -ForegroundColor Gray

Set-Location $PSScriptRoot
python frontend/main.py

Write-Host "`nApp closed." -ForegroundColor Yellow
Read-Host "Press Enter to exit"
