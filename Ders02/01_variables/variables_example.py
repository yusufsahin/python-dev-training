import math
from annotationlib import type_repr

x=5
y=5.0
a=4.5
name="John"
is_student = True

print(x)
print(type(x))
print(y)
print(type(y))
print(a)
print(type(a))
print(name)
print(type(name))
print(is_student)
print(type(is_student))

#hatalı
#2degisken=8
#print(2degisken)

#tanımlanabilir
_2degisken=8
print(_2degisken)


x=x+6
print(x)
print(x+y)
print(type(x+y))

c= x+y
print(c)
print(type(c))

k= c-a
print(k)
print(type(k))

d=k/2
e=k//2
print(d)
print(type(d))
print(e)
print(type(e))

g=d*e
print(g)
print(type(g))

h=int(g)
print(h)

i= math.floor(g)
print(i)
print(type(i))
j=math.ceil(g)
print(j)
m=10
n=2
o=m/n
print(o)
print(type(o))

p=m//n
print(p)
print(type(p))

str1="Hello"
print(str1)
print(type(str1))

str2="World"
print(str2)
print(type(str2))

str3=str1+str2
print(str3)
#print(str3+x)

print(str3+str(x))

#List - Listler

meyveler=["apple", "banana", "cherry"]
print(meyveler)
print(type(meyveler))
print(len(meyveler))
print(meyveler[0])
print(meyveler[1])
print(meyveler[2])
print(type(meyveler[2]))
meyveler[0]="ananas"
print(meyveler)

numbers = [1, 2, 3, 4, 5]
print(sum(numbers))
mixed=[1,"apple",3.5,True]
print(mixed)

#Tuples - Demetler
point=(20,30)
print(point)
print(type(point))
coordinates=(5.0,6.7,8.3,8.3)
print(coordinates)
print(coordinates.index(6.7))

print(coordinates.count(8.3))

#dictionaries / sözlükler
person={"name":"John","age":25,"city":"New York"}
print(person)
print(type(person))
print(person["age"])
del person["age"]
print(person)
for key in person.keys():
    print(key,person[key])

for key,value in person.items():
    print(key,value)

values = person.values()
print(values)  # dict_values(['John', 26])

items = person.items()
print(items)  # dict_items([('name', 'John'), ('age', 26)])
person.update({"city":"Texas"})
print(person)


person2 = {
    "name": "John",
    "age": 25,
    "address": {
        "city": "New York",
        "zip": "10001"
    }
}
print(person2["address"]["city"])  # New York
print(person2["address"]["zip"])   # 10001


