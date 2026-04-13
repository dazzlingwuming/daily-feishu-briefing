$ErrorActionPreference = "Stop"

param(
    [string]$TaskName = "AI Daily Push"
)

Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
Write-Host "Scheduled task removed: $TaskName"
