# ESTRUCTURAS DE CONTROL

# CONDICIONALES
# FUNCIONES
# CICLOS

# CONDICIONALES
# if, if-else, elif

"""
saldo = 5490
if saldo < 5500:
    print("NO ABRIR")
if saldo >= 5500:
    print("ABRIR")
"""

"""
edad = 10

if edad > 15:
    print("edad mayor que 15")
    
elif edad <=20:
    print("edad menor o igual que 20")
"""

#OPERADORES DE COMPARACIONES
# >, <, >=, <=, ==

"""
saldo = 2000

if saldo < 5500:
    print("el saldo es menor que 5500")
    
else:
    print("el saldo es mayor que 5500")
"""
"""
daniela = 1100
sofia = 1200
andres = 2300
fabian = 400
juliana = 4200

salario = fabian
if salario < 500:
    print("salario básico")
    
if salario < 1000 and salario >500:
    print("salario medio")
    
if salario < 2000 and salario > 1000:
    print("salario alto")
    
if salario < 4000 and salario > 2000:
    print("salario superior")"""
"""
if salario < 500:
    print("salario básico")
    
elif salario < 1000:
    print("salario medio")
    
elif salario < 2000:
    print("salario alto")
    
elif salario < 4000:
    print("salario superior")
"""







edad = 10
estatura = 100

estatura_minima = 120
edad_minima = 13


if edad < edad_minima:
    print("¡ NO PUEDES ENTRAR !, no tienes la edad minima")
else:
    if estatura < estatura_minima:
        print(" ¡ NO PUEDES ENTRAR, tienes la edad pero no la estatura")
    else:
        print("Puedes entrar")


if edad >= edad_minima and estatura >= estatura_minima: 
    print("Puedes entrar")
else:
    print("NO PUEDES ENTRAR")