#with open("example2.txt", "wb") as f:
#    f.write("Merhaba Dünya! Python random access demo.\n".encode("utf-8"))

with open("example2.bin", "rb") as f:
    f.seek(3)          # 10. BYTE
    data = f.read(5)    # 5 BYTE
    print(data)         # b'...'
    print(f.tell())

#with open("example3.txt", "w", encoding="utf-8") as f:
#    f.write("Merhaba Dünya! Python random access demo.\n")

#with open("example3.txt", "r", encoding="utf-8") as f:
#    text = f.read()
#    print(text[10:15])      # 10. karakterden 5 karakter
#    print(len(text[:15]))   # gösterim amaçlı