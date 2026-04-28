from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.interfaces.http.deps import get_container, db_session_dependency
from app.interfaces.http.schemas import CariCreateRequest, CariResponse


router = APIRouter(tags=["cariler"])


def _to_response(payload) -> CariResponse:
    return CariResponse(
        id=payload.id,
        unvan=payload.unvan,
        vergiNo=payload.vergi_no,
        eposta=payload.eposta,
        telefon=payload.telefon,
    )


@router.get("/cariler", response_model=list[CariResponse])
def list_cariler(session: Session = Depends(db_session_dependency)) -> list[CariResponse]:
    service = get_container(session).cari_service()
    return [_to_response(item) for item in service.list_cariler()]


@router.get("/cariler/{cari_id}", response_model=CariResponse)
def get_cari(cari_id: str, session: Session = Depends(db_session_dependency)) -> CariResponse:
    service = get_container(session).cari_service()
    result = service.get_cari(cari_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cari bulunamadi.")
    return _to_response(result)


@router.post("/cariler", response_model=CariResponse, status_code=status.HTTP_201_CREATED)
def create_cari(payload: CariCreateRequest, session: Session = Depends(db_session_dependency)) -> CariResponse:
    service = get_container(session).cari_service()
    created = service.create_cari(payload.unvan, payload.vergiNo, payload.eposta, payload.telefon)
    return _to_response(created)


@router.patch("/cariler/{cari_id}", response_model=CariResponse)
def update_cari(
    cari_id: str,
    payload: CariCreateRequest,
    session: Session = Depends(db_session_dependency),
) -> CariResponse:
    service = get_container(session).cari_service()
    updated = service.update_cari(cari_id, payload.unvan, payload.vergiNo, payload.eposta, payload.telefon)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cari bulunamadi.")
    return _to_response(updated)


@router.delete("/cariler", include_in_schema=False)
def delete_cari_missing_id() -> None:
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="ID gerekli.")


@router.delete("/cariler/{cari_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_cari(cari_id: str, session: Session = Depends(db_session_dependency)) -> Response:
    service = get_container(session).cari_service()
    if not service.delete_cari(cari_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cari bulunamadi.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
