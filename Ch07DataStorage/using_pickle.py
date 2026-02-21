import pickle

data={'isim':'Alice','yas':25}

with open('data.pk1', 'wb') as file:
    pickle.dump(data, file,protocol=pickle.HIGHEST_PROTOCOL)

with open('data.pk1', 'rb') as file:
    loaded_data = pickle.load(file)
    print(loaded_data)
