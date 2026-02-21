import os
from pathlib import Path

current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'example1.bin')
with open(file_path, 'rb') as file:
    data = file.read()
    print("Okunan veri",data)

current_dir=Path(__file__).parent
file_path=current_dir/'example2.bin'
with open(file_path,'rb') as file:
    data = file.read()
    print("Okunan veri",data)