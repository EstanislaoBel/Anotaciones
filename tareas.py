import datetime  # Importa el módulo datetime para trabajar con fechas y horas en Python
from typing import Optional  # Importa el tipo de datos Optional para indicar que un parámetro puede ser None

class Tarea:
    def __init__(self, id: int, titulo:str, descripcion: str, estado:  str, creada: Optional[str] = None, actualizada: Optional[str] = None):
        # Inicializa la clase Tarea con los siguientes parámetros:
        # - id: int (ID de la tarea)
        # - titulo: str (título de la tarea)
        # - descripcion: str (descripción de la tarea)
        # - estado: str (estado de la tarea)
        # - creada: str (opcional) (fecha y hora de creación de la tarea, si no se proporciona, se establecerá la fecha y hora actual)
        # - actualizada: str (opcional) (fecha y hora de actualización de la tarea)
        
        self.id = id  # Asigna el valor del parámetro id al atributo id de la instancia de la clase
        self.titulo = titulo  # Asigna el valor del parámetro titulo al atributo titulo de la instancia de la clase
        self.descripcion = descripcion  # Asigna el valor del parámetro descripcion al atributo descripcion de la instancia de la clase
        self.estado = estado  # Asigna el valor del parámetro estado al atributo estado de la instancia de la clase
        if creada is None:  # Verifica si el parámetro creada es None
            self.creada = datetime.datetime.now()  # Si es None, asigna la fecha y hora actual al atributo creada
        else:
            self.creada = creada  # Si no es None, asigna el valor del parámetro creada al atributo creada
        self.actualizada = actualizada  # Asigna el valor del parámetro actualizada al atributo actualizada de la instancia de la clase
    
    def tarea_dict(self) -> dict:
        # Devuelve un diccionario con los atributos de la tarea y sus valores correspondientes
        return {
            "id" : self.id,
            "titulo" : self.titulo,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "creada": self.creada,
            "actualizada": self.actualizada
        }
    
    def obtener_id(self) -> id:
        # Devuelve el ID de la tarea
        return self.id
    
    def __str__(self):
        return f"Tarea: ID={self.id}, Título={self.titulo}, Descripción={self.descripcion}, Estado={self.estado}, Creada={self.creada}, Actualizada={self.actualizada}"