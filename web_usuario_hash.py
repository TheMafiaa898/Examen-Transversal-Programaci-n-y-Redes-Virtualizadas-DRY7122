# web_usuario_hash.py

from flask import Flask, request, render_template_string
import sqlite3
import hashlib

# Crear la base de datos y la tabla si no existe
def init_db():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            contraseña_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Hash de contraseña
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Agregar usuarios (nombres reales del grupo)
def registrar_usuarios():
    usuarios = {
        "Ignacio Faundez": "clave123",
        "Benjamin Martinez": "clave456",
        "Franco Rojas": "clave789"
    }

    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    for nombre, clave in usuarios.items():
        hash_clave = hash_password(clave)
        cursor.execute("INSERT INTO usuarios (nombre, contraseña_hash) VALUES (?, ?)", (nombre, hash_clave))

    conn.commit()
    conn.close()

# Validar usuario
def validar_usuario(nombre, clave):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT contraseña_hash FROM usuarios WHERE nombre = ?", (nombre,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0] == hash_password(clave)
    return False

# Inicialización
init_db()
registrar_usuarios()

# Configuración del servidor Flask
app = Flask(__name__)

formulario_html = """
<!doctype html>
<title>Ingreso al sistema</title>
<h2>Validador de Usuarios</h2>
<form method="post">
  Nombre: <input type="text" name="nombre"><br>
  Contraseña: <input type="password" name="clave"><br>
  <input type="submit" value="Validar">
</form>
<p>{{ mensaje }}</p>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    mensaje = ''
    if request.method == 'POST':
        nombre = request.form['nombre']
        clave = request.form['clave']
        if validar_usuario(nombre, clave):
            mensaje = "✅ Usuario válido. Acceso permitido."
        else:
            mensaje = "Usuario o contraseña inválidos."

    return render_template_string(formulario_html, mensaje=mensaje)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5800)
