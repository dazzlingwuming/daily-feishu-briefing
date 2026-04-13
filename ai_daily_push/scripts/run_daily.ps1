$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = "python"
$RunScript = Join-Path $PSScriptRoot "run_once.py"

if (-not (Get-Command $Python -ErrorAction SilentlyContinue)) {
    throw "python not found in PATH"
}

Set-Location $ProjectRoot
& $Python $RunScript
