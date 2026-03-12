param(
    [ValidateSet("start")]
    [string]$Command = "start"
)

$BACKEND_PORT = 8000
$FRONTEND_PORT = 5173
$BACKEND_PATH = "E:\JOB\git-hub-projects\CommitMentIssues\backend"
$FRONTEND_PATH = "E:\JOB\git-hub-projects\CommitMentIssues\frontend"

function Test-PortOpen {
    param([int]$Port)

    try {
        $client = New-Object System.Net.Sockets.TcpClient
        $async = $client.BeginConnect("localhost", $Port, $null, $null)
        $success = $async.AsyncWaitHandle.WaitOne(1000, $false)

        if (-not $success) {
            $client.Close()
            return $false
        }

        $client.EndConnect($async)
        $client.Close()
        return $true
    }
    catch {
        return $false
    }
}

function Wait-ForService {
    param(
        [int]$Port,
        [int]$TimeoutSeconds = 60
    )

    $startTime = Get-Date

    while (-not (Test-PortOpen -Port $Port)) {
        Start-Sleep -Seconds 1

        if (((Get-Date) - $startTime).TotalSeconds -ge $TimeoutSeconds) {
            throw "Service on port $Port did not start within $TimeoutSeconds seconds."
        }
    }
}

function Start-Backend {
    if (Test-PortOpen -Port $BACKEND_PORT) {
        Write-Host "Backend is already running on port $BACKEND_PORT."
        return
    }

    if (-not (Test-Path $BACKEND_PATH)) {
        throw "Backend path does not exist: $BACKEND_PATH"
    }

    Write-Host "Starting backend on port $BACKEND_PORT..."

    Start-Process `
        -FilePath "cmd.exe" `
        -ArgumentList '/k python -m uvicorn app.main:app --reload' `
        -WorkingDirectory $BACKEND_PATH `
        -WindowStyle Normal | Out-Null

    Wait-ForService -Port $BACKEND_PORT
    Write-Host "Backend started successfully."
}

function Start-Frontend {
    if (Test-PortOpen -Port $FRONTEND_PORT) {
        Write-Host "Frontend is already running on port $FRONTEND_PORT."
        return
    }

    if (-not (Test-Path $FRONTEND_PATH)) {
        throw "Frontend path does not exist: $FRONTEND_PATH"
    }

    Write-Host "Starting frontend on port $FRONTEND_PORT..."

    Start-Process `
        -FilePath "cmd.exe" `
        -ArgumentList '/k npm run dev -- --host localhost --port 5173' `
        -WorkingDirectory $FRONTEND_PATH `
        -WindowStyle Normal | Out-Null

    Wait-ForService -Port $FRONTEND_PORT
    Write-Host "Frontend started successfully."
}

if ($Command -eq "start") {
    Start-Backend
    Start-Frontend
    Write-Host "All services are running."
}