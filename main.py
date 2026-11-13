from DAO.libroDAO import LibrosDao
from DAO.socioDAO import SociosDao
from errores.excepciones import BibliotecaError


def opcion_listar_todos(libros_dao):
    print("\nLISTADO DE TODOS LOS LIBROS")
    for libro in libros_dao.obtener_todos():
        print(libro)


def opcion_listar_disponibles(libros_dao):
    print("\nLIBROS DISPONIBLES")
    disponibles = libros_dao.obtener_disponibles()
    if not disponibles:
        print("No hay libros disponibles en este momento.")
    for libro in disponibles:
        print(libro)


def opcion_buscar_libro(libros_dao):
    termino = input("\nIntroduce término de búsqueda en el título: ")
    resultados = libros_dao.buscar_por_titulo(termino)
    if not resultados:
        print(f"No se encontraron libros que contengan '{termino}'.")
    else:
        print(f"\nResultados encontrados ({len(resultados)}):")
        for libro in resultados:
            print(libro)


def opcion_prestar_libro(libros_dao, socios_dao):
    cod_libro = input("\nCódigo del libro a prestar: ")
    cod_socio = input("Código del socio: ")
    try:
        socio = socios_dao.buscar_por_codigo(cod_socio)
        libro = libros_dao.prestar_libro(cod_libro, socio)
        print(f"Préstamo realizado: '{libro.titulo}' prestado a {socio.nombre}.")
    except BibliotecaError as e:
        print(f"Error [{e.codigo_error}]: {e.mensaje}")


def opcion_devolver_libro(libros_dao, socios_dao):
    cod_socio = input("\nCódigo del socio que devuelve el libro: ")
    try:
        socio = socios_dao.buscar_por_codigo(cod_socio)
        libro = libros_dao.devolver_libro(socio)
        print(f"Devolución realizada: '{libro.titulo}' vuelve a estar disponible.")
    except BibliotecaError as e:
        print(f"Error [{e.codigo_error}]: {e.mensaje}")


def opcion_socios_con_libros(libros_dao, socios_dao):
    print("\nSOCIOS CON LIBROS PRESTADOS")
    socios_activos = socios_dao.obtener_socios_con_libro()
    if not socios_activos:
        print("Ningún socio tiene libros prestados actualmente.")
        return

    for socio in socios_activos:
        try:
            libro = libros_dao.buscar_por_codigo(socio.libro_prestado)
            print(f"Socio [{socio.codigo_socio}] {socio.nombre} -> Tiene: [{libro.codigo}] {libro.titulo}")
        except BibliotecaError as e:
            print(f"Error [{e.codigo_error}]: {e.mensaje}")


def opcion_anadir(libros_dao, socios_dao):
    print("\n1. Añadir nuevo socio")
    print("2. Añadir nuevo libro")
    sub = input("Elige una opción: ")
    try:
        if sub == "1":
            cod = input("Código del nuevo socio: ")
            nombre = input("Nombre completo: ")
            email = input("Email: ")
            socios_dao.anadir_socio(cod, nombre, email)
            print("Socio añadido correctamente.")
        elif sub == "2":
            cod = input("Código del nuevo libro: ")
            titulo = input("Título: ")
            autor = input("Autor: ")
            anio = int(input("Año de publicación: "))
            cat = input("Categoría: ")
            libros_dao.anadir_libro(cod, titulo, autor, anio, cat)
            print("Libro añadido correctamente.")
        else:
            print("Opción no válida.")
    except BibliotecaError as e:
        print(f"Error [{e.codigo_error}]: {e.mensaje}")
    except ValueError:
        print("Error de formato: El año debe ser un número entero.")


def main():
    try:
        libros_dao = LibrosDao()
        socios_dao = SociosDao()
        print(f"Carga inicial completada: {len(libros_dao.obtener_todos())} libros y {len(socios_dao.obtener_todos())} socios cargados.")
    except BibliotecaError as e:
        print(f"Error crítico al iniciar [{e.codigo_error}]: {e.mensaje}")
        return

    opcion = ""
    while opcion != "8":
        print("\nGESTIÓN DE BIBLIOTECA")
        print("1. Mostrar todos los libros")
        print("2. Mostrar libros disponibles")
        print("3. Buscar libro por título")
        print("4. Prestar libro a un socio")
        print("5. Devolver libro de un socio")
        print("6. Mostrar socios con libros prestados")
        print("7. Añadir socios y libros")
        print("8. Acabar y guardar cambios")
        opcion = input("Selecciona una opción (1-8): ")

        if opcion == "1":
            opcion_listar_todos(libros_dao)
        elif opcion == "2":
            opcion_listar_disponibles(libros_dao)
        elif opcion == "3":
            opcion_buscar_libro(libros_dao)
        elif opcion == "4":
            opcion_prestar_libro(libros_dao, socios_dao)
        elif opcion == "5":
            opcion_devolver_libro(libros_dao, socios_dao)
        elif opcion == "6":
            opcion_socios_con_libros(libros_dao, socios_dao)
        elif opcion == "7":
            opcion_anadir(libros_dao, socios_dao)
        elif opcion == "8":
            libros_dao.volcar_a_fichero()
            socios_dao.volcar_a_fichero()
            print("Datos volcados a los archivos correctamente. ¡Hasta pronto!")
        else:
            print("Opción incorrecta. Introduce un número del 1 al 8.")


if __name__ == "__main__":
    main()