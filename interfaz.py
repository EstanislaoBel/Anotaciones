import tkinter as tk
from tkinter import messagebox
import requests
import json
from administrador import administradorDeTarea
import hashlib
from datetime import datetime

class Persona:
    personas = []  # Lista para almacenar todas las instancias de la clase Persona

    def __init__(self, id: int, nombre: str, apellido: str, fecha: int, dni: int, contraseña):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.fecha = fecha
        self.dni = dni
        self.contraseña = contraseña
        Persona.personas.append(self)  # Agrega la instancia actual a la lista de personas

    def persona_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha": self.fecha,
            "dni": self.dni,
            "contraseña": self.contraseña
        }

    def obtener_id(self) -> id:
        return self.id

    def __str__(self):
        return f"Usuario: ID={self.id}, Nombre={self.nombre}, Apellido={self.apellido}, Fecha={self.fecha}, DNI={self.dni}"

class Usuario(Persona):
    def __init__(self, id, nombre, apellido, fecha, dni, contraseña):
        super().__init__(id, nombre, apellido, fecha, dni, contraseña)
        self.contraseña = self.encriptar_contraseña(contraseña)
        self.ultimo_acceso = None

    def encriptar_contraseña(self, contraseña):
        md5 = hashlib.md5()  # Crea un objeto MD5
        md5.update(contraseña.encode('utf-8'))  # Codifica y actualiza el objeto MD5 con la contraseña
        return md5.hexdigest()  # Devuelve la contraseña encriptada utilizando el algoritmo MD5

    def verificar_contraseña(self, contraseña):
        return self.encriptar_contraseña(contraseña) == self.contraseña

    def registrar_ultimo_acceso(self):
        self.ultimo_acceso = datetime.now()  # Registra la fecha y hora actual como el último acceso del usuario

def interfaz_usuario():
    def enviar():
        # Obtiene los valores ingresados en los campos de entrada
        id = id_entry.get()
        nombre = nombre_entry.get()
        apellido = apellido_entry.get()
        fecha = fecha_entry.get()
        dni = dni_entry.get()
        contraseña = pass_entry.get()

        # Crea una instancia de Usuario con los valores ingresados y registra el último acceso
        usuario = Usuario(id, nombre, apellido, fecha, dni, contraseña)
        usuario.registrar_ultimo_acceso()

        usuario_window.destroy()  # Cierra la ventana actual
        mostrar_token(usuario.contraseña)  # Muestra el token en una nueva ventana

    usuario_window = tk.Tk()  # Crea una nueva ventana
    usuario_window.title("Inicio de sesión")  # Establece el título de la ventana
    usuario_window.geometry("500x400")  # Establece las dimensiones de la ventana

    # Crea etiquetas y campos de entrada para cada dato requerido
    id_label = tk.Label(usuario_window, text="ID:")
    id_label.pack()
    id_entry = tk.Entry(usuario_window)
    id_entry.pack()

    nombre_label = tk.Label(usuario_window, text="Nombre:")
    nombre_label.pack()
    nombre_entry = tk.Entry(usuario_window)
    nombre_entry.pack()

    apellido_label = tk.Label(usuario_window, text="Apellido:")
    apellido_label.pack()
    apellido_entry = tk.Entry(usuario_window)
    apellido_entry.pack()

    fecha_label = tk.Label(usuario_window, text="Fecha de nacimiento:")
    fecha_label.pack()
    fecha_entry = tk.Entry(usuario_window)
    fecha_entry.pack()

    dni_label = tk.Label(usuario_window, text="DNI:")
    dni_label.pack()
    dni_entry = tk.Entry(usuario_window)
    dni_entry.pack()

    pass_label = tk.Label(usuario_window, text="Contraseña:")
    pass_label.pack()
    pass_entry = tk.Entry(usuario_window, show="*")
    pass_entry.pack()

    enviar_button = tk.Button(usuario_window, text="Enviar", command=enviar)
    enviar_button.pack(pady=10)

    usuario_window.mainloop()  # Inicia el bucle principal de la interfaz gráfica

