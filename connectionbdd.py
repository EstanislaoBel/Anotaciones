import sqlite3 as sql
from tareas import Tarea
import datetime

def crearBaseDeDatos(db_file):
    conn = sql.connect(db_file)  # Establece una conexión con la base de datos utilizando el archivo especificado en db_file
    conn.commit()  # Guarda los cambios en la base de datos
    conn.close()  # Cierra la conexión con la base de datos

def crearTabla():
    conn = sql.connect('tareas.db')  # Establece una conexión con la base de datos SQLite 'tareas.db'
    cursor = conn.cursor()  # Crea un cursor para ejecutar consultas SQL en la base de datos
    cursor.execute("""CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER,
            titulo TEXT,
            descripcion TEXT,
            estado TEXT,
            creada TEXT,
            actualizada TEXT)""")  # Crea una tabla llamada 'tareas' con las columnas especificadas si no existe ya
    conn.commit()  # Guarda los cambios en la base de datos
    conn.close()  # Cierra la conexión con la base de datos

def agregarFila(tarea:Tarea):
    conn = sql.connect('tareas.db')  # Establece una conexión con la base de datos SQLite 'tareas.db'
    cursor = conn.cursor()  # Crea un cursor para ejecutar consultas SQL en la base de datos
    cursor.execute("""INSERT INTO tareas (id, titulo, descripcion, estado, creada, actualizada)
                      VALUES (?, ?, ?, ?, ?, ?)""", tuple(tarea.values()))  # Inserta los valores de la tarea en la tabla 'tareas'
    tarea_id = cursor.lastrowid  # Obtiene el ID de la fila recién insertada
    conn.commit()  # Guarda los cambios en la base de datos
    conn.close()  # Cierra la conexión con la base de datos
    return tarea_id  # Devuelve el ID de la fila recién insertada

def traerTareaDeBDD(id):
    conn = sql.connect('tareas.db')  # Establece una conexión con la base de datos SQLite 'tareas.db'
    cursor = conn.cursor()  # Crea un cursor para ejecutar consultas SQL en la base de datos
    cursor.execute("SELECT * FROM tareas WHERE id=?", (id,))  # Selecciona la fila con el ID especificado de la tabla 'tareas'
    tarea = cursor.fetchone()  # Obtiene la fila resultante de la consulta
    conn.commit()  # Guarda los cambios en la base de datos
    conn.close()  # Cierra la conexión con la base de datos
    return tarea  # Devuelve la fila obtenida

def traerTareasDeBDD():
    conn = sql.connect('tareas.db')  # Establece una conexión con la base de datos SQLite 'tareas.db'
    cursor = conn.cursor()  # Crea un cursor para ejecutar consultas SQL en la base de datos
    cursor.execute("SELECT * FROM tareas")  # Selecciona todas las filas de la tabla 'tareas'
    tareas = cursor.fetchall()  # Obtiene todas las filas resultantes de la consulta
    conn.commit()  # Guarda los cambios en la base de datos
    conn.close()  # Cierra la conexión con la base de datos
    return tareas  # Devuelve todas las filas obtenidas

def modificarValor(id, estado, actualizada):
    conn = sql.connect('tareas.db')  # Establece una conexión con la base de datos SQLite 'tareas.db'
    cursor = conn.cursor()  # Crea un cursor para ejecutar consultas SQL en la base de datos
    cursor.execute("UPDATE tareas SET estado=?, actualizada=? WHERE id=?", (estado, actualizada, id))  # Actualiza el estado y la fecha actualizada de la fila con el ID especificado
    conn.commit()  # Guarda los cambios en la base de datos
