"""
OpenAPI kontratını infra/contracts/openapi.json olarak dondurur.
Çalıştırma: python scripts/export_openapi.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app  # noqa: E402

output_path = Path(__file__).parent.parent / "infra" / "contracts" / "openapi.json"
output_path.parent.mkdir(parents=True, exist_ok=True)

schema = app.openapi()
output_path.write_text(json.dumps(schema, indent=2, ensure_ascii=False))
print(f"OpenAPI schema written: {output_path}")
