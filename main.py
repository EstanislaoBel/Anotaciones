import threading
from uvicorn import Config,Server
from connectionbdd import crearBaseDeDatos, crearTabla
from interfaz import MenuPrincipal
from interfaz import interfaz_usuario
from administrador import administradorDeTarea
from tareas import Tarea
from fastapi import FastAPI
from pydantic import BaseModel
from administrador import administradorDeTarea
from tareas import Tarea
from connectionbdd import crearBaseDeDatos, crearTabla
from fastapi import FastAPI, status
import datetime

# Definición del modelo de datos para una tarea en la API
class apiTarea(BaseModel):
    id: int
    titulo: str
    descripcion: str
    estado: str
    creada: str | None
    actualizada: str | None

app = FastAPI()  # Crea una instancia de la clase FastAPI para la aplicación web

administrador = administradorDeTarea('tareas.db')  # Crea una instancia de la clase administradorDeTarea para administrar las tareas

# Define una ruta POST para insertar una nueva tarea en la base de datos
@app.post('/tarea')
def insertar_tarea(tarea:apiTarea):
    tarea_dict = dict(tarea)  # Convierte el objeto tarea en un diccionario
    tarea_objeto = Tarea(**tarea_dict)  # Crea una instancia de la clase Tarea con los datos del diccionario
    administrador.agregar_tarea(tarea_objeto)  # Agrega la tarea a la base de datos
    return tarea_objeto  # Devuelve la tarea creada

# Define una ruta DELETE para eliminar una tarea de la base de datos
@app.delete("/tarea/{id}")
def eliminar_tarea_endpoint(id: int):
    tarea_id = administrador.eliminar_tarea(id)  # Elimina la tarea con el ID especificado
    if tarea_id is not None:
        return {"mensaje": f"Tarea con ID {tarea_id} eliminada"}  # Devuelve un mensaje de éxito si se eliminó la tarea

# Define una ruta PUT para actualizar el estado de una tarea en la base de datos
@app.put('/tarea/{id}/{estado}')
def actualizarestado_api(id:int, estado:str):
    tarea_actual = administrador.traer_tarea(id)  # Obtiene la tarea actual con el ID especificado
    if tarea_actual:
        tarea_actual.estado = estado  # Actualiza el estado de la tarea
        tarea_actual.actualizada = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Actualiza la fecha y hora de actualización de la tarea
        administrador.actualizar_estado_tarea(tarea_actual.id, tarea_actual.estado, tarea_actual.actualizada)  # Actualiza el estado y la fecha de actualización de la tarea en la base de datos
        return {"mensaje": f"Tarea con id {id} actualizada"}  # Devuelve un mensaje de éxito si se actualizó la tarea

# Define una ruta GET para obtener una tarea de la base de datos
@app.get('/tarea/{id}')
def traertarea_api(id: int):
    tarea = administrador.traer_tarea(id)  # Obtiene la tarea con el ID especificado
    if tarea:
        return tarea  # Devuelve la tarea encontrada

# Función para iniciar la ventana de la interfaz de usuario
def iniciar_ventana():
    ventana = interfaz_usuario()  # Crea una instancia de la clase interfaz_usuario para la ventana de la interfaz de usuario
    ventana.mainloop()  # Inicia el bucle principal de la ventana

# Función para iniciar el servidor
def iniciar_servidor():
    config = Config(app="main:app", host="0.0.0.0", port=8000, reload=True)  # Configura el servidor con la aplicación y las opciones de host y puerto
    server = Server(config)  # Crea una instancia de la clase Server con la configuración
    server.run()  # Ejecuta el servidor

if __name__ == "__main__":
    ventana_thread = threading.Thread(target=iniciar_ventana)  # Crea un hilo para ejecutar la función iniciar_ventana
    servidor_thread = threading.Thread(target=iniciar_servidor)  # Crea un hilo para ejecutar la función iniciar_servidor

    servidor_thread.start()  # Inicia el hilo del servidor
    ventana_thread.start()  # Inicia el hilo de la ventana
