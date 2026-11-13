class Socio:
    def __init__(self, codigo_socio, nombre, email, libro_prestado=None):
        self.codigo_socio = str(codigo_socio).strip()
        self.nombre = str(nombre).strip()
        self.email = str(email).strip()
        
        valor_libro = str(libro_prestado).strip() if libro_prestado is not None else ""
        if valor_libro == "" or valor_libro.lower() == "none":
            self.libro_prestado = None
        else:
            self.libro_prestado = valor_libro

    def tiene_libro(self):
        return self.libro_prestado is not None and str(self.libro_prestado).strip().lower() != "none"

    def __str__(self):
        estado = f"Tiene libro: {self.libro_prestado}" if self.tiene_libro() else "Sin préstamos"
        return f"[{self.codigo_socio}] {self.nombre} ({self.email}) | {estado}"