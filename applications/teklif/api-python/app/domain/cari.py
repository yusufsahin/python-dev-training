from dataclasses import dataclass


@dataclass(slots=True)
class Cari:
    id: str
    unvan: str
    vergi_no: str
    eposta: str
    telefon: str
