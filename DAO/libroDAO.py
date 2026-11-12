import os
from datetime import datetime
from modelo.libro import Libro
from errores.excepciones import BibliotecaError

class LibroDAO:
    def __init__(self, ruta_fichero ="datos/libros.txt", ruta_log="datos/log.txt"):
        self.ruta_fichero = ruta_fichero
        self.ruta_log = ruta_log
        self.libros = self.cargar_libros()

    def cargar_libros(self):
        lista = []
        if not os.path.exists(self.ruta_fichero):
            raise BibliotecaError(f"No existe el fichero {self.ruta_fichero}", "ERR_FICHERO")
        with open(self.ruta_fichero, "r") as f:
            for linea in f:
                partes = linea.strip().split(",")
                if len(partes) == 6: 
                    lista.append(Libro(*partes))
        return lista

    def registrar_log(self, evento, detalles):
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.ruta_log, "a") as f:
            f.write(f"{fecha_hora} - {evento}: {detalles}\n")

    def obtener_todos(self):
        return self.libros

    def obtener_disponibles(self):
        return [libro for libro in self.libros if libro.esta_disponible()]

    def buscar_por_titulo(self, termino):
        termino = termino.lower()
        return [libro for libro in self.libros if termino in libro.titulo.lower()]

    def buscar_por_codigo(self, codigo):
        for libro in self.libros:
            if libro.codigo == str(codigo):
                return libro
        raise BibliotecaError(f"No se encontró el libro con código {codigo}", "LIBRO_NO_ENCONTRADO")

    def anadir_libro(self, codigo, titulo, autor, anio, categoria):
         for libro in self.libros:
            if libro.codigo == str(codigo):
                raise BibliotecaError(f"Ya existe un libro con código {codigo}", "CODIGO_DUPLICADO")
         nuevo = Libro(codigo, titulo, autor, anio, categoria, None)
         self.libros.append(nuevo)
         self.registrar_log("ALTA_LIBRO", f"Libro '{titulo}' ({codigo}) añadido")

    