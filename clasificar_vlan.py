# clasificar_vlan.py

def clasificar_vlan(vlan):
    if 1 <= vlan <= 1005:
        return "VLAN de Rango Normal"
    elif 1006 <= vlan <= 4094:
        return "VLAN de Rango Extendido"
    else:
        return "Número de VLAN inválido (fuera del rango 1-4094)"

try:
    vlan = int(input("Ingrese el número de VLAN: "))
    resultado = clasificar_vlan(vlan)
    print(resultado)
except ValueError:
    print("Error: Debe ingresar un número entero.")
