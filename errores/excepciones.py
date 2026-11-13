class BibliotecaError(Exception):
    """Excepción personalizada para gestionar los errores de negocio de la biblioteca."""

    def __init__(self, mensaje, codigo_error):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo_error = codigo_error

    def __str__(self):
        return f"[{self.codigo_error}] {self.mensaje}"