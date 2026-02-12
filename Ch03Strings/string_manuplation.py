tek_tirnak_str='Merhaba'
cift_tirnak_str="Dünya"
cok_satir_str="""Bu
bir
çok 
satırlı
stringtir.
"""
print(tek_tirnak_str)
print(cift_tirnak_str)
print(cok_satir_str)

print('Merhaba Dünya!-tek tırnak')
print("Merhaba Dünya!-Çift tırnak")
print("""
Merhaba
Dünya
!
""")


#isim=input("İsim giriniz : ")
#print("Merhaba, {isim}!".format(isim=isim))
#print("Merhaba, "+isim+"!")
#a=input("1.sayıyı giriniz : ") #input string 'tir. 5 verilim
#b=input("2.sayıyı giriniz : ") #4 verelim
#print(a+b) #54
#print(int(a)+int(b)) #9


#Ayırıcı / Separatör ile
print("Merhaba","dünya","!")
print("Merhaba","dünya","!",sep="-")
print("Merhaba","dünya","!",sep=";")
print("Merhaba","dünya","!",sep=",")
print("Merhaba","dünya","!",sep="|")


#Sonlandırıcı
print("Merhaba Dünya!",end=" BİTTİ\nYeni satır")
print("Merhaba Dünya!",end=" BİTTİ\tYeni satır")

yeni_satir_str="\nMerhaba\tDünya\n!"
print(yeni_satir_str)

print('O, "Merhaba" dedi')
print("O, \"Merhaba\" dedi")
print("10\\2=5")
ters_slas_str="Bu bir ters slash \\"
print(ters_slas_str)

#Concateation/String Birleştirme İşlemleri
merhaba="Merhaba"
dunya="Dünya"
unlem="!"

merhaba_dunya_unlem=merhaba+" "+dunya+unlem
print(merhaba_dunya_unlem)

#tekrar
tekrar_str="Merhaba"*3
print(tekrar_str)
uc_tirnak_str="""Bu bir çok satırlı ve 'tek tırnak' ile "çift tırnak" içeren string"""
print(uc_tirnak_str)

#string yöntenleri/methodları/fonk.

s="merhaba"
print(s)
print(s.upper())
k="DÜNYA"
print(k.lower())
print(s.capitalize())
print(uc_tirnak_str.title())
print(uc_tirnak_str.capitalize())

v="    Merhaba Dünya      "
print(v)
print(len(v))
print(v.strip())
u=v.strip()
print(len(u))

z="merhaba dünya"
print(z.replace("dünya","python"))
print(z.find("dünya"))

l="merhaba dünya, merhaba uzay, merhaba Python"
print(l.count("merhaba"))
print(l.count(" "))
print(l.count(","))

#String Testleri

print("merhaba Python".startswith("merhaba"))
print("merhaba Python".startswith("Merhaba"))
print("merhaba Python".startswith("Python"))
print("merhaba Python".endswith("Python"))
print("merhaba Python".endswith("python"))

g="merhaba"
print(g.isalpha())

print("12345".isdigit())

print("    ".isspace())

#string formatlama
#% operatoru
name="Alice"
age=30
formatted_str="İsim: %s , Yaş: %d" % (name,age)
print(formatted_str)

format_func_str="İsim: {} , Yaş: {}".format(name,age)
print(format_func_str)

#f String
f_str=f"İsim: {name} , Yaş: {age}"
print(f_str)


#Diğer yardımcılar
person={"name":"Alice","age":30}
formatted_dict_str="İsim: {name} , Yaş: {age}".format(**person)
print(formatted_dict_str)

formatted_dict_str2 = f"İsim: {person['name']} , Yaş: {person['age']}"
print(formatted_dict_str2)
formatted_dict_str_map = "İsim: {name} , Yaş: {age}".format_map(person)
print(formatted_dict_str_map)

from string import Template
template=Template("İsim: $name , Yaş: $age")
formatted_temp_str=template.substitute(name="Alice",age=30)
print(formatted_temp_str)

#Slicing s[start:stop:step]
h="merhaba dünya"

print(h[0:7])
print(h[8:])
print(h[8::2])
print(h[:7])
print(h[::2])
print(h[::-1])

#split
n="merhaba dünya"
kelimeler=n.split()
print(kelimeler)
print(kelimeler[0])

csv="elma;armut;çilek"
meyveler=csv.split(";")
print(meyveler)
print(meyveler[0])
print(meyveler[1])

sozcukler=['merhaba','dünya','merhaba','python']
print(' '.join(sozcukler))
fruits=['apple','banana','ananas']
csv2='|'.join(fruits)
print(csv2)

csv3=';'.join(fruits)
print(csv3)

#casefold() (Türkçe/Unicode karşılaştırmada daha sağlam)
a = "Straße"
b = "STRASSE"
print(a.lower() == b.lower())      # False
print(a.casefold() == b.casefold())# True

h="Isim"
l="isim"
print(h.lower() == l.lower())
print(h.casefold() == l.casefold())

text = "a\nb\r\nc"
print(text.splitlines())           # ['a', 'b', 'c']

s = "host=10.10.10.5;port=5432"
left, sep, right = s.partition(";")
print(left)   # host=10.10.10.5
print(right)  # port=5432

path = "/api/v1/users"
print(path.removeprefix("/api"))   # /v1/users

fn = "report.csv"
print(fn.removesuffix(".csv"))     # report

x = "---Merhaba---"
print(x.strip("-"))  # Merhaba

table = str.maketrans({"ç":"c","ğ":"g","ş":"s","ü":"u","ö":"o","ı":"i"})
print("çalışma".translate(table))  # calisma

b = "Merhaba".encode("utf-8")
print(b)                 # b'Merhaba'
print(b.decode("utf-8")) # Merhaba


























