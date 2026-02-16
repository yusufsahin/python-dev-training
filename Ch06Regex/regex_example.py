import re

pattern = r"\d+" #Bir veya daha fazla rakamı eşler

#derleme compile

p=re.compile(r"\d+")

match=re.match(r"\d+","123abc")
if match:
    print(match.group())
search=re.search(r"\d+","abc123def456ghi789")
if search:
    print(search.group())
matches= re.findall(r"\d+","abc123def456ghi789")
print(matches)
matches2= re.findall(r"\D+","abc123def456ghi789")
print(matches2)

for match in re.finditer(r"\d+","abc123def456ghi789"):
    print(match.group())
for match in re.finditer(r"\D+", "abc123def456ghi789"):
    print(match.group())
result=re.sub(r"\d+","#","abc123def456ghi789")
print(result)
result=re.sub(r"\D+","*","abc123def456ghi789")
print(result)

pattern2=re.compile(r"cat|dog")
match3=pattern2.search("I have a cat and dog.")
print(match3.group())

#Çapa / Anchor dizgedeki konumu eşler ^ ve $
pattern3= re.compile(r"^hello")
match4=pattern3.match("hello world")
if match4:
    print(match4.group())
pattern4=re.compile(r"world$")
match5=pattern4.search("hello world")
if match5:
    print(match5.group())

#Sınıf kısa yolları
#Karakter Sınıfları:
#Köşeli parantezler [] kullanarak bir karakter sınıfı tanımlayın, bu sınıf içindeki herhangi bir karakteri eşler.

#\d: Herhangi bir rakamı eşler (eşdeğer [0-9]).
#\D: Rakam olmayan herhangi bir karakteri eşler.
#\w: Herhangi bir kelime karakterini eşler (alfanumerik + alt çizgi).
#\W: Kelime olmayan herhangi bir karakteri eşler.
#\s: Herhangi bir boşluk karakterini eşler.
#\S: Boşluk olmayan herhangi bir karakteri eşler.

#pattern5=re.compile(r"\d+")
pattern5=re.compile(r"\D+")
match6= pattern5.search("There are 123 apples")
print(match6.group())

#Flags  / Bayraklar
pattern6= re.compile(r"hello",re.IGNORECASE)
#pattern6= re.compile(r"hello")
match7=pattern6.search("Hello World")
if match7:
    print(match7.group())

#Tekrarlayıcılar

#{m,n} kullanarak minimum ve maksimum tekrar sayısını belirleyin.

#*: 0 veya daha fazla tekrar eşler.
#+: 1 veya daha fazla tekrar eşler.
#?: 0 veya 1 tekrar eşler.
#{m}: Tam olarak m tekrar eşler.
#{m,}: m veya daha fazla tekrar eşler.
#{m,n}: m ile n arasında tekrar eşler.


pattern7=re.compile(r"\d{3,}")
match8=pattern7.search("12345")
print(match8.group())

#Açgözlü ve Açgözsüz:
#Tekrarlayıcılar varsayılan olarak açgözlüdür, yani mümkün olan en fazla karakteri eşler.
#Tekrarlayıcıları açgözsüz yapmak için ? ekleyin (yani mümkün olan en az karakteri eşler).

greedy_pattern=re.compile(r"<.*>")
non_greedy_pattern=re.compile(r"<.*?>")
text="<div>hello</div>"
greedy_match=greedy_pattern.search(text)
print(greedy_match.group())
non_greedy_match=non_greedy_pattern.search(text)
print(non_greedy_match.group())

#Parantez grupları
pattern8= re.compile(r"(hello) (world)")
match9= pattern8.search("hello world")
print(match9.group(0))
print(match9.group(1))
print(match9.group(2))


#Geriye dönük referanslar \number
pattern9= re.compile(r"(\b\w+)\s+\1")
match10=pattern9.search("hello hello")

if match10:
    print(match10.group())

# Global Eşleştirme
# Tüm eşleştirmeleri bulma

pattern10= re.compile(r"\b\w+\b")
matches3=pattern10.findall("hello world")
print(matches3)

for match in pattern10.finditer("hello world"):
    print(match.group())

import  re
def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None
email ="example@example.com"
print(validate_email(email))
email2 ="john@doe.com"
print(validate_email(email2))
email3 = "ha?c.com"
print(validate_email(email3))

import  re
def validate_phone_number(phone):
    pattern = r'^\+?(\d{1,3})?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}$'
    return re.match(pattern, phone) is not None
phone = "+90-550-555-1234"
print(validate_phone_number(phone))

import re

# 13–19 haneli; aralara boşluk veya - gelebilir
#CC_CANDIDATE_RE = re.compile(r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)")
def validate_credit_card_number(credit_card):
    pattern = r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)"
    return re.match(pattern, credit_card) is not None

credit_card_number = "1045-1555-1555-1234"
print(validate_credit_card_number(credit_card_number))

import  re
def validate_ip(ip):
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    return re.match(pattern,ip) is not None
ip="192.168.3.11"
print(validate_ip(ip))

import  re
def validate_date(date):
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    return re.match(pattern,date) is not None

date="2024-05-28"
print(validate_date(date))

import re

def validate_url(url):
    pattern = r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
    return  re.match(pattern,url) is not None

url="http://www.example.com"
print(validate_url(url))