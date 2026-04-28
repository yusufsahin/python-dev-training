import pytest

from app.domain.teklif import Teklif, TeklifKalemi


def test_teklif_hesaplama() -> None:
    teklif = Teklif(
        id="t1",
        cari_id="c1",
        para_birimi="TRY",
        kalemler=[TeklifKalemi(urun_id="u1", miktar=2, birim_fiyat=100, kdv_orani=20)],
    )

    assert teklif.toplam_tutar() == pytest.approx(200)
    assert teklif.toplam_kdv() == pytest.approx(40)
    assert teklif.genel_toplam() == pytest.approx(240)
