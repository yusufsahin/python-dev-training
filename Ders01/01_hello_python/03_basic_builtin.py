import builtins

x=10
print(type(x))
print(isinstance(x,int))

y=10.0
print(type(y))
print(isinstance(y,int))
print(isinstance(y,float))

float(x)
print(type(x))
print(float(x))
print(isinstance(float(x),float))

print(abs(-10))

print(dir(builtins))
print(help(abs))