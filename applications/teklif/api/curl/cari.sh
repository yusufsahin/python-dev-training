#!/usr/bin/env bash
# Örnek curl komutları — backend URL'ini kendi ortamınıza göre değiştirin.
set -euo pipefail

BASE="${TEKLIF_API_BASE:-http://localhost:3000}"

echo "GET $BASE/api/cariler"
curl -sS -H "Accept: application/json" "$BASE/api/cariler" | jq .

echo
echo "POST $BASE/api/cariler"
curl -sS -X POST "$BASE/api/cariler" \
  -H "Content-Type: application/json" \
  -d '{"unvan":"cURL Müşteri","vergiNo":"1111111111","eposta":"curl@ornek.com","telefon":"+902120000000"}' | jq .
