from Model.grafo import Grafo
import os

# Ruta donde se guardarán los nodos
ruta_json = "Data/nodos.json"

# Crear el grafo y cargar desde archivo si existe
grafo = Grafo()
grafo.cargar_desde_json(ruta_json)

def agregar_nodo(nombre, lat, lon):
    grafo.agregar_nodo(nombre, lat, lon)
    # Conectar automáticamente con todos los demás para mantenerlo conectado
    for otro in grafo.nodos:
        if otro != nombre:
            grafo.conectar_nodos(nombre, otro)
    grafo.guardar_en_json(ruta_json)

def obtener_nodos():
    return grafo.nodos

def calcular_ruta(inicio, fin):
    return grafo.dijkstra(inicio, fin)

def eliminar_nodo(nombre):
    if nombre in grafo.nodos:
        for otro in grafo.nodos.values():
            if nombre in otro.vecinos:
                del otro.vecinos[nombre]
        del grafo.nodos[nombre]
        grafo.guardar_en_json(ruta_json)
from Model.grafo import Grafo
import os

# Ruta donde se guardarán los nodos
ruta_json = "Data/nodos.json"

# Crear el grafo y cargar desde archivo si existe
grafo = Grafo()
grafo.cargar_desde_json(ruta_json)

def agregar_nodo(nombre, lat, lon):
    grafo.agregar_nodo(nombre, lat, lon)
    # Conectar automáticamente con todos los demás para mantenerlo conectado
    for otro in grafo.nodos:
        if otro != nombre:
            grafo.conectar_nodos(nombre, otro)
    grafo.guardar_en_json(ruta_json)

def obtener_nodos():
    return grafo.nodos

def calcular_ruta(inicio, fin):
    return grafo.dijkstra(inicio, fin)

def eliminar_nodo(nombre):
    if nombre in grafo.nodos:
        for otro in grafo.nodos.values():
            if nombre in otro.vecinos:
                del otro.vecinos[nombre]
        del grafo.nodos[nombre]
        grafo.guardar_en_json(ruta_json)
