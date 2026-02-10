#while döngüsü
count=0
print("While loop")
while count<10:
    print("count",count)
    count=count+1
    #count += 2
    #count+=2
print("While loop odds")
count2=0
while count2<10:
    print("count2",count2)
    #count=count+1
    count2 += 2
    #count+=2

print("for loop") #default step 1
for i in range(10):
    print(i)
print("for loop step")

print("for loop") #default step 1
for i in range(10):
    print(i)
for i in range(0,10):
    print(i)
print("for loop step")
for i in range(0, 10, 1):
    print(i)
print("for loop step by 2")
for i in range(0, 10, 2):
    print(i)

for i in range(8):
    if i==5:
        break
    print(i)

meyveler=["elma","portakal","mandalina"]

for meyve in meyveler:
    print(meyve)

for index,meyve in enumerate(meyveler):
    print(index,meyve)

names = ["Alice","Bob","Carol"]
ages = [25,35,28]
for name,age in zip(names,ages):
    print(f"{name} is {age} years old")

age=17
status="Adult" if age>=18 else "Minor"
print(status)

m=4
if m>0:
    pass
else:
    print("m nagatif bir sayı")

numbers=[]
for i in range(10):
    numbers.append(i)
print(numbers)

x=range(3,6)
for num in x:
    print(num)