$ErrorActionPreference = "Stop"

chcp 65001 > $null
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)

$Workspace = Split-Path -Parent $PSScriptRoot
$PromptFile = Join-Path $PSScriptRoot "briefing_prompt.txt"
$LogsDir = Join-Path $PSScriptRoot "logs"
$OutputDir = Join-Path $PSScriptRoot "output"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$StdoutLog = Join-Path $LogsDir "codex_briefing_$Timestamp.log"
$LastMessageFile = Join-Path $LogsDir "codex_briefing_last_message_$Timestamp.txt"
$ReportFile = Join-Path $OutputDir "briefing_feishu_today.txt"
$ShellEdition = $PSVersionTable.PSEdition
$DirectSendMode = $ShellEdition -eq "Core"

$Codex = "C:\Users\lihaodong\AppData\Roaming\npm\codex.CMD"

if (-not (Test-Path $Codex)) {
    throw "codex executable not found: $Codex"
}

if (-not (Test-Path $PromptFile)) {
    throw "briefing_prompt.txt not found"
}

New-Item -ItemType Directory -Force $LogsDir | Out-Null
New-Item -ItemType Directory -Force $OutputDir | Out-Null
Set-Location $Workspace
if (Test-Path $ReportFile) {
    Remove-Item -LiteralPath $ReportFile -Force
}

$prompt = Get-Content $PromptFile -Raw -Encoding UTF8
$prompt = $prompt + "`r`n`r`nWrite the final report to this exact UTF-8 file path:`r`n$ReportFile`r`n"
if ($DirectSendMode) {
    $prompt = $prompt + @"

Execution mode from wrapper:
- The current shell is PowerShell Core (`pwsh`).
- After you finish the report and write it to the report file, send the final report to Feishu yourself with local `lark-cli`.
- Read `FEISHU_RECEIVER_OPEN_ID` from `D:\APP_self\热点论文和学术skill\ai_daily_push\.env`.
- Use `--as bot`.
- Do not use any Python sender helper for this send step.
- After sending, briefly confirm success and include the Feishu message id.
"@
}
else {
    $prompt = $prompt + @"

Execution mode from wrapper:
- The current shell is Windows PowerShell Desktop.
- Do not send the Feishu message yourself in this mode.
- Only write the finished report to the report file and confirm the file was created.
- The wrapper will send the UTF-8 file through the Python fallback sender after Codex exits.
"@
}
Write-Host "Starting Codex briefing run..."
Write-Host "Workspace: $Workspace"
Write-Host "Log: $StdoutLog"
Write-Host "Last message: $LastMessageFile"
Write-Host "Report file: $ReportFile"
Write-Host "Shell edition: $ShellEdition"
Write-Host ("Delivery mode: " + ($(if ($DirectSendMode) { "Codex direct lark-cli send" } else { "Python fallback sender" })))
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

if ($DirectSendMode) {
    $hasMessageId = $false
    if (Test-Path $StdoutLog) {
        $hasMessageId = [bool](Select-String -Path $StdoutLog -Pattern "message_id|message id" -Quiet)
    }
    if (-not $hasMessageId -and (Test-Path $LastMessageFile)) {
        $hasMessageId = [bool](Select-String -Path $LastMessageFile -Pattern "message_id|message id" -Quiet)
    }
    if (-not $hasMessageId) {
        throw "codex direct-send mode finished without any message id in the log output"
    }
    Write-Host "Report generated and Codex direct Feishu delivery completed."
}
else {
    python .\codex_scheduler\send_feishu_from_file.py --file $ReportFile | Tee-Object -FilePath $StdoutLog -Append

    if ($LASTEXITCODE -ne 0) {
        throw "report send failed with exit code $LASTEXITCODE"
    }

    Write-Host "Report generated and Feishu delivery completed via Python fallback sender."
}
