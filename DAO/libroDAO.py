import os
from datetime import datetime
from modelo.libro import Libro
from errores.excepciones import BibliotecaError


class LibrosDao:
    def __init__(self, ruta_fichero="datos/libros.txt", ruta_log="datos/log.txt"):
        self.ruta_fichero = ruta_fichero
        self.ruta_log = ruta_log
        self.libros = self._cargar_libros()

    def _cargar_libros(self):
        lista = []
        if not os.path.exists(self.ruta_fichero):
            raise BibliotecaError(f"No se encontró el fichero {self.ruta_fichero}", "FICHERO_NO_ENCONTRADO")
        with open(self.ruta_fichero, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split(";")
                if len(partes) == 6:
                    lista.append(Libro(*partes))
        return lista

    def registrar_log(self, evento, detalles):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.ruta_log, "a", encoding="utf-8") as f:
            f.write(f"[{fecha}][{evento}][{detalles}]\n")

    def obtener_todos(self):
        return self.libros

    def obtener_disponibles(self):
        return [libro for libro in self.libros if libro.esta_disponible()]

    def buscar_por_titulo(self, termino):
        termino_limpio = termino.strip().lower()
        return [libro for libro in self.libros if termino_limpio in libro.titulo.lower()]

    def buscar_por_codigo(self, codigo):
        for libro in self.libros:
            if libro.codigo == str(codigo).strip():
                return libro
        raise BibliotecaError(f"No existe ningún libro con el código '{codigo}'.", "LIBRO_NO_ENCONTRADO")

    def prestar_libro(self, codigo_libro, socio):
        libro = self.buscar_por_codigo(codigo_libro)
        if socio.tiene_libro():
            raise BibliotecaError(
                f"El socio '{socio.nombre}' ya tiene prestado el libro {socio.libro_prestado}.",
                "SOCIO_YA_TIENE_LIBRO"
            )
        if not libro.esta_disponible():
            raise BibliotecaError(
                f"El libro '{libro.titulo}' ya está prestado al socio {libro.codigo_socio}.",
                "LIBRO_YA_PRESTADO"
            )

        libro.codigo_socio = socio.codigo_socio
        socio.libro_prestado = libro.codigo
        self.registrar_log("PRESTAMO", f"Libro {libro.codigo} ('{libro.titulo}') prestado al socio {socio.codigo_socio}")
        return libro

    def devolver_libro(self, socio):
        if not socio.tiene_libro():
            raise BibliotecaError(
                f"El socio '{socio.nombre}' no tiene ningún libro prestado.",
                "SOCIO_SIN_LIBRO"
            )

        libro = self.buscar_por_codigo(socio.libro_prestado)
        libro.codigo_socio = None
        socio.libro_prestado = None
        self.registrar_log("DEVOLUCION", f"Socio {socio.codigo_socio} devolvió el libro {libro.codigo} ('{libro.titulo}')")
        return libro

    def anadir_libro(self, codigo, titulo, autor, anio, categoria):
        codigo_limpio = str(codigo).strip()
        for libro in self.libros:
            if libro.codigo == codigo_limpio:
                raise BibliotecaError(f"Ya existe un libro con el código '{codigo_limpio}'.", "CODIGO_LIBRO_DUPLICADO")

        nuevo_libro = Libro(codigo_limpio, titulo.strip(), autor.strip(), anio, categoria.strip(), None)
        self.libros.append(nuevo_libro)
        self.registrar_log("ALTA_LIBRO", f"Libro '{nuevo_libro.titulo}' ({nuevo_libro.codigo}) añadido")

    def volcar_a_fichero(self):
        with open(self.ruta_fichero, "w", encoding="utf-8") as f:
            for libro in self.libros:
                socio = libro.codigo_socio if libro.codigo_socio is not None else "None"
                f.write(f"{libro.codigo};{libro.titulo};{libro.autor};{libro.anio};{libro.categoria};{socio}\n")