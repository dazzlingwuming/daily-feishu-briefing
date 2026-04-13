$ErrorActionPreference = "Stop"

param(
    [string]$TaskName = "Codex AI Daily Briefing"
)

Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
Write-Host "Scheduled task removed: $TaskName"
