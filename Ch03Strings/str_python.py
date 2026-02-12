# =============================================================================
# PYTHON STRING MANİPÜLASYONLARI - TUTORIAL & CHEATSHEET
# =============================================================================

# -----------------------------------------------------------------------------
# 1. STRING OLUŞTURMA
# -----------------------------------------------------------------------------
s1 = "çift tırnak"
s2 = 'tek tırnak'
s3 = """çok satırlı
string"""
s4 = str(42)           # "42"
s5 = str(3.14)         # "3.14"

# -----------------------------------------------------------------------------
# 2. RAW STRING (kaçış karakterleri yorumlanmaz)
# -----------------------------------------------------------------------------
path = r"C:\Users\dosya\yol.txt"   # \U, \d vb. kaçış olarak algılanmaz
regex = r"\d+\s+\w+"

# -----------------------------------------------------------------------------
# 3. INDEXLEME VE DİLİMLEME (slicing)
# -----------------------------------------------------------------------------
s = "Python"
#  P   y   t   h   o   n
#  0   1   2   3   4   5   (pozitif index)
# -6  -5  -4  -3  -2  -1   (negatif index)

print(s[0])      # "P"
print(s[-1])     # "n" (son karakter)
print(s[1:4])    # "yth" (1 dahil, 4 hariç)
print(s[:3])     # "Pyt" (baştan 3'e kadar)
print(s[3:])     # "hon" (3'ten sona kadar)
print(s[-3:])    # "hon" (sondan 3 karakter)
print(s[::2])    # "Pto" (2'şer atlayarak)
print(s[::-1])   # "nohtyP" (ters çevirme)

# -----------------------------------------------------------------------------
# 4. TEMEL METODLAR - BÜYÜK/KÜÇÜK HARF
# -----------------------------------------------------------------------------
s = "Merhaba Dünya"
print(s.upper())       # "MERHABA DÜNYA"
print(s.lower())       # "merhaba dünya"
print(s.capitalize())  # "Merhaba dünya" (ilk harf büyük)
print(s.title())       # "Merhaba Dünya" (her kelime büyük)
print(s.swapcase())    # "mERHABA dÜNYA" (ters çevir)

# -----------------------------------------------------------------------------
# 5. BOŞLUK VE KARAKTER TEMİZLEME
# -----------------------------------------------------------------------------
s = "   hello world   "
print(s.strip())       # "hello world" (baş/son boşluk)
print(s.lstrip())      # "hello world   " (sadece soldan)
print(s.rstrip())      # "   hello world" (sadece sağdan)

s2 = "***test***"
print(s2.strip("*"))   # "test"

# -----------------------------------------------------------------------------
# 6. BÖLME VE BİRLEŞTİRME
# -----------------------------------------------------------------------------
# split - string'i liste yapar
s = "elma,armut,kiraz"
print(s.split(","))           # ["elma", "armut", "kiraz"]
print("a b c".split())        # ["a", "b", "c"] (varsayılan: boşluk)
print("a\nb\nc".splitlines()) # ["a", "b", "c"]

# join - listeyi string yapar
liste = ["Python", "Java", "Go"]
print(", ".join(liste))       # "Python, Java, Go"
print("".join(liste))         # "PythonJavaGo"

# partition / rpartition - 3 parçaya böler
s = "isim:Ahmet"
print(s.partition(":"))       # ("isim", ":", "Ahmet")

# -----------------------------------------------------------------------------
# 7. DEĞİŞTİRME VE YERİNE KOYMA
# -----------------------------------------------------------------------------
s = "Merhaba dünya, dünya güzel"
print(s.replace("dünya", "Python"))        # "Merhaba Python, Python güzel"
print(s.replace("dünya", "Python", 1))     # sadece ilk 1 tane: "Merhaba Python, dünya güzel"

# translate - karakter eşlemesi (önceden str.maketrans ile tablo)
tablo = str.maketrans("aeiou", "12345")
print("merhaba".translate(tablo))          # "m2rh1b1"

# -----------------------------------------------------------------------------
# 8. ARAMA VE KONTROL
# -----------------------------------------------------------------------------
s = "Python programlama"
print("Python" in s)           # True
print("Java" not in s)         # True
print(s.startswith("Py"))      # True
print(s.endswith("ma"))        # True
print(s.find("pro"))           # 7 (index; yoksa -1)
print(s.rfind("a"))            # 17 (sağdan ilk)
print(s.index("pro"))          # 7 (yoksa ValueError)
print(s.count("a"))            # 3

