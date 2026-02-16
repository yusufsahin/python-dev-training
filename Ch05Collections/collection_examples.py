#Tuple - Demet oluşturup erişelim

t=(1,2,3,4,2,5,6,2)
print(t.count(2))
print(t.index(3))
print(t.index(4))
print(t.index(4,3))
print(t.index(2, 1)) #“1. indexten başlayarak 2’yi ara ve ilk bulduğun yerin indexini ver.”
p = (10, 20, 30, 20, 40)
print(p.index(20, 2, 5))
print(p[0])
print(p[-1])
#Tuple - Demet oluşturup erişelim

t=(1,2,3,4,2,5,6,2)
print(t.count(2))
print(t.index(3))
print(t.index(4))
print(t.index(4,3))
print(t.index(2, 1)) #“1. indexten başlayarak 2’yi ara ve ilk bulduğun yerin indexini ver.”
p = (10, 20, 30, 20, 40)
print(p.index(20, 2, 5))

print(p[0])
print(p[0])
print(p[-1])
#Slicing
print(p[2:4])
print(p[2:5])
print(p[1:5])
print(p[0:5])
print(p[0:5:2])
print(p[0:5:3])
print(p[0:5:4])
print(p[0:5:5])
print(p)
l = (10, 20, 30, 20, 40,10, 20, 30, 20, 40)
print(l[0:5:4])
print(l[0:5:5])
print(l[0:10:4])
print(l[0:10:5])

#Liste

my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(my_list)
print(my_list[0])
print(my_list[-1])
print(my_list[5])
print(my_list[-5])
my_list[0] = 10
print(my_list)
my_list.append(20)
print(my_list)
my_list.insert(1, 20)
print(my_list)
my_list.remove(3)
print(my_list)
my_list.reverse()
print(my_list)
my_list.pop(-1)
print(my_list)
my_list.sort()
print(my_list)
my_list.reverse()
print(my_list)
print(my_list[1:4])
print(my_list[2:6])
print(my_list[2:6:2])
print(my_list[2:6:3])

#Genişletilmiş Yinelemeli Paketleme (Extended Iterable Unpacking)
#Yinelemeli Paketleme

a,b,*rest=[1,2,3,4,5]
print(a,b,rest)

a=[1,2,3]
a.append(4)
print(a)
a.extend([5,6])
print(a)
a.insert(0,0)
print(a)

a.pop(1)
print(a)
del a[0]
print(a)
#Kümeler Set(unique + unordered)

s={1,2,3}
s=set([1,2,3])
print(s)
s.add(4)
print(s)
s.update([5,6,8])
print(s)
s.update([7,0])
print(s)
s.remove(2)
print(s)
s.discard(3)
print(s)
s.pop()
print(s)
s.clear()
print(s)

s1={1,2,3}
s2={3,4,5}
print(s1 | s2)
print(s1 & s2)
print(s1 - s2)
print(s2 - s1)
print(s1 ^ s2) #simetrik fark
print(s1.intersection(s2))
print(s1.difference(s2))

#Küme Operatörleri
a1={1,2,3}
a2={1,2}
#a1 alt kümesi midir a2 (subset or equal)
print(a1<=a2)
#a1 alt kümesi midir a2 (proper subset)
print(a1<a2)
print(a1>=a2) #(superset or equal)
print(a1>a2) #(proper superset)
#İlişki	Anlam
#<=	alt küme (eşit olabilir)
#<	gerçek alt küme
#>=	üst küme
#>	gerçek üst küme


#Dictionary - sözlükler
d= {'isim':'Alice','yaş':25}
print(d['isim'])
print(d)
d['yaş']=26
print(d)

del d['yaş']
print(d)

isim=d.pop('isim')
print(d)
print(isim)

sozluk={'isim':'John','yaş':'25'}
print(sozluk.keys())
print(sozluk.values())
print(sozluk.items())
print(sozluk.get('isim'))
sozluk.update({'yaş':27,'şehir':'Texas'})
print(sozluk)

#Görünüm Nesneleri (View Objects)
#Sözlük Görünüm Nesneleri

v={'isim':'Alice','yaş':25}
keys_view=v.keys()
v['şehir']='Texas'
print(keys_view)



