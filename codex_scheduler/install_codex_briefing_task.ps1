param(
    [string]$TaskName = "Codex AI Daily Briefing",
    [string]$Time = "09:00"
)

$ErrorActionPreference = "Stop"

$RunScript = Join-Path $PSScriptRoot "run_codex_briefing.ps1"
$PowerShellExe = (Get-Command powershell).Source

if (-not (Test-Path $RunScript)) {
    throw "run_codex_briefing.ps1 not found"
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
    -Description "Run Codex with ai-daily-feishu-briefing and send a Feishu daily briefing." `
    -Force | Out-Null

Write-Host "Scheduled task installed."
Write-Host "TaskName: $TaskName"
Write-Host "Time: $Time"
