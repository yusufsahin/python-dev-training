from dataclasses import dataclass
from enum import Enum


class UrunTur(str, Enum):
    URUN = "URUN"
    HIZMET = "HIZMET"


@dataclass(slots=True)
class Urun:
    id: str
    tur: UrunTur
    ad: str
    sku: str
    barkod: str
    birim: str
    kdv_orani: int
    satis_fiyati: float
    alis_fiyati: float
    doviz_kodu: str
    kategori: str
    fiyat_listesi_adi: str
    aktif: bool
