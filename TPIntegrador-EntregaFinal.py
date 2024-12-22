import sqlite3
from sqlite3 import Error

def conectar_db():
    try:
        conexion = sqlite3.connect("inventario.db")
        return conexion
    except Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

def crear_tabla():
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT UNIQUE,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    cantidad INTEGER NOT NULL,
                    precio REAL NOT NULL,
                    categoria TEXT
                )
            ''')
            conexion.commit()
            print("Tabla 'productos' creada o ya existente.")
        except Error as e:
            print(f"Error al crear la tabla: {e}")
        finally:
            conexion.close()

def mostrar_menu():
    print("Menú para la carga de productos:\n")
    print("1-Registrar: Alta de nuevos productos")
    print("2-Visualizar: Consultar datos de productos")
    print("3-Actualizar: Modificar stock")
    print("4-Eliminar: Dar de baja un producto")
    print("5-Listar: Mostrar todos los productos de la base de datos")
    print("6-Reportar bajo stock: Listar los productos con stock mínimo")
    print("7-Salir")

def registrar_producto():
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()

            nombre = input("Ingrese el nombre del producto: ").strip()
            descripcion = input("Ingrese la descripción del producto: ").strip()
            while True:
                try:
                    cantidad = int(input("Ingrese la cantidad del producto: ").strip())
                    if cantidad < 0:
                        print("La cantidad debe ser un número positivo.")
                        continue
                    break
                except ValueError:
                    print("Debe ingresar un número entero para la cantidad.")

            while True:
                try:
                    precio = float(input("Ingrese el precio del producto: ").strip())
                    if precio <= 0:
                        print("El precio debe ser mayor a cero.")
                        continue
                    break
                except ValueError:
                    print("Debe ingresar un número válido para el precio.")

            categoria = input("Ingrese la categoría del producto: ").strip()

            cursor.execute('''
                INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
                VALUES (?, ?, ?, ?, ?)
            ''', (nombre, descripcion, cantidad, precio, categoria))

            conexion.commit()
            print("Producto registrado con éxito.")
        except Error as e:
            print(f"Error al registrar el producto: {e}")
        finally:
            conexion.close()

def visualizar_productos():
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM productos")
            productos = cursor.fetchall()

            if productos:
                print("\nProductos en el inventario:")
                for producto in productos:
                    print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Cantidad: {producto[3]}, Precio: ${producto[4]:.2f}, Categoría: {producto[5]}")
            else:
                print("No hay productos registrados en el inventario.")
        except Error as e:
            print(f"Error al visualizar productos: {e}")
        finally:
            conexion.close()

def actualizar_producto():
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            producto_id = input("Ingrese el ID del producto que desea actualizar: ").strip()
            while True:
                try:
                    nueva_cantidad = int(input("Ingrese la nueva cantidad: ").strip())
                    if nueva_cantidad < 0:
                        print("La cantidad debe ser un número positivo.")
                        continue
                    break
                except ValueError:
                    print("Debe ingresar un número entero.")

            cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (nueva_cantidad, producto_id))
            conexion.commit()

            if cursor.rowcount > 0:
                print("Cantidad actualizada con éxito.")
            else:
                print("No se encontró un producto con el ID especificado.")
        except Error as e:
            print(f"Error al actualizar producto: {e}")
        finally:
            conexion.close()

def eliminar_producto():
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            producto_id = input("Ingrese el ID del producto que desea eliminar: ").strip()
            cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
            conexion.commit()

            if cursor.rowcount > 0:
                print("Producto eliminado con éxito.")
            else:
                print("No se encontró un producto con el ID especificado.")
        except Error as e:
            print(f"Error al eliminar producto: {e}")
        finally:
            conexion.close()

def reportar_bajo_stock():
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            while True:
                try:
                    limite = int(input("Ingrese el límite de stock para generar el reporte: ").strip())
                    if limite < 0:
                        print("El límite debe ser un número positivo.")
                        continue
                    break
                except ValueError:
                    print("Debe ingresar un número entero.")

            cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
            productos = cursor.fetchall()

            if productos:
                print("\nProductos con bajo stock:")
                for producto in productos:
                    print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Cantidad: {producto[3]}, Precio: ${producto[4]:.2f}, Categoría: {producto[5]}")
            else:
                print("No hay productos con stock por debajo del límite especificado.")
        except Error as e:
            print(f"Error al generar el reporte: {e}")
        finally:
            conexion.close()

def listar_todos_los_productos():
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM productos")
            productos = cursor.fetchall()

            if productos:
                print("\nListado completo de productos:")
                for producto in productos:
                    print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Cantidad: {producto[3]}, Precio: ${producto[4]:.2f}, Categoría: {producto[5]}")
            else:
                print("No hay productos registrados en el inventario.")
        except Error as e:
            print(f"Error al listar productos: {e}")
        finally:
            conexion.close()

def menu_principal():
    crear_tabla()
    while True:
        print("\nMenú para la gestión de inventario:")
        print("1 - Registrar producto")
        print("2 - Visualizar productos")
        print("3 - Actualizar producto")
        print("4 - Eliminar producto")
        print("5 - Listar todos los productos")
        print("6 - Reportar bajo stock")
        print("7 - Salir")

        try:
            opcion = int(input("Seleccione una opción (1-7): ").strip())

            if opcion == 1:
                registrar_producto()
            elif opcion == 2:
                visualizar_productos()
            elif opcion == 3:
                actualizar_producto()
            elif opcion == 4:
                eliminar_producto()
            elif opcion == 5:
                listar_todos_los_productos()
            elif opcion == 6:
                reportar_bajo_stock()
            elif opcion == 7:
                print("Saliendo del programa.")
                break
            else:
                print("Opción inválida.")
        except ValueError:
            print("Por favor, ingrese un número válido entre 1 y 7.")

if __name__ == "__main__":
    menu_principal()
