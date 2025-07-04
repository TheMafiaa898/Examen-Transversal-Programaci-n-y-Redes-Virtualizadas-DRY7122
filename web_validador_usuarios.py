# web_validador_usuarios.py

from flask import Flask, request, render_template_string
import sqlite3
import hashlib
import os

# Crear base de datos y tabla si no existen
def init_db():
    if not os.path.exists('usuarios.db'):
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                clave_hash TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        registrar_usuarios()

# Encriptar contraseña
def hash_password(clave):
    return hashlib.sha256(clave.encode()).hexdigest()

# Registrar usuarios con contraseñas hasheadas
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
        cursor.execute("INSERT INTO usuarios (nombre, clave_hash) VALUES (?, ?)", (nombre, hash_clave))

    conn.commit()
    conn.close()

# Validar usuario ingresado
def validar_usuario(nombre, clave):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT clave_hash FROM usuarios WHERE nombre = ?", (nombre,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0] == hash_password(clave)
    return False

# Inicializar base de datos
init_db()

# Configurar aplicación web con Flask
app = Flask(__name__)

html_formulario = """
<!doctype html>
<title>Validador de Usuarios</title>
<h2>Ingreso de Usuarios Autorizados</h2>
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
            mensaje = "✅ Usuario válido. Bienvenido."
        else:
            mensaje = "❌ Usuario o contraseña incorrecta."

    return render_template_string(html_formulario, mensaje=mensaje)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5800)