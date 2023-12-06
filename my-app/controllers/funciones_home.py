import random
import datetime
# Para subir archivo tipo foto al servidor
from werkzeug.utils import secure_filename
import uuid  # Modulo de python para crear un string

from conexion.conexionBD import connectionBD  # Conexión a BD

import datetime
import re
import os

from os import remove  # Modulo  para remover archivo
from os import path  # Modulo para obtener la ruta o directorio


import openpyxl  # Para generar el excel
# biblioteca o modulo send_file para forzar la descarga
from flask import send_file



#PRODUCTOS
def procesar_form_producto(dataForm, foto_perfil):


    result_foto_perfil = procesar_imagen_perfil(foto_perfil)
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:

                sql = "INSERT INTO tbl_productos (nombre_producto, precio_producto, categoria_producto, foto_producto) VALUES (%s, %s, %s, %s)"

                # Creando una tupla con los valores del INSERT
                valores = (dataForm['nombre_producto'], dataForm['precio_producto'], dataForm['categoria_producto'], result_foto_perfil)
                cursor.execute(sql, valores)

                conexion_MySQLdb.commit()
                resultado_insert = cursor.rowcount
                return resultado_insert

    except Exception as e:
        return f'Se produjo un error en procesar_form_producto: {str(e)}'



# Lista de productos
def sql_lista_productosBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = (f"""
                    SELECT 
                        e.id_producto,
                        e.nombre_producto, 
                        e.precio_producto,
                        e.foto_producto,
                        CASE
                            WHEN e.categoria_producto = 1 THEN 'Bebida'
                            WHEN e.categoria_producto = 2 THEN 'Desayuno'
                            WHEN e.categoria_producto = 3 THEN 'Almuerzo'
                            WHEN e.categoria_producto = 4 THEN 'Cena'
                            WHEN e.categoria_producto = 5 THEN 'Aperitivos'
                            WHEN e.categoria_producto = 6 THEN 'Dulces'
                            WHEN e.categoria_producto = 7 THEN 'Congelados'
                            WHEN e.categoria_producto = 8 THEN 'Cafe'
                            ELSE 'Otro'
                        END AS categoria_producto
                    FROM tbl_productos AS e
                    ORDER BY e.id_producto DESC
                    """)
                cursor.execute(querySQL,)
                productosBD = cursor.fetchall()
        return productosBD
    except Exception as e:
        print(
            f"Errro en la función sql_lista_productosBD: {e}")
        return None



