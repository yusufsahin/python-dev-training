from uuid import uuid4

from app.domain.repositories import TeklifRepositoryPort
from app.domain.teklif import Teklif, TeklifDurum, TeklifKalemi


class TeklifService:
    def __init__(self, repo: TeklifRepositoryPort) -> None:
        self.repo = repo

    def list_teklifler(self) -> list[Teklif]:
        return self.repo.list_all()

    def get_teklif(self, teklif_id: str) -> Teklif | None:
        return self.repo.get_by_id(teklif_id)

    def create_teklif(self, payload: dict) -> Teklif:
        kalemler = [
            TeklifKalemi(
                urun_id=kalem["urun_id"],
                miktar=kalem["miktar"],
                birim_fiyat=kalem["birim_fiyat"],
                kdv_orani=kalem["kdv_orani"],
            )
            for kalem in payload["kalemler"]
        ]
        teklif = Teklif(
            id=str(uuid4()),
            cari_id=payload["cari_id"],
            para_birimi=payload.get("para_birimi", "TRY"),
            durum=TeklifDurum.TASLAK,
            kalemler=kalemler,
        )
        return self.repo.create(teklif)

    def update_durum(self, teklif_id: str, durum: TeklifDurum) -> Teklif | None:
        teklif = self.repo.get_by_id(teklif_id)
        if teklif is None:
            return None
        teklif.durum = durum
        return self.repo.update(teklif)
