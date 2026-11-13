import os
from datetime import datetime
from modelo.socio import Socio
from errores.excepciones import BibliotecaError


class SociosDao:
    def __init__(self, ruta_fichero="datos/socios.txt", ruta_log="datos/log.txt"):
        self.ruta_fichero = ruta_fichero
        self.ruta_log = ruta_log
        self.socios = self._cargar_socios()

    def _cargar_socios(self):
        lista = []
        if not os.path.exists(self.ruta_fichero):
            raise BibliotecaError(f"No se encontró el fichero {self.ruta_fichero}", "FICHERO_NO_ENCONTRADO")
        with open(self.ruta_fichero, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split(";")
                if len(partes) == 4:
                    lista.append(Socio(*partes))
        return lista

    def registrar_log(self, evento, detalles):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.ruta_log, "a", encoding="utf-8") as f:
            f.write(f"[{fecha}][{evento}][{detalles}]\n")

    def obtener_todos(self):
        return self.socios

    def buscar_por_codigo(self, codigo_socio):
        for socio in self.socios:
            if socio.codigo_socio == str(codigo_socio).strip():
                return socio
        raise BibliotecaError(f"No existe ningún socio con el código '{codigo_socio}'.", "SOCIO_NO_ENCONTRADO")

    def obtener_socios_con_libro(self):
        return [socio for socio in self.socios if socio.tiene_libro()]

    def anadir_socio(self, codigo_socio, nombre, email):
        codigo_limpio = str(codigo_socio).strip()
        for socio in self.socios:
            if socio.codigo_socio == codigo_limpio:
                raise BibliotecaError(f"Ya existe un socio con el código '{codigo_limpio}'.", "CODIGO_SOCIO_DUPLICADO")

        nuevo_socio = Socio(codigo_limpio, nombre.strip(), email.strip(), None)
        self.socios.append(nuevo_socio)
        self.registrar_log("ALTA_SOCIO", f"Socio '{nuevo_socio.nombre}' ({nuevo_socio.codigo_socio}) registrado")

    def volcar_a_fichero(self):
        with open(self.ruta_fichero, "w", encoding="utf-8") as f:
            for socio in self.socios:
                libro = socio.libro_prestado if socio.libro_prestado is not None else "None"
                f.write(f"{socio.codigo_socio};{socio.nombre};{socio.email};{libro}\n")