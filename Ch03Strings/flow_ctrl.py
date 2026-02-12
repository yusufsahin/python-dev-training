# ============================================================================
# PYTHON KONTROL YAPILARI (CONTROL FLOW) - Cheatsheet & Tutorial
# ============================================================================

# ----------------------------------------------------------------------------
# 1. IF - ELIF - ELSE (Koşullu dallanma)
# ----------------------------------------------------------------------------

# Basit if
age = 18
if age >= 18:
    print("Yetişkinsiniz")

# if - else
score = 75
if score >= 50:
    print("Geçtiniz")
else:
    print("Kaldınız")

# if - elif - else (çoklu koşul)
grade = 85
if grade >= 90:
    print("A")
elif grade >= 80:
    print("B")
elif grade >= 70:
    print("C")
elif grade >= 60:
    print("D")
else:
    print("F")

# İç içe if (nested)
x, y = 10, 20
if x > 5:
    if y > 15:
        print("Her iki koşul da sağlandı")

# Tek satırda if (ternary / conditional expression)
durum = "Başarılı" if score >= 50 else "Başarısız"

# and, or, not operatörleri
a, b = 5, 10
if a > 0 and b > 0:
    print("Her ikisi de pozitif")

if a < 0 or b < 0:
    print("En az biri negatif")

if not (a == 0):
    print("a sıfır değil")


# ----------------------------------------------------------------------------
# 2. WHILE Döngüsü (Koşul sağlandığı sürece tekrarla)
# ----------------------------------------------------------------------------

# Basit while
i = 0
while i < 5:
    print(f"i = {i}")
    i += 1

# while - else (döngü break ile kesilmediyse else çalışır)
j = 0
while j < 3:
    print(j)
    j += 1
else:
    print("Döngü normal sona erdi")

# Sonsuz döngü (break ile çıkış)
# while True:
#     komut = input("Çıkmak için 'q' yazın: ")
#     if komut == 'q':
#         break


# ----------------------------------------------------------------------------
# 3. FOR Döngüsü (Sıralı iterasyon)
# ----------------------------------------------------------------------------

# Liste üzerinde döngü
meyveler = ["elma", "armut", "kiraz"]
for meyve in meyveler:
    print(meyve)

# range() ile sayı döngüsü
for i in range(5):          # 0, 1, 2, 3, 4
    print(i, end=" ")
print()

for i in range(2, 6):       # 2, 3, 4, 5 (başlangıç, bitiş)
    print(i, end=" ")
print()

for i in range(0, 10, 2):   # 0, 2, 4, 6, 8 (adım 2)
    print(i, end=" ")
print()

# enumerate() - indeks ve değer birlikte
for index, meyve in enumerate(meyveler):
    print(f"{index}: {meyve}")

# zip() - iki listeyi paralel döngü
isimler = ["Ali", "Veli", "Ayşe"]
yaslar = [25, 30, 22]
for isim, yas in zip(isimler, yaslar):
    print(f"{isim} - {yas} yaşında")

# Sözlük (dict) üzerinde döngü
kisi = {"ad": "Ali", "yas": 25, "sehir": "İstanbul"}
for anahtar in kisi:
    print(anahtar, ":", kisi[anahtar])

for anahtar, deger in kisi.items():
    print(f"{anahtar} = {deger}")

# for - else (break olmadan biterse else çalışır)
for sayi in [1, 2, 3]:
    if sayi == 5:
        break
else:
    print("5 bulunamadı")


# ----------------------------------------------------------------------------
# 4. BREAK ve CONTINUE
# ----------------------------------------------------------------------------

# break - döngüyü tamamen sonlandır
for i in range(10):
    if i == 5:
        break
    print(i, end=" ")  # 0 1 2 3 4

# continue - mevcut iterasyonu atla, sonrakine geç
print()
for i in range(6):
    if i % 2 == 0:
        continue
    print(i, end=" ")  # 1 3 5


# ----------------------------------------------------------------------------
# 5. MATCH-CASE (Python 3.10+) - Pattern Matching
# ----------------------------------------------------------------------------

def http_durum_kodu(kod):
    match kod:
        case 200:
            return "OK"
        case 404:
            return "Bulunamadı"
        case 500:
            return "Sunucu Hatası"
        case _:
            return "Bilinmeyen"

# print(http_durum_kodu(404))  # "Bulunamadı"


# ----------------------------------------------------------------------------
# 6. PASS (Placeholder - geçici boş blok)
# ----------------------------------------------------------------------------

def henuz_yazilacak():
    pass  # Hiçbir şey yapma, syntax hatasını önle


# ----------------------------------------------------------------------------
# 7. COMPREHENSION (Kısa döngü notasyonu)
# ----------------------------------------------------------------------------

# List comprehension
kareler = [x**2 for x in range(5)]           # [0, 1, 4, 9, 16]
cift_sayilar = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]

# Dict comprehension
sayi_kareleri = {x: x**2 for x in range(5)}  # {0:0, 1:1, 2:4, 3:9, 4:16}

# Set comprehension
benzersiz_uzunluklar = {len(s) for s in ["ali", "veli", "ayşe"]}  # {3, 4}


# ----------------------------------------------------------------------------
# 8. ÖRNEKLER - Pratik Kullanım
# ----------------------------------------------------------------------------

# Faktöriyel (while)
def faktoriyel(n):
    sonuc = 1
    while n > 0:
        sonuc *= n
        n -= 1
    return sonuc

# Faktöriyel (for)
def faktoriyel_for(n):
    sonuc = 1
    for i in range(1, n + 1):
        sonuc *= i
    return sonuc

# Basit menü örneği
def menu_dongusu():
    while True:
        print("\n1. Topla 2. Çıkar 3. Çık")
        secim = input("Seçiminiz: ")
        if secim == "3":
            break
        elif secim == "1":
            print("Toplama işlemi...")
        elif secim == "2":
            print("Çıkarma işlemi...")
        else:
            print("Geçersiz seçim")


# ============================================================================
# ÖZET TABLO
# ============================================================================
# | Yapı      | Kullanım                         | Açıklama              |
# |-----------|----------------------------------|------------------------|
# | if        | if koşul:                        | Koşullu dallanma       |
# | elif      | elif koşul:                      | Alternatif koşul       |
# | else      | else:                            | Diğer tüm durumlar     |
# | while     | while koşul:                     | Koşullu tekrar         |
# | for       | for x in iterable:               | Sıralı tekrar          |
# | break     | break                            | Döngüden çık           |
# | continue  | continue                         | İterasyonu atla        |
# | pass      | pass                             | Boş blok               |
# | match     | match x: case y:                  | Pattern matching       |
# ============================================================================
