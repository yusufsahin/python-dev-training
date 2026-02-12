import os
import time

frames = [
r"""
   .--.
  |o_o |
  |:_/ |
 //   \ \
(|     | )
/'\_   _/`\
\___)=(___/
""",
r"""
   .--.
  |o_o |
  |:_/ |
 //   \ \
(|     | )
/'\_   _/`\
 \__)=(___/
""",
]

def clear():
    os.system("cls" if os.name == "nt" else "clear")

for i in range(20):
    clear()
    print("Penguen yürüyor...  (Ctrl+C ile durdur)\n")
    print(frames[i % len(frames)])
    time.sleep(0.15)
