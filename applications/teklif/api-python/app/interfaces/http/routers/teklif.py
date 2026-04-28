from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.domain.teklif import TeklifDurum
from app.interfaces.http.deps import get_container, db_session_dependency
from app.interfaces.http.schemas import (
    TeklifCreateRequest,
    TeklifDurumUpdateRequest,
    TeklifKalemiResponse,
    TeklifResponse,
)


router = APIRouter(tags=["teklifler"])


def _to_response(item) -> TeklifResponse:
    return TeklifResponse(
        id=item.id,
        cariId=item.cari_id,
        paraBirimi=item.para_birimi,
        durum=item.durum.value,
        kalemler=[
            TeklifKalemiResponse(
                urunId=k.urun_id,
                miktar=k.miktar,
                birimFiyat=k.birim_fiyat,
                kdvOrani=k.kdv_orani,
                araToplam=k.ara_toplam(),
                kdvTutari=k.kdv_tutari(),
            )
            for k in item.kalemler
        ],
        toplamTutar=item.toplam_tutar(),
        toplamKdv=item.toplam_kdv(),
        genelToplam=item.genel_toplam(),
        createdAt=item.created_at,
    )


@router.get("/teklifler", response_model=list[TeklifResponse])
def list_teklifler(session: Session = Depends(db_session_dependency)) -> list[TeklifResponse]:
    service = get_container(session).teklif_service()
    return [_to_response(item) for item in service.list_teklifler()]


@router.get("/teklifler/{teklif_id}", response_model=TeklifResponse)
def get_teklif(teklif_id: str, session: Session = Depends(db_session_dependency)) -> TeklifResponse:
    service = get_container(session).teklif_service()
    teklif = service.get_teklif(teklif_id)
    if teklif is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teklif bulunamadi.")
    return _to_response(teklif)


@router.post("/teklifler", response_model=TeklifResponse, status_code=status.HTTP_201_CREATED)
def create_teklif(payload: TeklifCreateRequest, session: Session = Depends(db_session_dependency)) -> TeklifResponse:
    service = get_container(session).teklif_service()
    created = service.create_teklif(
        {
            "cari_id": payload.cariId,
            "para_birimi": payload.paraBirimi,
            "kalemler": [
                {
                    "urun_id": k.urunId,
                    "miktar": k.miktar,
                    "birim_fiyat": k.birimFiyat,
                    "kdv_orani": k.kdvOrani,
                }
                for k in payload.kalemler
            ],
        }
    )
    return _to_response(created)


@router.patch("/teklifler/{teklif_id}/durum", response_model=TeklifResponse)
def update_teklif_durum(
    teklif_id: str,
    payload: TeklifDurumUpdateRequest,
    session: Session = Depends(db_session_dependency),
) -> TeklifResponse:
    service = get_container(session).teklif_service()
    updated = service.update_durum(teklif_id, TeklifDurum(payload.durum))
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teklif bulunamadi.")
    return _to_response(updated)
