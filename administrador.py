from tareas import Tarea
from connectionbdd import agregarFila, crearBaseDeDatos, crearTabla, traerTareaDeBDD, traerTareasDeBDD, modificarValor
import sqlite3 as sql
from fastapi import FastAPI
from fastapi import  status
from datetime import datetime
from pydantic import BaseModel
from tkinter import messagebox
import tkinter.messagebox as messagebox
import datetime
import tkinter as tk
import requests
from flask import Response

class administradorDeTarea:
    def __init__(self, db_file:str):
        self.db = sql.connect(db_file)  # Establece una conexión con la base de datos SQLite utilizando el archivo especificado en db_file
        
    def agregar_tarea(self, tarea: Tarea) -> int:
        tarea_dic = tarea.tarea_dict()  # Obtiene un diccionario con los datos de la tarea utilizando el método tarea_dict() de la clase Tarea
        conn = sql.connect('tareas.db')  # Establece una conexión con la base de datos SQLite 'tareas.db'
        cursor = conn.cursor()  # Crea un cursor para ejecutar consultas SQL en la base de datos
        cursor.execute("""INSERT INTO tareas (id, titulo, descripcion, estado, creada, actualizada)
                        VALUES (?, ?, ?, ?, ?, ?)""", tuple(tarea_dic.values()))  # Inserta los valores del diccionario en la tabla 'tareas'
        tarea_id = cursor.lastrowid  # Obtiene el ID de la tarea recién insertada
        conn.commit()  # Guarda los cambios en la base de datos
        conn.close()  # Cierra la conexión con la base de datos
        return tarea_id  # Devuelve el ID de la tarea recién insertada

    def traer_tarea(self, tarea_id: int) -> Tarea:
        tarea=traerTareaDeBDD(tarea_id)  # Llama a la función traerTareaDeBDD para obtener la información de la tarea con el ID especificado
        if tarea:
            return Tarea(*tarea)  # Si se encuentra la tarea, crea un objeto Tarea con los datos obtenidos y lo devuelve
        else:
            return None  # Si no se encuentra la tarea, devuelve None
        
    def id_repetido(self, id):
        conexion = sql.connect('tareas.db')  # Establece una conexión con la base de datos SQLite 'tareas.db'
        cursor = conexion.cursor()  # Crea un cursor para ejecutar consultas SQL en la base de datos
        cursor.execute("SELECT COUNT(*) FROM tareas WHERE id = ?", (id,))  # Cuenta el número de filas en la tabla 'tareas' que tienen el ID especificado
        resultado = cursor.fetchone()  # Obtiene el resultado de la consulta
        ids = resultado[0]  # Obtiene el valor de la columna COUNT(*)
        conexion.close()  # Cierra la conexión con la base de datos
        return ids  # Devuelve el número de IDs repetidos

    def traer_todas_tareas(self):
        conn = sql.connect('tareas.db')  # Establece una conexión con la base de datos SQLite 'tareas.db'
        cursor = conn.cursor()  # Crea un cursor para ejecutar consultas SQL en la base de datos
        cursor.execute("SELECT * FROM tareas")  # Selecciona todas las filas de la tabla 'tareas'
        tareas = cursor.fetchall()  # Obtiene todas las filas resultantes de la consulta
        conn.close()  # Cierra la conexión con la base de datos
        todas_tareas = ""  # Variable para almacenar todas las tareas como una cadena de texto
        for tarea in tareas:
            tarea = Tarea(*tarea)  # Crea un objeto Tarea con los datos de la fila actual
            todas_tareas += f"ID: {tarea.id}\nTítulo: {tarea.titulo}\nDescripción: {tarea.descripcion}\nEstado: {tarea.estado}\n\n"  # Agrega los datos de la tarea a la cadena de texto
        return todas_tareas  # Devuelve todas las tareas como una cadena de texto
    
    def actualizar_estado_tarea(self, tarea_id: int, estado: str, actualizada:str):
        conn = sql.connect('tareas.db')  # Establece una conexión con la base de datos SQLite 'tareas.db'
        cursor = conn.cursor()  # Crea un cursor para ejecutar consultas SQL en la base de datos
        cursor.execute("UPDATE tareas SET estado=?, actualizada=? WHERE id=?", (estado, actualizada, tarea_id))  # Actualiza el estado y la fecha actualizada de la tarea con el ID especificado
        conn.commit()  # Guarda los cambios en la base de datos
        conn.close()  # Cierra la conexión con la base de datos

    def eliminar_tarea(self, tarea_id: int):
        conn = sql.connect('tareas.db')  # Establece una conexión con la base de datos SQLite 'tareas.db'
        cursor = conn.cursor()  # Crea un cursor para ejecutar consultas SQL en la base de datos

        cursor.execute("SELECT id FROM tareas WHERE id=?", (tarea_id,))  # Selecciona el ID de la tarea con el ID especificado
        tarea = cursor.fetchone()  # Obtiene el resultado de la consulta
