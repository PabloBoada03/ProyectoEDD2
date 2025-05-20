from flask import Flask, render_template, request, redirect, flash, url_for
from Controller.controller import agregar_nodo, obtener_nodos, calcular_ruta
import itertools

app = Flask(__name__, template_folder="View/templates")
app.secret_key = 'super-secret-key'  # Necesaria para usar flash

def serializar_nodos(nodos):
    return {
        nombre: {
            "latitud": nodo.latitud,
            "longitud": nodo.longitud
        } for nombre, nodo in nodos.items()
    }

@app.route('/')
def index():
    nodos = obtener_nodos()
    nodos_json = serializar_nodos(nodos)
    return render_template('index.html', nodos=nodos, nodos_json=nodos_json)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    lat = float(request.form['lat'])
    lon = float(request.form['lon'])
    agregar_nodo(nombre, lat, lon)
    return redirect('/')

@app.route('/ruta', methods=['POST'])
def ruta():
    inicio = request.form['inicio']
    fin = request.form['fin']
    intermedios = request.form.getlist('intermedios')

    nodos = obtener_nodos()
    nodos_json = serializar_nodos(nodos)

    mejor_ruta = None
    mejor_costo = float('inf')

    for perm in itertools.permutations(intermedios):
        puntos = [inicio] + list(perm) + [fin]
        ruta_total = []
        costo_total = 0
        valido = True

        for i in range(len(puntos) - 1):
            subcamino, subcosto = calcular_ruta(puntos[i], puntos[i+1])
            if not subcamino:
                valido = False
                break
            if ruta_total:
                ruta_total += subcamino[1:]
            else:
                ruta_total += subcamino
            costo_total += subcosto

        if valido and costo_total < mejor_costo:
            mejor_ruta = ruta_total
            mejor_costo = costo_total

    if mejor_ruta:
        flash("Ruta óptima calculada con éxito.")
        return render_template('index.html',
                               nodos=nodos,
                               camino=mejor_ruta,
                               costo=round(mejor_costo, 2),
                               nodos_json=nodos_json)
    else:
        flash("No se pudo calcular una ruta válida con los nodos seleccionados.")
        return redirect('/')

@app.route('/eliminar/<nombre>')
def eliminar(nombre):
    from Controller.controller import eliminar_nodo
    eliminar_nodo(nombre)
    flash(f'Nodo \"{nombre}\" eliminado exitosamente.')
    return redirect('/')

@app.route('/editar/<nombre>', methods=['POST'])
def editar(nombre):
    from Controller.controller import eliminar_nodo, agregar_nodo
    nuevo_nombre = request.form['nuevo_nombre']
    nueva_lat = float(request.form['nueva_lat'])
    nueva_lon = float(request.form['nueva_lon'])

    eliminar_nodo(nombre)
    agregar_nodo(nuevo_nombre, nueva_lat, nueva_lon)

    flash(f'Nodo "{nombre}" fue modificado a "{nuevo_nombre}".')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
