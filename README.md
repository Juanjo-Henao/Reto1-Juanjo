# Sistema de Gestión de Biblioteca (Python)

Juan Jose Henao 2DAM3

# Estructura del proyecto
Reto1-Python-Juanjo/
│
├── DAO/
│   ├── libroDAO.py          # Persistencia, consultas, préstamos, devoluciones y log de libros
│   └── socioDAO.py          # Persistencia, consultas y altas de socios
│
├── datos/
│   ├── libros.txt           # Catálogo inicial y persistente de libros (100 registros)
│   ├── socios.txt           # Registro inicial y persistente de socios (15 registros)
│   └── log.txt              # Registro cronológico automático eventos realizados
│
├── errores/
│   └── excepciones.py       # Excepción personalizada BibliotecaError con código de error
│
├── modelo/
│   ├── libro.py             # Clase entidad Libro 
│   └── socio.py             # Clase entidad Socio 
│
├── main.py                  # Punto de entrada y menú interactivo por consola
└── README.md                # Documentación del proyecto


# Metodos en las clases Libro y Socio

Las clases libro y socio son independientes, es decir no heredan entre sí y usan metodos para gestionar el estado.

-esta_disponible() comprueba si un libro esta libre y tiene_libro() verifica si un socio ya tiene algun prestamo. Por otro lado, LibrosDao y SociosDao agrupan métodos que hacen funcionar el sistema(prestar_libro, devolver_libro, buscar_por_titulo, dar de alta y guardar en los ficheros.)

# Excepción personalizada (BibliotecaError)
BibliotecaError es la única clase que usa herencia (hereda de Exception) y añade un atributo propio llamado codigo_error. Cuando alguien intenta hacer algo no permitido ya sea prestar un libro ya ocupado o buscar un código que no existe, el DAO lanza este error con raise y main.py lo captura con try/except para mostrar el fallo de forma clara sin que el programa se cierre.


# Posibles mejoras que se podrían implementar

-Conexión con base de datos: Podriamos sustituir los ficheros .txt por una base de datos SQL sin alterar la logica del programa ni la interfaz.

-Préstamos multiples y fechas de vencimiento: Permitir que un socio tenga más de un libro prestado a la vez e incorporar fechas de préstamos, devoluciones estimadas y calcular alguna sanción economica en caso de retraso.

-Busquedas y filtros avanzados: Añadir búsqueda por autor, categoría, codigo o disponibilidad.

-Posible interfaz gráfica: Desarrollar algun tipo de interfaz visual para el programa.

-Pruebas automatizadas: Implementar una batería de tests para verificar automaticamente préstamos, devoluciones, persistencia y excepciones personalizadas.