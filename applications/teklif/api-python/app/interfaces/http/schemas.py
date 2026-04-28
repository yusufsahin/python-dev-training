from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class CariCreateRequest(BaseModel):
    unvan: str
    vergiNo: str
    eposta: str
    telefon: str


class CariResponse(CariCreateRequest):
    id: str


class UrunCreateRequest(BaseModel):
    tur: Literal["URUN", "HIZMET"]
    ad: str
    sku: str
    barkod: str = ""
    birim: str
    kdvOrani: int = Field(ge=0, le=100)
    satisFiyati: float
    alisFiyati: float
    dovizKodu: Literal["TRY"] = "TRY"
    kategori: str
    fiyatListesiAdi: str
    aktif: bool = True


class UrunResponse(UrunCreateRequest):
    id: str


class TeklifKalemiRequest(BaseModel):
    urunId: str
    miktar: float = Field(gt=0)
    birimFiyat: float
    kdvOrani: int = Field(ge=0, le=100)


class TeklifCreateRequest(BaseModel):
    cariId: str
    paraBirimi: Literal["TRY"] = "TRY"
    kalemler: list[TeklifKalemiRequest]


class TeklifDurumUpdateRequest(BaseModel):
    durum: Literal["TASLAK", "GONDERILDI", "ONAYLANDI", "IPTAL"]


class TeklifKalemiResponse(TeklifKalemiRequest):
    araToplam: float
    kdvTutari: float


class TeklifResponse(BaseModel):
    id: str
    cariId: str
    paraBirimi: str
    durum: str
    kalemler: list[TeklifKalemiResponse]
    toplamTutar: float
    toplamKdv: float
    genelToplam: float
    createdAt: datetime
