import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.infrastructure.db.models import CariModel, UrunModel


def seed_from_legacy_json(session: Session) -> None:
    if session.query(CariModel).first() is not None:
        return

    legacy_path = Path(__file__).resolve().parents[4] / "api" / "db.json"
    if not legacy_path.exists():
        return

    payload = json.loads(legacy_path.read_text(encoding="utf-8"))

    for cari in payload.get("cariler", []):
        session.add(
            CariModel(
                id=cari["id"],
                unvan=cari["unvan"],
                vergi_no=cari["vergiNo"],
                eposta=cari["eposta"],
                telefon=cari["telefon"],
            )
        )

    for urun in payload.get("urunler", []):
        session.add(
            UrunModel(
                id=urun["id"],
                tur=urun["tur"],
                ad=urun["ad"],
                sku=urun["sku"],
                barkod=urun.get("barkod", ""),
                birim=urun["birim"],
                kdv_orani=urun["kdvOrani"],
                satis_fiyati=urun["satisFiyati"],
                alis_fiyati=urun["alisFiyati"],
                doviz_kodu=urun.get("dovizKodu", "TRY"),
                kategori=urun["kategori"],
                fiyat_listesi_adi=urun["fiyatListesiAdi"],
                aktif=urun["aktif"],
            )
        )

    session.commit()
