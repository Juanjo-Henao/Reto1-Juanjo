class Libro:
    def __init__(self, codigo, titulo, autor, anio, categoria, codigo_socio=None):
        self.codigo = codigo
        self.titulo = titulo
        self.autor = autor
        self.anio = anio
        self.categoria = categoria
        self.codigo_socio = codigo_socio


    def esta_disponible(self):
        return self.codigo_socio is None

    def __str__(self):
        estado = "Disponible" if self.esta_disponible() else f"Prestado (Socio: {self.codigo_socio})"
        return f"[{self.codigo}] {self.titulo} - {self.autor} ({self.anio}) | {estado}"
        