class Socio:
    def __init__(self, codigo_socio, nombre, email, libro_prestado=None):
        self.codigo_socio = codigo_socio
        self.nombre = nombre
        self.email = email
        self.libro_prestado = libro_prestado
        self.codigo_socio = codigo_socio


    def tiene_libro(self):
        return self.libro_prestado is not None

    def __str__(self):
        estado = f"Tiene libro: {self.libro_prestado}" if self.tiene_libro() else "Sin préstamos"
        return f"[{self.codigo_socio}] {self.nombre} ({self.email}) | {estado}"