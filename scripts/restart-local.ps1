param(
    [int]$Port = 8001,
    [string]$AdminCode = ""
)

$ErrorActionPreference = "Stop"
$workspacePath = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$pythonPath = Join-Path $workspacePath ".venv\Scripts\python.exe"
$dataPath = Join-Path $workspacePath "workshop_data\live-manual"

if (-not (Test-Path -LiteralPath $pythonPath -PathType Leaf)) {
    throw "Virtual environment not found at $pythonPath"
}

$secureKey = Read-Host "Paste DEEPAGENTS_CODE_OPENAI_API_KEY" -AsSecureString
$keyPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureKey)
try {
    $plainKey = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($keyPointer)
} finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($keyPointer)
}
if ([string]::IsNullOrWhiteSpace($plainKey)) {
    throw "API key cannot be empty"
}

$listeners = @(
    Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty OwningProcess -Unique
)
if ($listeners.Count -gt 1) {
    throw "More than one process is listening on port $Port"
}
if ($listeners.Count -eq 1) {
    $listener = Get-CimInstance Win32_Process -Filter "ProcessId=$($listeners[0])"
    if (-not $listener -or $listener.CommandLine -notmatch "workshop_runner") {
        throw "Port $Port is not owned by the workshop runner"
    }
    Stop-Process -Id $listeners[0] -Force
    $stopDeadline = (Get-Date).AddSeconds(10)
    do {
        Start-Sleep -Milliseconds 200
        $occupied = Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue
    } while ($occupied -and (Get-Date) -lt $stopDeadline)
    if ($occupied) {
        throw "The old workshop process did not release port $Port"
    }
}

$env:DEEPAGENTS_CODE_OPENAI_API_KEY = $plainKey
$env:WORKSHOP_ADMIN_CODE = $AdminCode
$env:WORKSHOP_PARTICIPANTS = "12"
$env:WORKSHOP_MIN_PARTICIPANTS = "2"
$env:WORKSHOP_ROUTING_MODE = "circular"
$env:WORKSHOP_AGENT_MODE = "dcode"
$env:WORKSHOP_MODEL = "gpt-5.6-luna"
$env:WORKSHOP_REASONING_EFFORT = "medium"
$env:WORKSHOP_HOST = "0.0.0.0"
$env:WORKSHOP_PORT = "$Port"
$env:WORKSHOP_OPEN_BROWSER = "false"
$env:WORKSHOP_DATA_DIR = $dataPath

$stdoutPath = Join-Path $dataPath "server.stdout.log"
$stderrPath = Join-Path $dataPath "server.stderr.log"
$process = Start-Process `
    -FilePath $pythonPath `
    -ArgumentList @("-m", "workshop_runner") `
    -WorkingDirectory $workspacePath `
    -WindowStyle Hidden `
    -RedirectStandardOutput $stdoutPath `
    -RedirectStandardError $stderrPath `
    -PassThru

$plainKey = $null
$env:DEEPAGENTS_CODE_OPENAI_API_KEY = $null

$readyDeadline = (Get-Date).AddSeconds(25)
do {
    Start-Sleep -Milliseconds 300
    try {
        $health = Invoke-RestMethod "http://127.0.0.1:$Port/api/health" -TimeoutSec 2
    } catch {
        $health = $null
    }
} while (-not $health -and (Get-Date) -lt $readyDeadline)

if (-not $health) {
    throw "The new workshop process did not become healthy. See $stderrPath"
}

Write-Host "Workshop restarted (PID $($process.Id))." -ForegroundColor Green
Write-Host ($health | ConvertTo-Json -Compress)
Start-Sleep -Seconds 4
