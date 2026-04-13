$ErrorActionPreference = "Stop"

chcp 65001 > $null
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)

$Workspace = Split-Path -Parent $PSScriptRoot
$PromptFile = Join-Path $PSScriptRoot "briefing_prompt.txt"
$LogsDir = Join-Path $PSScriptRoot "logs"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$StdoutLog = Join-Path $LogsDir "codex_briefing_$Timestamp.log"
$LastMessageFile = Join-Path $LogsDir "codex_briefing_last_message_$Timestamp.txt"
$ReportFile = Join-Path $Workspace "ai_daily_push\briefing_feishu_today.txt"

$Codex = "C:\Users\lihaodong\AppData\Roaming\npm\codex.CMD"

if (-not (Test-Path $Codex)) {
    throw "codex executable not found: $Codex"
}

if (-not (Test-Path $PromptFile)) {
    throw "briefing_prompt.txt not found"
}

New-Item -ItemType Directory -Force $LogsDir | Out-Null
Set-Location $Workspace
if (Test-Path $ReportFile) {
    Remove-Item -LiteralPath $ReportFile -Force
}

$prompt = Get-Content $PromptFile -Raw -Encoding UTF8
$prompt = $prompt + "`r`n`r`nWrite the final report to this exact UTF-8 file path:`r`n$ReportFile`r`n"
Write-Host "Starting Codex briefing run..."
Write-Host "Workspace: $Workspace"
Write-Host "Log: $StdoutLog"
Write-Host "Last message: $LastMessageFile"
Write-Host "Report file: $ReportFile"
$codexFailed = $false
$codexExitCode = 0

try {
    $prompt | & $Codex `
        --search `
        exec `
        --json `
        --color never `
        --skip-git-repo-check `
        --dangerously-bypass-approvals-and-sandbox `
        -C $Workspace `
        -o $LastMessageFile `
        - 2>&1 | Tee-Object -FilePath $StdoutLog
    $codexExitCode = $LASTEXITCODE
}
catch {
    $codexFailed = $true
    $codexExitCode = $LASTEXITCODE
    $_ | Out-String | Tee-Object -FilePath $StdoutLog -Append | Out-Null
}

if (-not (Test-Path $ReportFile)) {
    if ($codexFailed -or $codexExitCode -ne 0) {
        throw "codex exec failed with exit code $codexExitCode and report file was not created"
    }
    throw "codex completed but report file was not created: $ReportFile"
}

python .\ai_daily_push\scripts\send_test_message.py --file $ReportFile | Tee-Object -FilePath $StdoutLog -Append

if ($LASTEXITCODE -ne 0) {
    throw "report send failed with exit code $LASTEXITCODE"
}

Write-Host "Report generated and Feishu delivery completed."
