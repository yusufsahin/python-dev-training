from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.base import Base


class CariModel(Base):
    __tablename__ = "cariler"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    unvan: Mapped[str] = mapped_column(String(255), nullable=False)
    vergi_no: Mapped[str] = mapped_column(String(20), nullable=False)
    eposta: Mapped[str] = mapped_column(String(255), nullable=False)
    telefon: Mapped[str] = mapped_column(String(64), nullable=False)


class UrunModel(Base):
    __tablename__ = "urunler"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tur: Mapped[str] = mapped_column(String(16), nullable=False)
    ad: Mapped[str] = mapped_column(String(255), nullable=False)
    sku: Mapped[str] = mapped_column(String(100), nullable=False)
    barkod: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    birim: Mapped[str] = mapped_column(String(50), nullable=False)
    kdv_orani: Mapped[int] = mapped_column(Integer, nullable=False)
    satis_fiyati: Mapped[float] = mapped_column(Float, nullable=False)
    alis_fiyati: Mapped[float] = mapped_column(Float, nullable=False)
    doviz_kodu: Mapped[str] = mapped_column(String(8), nullable=False, default="TRY")
    kategori: Mapped[str] = mapped_column(String(100), nullable=False)
    fiyat_listesi_adi: Mapped[str] = mapped_column(String(100), nullable=False)
    aktif: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class TeklifModel(Base):
    __tablename__ = "teklifler"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    cari_id: Mapped[str] = mapped_column(String(64), ForeignKey("cariler.id"), nullable=False)
    para_birimi: Mapped[str] = mapped_column(String(8), nullable=False, default="TRY")
    durum: Mapped[str] = mapped_column(String(32), nullable=False, default="TASLAK")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    kalemler: Mapped[list["TeklifKalemiModel"]] = relationship(
        back_populates="teklif",
        cascade="all, delete-orphan",
    )


class TeklifKalemiModel(Base):
    __tablename__ = "teklif_kalemleri"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    teklif_id: Mapped[str] = mapped_column(String(64), ForeignKey("teklifler.id"), nullable=False)
    urun_id: Mapped[str] = mapped_column(String(64), ForeignKey("urunler.id"), nullable=False)
    miktar: Mapped[float] = mapped_column(Float, nullable=False)
    birim_fiyat: Mapped[float] = mapped_column(Float, nullable=False)
    kdv_orani: Mapped[int] = mapped_column(Integer, nullable=False)

    teklif: Mapped["TeklifModel"] = relationship(back_populates="kalemler")