# Las siguientes funciones tienen una estructura similar y crean ventanas con etiquetas, botones y acciones asociadas.
# Estas funciones se encargan de mostrar diferentes vistas y ejecutar acciones relacionadas con la interfaz gráfica.

def Opciones():
    opciones_window = tk.Tk()
    opciones_window.title("Opciones")
    opciones_window.geometry("300x200")

    def seguir():
        opciones_window.destroy()
        mostrar_datos_persona()

    datos_button = tk.Button(opciones_window, text="Ver Datos", command=seguir)
    datos_button.pack(pady=10)

    opciones_window.mainloop()

def mostrar_token(token):
    token_window = tk.Tk()
    token_window.title("Token")
    token_window.geometry("300x100")

    token_label = tk.Label(token_window, text="Token:")
    token_label.pack()

    token_value = tk.Label(token_window, text=token)
    token_value.pack()

    def seguir():
        token_window.destroy()
        Opciones()

    continuar_button = tk.Button(token_window, text="Continuar", command=seguir)
    continuar_button.pack(pady=10)

    token_window.mainloop()

def mostrar_datos_persona():
    datos_window = tk.Tk()
    datos_window.title("Datos Personales")
    datos_window.geometry("600x200")

    for persona in Persona.personas:
        datos_label = tk.Label(datos_window, text=str(persona))
        datos_label.pack(side="top")

    def seguir():
        datos_window.destroy()
        MenuPrincipal()

    continuar_button = tk.Button(datos_window, text="Continuar", command=seguir)
    continuar_button.pack(pady=10)

    datos_window.mainloop()



class MenuPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ventana principal")
        self.geometry('300x300')
        self.ventana_principal = self

        # Crea una etiqueta de título para la ventana principal
        titulo_label = tk.Label(self, text="Administrador de Tareas", font=("Arial", 14, "bold"))
        titulo_label.pack(pady=10)

        # Crea botones para cada acción en la ventana principal y los asocia con sus respectivas funciones
        btn_crear_tarea = tk.Button(self, text="Crear tarea", command=self.crear_tarea)
        btn_crear_tarea.pack(pady=10)

        btn_traer_tarea = tk.Button(self, text="Traer tarea", command=self.traer_tarea)
        btn_traer_tarea.pack(pady=10)

        btn_actualizar_estado = tk.Button(self, text="Actualizar estado", command=self.actualizar_estado)
        btn_actualizar_estado.pack(pady=10)

        btn_eliminar_tarea = tk.Button(self, text="Eliminar tarea", command=self.eliminar_tarea)
        btn_eliminar_tarea.pack(pady=10)

    def crear_tarea(self):
        # Crea una nueva ventana emergente para crear una tarea
        ventana = tk.Toplevel()
        ventana.title('Crear tarea')
        ventana.geometry("300x300")

        # Crea etiquetas y campos de entrada para cada dato de la tarea
        id_label = tk.Label(ventana, text="ID:")
        id_label.pack()

        id_entry = tk.Entry(ventana)
        id_entry.pack()

        titulo_label = tk.Label(ventana, text="Título:")
        titulo_label.pack()

        titulo_entry = tk.Entry(ventana)
        titulo_entry.pack()

        descripcion_label = tk.Label(ventana, text="Descripción:")
        descripcion_label.pack()

        descripcion_entry = tk.Entry(ventana)
        descripcion_entry.pack()

        estado_label = tk.Label(ventana, text="Estado:")
        estado_label.pack()

        estado_entry = tk.Entry(ventana)
        estado_entry.pack()

        def crear_tareadb():
            # Obtiene los valores ingresados en los campos de entrada
            id_value = id_entry.get()
            titulo_value = titulo_entry.get()
            descripcion_value = descripcion_entry.get()
            estado_value = estado_entry.get()

            # Crea un diccionario con los valores de la tarea
            tarea = {
                "id": id_value,
                "titulo": titulo_value,
                "descripcion": descripcion_value,
                "estado": estado_value
            }

            try:
                # Envía una solicitud POST al servidor para crear la tarea utilizando el diccionario como JSON
                response = requests.post('http://127.0.0.1:8000/tarea', json=tarea)
                response.raise_for_status()

                # Muestra un mensaje con la tarea creada y sus datos
                tarea_creada = response.json()
                messagebox.showinfo("Tarea creada", f"Tarea creada:\nID: {tarea_creada['id']}\nTítulo: {tarea_creada['titulo']}\nDescripción: {tarea_creada['descripcion']}\nEstado: {tarea_creada['estado']}")

                # Cierra la ventana actual y vuelve a la ventana principal
                self.destroy()
                ventana_principal = MenuPrincipal()
                ventana_principal.mainloop()

            except requests.exceptions.HTTPError as err:
                # Maneja los posibles errores HTTP y muestra mensajes de error correspondientes
                if response.status_code == 422:
                    messagebox.showerror("Error", "El ID debe ser un número entero")
                elif response.status_code == 409:
                    messagebox.showerror("Error", "Ya existe una tarea con ese ID")
                elif response.status_code == 400:
                    messagebox.showerror("Error", "Campos vacíos")

            except requests.exceptions.RequestException:
                messagebox.showerror("Error", "Error de conexión con el servidor")

        btn_crear = tk.Button(ventana, text="Crear", command=crear_tareadb)
        btn_crear.pack(pady=10)

        volver_button = tk.Button(ventana, text="Volver", command=self.volver)
        volver_button.pack(pady=10)

    def volver(self):
        # Cierra la ventana actual y vuelve a la ventana principal
        self.destroy()
        ventana_principal = MenuPrincipal()
        ventana_principal.mainloop()

    def actualizar_estado(self):
        # Crea una nueva ventana emergente para actualizar el estado de una tarea
        ventana = tk.Toplevel()
        ventana.title('Actualizar estado')
        ventana.geometry("300x300")

        def actualizar_estadodb():
            # Obtiene el ID y el nuevo estado ingresados en los campos de entrada
            id = id_entry.get()
            estado = estado_entry.get()
            payload = {"id": id, "estado": estado}

            try:
                # Envía una solicitud PUT al servidor para actualizar el estado de la tarea
                response = requests.put(f'http://127.0.0.1:8000/tarea/{id}/{estado}', json=payload)
                response.raise_for_status()

                # Muestra un mensaje de éxito
                messagebox.showinfo("Tarea actualizada", "Se ha actualizado la tarea")

                # Cierra la ventana actual y vuelve a la ventana principal
                self.destroy()
                ventana_principal = MenuPrincipal()
                ventana_principal.mainloop()

            except requests.exceptions.HTTPError as err:
                # Maneja los posibles errores HTTP y muestra mensajes de error correspondientes
                if response.status_code == 404:
                    messagebox.showerror("Error", "No se encontró una tarea con ese ID")
                elif response.status_code == 422:
                    messagebox.showerror("Error", "El ID no es un número entero")
                else:
                    messagebox.showerror("Error", "No se completó el campo estado")

            except requests.exceptions.RequestException:
                messagebox.showerror("Error", "Error de conexión con el servidor")

        id_label = tk.Label(ventana, text="ID:")
        id_label.pack()

        id_entry = tk.Entry(ventana)
        id_entry.pack()

        estado_label = tk.Label(ventana, text="Estado:")
        estado_label.pack()

        estado_entry = tk.Entry(ventana)
        estado_entry.pack()

        btn_actualizar = tk.Button(ventana, text="Actualizar", command=actualizar_estadodb)
        btn_actualizar.pack(pady=10)

        volver_button = tk.Button(ventana, text="Volver", command=self.volver)
        volver_button.pack(pady=10)



        # -----------------------------------------------------
        
    def eliminar_tarea(self):
        # Crea una nueva ventana emergente para eliminar una tarea
        ventana = tk.Toplevel()
        ventana.title('Crear tarea')
        ventana.geometry("300x300")
    
        def eliminartarea_api(id):
            try:
                # Envía una solicitud DELETE al servidor para eliminar la tarea con el ID especificado
                response = requests.delete(f'http://127.0.0.1:8000/tarea/{id}', json={"id": id})
                response.raise_for_status()

                # Muestra un mensaje de éxito y vuelve a la ventana principal
                messagebox.showinfo("Tarea eliminada", f"Tarea con ID {id} eliminada")
                self.destroy()
                ventana_principal = MenuPrincipal()
                ventana_principal.mainloop()

            except requests.exceptions.HTTPError as err:
                # Maneja los posibles errores HTTP y muestra mensajes de error correspondientes
                if response.status_code == 404:
                    messagebox.showerror("Error", "No se encontró una tarea con ese ID")
                elif response.status_code == 422:
                    messagebox.showerror("Error", "El ID debe ser un número entero")
                else:
                    messagebox.showerror("Error", "Complete el ID")

            except requests.exceptions.RequestException:
                messagebox.showerror("Error", "Error de conexión con el servidor")

        id_label = tk.Label(ventana, text="ID:")
        id_label.pack()

        id_entry = tk.Entry(ventana)
        id_entry.pack()
        
        btn_eliminar = tk.Button(ventana, text="Eliminar", command=lambda: eliminartarea_api(id_entry.get()))
        btn_eliminar.pack(pady=10)

        volver_button = tk.Button(ventana, text="Volver", command=self.volver)
        volver_button.pack(pady=10)

    def traer_tarea(self):
        # Crea una nueva ventana emergente para obtener información sobre una tarea específica o todas las tareas
        ventana = tk.Toplevel()
        ventana.title('Crear tarea')
        ventana.geometry("300x300")

        def traertarea_api(id):
            try:
                # Envía una solicitud GET al servidor para obtener la información de la tarea con el ID especificado
                response = requests.get(f'http://127.0.0.1:8000/tarea/{id}', json={"id": id})
                response.raise_for_status()

                # Obtiene la tarea y muestra su información en un cuadro de mensaje
                tarea_creada = response.json()
                messagebox.showinfo("Tarea", f"Tarea:\nID: {tarea_creada['id']}\nTítulo: {tarea_creada['titulo']}\nDescripción: {tarea_creada['descripcion']}\nEstado: {tarea_creada['estado']}\nActualizada: {tarea_creada['actualizada']}")
                self.destroy()
                ventana_principal = MenuPrincipal()
                ventana_principal.mainloop()

            except requests.exceptions.HTTPError as err:
                # Maneja los posibles errores HTTP y muestra mensajes de error correspondientes
                if response.status_code == 404:
                    messagebox.showerror("Error", "No hay una tarea con ese ID")
                elif response.status_code == 422:
                    messagebox.showerror("Error", "El ID no es un número entero")
                else:
                    messagebox.showerror("Error", "Falta el ID")

            except requests.exceptions.RequestException:
                messagebox.showerror("Error", "Error de conexión con el servidor")

        def traer_todas_tareas():
            # Obtiene todas las tareas y las muestra en un cuadro de mensaje
            administrador = administradorDeTarea("tareas.db")
            tareas = administrador.traer_todas_tareas()
            if tareas:
                messagebox.showinfo("Todas las Tareas", "Lista de todas las tareas:\n" + tareas)
            else:
                messagebox.showinfo("Todas las Tareas", "No hay tareas registradas")
            self.destroy()
            ventana_principal = MenuPrincipal()
            ventana_principal.mainloop()

        id_label = tk.Label(ventana, text="ID:")
        id_label.pack()

        id_entry = tk.Entry(ventana)
        id_entry.pack()
        
        btn_eliminar = tk.Button(ventana, text="Traer tarea", command=lambda: traertarea_api(id_entry.get()))
        btn_eliminar.pack(pady=10)
    

        todas_tareas_button = tk.Button(ventana, text="Todas las Tareas", command=traer_todas_tareas)
        todas_tareas_button.pack(pady=5)

        volver_button = tk.Button(ventana, text="Volver", command=self.volver)
        volver_button.pack(pady=10)
