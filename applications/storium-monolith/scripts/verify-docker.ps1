# Yerel Docker: imaj derle, kaldır, ana sayfaya HTTP isteği at
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

docker version | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Error "Docker erişilemiyor. Docker Desktop'ı başlatıp tekrar deneyin."
    exit 1
}

Write-Host "docker compose build..."
docker compose build web
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "docker compose up -d..."
docker compose up -d
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$deadline = (Get-Date).AddSeconds(90)
$ok = $false
while ((Get-Date) -lt $deadline) {
    try {
        $r = Invoke-WebRequest -Uri "http://127.0.0.1:8000/" -UseBasicParsing -TimeoutSec 5
        if ($r.StatusCode -eq 200) {
            $ok = $true
            break
        }
    } catch {
        Start-Sleep -Seconds 3
    }
}

if (-not $ok) {
    Write-Host "Ana sayfa yanit vermedi. Son loglar:"
    docker compose logs --tail 80 web
    exit 1
}

Write-Host "OK: http://localhost:8000/ HTTP 200"
docker compose ps
