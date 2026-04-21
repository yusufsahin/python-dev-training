# PowerShell curl örnekleri (Invoke-RestMethod)
$Base = if ($env:TEKLIF_API_BASE) { $env:TEKLIF_API_BASE } else { "http://localhost:3000" }

Write-Host "GET $Base/api/cariler"
Invoke-RestMethod -Uri "$Base/api/cariler" -Method Get

Write-Host "`nPOST $Base/api/cariler"
$body = @{
  unvan    = "PowerShell Müşteri"
  vergiNo  = "2222222222"
  eposta   = "ps@ornek.com"
  telefon  = "+902121112233"
} | ConvertTo-Json

Invoke-RestMethod -Uri "$Base/api/cariler" -Method Post -Body $body -ContentType "application/json"