def buscarProductoUnico(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = ("""
                        SELECT 
                            e.id_producto,
                            e.nombre_producto, 
                            e.precio_producto,
                            e.categoria_producto,
                            e.foto_producto
                        FROM tbl_productos AS e
                        WHERE e.id_producto =%s LIMIT 1
                    """)
                mycursor.execute(querySQL, (id,))
                producto = mycursor.fetchone()
                return producto

    except Exception as e:
        print(f"Ocurrió un error en def buscarProductoUnico: {e}")
        return []


def procesar_actualizacion_formProducto(data):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                nombre_producto = data.form['nombre_producto']
                precio_producto = data.form['precio_producto']
                categoria_producto = data.form['categoria_producto']
                id_producto = data.form['id_producto']

                print("hhhhhh")
                if data.files['foto_producto']:
                    file = data.files['foto_producto']
                    fotoForm = procesar_imagen_perfil(file)

                    querySQL = """
                        UPDATE tbl_productos
                        SET 
                            nombre_producto = %s,
                            precio_producto = %s,
                            categoria_producto = %s,
                            foto_producto = %s
                        WHERE id_producto = %s
                    """
                    values = (nombre_producto, precio_producto, categoria_producto, fotoForm, id_producto)
                else:
                    querySQL = """
                        UPDATE tbl_productos
                        SET 
                            nombre_producto = %s,
                            precio_producto = %s,
                            categoria_producto = %s
                        WHERE id_producto = %s
                    """
                    values = (nombre_producto, precio_producto, categoria_producto, id_producto)

                cursor.execute(querySQL, values)
                conexion_MySQLdb.commit()

        return cursor.rowcount or []
    except Exception as e:
        print(f"Ocurrió un error en procesar_actualizacion_formProducto: {e}")
        return None




def eliminarProducto(id_producto, foto_producto):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "DELETE FROM tbl_productos WHERE id_producto=%s"
                cursor.execute(querySQL, (id_producto,))
                conexion_MySQLdb.commit()
                resultado_eliminar = cursor.rowcount

                if resultado_eliminar:
                    # Eliminadon foto_producto desde el directorio
                    basepath = path.dirname(__file__)
                    url_File = path.join(
                        basepath, '../static/fotos_productos', foto_producto)

                    if path.exists(url_File):
                        remove(url_File)  # Borrar foto desde la carpeta

        return resultado_eliminar
    except Exception as e:
        print(f"Error en eliminarProducto : {e}")
        return []


def buscarProductoBD(search):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = ("""
                        SELECT 
                            e.id_producto,
                        e.nombre_producto, 
                        e.precio_producto,
                        e.foto_producto,
                        CASE
                            WHEN e.categoria_producto = 1 THEN 'Bebida'
                            WHEN e.categoria_producto = 2 THEN 'Desayuno'
                            WHEN e.categoria_producto = 3 THEN 'Almuerzo'
                            WHEN e.categoria_producto = 4 THEN 'Cena'
                            WHEN e.categoria_producto = 5 THEN 'Aperitivos'
                            WHEN e.categoria_producto = 6 THEN 'Dulces'
                            WHEN e.categoria_producto = 7 THEN 'Congelados'
                            WHEN e.categoria_producto = 8 THEN 'Cafe'
                            ELSE 'Otro'
                            END AS categoria_producto
                        FROM tbl_productos AS e
                        WHERE e.nombre_producto LIKE %s 
                        ORDER BY e.id_producto DESC
                    """)
                search_pattern = f"%{search}%"  # Agregar "%" alrededor del término de búsqueda
                mycursor.execute(querySQL, (search_pattern,))
                resultado_busqueda = mycursor.fetchall()
                return resultado_busqueda

    except Exception as e:
        print(f"Ocurrió un error en def buscarProductoBD: {e}")
        return []








def procesar_imagen_perfil(foto):
    try:
        # Nombre original del archivo
        filename = secure_filename(foto.filename)
        extension = os.path.splitext(filename)[1]

        # Creando un string de 50 caracteres
        nuevoNameFile = (uuid.uuid4().hex + uuid.uuid4().hex)[:100]
        nombreFile = nuevoNameFile + extension

        # Construir la ruta completa de subida del archivo
        basepath = os.path.abspath(os.path.dirname(__file__))
        upload_dir = os.path.join(basepath, f'../static/fotos_productos/')

        # Validar si existe la ruta y crearla si no existe
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            # Dando permiso a la carpeta
            os.chmod(upload_dir, 0o755)

        # Construir la ruta completa de subida del archivo
        upload_path = os.path.join(upload_dir, nombreFile)
        foto.save(upload_path)

        return nombreFile

    except Exception as e:
        print("Error al procesar archivo:", e)
        return []





#USUARIOS



# Lista de Usuarios creados
def lista_usuariosBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT id, name_surname, email_user, created_user, id_rol FROM users"
                cursor.execute(querySQL,)
                usuariosBD = cursor.fetchall()
        return usuariosBD
    except Exception as e:
        print(f"Error en lista_usuariosBD : {e}")
        return []


def buscarUsuarioUnico(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = ("""
                        SELECT 
                        e.id,
                        e.name_surname,
                        e.email_user,
                        e.created_user,
                        e.id_rol
                        FROM users AS e
                        WHERE e.id =%s LIMIT 1
                    """)
                mycursor.execute(querySQL, (id,))
                usuario = mycursor.fetchone()
                return usuario

    except Exception as e:
        print(f"Ocurrió un error en def buscarUsuarioUnico: {e}")
        return []


def procesar_actualizacion_formUser(data):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                name_surname = data.form['name_surname']
                id_rol = data.form['id_rol']
                id = data.form['id']

                querySQL = """
                    UPDATE users
                    SET 
                        name_surname = %s,
                        id_rol = %s
                    WHERE id = %s
                """
                values = (name_surname, id_rol, id)

                cursor.execute(querySQL, values)
                conexion_MySQLdb.commit()

        return cursor.rowcount or []
    except Exception as e:
        print(f"Ocurrió un error en procesar_actualizacion_formUser: {e}")
        return None



# Eliminar usuario
def eliminarUsuario(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "DELETE FROM users WHERE id=%s"
                cursor.execute(querySQL, (id,))
                conexion_MySQLdb.commit()
                resultado_eliminar = cursor.rowcount

        return resultado_eliminar
    except Exception as e:
        print(f"Error en eliminarUsuario : {e}")
        return []


def buscarUsuarioBD(search):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = ("""
                        SELECT 
                        e.id,
                        e.name_surname,
                        e.email_user,
                        e.id_rol,
                        e.created_user
                        FROM users AS e
                        WHERE e.name_surname LIKE %s 
                        ORDER BY e.id DESC
                    """)
                search_pattern = f"%{search}%"  # Agregar "%" alrededor del término de búsqueda
                mycursor.execute(querySQL, (search_pattern,))
                resultado_busqueda = mycursor.fetchall()
                return resultado_busqueda

    except Exception as e:
        print(f"Ocurrió un error en def buscarUsuarioBD: {e}")
        return []




















#MESAS


def procesar_form_mesa(dataForm):

    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:

                sql = "INSERT INTO tbl_mesas (nombre_mesa, cantidad_mesa, id_mesero) VALUES (%s, %s, %s)"



                valores = (dataForm['nombre_mesa'], dataForm['cantidad_mesa'],
                           dataForm['id_mesero'])
                cursor.execute(sql, valores)

                conexion_MySQLdb.commit()
                resultado_insert = cursor.rowcount
                return resultado_insert

    except Exception as e:
        return f'Se produjo un error en procesar_form_mesa: {str(e)}'


def obtener_meseros():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = (f"""
                    SELECT id, name_surname
                    FROM users
                    WHERE id_rol = 3
                    """)
                cursor.execute(querySQL,)
                meseros = cursor.fetchall()
        return meseros
    except Exception as e:
        print(f"Error en la función obtener_meseros: {e}")
        return None


# Lista de mesas
def sql_lista_mesasBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = (f"""
                    SELECT 
                        e.id_mesa,
                        e.nombre_mesa, 
                        e.cantidad_mesa,
                        e.fecha_mesa,
                        u.name_surname AS nombre_mesero,
                        CASE
                            WHEN e.disponible_mesa = 1 THEN 'Disponible'
                            ELSE 'No disponible'
                        END AS disponible_mesa
                    FROM tbl_mesas AS e
                    JOIN users AS u ON e.id_mesero = u.id
                    WHERE u.id_rol = 3
                    ORDER BY e.id_mesa DESC
                    """)
                cursor.execute(querySQL,)
                mesasBD = cursor.fetchall()
        return mesasBD
    except Exception as e:
        print(
            f"Error en la función sql_lista_mesasBD: {e}")
        return None




def buscarMesaBD(search):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = ("""
                        SELECT 
                        e.id_mesa,
                        e.nombre_mesa, 
                        e.cantidad_mesa,
                        u.name_surname AS nombre_mesero,
                        CASE
                            WHEN e.disponible_mesa = 1 THEN 'Disponible'
                            ELSE 'No disponible'
                        END AS disponible_mesa
                        FROM tbl_mesas AS e
                        JOIN users AS u ON e.id_mesero = u.id
                        WHERE e.nombre_mesa LIKE %s 
                        ORDER BY e.id_mesa DESC
                    """)
                search_pattern = f"%{search}%"  # Agregar "%" alrededor del término de búsqueda
                mycursor.execute(querySQL, (search_pattern,))
                resultado_busqueda = mycursor.fetchall()
                return resultado_busqueda

    except Exception as e:
        print(f"Ocurrió un error en def buscarMesaBD: {e}")
        return []


def buscarMesaUnico(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = ("""
                        SELECT 
                        e.id_mesa,
                        e.nombre_mesa, 
                        e.cantidad_mesa,
                        e.disponible_mesa,
                        e.id_mesero
                        FROM tbl_mesas AS e
                        WHERE e.id_mesa =%s LIMIT 1
                    """)
                mycursor.execute(querySQL, (id,))
                mesa = mycursor.fetchone()
                return mesa

    except Exception as e:
        print(f"Ocurrió un error en def buscarMesaUnico: {e}")
        return []


def procesar_actualizacion_formMesa(data):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                nombre_mesa = data.form['nombre_mesa']
                cantidad_mesa = data.form['cantidad_mesa']
                disponible_mesa = data.form['disponible_mesa']
                id_mesero = data.form['id_mesero']
                id_mesa = data.form['id_mesa']

                querySQL = """
                    UPDATE tbl_mesas
                    SET 
                        nombre_mesa = %s,
                        cantidad_mesa = %s,
                        disponible_mesa = %s,
                        id_mesero = %s
                    WHERE id_mesa = %s
                """
                values = (nombre_mesa, cantidad_mesa, disponible_mesa, id_mesero,
                          id_mesa)

                cursor.execute(querySQL, values)
                conexion_MySQLdb.commit()

        return cursor.rowcount or []
    except Exception as e:
        print(f"Ocurrió un error en procesar_actualizacion_formlibMesa: {e}")
        return None



def eliminarMesa(id_mesa):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "DELETE FROM tbl_mesas WHERE id_mesa=%s"
                cursor.execute(querySQL, (id_mesa,))
                conexion_MySQLdb.commit()
                resultado_eliminar = cursor.rowcount



        return resultado_eliminar
    except Exception as e:
        print(f"Error en eliminarMesa : {e}")
        return []


def procesar_form_reserva(dataForm, id_usuario):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Obtén todas las mesas que cumplen con las condiciones
                fecha_actual = datetime.date.today()
                print(fecha_actual)
                sql = """
                SELECT id_mesa FROM tbl_mesas
                WHERE cantidad_mesa = %s
                AND (fecha_mesa != %s OR fecha_mesa IS NULL OR fecha_mesa < %s)
                """
                valores = (dataForm['cantidad_reserva'], dataForm['fecha_reserva'], fecha_actual)
                cursor.execute(sql, valores)
                mesas_disponibles = cursor.fetchall()

                # Si no hay mesas disponibles, retorna un error
                if not mesas_disponibles:
                    return 'No hay mesas disponibles que cumplan con las condiciones especificadas.'

                # Selecciona una mesa de forma aleatoria
                mesa_seleccionada = random.choice(mesas_disponibles)

                # Inserta la reserva en la base de datos
                sql = "INSERT INTO tbl_reservas (fecha_reserva, cantidad_reserva, id_mesa, id_usuario) VALUES (%s, %s, %s, %s)"
                valores = (dataForm['fecha_reserva'], dataForm['cantidad_reserva'], mesa_seleccionada['id_mesa'], id_usuario)
                cursor.execute(sql, valores)

                # Actualiza la fecha_mesa de la mesa seleccionada
                sql = "UPDATE tbl_mesas SET fecha_mesa = %s WHERE id_mesa = %s"
                valores = (dataForm['fecha_reserva'], mesa_seleccionada['id_mesa'])
                cursor.execute(sql, valores)

                conexion_MySQLdb.commit()
                resultado_insert = cursor.rowcount
                return resultado_insert

    except Exception as e:
        return f'Se produjo un error en procesar_form_reserva: {str(e)}'

