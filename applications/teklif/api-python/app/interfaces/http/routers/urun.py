from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.interfaces.http.deps import get_container, db_session_dependency
from app.interfaces.http.schemas import UrunCreateRequest, UrunResponse


router = APIRouter(tags=["urunler"])


def _to_service_payload(payload: UrunCreateRequest) -> dict:
    return {
        "tur": payload.tur,
        "ad": payload.ad,
        "sku": payload.sku,
        "barkod": payload.barkod,
        "birim": payload.birim,
        "kdv_orani": payload.kdvOrani,
        "satis_fiyati": payload.satisFiyati,
        "alis_fiyati": payload.alisFiyati,
        "doviz_kodu": payload.dovizKodu,
        "kategori": payload.kategori,
        "fiyat_listesi_adi": payload.fiyatListesiAdi,
        "aktif": payload.aktif,
    }


def _to_response(item) -> UrunResponse:
    return UrunResponse(
        id=item.id,
        tur=item.tur.value,
        ad=item.ad,
        sku=item.sku,
        barkod=item.barkod,
        birim=item.birim,
        kdvOrani=item.kdv_orani,
        satisFiyati=item.satis_fiyati,
        alisFiyati=item.alis_fiyati,
        dovizKodu=item.doviz_kodu,
        kategori=item.kategori,
        fiyatListesiAdi=item.fiyat_listesi_adi,
        aktif=item.aktif,
    )


@router.get("/urunler", response_model=list[UrunResponse])
def list_urunler(session: Session = Depends(db_session_dependency)) -> list[UrunResponse]:
    service = get_container(session).urun_service()
    return [_to_response(item) for item in service.list_urunler()]


@router.get("/urunler/{urun_id}", response_model=UrunResponse)
def get_urun(urun_id: str, session: Session = Depends(db_session_dependency)) -> UrunResponse:
    service = get_container(session).urun_service()
    result = service.get_urun(urun_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Urun bulunamadi.")
    return _to_response(result)


@router.post("/urunler", response_model=UrunResponse, status_code=status.HTTP_201_CREATED)
def create_urun(payload: UrunCreateRequest, session: Session = Depends(db_session_dependency)) -> UrunResponse:
    service = get_container(session).urun_service()
    created = service.create_urun(_to_service_payload(payload))
    return _to_response(created)


@router.patch("/urunler/{urun_id}", response_model=UrunResponse)
def update_urun(
    urun_id: str,
    payload: UrunCreateRequest,
    session: Session = Depends(db_session_dependency),
) -> UrunResponse:
    service = get_container(session).urun_service()
    updated = service.update_urun(urun_id, _to_service_payload(payload))
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Urun bulunamadi.")
    return _to_response(updated)


@router.delete("/urunler/{urun_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_urun(urun_id: str, session: Session = Depends(db_session_dependency)) -> Response:
    service = get_container(session).urun_service()
    if not service.delete_urun(urun_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Urun bulunamadi.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
