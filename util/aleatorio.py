import random as rnd
lista = []
for i in range(100):
    numero = rnd.randint(0, 9999)
    lista.append(numero)
    aleatorio = 'aleatorio' + f"{numero:04d}"
    print(aleatorio)
lista.sort()
lista_cadenas = list(map(lambda numero: 'num'+ f"{numero:04d}" , lista))

for cadena in lista_cadenas:
    print(cadena)
