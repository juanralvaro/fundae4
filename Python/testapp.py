from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista en memoria para almacenar los elementos
items = []

@app.route('/')
def home():
    return """
    <h1>Bienvenido a la aplicación Flask!</h1>
    <p>Usa los siguientes enlaces para interactuar:</p>
    <ul>
        <li><a href="/items">Ver lista de elementos</a></li>
    </ul>
    """

@app.route('/items', methods=['GET'])
def get_items():
    """Devuelve la lista de elementos."""
    item_list = "<ul>" + "".join(f"<li>{item} <form action='/items/{index}' method='post' style='display:inline'>" \
                                 f"<input type='hidden' name='_method' value='DELETE'>" \
                                 f"<button type='submit'>Eliminar</button></form> " \
                                 f"<form action='/items/{index}' method='post' style='display:inline'>" \
                                 f"<input type='hidden' name='_method' value='PUT'>" \
                                 f"<input type='text' name='item' placeholder='Modificar elemento' required>" \
                                 f"<button type='submit'>Modificar</button></form></li>" \
                                 for index, item in enumerate(items)) + "</ul>"
    return f"""
    <h1>Lista de elementos</h1>
    {item_list if items else '<p>No hay elementos en la lista.</p>'}
    <form action="/items" method="post">
        <input type="text" name="item" placeholder="Nuevo elemento" required>
        <button type="submit">Agregar</button>
    </form>
    <a href="/">Volver a la página principal</a>
    """

@app.route('/items', methods=['POST'])
def add_item():
    """Agrega un nuevo elemento a la lista."""
    item = request.form.get('item')
    if not item:
        return "<p>Error: El campo 'item' es requerido.</p><a href='/items'>Volver</a>", 400
    
    items.append(item)
    return f"<p>Elemento agregado con éxito: {item}</p><a href='/items'>Volver a la lista</a>", 201

@app.route('/items/<int:index>', methods=['POST'])
def modify_or_delete_item(index):
    """Modifica o elimina un elemento según el método enviado."""
    method = request.form.get('_method')

    if method == 'DELETE':
        if index < 0 or index >= len(items):
            return "<p>Error: Índice fuera de rango.</p><a href='/items'>Volver</a>", 404

        removed_item = items.pop(index)
        return f"<p>Elemento eliminado con éxito: {removed_item}</p><a href='/items'>Volver a la lista</a>", 200

    elif method == 'PUT':
        new_item = request.form.get('item')
        if not new_item:
            return "<p>Error: El campo 'item' es requerido.</p><a href='/items'>Volver</a>", 400

        if index < 0 or index >= len(items):
            return "<p>Error: Índice fuera de rango.</p><a href='/items'>Volver</a>", 404

        items[index] = new_item
        return f"<p>Elemento modificado con éxito: {new_item}</p><a href='/items'>Volver a la lista</a>", 200

    return "<p>Acción no permitida.</p><a href='/items'>Volver</a>", 405

if __name__ == '__main__':
    import sys
    if sys.version_info < (3, 13):
        raise RuntimeError("Esta aplicación requiere Python 3.13 o superior.")
    app.run(debug=True)
