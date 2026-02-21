import gzip
with gzip.open('example.txt.gz', 'wb') as file:
    data="Merhaba,Dünya!".encode('utf-8')
    file.write(data)
    print("Veri sıkıştırıldı ve yazıldı")
with gzip.open('example.txt.gz', 'rb') as file:
    data = file.read()
    print("Okunan sıkıştırılmış veri")
    print(data)
    decoded_data = data.decode('utf-8')
    print("Çözülen veri")
    print(decoded_data)