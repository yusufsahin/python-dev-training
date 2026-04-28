from sqlalchemy.orm import Session

from app.domain.cari import Cari
from app.domain.repositories import CariRepositoryPort, TeklifRepositoryPort, UrunRepositoryPort
from app.domain.teklif import Teklif, TeklifDurum, TeklifKalemi
from app.domain.urun import Urun, UrunTur
from app.infrastructure.db.models import CariModel, TeklifKalemiModel, TeklifModel, UrunModel


class SqlAlchemyCariRepository(CariRepositoryPort):
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_all(self) -> list[Cari]:
        rows = self.session.query(CariModel).all()
        return [Cari(id=r.id, unvan=r.unvan, vergi_no=r.vergi_no, eposta=r.eposta, telefon=r.telefon) for r in rows]

    def get_by_id(self, entity_id: str) -> Cari | None:
        row = self.session.get(CariModel, entity_id)
        if row is None:
            return None
        return Cari(id=row.id, unvan=row.unvan, vergi_no=row.vergi_no, eposta=row.eposta, telefon=row.telefon)

    def create(self, cari: Cari) -> Cari:
        row = CariModel(
            id=cari.id,
            unvan=cari.unvan,
            vergi_no=cari.vergi_no,
            eposta=cari.eposta,
            telefon=cari.telefon,
        )
        self.session.add(row)
        self.session.commit()
        return cari

    def update(self, cari: Cari) -> Cari | None:
        row = self.session.get(CariModel, cari.id)
        if row is None:
            return None
        row.unvan = cari.unvan
        row.vergi_no = cari.vergi_no
        row.eposta = cari.eposta
        row.telefon = cari.telefon
        self.session.commit()
        return cari

    def delete(self, entity_id: str) -> bool:
        row = self.session.get(CariModel, entity_id)
        if row is None:
            return False
        self.session.delete(row)
        self.session.commit()
        return True


class SqlAlchemyUrunRepository(UrunRepositoryPort):
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_all(self) -> list[Urun]:
        rows = self.session.query(UrunModel).all()
        return [
            Urun(
                id=r.id,
                tur=UrunTur(r.tur),
                ad=r.ad,
                sku=r.sku,
                barkod=r.barkod,
                birim=r.birim,
                kdv_orani=r.kdv_orani,
                satis_fiyati=r.satis_fiyati,
                alis_fiyati=r.alis_fiyati,
                doviz_kodu=r.doviz_kodu,
                kategori=r.kategori,
                fiyat_listesi_adi=r.fiyat_listesi_adi,
                aktif=r.aktif,
            )
            for r in rows
        ]

    def get_by_id(self, entity_id: str) -> Urun | None:
        r = self.session.get(UrunModel, entity_id)
        if r is None:
            return None
        return Urun(
            id=r.id,
            tur=UrunTur(r.tur),
            ad=r.ad,
            sku=r.sku,
            barkod=r.barkod,
            birim=r.birim,
            kdv_orani=r.kdv_orani,
            satis_fiyati=r.satis_fiyati,
            alis_fiyati=r.alis_fiyati,
            doviz_kodu=r.doviz_kodu,
            kategori=r.kategori,
            fiyat_listesi_adi=r.fiyat_listesi_adi,
            aktif=r.aktif,
        )

    def create(self, urun: Urun) -> Urun:
        self.session.add(
            UrunModel(
                id=urun.id,
                tur=urun.tur.value,
                ad=urun.ad,
                sku=urun.sku,
                barkod=urun.barkod,
                birim=urun.birim,
                kdv_orani=urun.kdv_orani,
                satis_fiyati=urun.satis_fiyati,
                alis_fiyati=urun.alis_fiyati,
                doviz_kodu=urun.doviz_kodu,
                kategori=urun.kategori,
                fiyat_listesi_adi=urun.fiyat_listesi_adi,
                aktif=urun.aktif,
            )
        )
        self.session.commit()
        return urun

    def update(self, urun: Urun) -> Urun | None:
        r = self.session.get(UrunModel, urun.id)
        if r is None:
            return None
        r.tur = urun.tur.value
        r.ad = urun.ad
        r.sku = urun.sku
        r.barkod = urun.barkod
        r.birim = urun.birim
        r.kdv_orani = urun.kdv_orani
        r.satis_fiyati = urun.satis_fiyati
        r.alis_fiyati = urun.alis_fiyati
        r.doviz_kodu = urun.doviz_kodu
        r.kategori = urun.kategori
        r.fiyat_listesi_adi = urun.fiyat_listesi_adi
        r.aktif = urun.aktif
        self.session.commit()
        return urun

    def delete(self, entity_id: str) -> bool:
        row = self.session.get(UrunModel, entity_id)
        if row is None:
            return False
        self.session.delete(row)
        self.session.commit()
        return True


class SqlAlchemyTeklifRepository(TeklifRepositoryPort):
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_all(self) -> list[Teklif]:
        rows = self.session.query(TeklifModel).all()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, entity_id: str) -> Teklif | None:
        row = self.session.get(TeklifModel, entity_id)
        if row is None:
            return None
        return self._to_domain(row)

    def create(self, teklif: Teklif) -> Teklif:
        row = TeklifModel(
            id=teklif.id,
            cari_id=teklif.cari_id,
            para_birimi=teklif.para_birimi,
            durum=teklif.durum.value,
            created_at=teklif.created_at,
            kalemler=[
                TeklifKalemiModel(
                    urun_id=k.urun_id,
                    miktar=k.miktar,
                    birim_fiyat=k.birim_fiyat,
                    kdv_orani=k.kdv_orani,
                )
                for k in teklif.kalemler
            ],
        )
        self.session.add(row)
        self.session.commit()
        return teklif

    def update(self, teklif: Teklif) -> Teklif | None:
        row = self.session.get(TeklifModel, teklif.id)
        if row is None:
            return None
        row.durum = teklif.durum.value
        self.session.commit()
        return teklif

    @staticmethod
    def _to_domain(model: TeklifModel) -> Teklif:
        return Teklif(
            id=model.id,
            cari_id=model.cari_id,
            para_birimi=model.para_birimi,
            durum=TeklifDurum(model.durum),
            kalemler=[
                TeklifKalemi(
                    urun_id=k.urun_id,
                    miktar=k.miktar,
                    birim_fiyat=k.birim_fiyat,
                    kdv_orani=k.kdv_orani,
                )
                for k in model.kalemler
            ],
            created_at=model.created_at,
        )
