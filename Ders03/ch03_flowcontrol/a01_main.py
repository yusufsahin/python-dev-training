a=int(input('Bir sayı giriniz: '))
if a>0:
    print("sayı pozitif")
elif a==0:
    print("sayı sıfıra eşit")
else:
    print("sayı negatif")


x=int(input("Enter a number : "))
#print(x)
#y=x+5
#print(y)
if x>0:
    print("Sayı pozitif")
    print("if scope u")
    if x % 2 == 0:
        print("Sayı pozitif ve ÇİFT")
        print("pozitif ve çift scope u")
        #if x > 100:
        #   print("x sayısı ÇİFT sayı  100 den büyük")
        #   print("x sayısı ÇİFT sayı  100 den büyük scope u")
    else:
        print("Sayı pozitif ve TEK")
        print("pozitif ve TEK scope u")
        #if x > 100:
        #    print("x sayısı tek sayı  100 den büyük")
        #    print("x sayısı tek sayı  100 den büyük scope u")
    if x>100:
        print("x sayısı 100 den büyük")
        print("if x>100 den scope u")
    print("if scope u")
elif x==0:
    print("Sayı sıfıra eşit")
    print("elif sayı 0 a eşit scope u")
else:
    print("Sayı negatif")
    print("else scope u")
print("ana program  scope u")

if None: #False
    print("None is considered False")
if not None: #False
    print("None is considered False")
if not []:
    print("Empty list is considered False")
if not 0:
    print("0 is considered False")

k=input("Enter a number : ")
l=input("Enter a number : ")
print(k+l) #bu durumda string birleştirme yapar , sayı topla için int e çevrilmeli


a=True
b=False
print(a and b)
print(a or b)
print(not a)
print(a ^ b)
print(a!=b)
print(a==b)

xor=(a and not b) or (b and not a)
print(xor)

m=7
print(1<m<10)
print(10<m<20)

meyveler=["elma","portakal","mandalina"]
print("elma" in meyveler)
print("muz" in meyveler)
print("muz" not in meyveler)

#Object Types

z=42
#z=42.0
print(type(z) is int)
print(type(z) is float)

print(isinstance(z,int))

try:
    result=10/0
    #result = 10/2
    print(type(result) is int)
    print(type(result) is float)
except:
    print("Sayı sıfıra bölünemez")
else:
    print("Hata ile karşılaşılmadı")
finally:
    print("Her durumda çalışır")

