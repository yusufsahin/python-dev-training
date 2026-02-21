#Dosya okuma

print("tüm içeriği okuma")
with open('example.txt','r',encoding="utf-8") as file:
    content=file.read()
    print(content)

print("\nsatır satır okuma")
with open('example.txt','r',encoding="utf-8") as file:
    line=file.readline()
    while line:
        print(line, end='')
        line = file.readline()

print("\nDosyanın tüm satırlarını liste olarak okuma")
with open('example.txt','r',encoding="utf-8") as file:
    lines=file.readlines()
    for line in lines:
        print(line, end='')


print("\n'for' döngüsü kullanarak dosyayı okuma")
with open('example.txt','r',encoding="utf-8") as file:
    for  line in file:
        print(line, end='')