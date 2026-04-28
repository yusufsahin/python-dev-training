from dataclasses import dataclass, field
from datetime import datetime, UTC
from enum import Enum


class TeklifDurum(str, Enum):
    TASLAK = "TASLAK"
    GONDERILDI = "GONDERILDI"
    ONAYLANDI = "ONAYLANDI"
    IPTAL = "IPTAL"


@dataclass(slots=True)
class TeklifKalemi:
    urun_id: str
    miktar: float
    birim_fiyat: float
    kdv_orani: int

    def ara_toplam(self) -> float:
        if self.miktar <= 0:
            raise ValueError("Kalem miktari 0'dan buyuk olmalidir.")
        if self.kdv_orani < 0 or self.kdv_orani > 100:
            raise ValueError("KDV orani 0-100 araliginda olmalidir.")
        return self.miktar * self.birim_fiyat

    def kdv_tutari(self) -> float:
        return self.ara_toplam() * self.kdv_orani / 100


@dataclass(slots=True)
class Teklif:
    id: str
    cari_id: str
    para_birimi: str
    durum: TeklifDurum = TeklifDurum.TASLAK
    kalemler: list[TeklifKalemi] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def toplam_tutar(self) -> float:
        return sum(k.ara_toplam() for k in self.kalemler)

    def toplam_kdv(self) -> float:
        return sum(k.kdv_tutari() for k in self.kalemler)

    def genel_toplam(self) -> float:
        return self.toplam_tutar() + self.toplam_kdv()
