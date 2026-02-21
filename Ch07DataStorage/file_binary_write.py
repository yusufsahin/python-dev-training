import os
from pathlib import Path


current_dir = os.path.dirname(__file__)
file_path=os.path.join(current_dir,'example1.bin')
with open(file_path, "wb") as file:
    data = b'\x00\x01\x02\x03\x04\x05'
    file.write(data)
    print('Veri yazıldı : ',data)

current_dir = Path(__file__).parent
file_path = os.path.join(current_dir, 'example2.bin')

with open(file_path, 'wb') as file:
    data = b'\x00\x01\x02\x03\x04\x05'
    file.write(data)
    print("Veri yazıldı",data)