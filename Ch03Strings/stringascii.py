"""
y = x fonksiyonunu konsolda karakterlerle gösterir.
"""

def ciz_y_esittir_x(boyut=11):
    """y=x doğrusunu karakter tabanlı bir koordinat düzleminde çizer."""
    # Koordinat düzlemi: boyut x boyut (örn. 11x11)
    # Merkez (0,0) ortada olacak şekilde
    yari = boyut // 2  # Örn. 11 -> 5

    print("  y = x  fonksiyonu (konsol grafigi)\n")

    # y ekseni yukarıdan aşağı (matematikte y yukarı artar, konsolda satır aşağı artar)
    # Bu yüzden üst satırlar büyük y değerine karşılık gelir
    for satir in range(boyut):
        y = yari - satir  # Üst satır = +yari, alt satır = -yari
        satir_metni = []
        for sutun in range(boyut):
            x = sutun - yari  # Sol = -yari, sağ = +yari
            if y == x:
                satir_metni.append("*")
            else:
                satir_metni.append(".")
        # y ekseni etiketi
        etiket = f"{y:2d}|" if y != 0 else " 0|"
        print(etiket + "".join(satir_metni))
    # x ekseni
    print("   " + "-" * boyut)
    # x degerleri: -5 -4 ... 4 5 (tek haneli gosterim)
    x_etiketi = "".join(str(i - yari)[-1] if i != yari else "0" for i in range(boyut))
    print("   " + x_etiketi + "  <- x")


if __name__ == "__main__":
    ciz_y_esittir_x()
