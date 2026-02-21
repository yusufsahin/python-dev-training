import os
from pathlib import Path


#os kullanarak dosya yolu oluşturma

current_dir=os.path.dirname(__file__) #bulunduğun klasörü al
file_path=os.path.join(current_dir,'example.txt') #example.txt oluştur

#Dosyayı yazmak için write /w mode aç ve yaz

with open(file_path,'w', encoding="utf-8") as file:
    file.write("Merhaba Dünya!\n")
    file.write("Bu, os modulü ile belirtilen dosya yoludur.\n")
    file.write("Bu, os modulü ile belirtilen dosya yoludur. satır 2\n")

#pathlib kullanarak dosya yolu oluşturma

current_dir=Path(__file__).parent
file_path=current_dir/'example.txt'
with open(file_path,'a',encoding="utf-8") as file: # w /write açsaydık üzerine yazacaktı
    file.write("Merhaba Dünya!\n")
    file.write("Bu, pathlib modülü ile belirtilen dosya yoludur.\n")
