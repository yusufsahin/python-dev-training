from uuid import uuid4

from app.domain.cari import Cari
from app.domain.repositories import CariRepositoryPort


class CariService:
    def __init__(self, repo: CariRepositoryPort) -> None:
        self.repo = repo

    def list_cariler(self) -> list[Cari]:
        return self.repo.list_all()

    def get_cari(self, cari_id: str) -> Cari | None:
        return self.repo.get_by_id(cari_id)

    def create_cari(self, unvan: str, vergi_no: str, eposta: str, telefon: str) -> Cari:
        return self.repo.create(
            Cari(
                id=str(uuid4()),
                unvan=unvan,
                vergi_no=vergi_no,
                eposta=eposta,
                telefon=telefon,
            )
        )

    def update_cari(
        self,
        cari_id: str,
        unvan: str,
        vergi_no: str,
        eposta: str,
        telefon: str,
    ) -> Cari | None:
        return self.repo.update(
            Cari(
                id=cari_id,
                unvan=unvan,
                vergi_no=vergi_no,
                eposta=eposta,
                telefon=telefon,
            )
        )

    def delete_cari(self, cari_id: str) -> bool:
        return self.repo.delete(cari_id)
