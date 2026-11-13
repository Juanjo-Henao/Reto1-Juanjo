class Libro:
    def __init__(self, codigo, titulo, autor, anio, categoria, codigo_socio=None):
        self.codigo = str(codigo).strip()
        self.titulo = str(titulo).strip()
        self.autor = str(autor).strip()
        self.anio = int(anio)
        self.categoria = str(categoria).strip()

        valor_socio = str(codigo_socio).strip() if codigo_socio is not None else ""
        if valor_socio == "" or valor_socio.lower() == "none":
            self.codigo_socio = None
        else:
            self.codigo_socio = valor_socio

    def esta_disponible(self):
        return self.codigo_socio is None

    def __str__(self):
        estado = "Disponible" if self.esta_disponible() else f"Prestado (Socio: {self.codigo_socio})"
        return f"[{self.codigo}] {self.titulo} - {self.autor} ({self.anio}) | {estado}"