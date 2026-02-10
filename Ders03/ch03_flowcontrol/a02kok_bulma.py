import math
#y=0=ax^2+bx+c
a=float(input("a : "))
b=float(input("b : "))
c=float(input("c : "))
print("Denklem:", f"{a}x^2 + {b}x + {c} = 0")
#delta = b^2-4ac
delta= b**2-4*a*c
print("delta = ",delta)
if delta>0:
    print("iki farklı gerçek kök var")
    x1= (-b+math.sqrt(delta))/(2*a)
    x2= (-b-math.sqrt(delta))/(2*a)
    print("x1 = ",x1)
    print("x2 = ",x2)
elif delta==0:
    print("Çift kök")
    x=-b/(2*a)
    print("x1,x2 = ",x)
else:
    print("delta < 0 :  yani  delta negatif ise, denklemin gerçel kökü yoktur.Denklemin çözümü bulunamaz.")