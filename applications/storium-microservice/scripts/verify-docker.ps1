# Yerel Docker: API + Next.js UI doğrulama
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

docker version | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Error "Docker erişilemiyor. Docker Desktop'ı başlatıp tekrar deneyin."
    exit 1
}

$apiPort = if ($env:DOCKER_API_PORT) { $env:DOCKER_API_PORT } else { "8001" }
$uiPort = if ($env:DOCKER_UI_PORT) { $env:DOCKER_UI_PORT } else { "3000" }
$gwPort = if ($env:DOCKER_GATEWAY_WEB_PORT) { $env:DOCKER_GATEWAY_WEB_PORT } else { "9080" }
$apiBase = "http://127.0.0.1:$apiPort"
$uiBase = "http://127.0.0.1:$uiPort"
$gwBase = "http://127.0.0.1:$gwPort"

Write-Host "docker compose build..."
docker compose build
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "docker compose up -d..."
docker compose up -d
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$deadline = (Get-Date).AddSeconds(180)
$apiOk = $false
while ((Get-Date) -lt $deadline -and -not $apiOk) {
    try {
        $r = Invoke-WebRequest -Uri "$apiBase/api/health" -UseBasicParsing -TimeoutSec 5
        if ($r.StatusCode -eq 200) { $apiOk = $true }
    } catch {
        Start-Sleep -Seconds 3
    }
}

if (-not $apiOk) {
    Write-Host "API sağlık uç noktası yanıt vermedi. Son loglar:"
    docker compose logs --tail 80 api
    exit 1
}

$deadline2 = (Get-Date).AddSeconds(120)
$uiOk = $false
while ((Get-Date) -lt $deadline2 -and -not $uiOk) {
    try {
        $r2 = Invoke-WebRequest -Uri $uiBase -UseBasicParsing -TimeoutSec 5
        if ($r2.StatusCode -eq 200) { $uiOk = $true }
    } catch {
        Start-Sleep -Seconds 3
    }
}

if (-not $uiOk) {
    Write-Host "UI yanıt vermedi. Son loglar:"
    docker compose logs --tail 80 ui
    exit 1
}

$deadline3 = (Get-Date).AddSeconds(60)
$gwOk = $false
while ((Get-Date) -lt $deadline3 -and -not $gwOk) {
    try {
        $r3 = Invoke-WebRequest -Uri "$gwBase/api/health" -UseBasicParsing -TimeoutSec 5
        if ($r3.StatusCode -eq 200) { $gwOk = $true }
    } catch {
        Start-Sleep -Seconds 2
    }
}

if (-not $gwOk) {
    Write-Host "Traefik gateway üzerinden /api/health yanıt vermedi. Son loglar:"
    docker compose logs --tail 40 traefik
    docker compose logs --tail 40 api
    exit 1
}

Write-Host "OK: API $apiBase/api/health  |  Gateway $gwBase/api/health  |  UI $uiBase"
docker compose ps
