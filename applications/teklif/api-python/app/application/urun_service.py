from uuid import uuid4

from app.domain.repositories import UrunRepositoryPort
from app.domain.urun import Urun, UrunTur


class UrunService:
    def __init__(self, repo: UrunRepositoryPort) -> None:
        self.repo = repo

    def list_urunler(self) -> list[Urun]:
        return self.repo.list_all()

    def get_urun(self, urun_id: str) -> Urun | None:
        return self.repo.get_by_id(urun_id)

    def create_urun(self, payload: dict) -> Urun:
        urun = Urun(
            id=str(uuid4()),
            tur=UrunTur(payload["tur"]),
            ad=payload["ad"],
            sku=payload["sku"],
            barkod=payload.get("barkod", ""),
            birim=payload["birim"],
            kdv_orani=payload["kdv_orani"],
            satis_fiyati=payload["satis_fiyati"],
            alis_fiyati=payload["alis_fiyati"],
            doviz_kodu=payload["doviz_kodu"],
            kategori=payload["kategori"],
            fiyat_listesi_adi=payload["fiyat_listesi_adi"],
            aktif=payload["aktif"],
        )
        return self.repo.create(urun)

    def update_urun(self, urun_id: str, payload: dict) -> Urun | None:
        urun = Urun(
            id=urun_id,
            tur=UrunTur(payload["tur"]),
            ad=payload["ad"],
            sku=payload["sku"],
            barkod=payload.get("barkod", ""),
            birim=payload["birim"],
            kdv_orani=payload["kdv_orani"],
            satis_fiyati=payload["satis_fiyati"],
            alis_fiyati=payload["alis_fiyati"],
            doviz_kodu=payload["doviz_kodu"],
            kategori=payload["kategori"],
            fiyat_listesi_adi=payload["fiyat_listesi_adi"],
            aktif=payload["aktif"],
        )
        return self.repo.update(urun)

    def delete_urun(self, urun_id: str) -> bool:
        return self.repo.delete(urun_id)
