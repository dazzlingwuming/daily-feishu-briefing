$ErrorActionPreference = "Stop"

param(
    [string]$TaskName = "AI Daily Push",
    [string]$Time = "09:00"
)

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$RunScript = Join-Path $PSScriptRoot "run_daily.ps1"
$PowerShellExe = (Get-Command powershell).Source

if (-not (Test-Path $RunScript)) {
    throw "run_daily.ps1 not found"
}

$taskAction = New-ScheduledTaskAction `
    -Execute $PowerShellExe `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$RunScript`""

$taskTrigger = New-ScheduledTaskTrigger -Daily -At $Time
$taskSettings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $taskAction `
    -Trigger $taskTrigger `
    -Settings $taskSettings `
    -Description "Send the ai_daily_push Feishu briefing every day." `
    -Force | Out-Null

Write-Host "Scheduled task installed."
Write-Host "TaskName: $TaskName"
Write-Host "Time: $Time"
Write-Host "ProjectRoot: $ProjectRoot"
