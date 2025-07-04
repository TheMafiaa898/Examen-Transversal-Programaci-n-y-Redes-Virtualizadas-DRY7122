# ruta_chile_argentina.py

import requests

API_KEY = 'TU_API_KEY_AQUI'  # Reemplaza por tu API Key de GraphHopper
API_URL = 'https://graphhopper.com/api/1/route'

def obtener_ruta(origen, destino, modo):
    params = {
        'point': [origen, destino],
        'vehicle': modo,
        'locale': 'es',
        'instructions': 'true',
        'calc_points': 'true',
        'key': API_KEY
    }
    
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        distancia_km = round(data['paths'][0]['distance'] / 1000, 2)
        distancia_millas = round(distancia_km * 0.621371, 2)
        duracion_seg = data['paths'][0]['time'] / 1000
        duracion_horas = round(duracion_seg / 3600, 2)
        narrativa = data['paths'][0]['instructions']

        print(f"\nDistancia: {distancia_km} km / {distancia_millas} millas")
        print(f"Duración estimada: {duracion_horas} horas")
        print("\nNarrativa del viaje:")
        for paso in narrativa:
            print("-", paso['text'])
    else:
        print("Error al obtener la ruta:", response.text)

def main():
    while True:
        print("\n=== Calculador de Ruta Chile - Argentina ===")
        print("Escribe 's' para salir.")
        origen_ciudad = input("Ciudad de Origen (Ej: Santiago, Chile): ")
        if origen_ciudad.lower() == 's':
            break
        destino_ciudad = input("Ciudad de Destino (Ej: Mendoza, Argentina): ")
        if destino_ciudad.lower() == 's':
            break

        print("\nMedios de transporte disponibles:")
        print("1. coche")
        print("2. bicicleta")
        print("3. a pie")
        opcion = input("Seleccione medio de transporte (1/2/3): ")

        modo = {
            '1': 'car',
            '2': 'bike',
            '3': 'foot'
        }.get(opcion, 'car')

        origen = origen_ciudad
        destino = destino_ciudad

        obtener_ruta(origen, destino, modo)

if __name__ == "__main__":
    main()
