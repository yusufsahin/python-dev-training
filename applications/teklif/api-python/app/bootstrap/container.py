from sqlalchemy.orm import Session

from app.application.cari_service import CariService
from app.application.teklif_service import TeklifService
from app.application.urun_service import UrunService
from app.infrastructure.repositories import (
    SqlAlchemyCariRepository,
    SqlAlchemyTeklifRepository,
    SqlAlchemyUrunRepository,
)


class Container:
    def __init__(self, session: Session) -> None:
        self.session = session

    def cari_service(self) -> CariService:
        return CariService(SqlAlchemyCariRepository(self.session))

    def urun_service(self) -> UrunService:
        return UrunService(SqlAlchemyUrunRepository(self.session))

    def teklif_service(self) -> TeklifService:
        return TeklifService(SqlAlchemyTeklifRepository(self.session))
