a=10
b=5
print(a+b)

def greet(name):
    return f"Hello, {name}"

print(greet("John Doe"))

#dir("list")
print(dir("list"))


def topla(x,y):
    """İki sayıyı toplar ve sonucu döndürür."""
    return x+y
print(topla(3,4))
print(topla.__doc__)
help(topla)
