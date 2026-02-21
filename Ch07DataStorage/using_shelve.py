import shelve
with shelve.open('shelve.db') as db:
    db["isim"]="Alice"
    db["yaş"]="30"

with shelve.open('shelve.db') as db:
    print(db["isim"])
    print(db["yaş"])