# -----------------------------------------------------------------------------
# 9. İÇERİK KONTROLÜ (True/False döner)
# -----------------------------------------------------------------------------
print("123".isdigit())         # True
print("abc".isalpha())         # True
print("abc123".isalnum())      # True
print("   ".isspace())         # True
print("Merhaba".istitle())     # True (Her Kelime Büyük mü?)
print("HELLO".isupper())       # True
print("hello".islower())       # True

# -----------------------------------------------------------------------------
# 10. HİZALAMA VE DOLDURMA
# -----------------------------------------------------------------------------
s = "Py"
print(s.ljust(10))             # "Py        " (sola yasla, 10 karakter)
print(s.rjust(10))             # "        Py" (sağa yasla)
print(s.center(10))            # "    Py    " (ortala)
print(s.zfill(5))              # "000Py" (soldan 0 ile doldur)
print("42".zfill(5))           # "00042"

print(s.ljust(10, "-"))        # "Py--------"
print(s.rjust(10, "."))        # "........Py"

# -----------------------------------------------------------------------------
# 11. STRING FORMATLAMA
# -----------------------------------------------------------------------------
# % (eski stil)
print("Sayı: %d, Metin: %s" % (42, "test"))
print("Ondalık: %.2f" % 3.14159)   # "3.14"

# .format()
print("{} ve {}".format("Python", "Java"))
print("{1} önce {0}".format("ikinci", "birinci"))  # "birinci önce ikinci"
print("{ad}, {yas} yaşında".format(ad="Ali", yas=25))
print("{:.2f}".format(3.14159))    # "3.14"
print("{:>10}".format("sağ"))      # sağa yasla 10 karakter
print("{:0>5}".format(42))        # "00042"

# f-string (Python 3.6+)
ad, yas = "Ayşe", 30
print(f"{ad} {yas} yaşında")
print(f"Pi ≈ {3.14159:.2f}")
print(f"{'merhaba'.upper()}")    # ifade kullanımı
print(f"{42:05d}")               # "00042"

# -----------------------------------------------------------------------------
# 12. KARAKTER (ASCII/UNICODE) İŞLEMLERİ
# -----------------------------------------------------------------------------
print(ord("A"))         # 65
print(ord("ğ"))         # 287 (Unicode)
print(chr(65))          # "A"
print(chr(287))         # "ğ"

# -----------------------------------------------------------------------------
# 13. DİĞER FAYDALI METODLAR
# -----------------------------------------------------------------------------
s = "Merhaba"
print(len(s))           # 7 (uzunluk)
print(s * 3)            # "MerhabaMerhabaMerhaba" (tekrarlama)
print("a" + "b")        # "ab" (birleştirme)

# expandtabs - tab boyutunu değiştir
print("a\tb".expandtabs(4))   # "a   b"

# casefold - agresif küçük harf (karşılaştırma için, örn. Almanca ß)
print("STRASSE".casefold())   # "strasse"

# -----------------------------------------------------------------------------
# 14. ÖZET TABLO - Sık Kullanılanlar
# -----------------------------------------------------------------------------
# | Metod          | Açıklama                    | Örnek sonuç           |
# |----------------|-----------------------------|------------------------|
# | upper()        | Tümü büyük harf             | "HELLO"                |
# | lower()        | Tümü küçük harf             | "hello"                |
# | strip()        | Baş/son boşluk sil          | "text"                 |
# | split(sep)     | Separatöre göre böl         | ["a","b"]              |
# | join(iterable) | Listeyi string yap          | "a-b-c"                |
# | replace(a,b)   | a'yı b ile değiştir         | "yeni"                 |
# | find(s)        | s'in indexi (-1 yoksa)      | 3                      |
# | startswith(s)  | s ile mi başlıyor           | True/False             |
# | endswith(s)    | s ile mi bitiyor            | True/False             |
# | isdigit()      | Sadece rakam mı             | True/False             |
# | format() / f"" | Değişken yerleştir          | "Merhaba Ali"          |

if __name__ == "__main__":
    # Hızlı test
    demo = "  Python String Cheatsheet  "
    print("Demo:", demo.strip().upper())
    print("Kelime sayısı:", len(demo.split()))
