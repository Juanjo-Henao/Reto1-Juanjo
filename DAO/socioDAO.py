import os
from datetime import datetime
from modelo.socio import Socio
from errores.excepciones import BibliotecaError

class SocioDAO:
    def __init__(self, ruta_fichero="datos/socios.txt", ruta_log="datos/log.txt"):
        self.ruta_fichero = ruta_fichero
        self.ruta_log = ruta_log
        self.socios = self.cargar_socios()

    def cargar_socios(self):
        lista = []
        if not os.path.exists(self.ruta_fichero):
            raise BibliotecaError(f"No existe el fichero {self.ruta_fichero}", "ERR_FICHERO")
        with open(self.ruta_fichero, "r") as f:
            for linea in f:
                partes = linea.strip().split(",")
                if len(partes) == 4: 
                    lista.append(Socio(*partes))
        return lista

    def registrar_log(self, evento, detalles):
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.ruta_log, "a") as f:
            f.write(f"{fecha_hora} - {evento}: {detalles}\n")

    def buscar_por_codigo(self, codigo_socio):
        for socio in self.socios:
            if socio.codigo_socio == str(codigo_socio):
                return socio
        raise BibliotecaError(f"No se encontró el socio con código {codigo_socio}", "SOCIO_NO_ENCONTRADO")

    def obtener_socios_con_libro(self):
        return [socio for socio in self.socios if socio.tiene_libro()]

    def anadir_socio(self, codigo_socio, nombre, email):
         for socio in self.socios:
            if socio.codigo_socio == str(codigo_socio):
                raise BibliotecaError(f"Ya existe un socio con código {codigo_socio}", "CODIGO_DUPLICADO")
         nuevo = Socio(codigo_socio, nombre, email, None)
         self.socios.append(nuevo)
         self.registrar_log("ALTA_SOCIO", f"Socio '{nombre}' ({codigo_socio}) añadido")

    def volcar_a_fichero(self):
        with open(self.ruta_fichero, "w") as f:
            for socio in self.socios:
                libro = socio.libro_prestado if socio.libro_prestado else ""
                f.write(f"{socio.codigo_socio},{socio.nombre},{socio.email},{libro}\n")
       