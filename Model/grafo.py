import math
import json
import os

class Nodo:
    def __init__(self, nombre, latitud, longitud):
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud
        self.vecinos = {}

class Grafo:
    def __init__(self):
        self.nodos = {}

    def agregar_nodo(self, nombre, lat, lon):
        if nombre not in self.nodos:
            self.nodos[nombre] = Nodo(nombre, lat, lon)

    def conectar_nodos(self, nodo1, nodo2):
        if nodo1 in self.nodos and nodo2 in self.nodos:
            distancia = self.distancia(self.nodos[nodo1], self.nodos[nodo2])
            self.nodos[nodo1].vecinos[nodo2] = distancia
            self.nodos[nodo2].vecinos[nodo1] = distancia

    def recalcular_distancias(self):
        for nombre1, nodo1 in self.nodos.items():
            for nombre2, nodo2 in self.nodos.items():
                if nombre1 != nombre2:
                    distancia = self.distancia(nodo1, nodo2)
                    nodo1.vecinos[nombre2] = distancia
   
    def distancia(self, nodo1, nodo2):
    # Fórmula de Haversine
        R = 3958.8  # Radio de la Tierra en kilómetros
        lat1 = math.radians(nodo1.latitud)
        lon1 = math.radians(nodo1.longitud)
        lat2 = math.radians(nodo2.latitud)
        lon2 = math.radians(nodo2.longitud)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c
        

    def dijkstra(self, inicio, fin):
        dist = {n: float('inf') for n in self.nodos}
        dist[inicio] = 0
        prev = {}
        no_visitados = list(self.nodos.keys())

        while no_visitados:
            actual = min(no_visitados, key=lambda n: dist[n])
            no_visitados.remove(actual)

            if actual == fin:
                break

            for vecino, peso in self.nodos[actual].vecinos.items():
                nueva_dist = dist[actual] + peso
                if nueva_dist < dist[vecino]:
                    dist[vecino] = nueva_dist
                    prev[vecino] = actual

        camino = []
        nodo = fin
        while nodo in prev:
            camino.insert(0, nodo)
            nodo = prev[nodo]
        if camino:
            camino.insert(0, inicio)

        return camino, dist[fin]

    def guardar_en_json(self, archivo):
        datos = {
            nombre: {
                "latitud": nodo.latitud,
                "longitud": nodo.longitud,
                "vecinos": nodo.vecinos
            }
            for nombre, nodo in self.nodos.items()
        }
        with open(archivo, 'w') as f:
            json.dump(datos, f)

    def cargar_desde_json(self, archivo):
        if not os.path.exists(archivo):
            return
        with open(archivo, 'r') as f:
            datos = json.load(f)
        for nombre, info in datos.items():
            self.nodos[nombre] = Nodo(nombre, info['latitud'], info['longitud'])
        self.recalcular_distancias()  # <--- esta línea es clave
    