#Class Tanımlama
import math


class Arac:
    def __init__(self, marka,model):
        #attributes / alan/field /property
        self.marka = marka
        self.model = model

class Araba(Arac):
    sayac = 0

    def __init__(self, marka, model, kapi_sayisi):
        super().__init__(marka, model)
        #self.marka = marka
        #self.model = model
        self.kapi_sayisi = kapi_sayisi
        Araba.sayac +=1
        #type(self).sayac += 1
    @classmethod
    def araba_sayisi(cls):
        return  cls.sayac

    #method
    def bilgi(self):
        return f"{self.marka} {self.model} {self.kapi_sayisi}"
    def __str__(self):
        return f"{self.marka} {self.model} {self.kapi_sayisi}"

araba1=Araba("Toyota","Coralla",2)
print(Araba.araba_sayisi())
araba2=Araba("Honda","Type-R",1)
print(Araba.araba_sayisi())
print(araba1.bilgi())
print(araba2.bilgi())
print(araba1)
print(araba2)
araba3=Araba("Mercedes","E200",2)
print(araba3.bilgi())
print(Araba.araba_sayisi())
araba4=Araba("Volvo","V90",2)
print(araba4.bilgi())
print(Araba.araba_sayisi())

#operator aşırı yükleme(operator overloading)
#Operatör aşırı yükleme, Python'da operatörlerin özel anlamlar kazanmasını sağlar.
# Örneğin, + operatörünün __add__ yöntemi ile aşırı yüklenmesi.


class Vektor:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vektor(self.x+other.x, self.y+other.y)

    def __str__(self):
        #objeyi ayırt etmek için güvenilir bir “kimlik” verir.
        return f"Vektor(id ={id(self)}) : {self.x},{self.y}"

vektor1=Vektor(5,2)
print(vektor1)
vektor2=Vektor(3,7)
print(vektor2)
vektor3=vektor1+vektor2
print(vektor3)

#Özellikler ve Dekorator

class Dikdortgen:
    def __init__(self,en,boy):
        self.en = en
        self.boy = boy
    #def alan(self):
    #    return self.en * self.boy
    #def cevre(self):
    #    return self.en + self.boy
    @property
    def alan(self):
        return self.en * self.boy
    @property
    def cevre(self):
        return self.en + self.boy

dikdortgen=Dikdortgen(5,6)
#print(dikdortgen.alan())
#print(dikdortgen.cevre())
print(dikdortgen.alan)
print(dikdortgen.cevre)

#En basit class/ nesne
class User:
    def __init__(self,name:str,email:str):
        self.name = name
        self.email = email
    def greet(self)->str:
        return f"Hello,My name is {self.name} and you send email me via {self.email}"

user1=User("John","john@doe.com")
print(user1.greet())

#Encapsulation: private alan + property

#Python’da “tam private” yok, ama konvansiyon var:

#_x → “iç kullanım”
#__x → name-mangling (dışarıdan zor erişilir)

class BankAccount:
    def __init__(self,owner:str,balance:float=0.0):
        self.owner = owner
        self.__balance = balance
    @property
    def balance(self)->float:
        return self.__balance
    def deposit(self,amount:float)->None:
        if amount <=0:
            raise ValueError("Amount must be positive")
        self.__balance += amount
    def withdraw(self,amount:float)->None:
        if amount <=0:
            raise ValueError("Amount must be positive")
        if amount > self.__balance:
            raise ValueError("Amount must be less than or equal to balance")
        self.__balance -= amount
    def __str__(self):
        return f"Owner : {self.owner} with Balance : {self.balance}"

acc=BankAccount("John",1000)
print(acc)
acc.deposit(500)
print(acc)
acc.withdraw(200)
print(acc)

#Inheritance(Kalıtım) + Polymorphizm(Çok biçimlilik)


from math import pi

class Shape:
    def area(self)->float:
        raise NotImplementedError

class Rectangle(Shape):
    def __init__(self,width:float,height:float):
        self.width = width
        self.height = height

    def area(self)->float:
        return self.width * self.height

class Circle(Shape):
    def __init__(self,radius:float):
        self.radius = radius

    def area(self)->float:
        return math.pi * self.radius**2

shapes:list[Shape]=[Rectangle(10,20),Circle(5)]
for shape in shapes:
    print(shape.area())

#classmethod / staticmethod

class Temperature:
    def __init__(self,c:float):
        self.c = c

    @classmethod
    def from_fahrenheit(cls,f:float)->"Temperature":
        return cls((f-32)*5/9)
    @staticmethod
    def is_freezing(c:float)->bool:
        return c <= 0

t=Temperature.from_fahrenheit(98.6)
print(t.c)
print(t.is_freezing(t.c))
print(t.is_freezing(-5))

#Bu metot yeni nesne üretecek mi veya alt sınıfa göre davranmalı mı? → @classmethod

#Bu metot class-level bir ayarı/konfigürasyonu okuyup değiştirecek mi? → @classmethod

#Bu metot sadece girdi alıp çıktı üretiyor, self/cls gerekmiyor mu? → @staticmethod

#classmethod = sınıfı bilir (cls) → üretim / factory / class ayarı

#staticmethod = sınıfı bilmez → sadece yardımcı fonksiyon


#####
#Dataclass ile “model class” yazımı (çok pratik)

from dataclasses import dataclass
@dataclass
class Product:
    id: int
    name: str
    price: float

p=Product(1,"Keyboard",16.6)
print(p)

#Composition: “Kalıtımdan çok, parça ekle”

class TodoItem:
    def __init__(self,title:str):
        self.title = title
        self.done = False
    def mark_done(self):
        self.done = True

class TodoList:
    def __init__(self):
        self.items = []
    def add_item(self,title:str):
        self.items.append(TodoItem(title))

    def complete(self,index):
        self.items[index].mark_done()
    def show(self):
        for i,item in enumerate(self.items):
            status="+" if  item.done else "-"
            print(f"{status} {i}. {item.title}")

todoList=TodoList()
todoList.add_item("Study")
todoList.add_item("Exercise")
todoList.complete(0)
todoList.show()
todoList.add_item("Read Book")
todoList.complete(1)
todoList.show()
todoList.complete(2)
todoList.show()

from abc import ABC, abstractmethod
class Notifier(ABC):
    @abstractmethod
    def send(self,msg:str)->None:
        pass
#ABC = “Interface” (runtime zorlar)
class EmailNotifier(Notifier):
    def send(self,msg:str)->None:
        print("[E-Mail]",msg)

EmailNotifier().send("ABC works!")

class Bad(Notifier):
    pass
try:
    Bad()
except TypeError as e:
    print("Expected:", e)


#Protocol = “Modern interface” (duck typing)

from  typing import Protocol
class NotifierPrtcl(Protocol):
    def send(self,msg:str)->None: ...

class SMSNotifierPrtcl(NotifierPrtcl):
    def send(self,msg:str)->None:
        print("[SMS]",msg)

def notify(notifier:NotifierPrtcl):
    notifier.send("Protokol Works!")
notify(SMSNotifierPrtcl())
#ABC eksik implementasyonu başta yakalar,Protocol daha esnektir