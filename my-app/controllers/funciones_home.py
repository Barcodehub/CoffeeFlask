import json
import random
import datetime

import mysql
# Para subir archivo tipo foto al servidor
from werkzeug.utils import secure_filename
import uuid  # Modulo de python para crear un string

from conexion.conexionBD import connectionBD  # Conexión a BD

import datetime
import re
import os
#import stripe
from os import remove  # Modulo  para remover archivo
from os import path  # Modulo para obtener la ruta o directorio
from datetime import datetime

import openpyxl  # Para generar el excel
# biblioteca o modulo send_file para forzar la descarga
from flask import send_file, session
from routers.router_login import *
from controllers.funciones_logs import *

#PRODUCTOS
def procesar_form_producto(dataForm, foto_perfil):
    result_foto_perfil = procesar_imagen_perfil(foto_perfil)
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = "INSERT INTO tbl_productos (nombre_producto, precio_producto, categoria_producto, foto_producto) VALUES (%s, %s, %s, %s)"
                valores = (dataForm['nombre_producto'], dataForm['precio_producto'], dataForm['categoria_producto'],
                           result_foto_perfil)
                cursor.execute(sql, valores)
                producto_id = cursor.lastrowid
                conexion_MySQLdb.commit()

                # Registrar el cambio en log_cambios
                datos_nuevos = {
                    'id_producto': producto_id,
                    'nombre_producto': dataForm['nombre_producto'],
                    'precio_producto': dataForm['precio_producto'],
                    'categoria_producto': dataForm['categoria_producto'],
                    'foto_producto': result_foto_perfil
                }
                log_cambio = {
                    'tabla': 'tbl_productos',
                    'accion': 'inserción',
                    'datos_anteriores': None,
                    'datos_nuevos': json.dumps(datos_nuevos),
                    'usuario_id': session['usuario_id']  # Asegúrate de pasar el ID del usuario que realiza el cambio
                }
                insertar_log_cambio(log_cambio)

                return cursor.rowcount
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
                            e.cantidad,
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
                usuario_id = session['usuario_id']  # Asegúrate de pasar el ID del usuario que realiza el cambio

                # Obtener los datos anteriores del producto
                cursor.execute("SELECT * FROM tbl_productos WHERE id_producto = %s", (id_producto,))
                datos_anteriores = cursor.fetchone()

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

                # Registrar el cambio en log_cambios
                datos_nuevos = {
                    'id_producto': id_producto,
                    'nombre_producto': nombre_producto,
                    'precio_producto': precio_producto,
                    'categoria_producto': categoria_producto,
                    'foto_producto': fotoForm if data.files['foto_producto'] else datos_anteriores['foto_producto']
                }
                log_cambio = {
                    'tabla': 'tbl_productos',
                    'accion': 'actualización',
                    'datos_anteriores': json.dumps(datos_anteriores),
                    'datos_nuevos': json.dumps(datos_nuevos),
                    'usuario_id': session['usuario_id']
                }
                insertar_log_cambio(log_cambio)

        return cursor.rowcount or []
    except Exception as e:
        print(f"Ocurrió un error en procesar_actualizacion_formProducto: {e}")
        return None




def eliminarProducto(id_producto, foto_producto):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Obtener los datos anteriores del producto
                cursor.execute("SELECT * FROM tbl_productos WHERE id_producto = %s", (id_producto,))
                datos_anteriores = cursor.fetchone()

                querySQL = "DELETE FROM tbl_productos WHERE id_producto=%s"
                cursor.execute(querySQL, (id_producto,))
                conexion_MySQLdb.commit()
                resultado_eliminar = cursor.rowcount

                if resultado_eliminar:
                    # Eliminando foto_producto desde el directorio
                    basepath = path.dirname(__file__)
                    url_File = path.join(
                        basepath, '../static/fotos_productos', foto_producto)

                    if path.exists(url_File):
                        remove(url_File)  # Borrar foto desde la carpeta

                    # Registrar el cambio en log_cambios
                    log_cambio = {
                        'tabla': 'tbl_productos',
                        'accion': 'eliminación',
                        'datos_anteriores': json.dumps(datos_anteriores),
                        'datos_nuevos': None,
                        'usuario_id': session['usuario_id']
                    }
                    insertar_log_cambio(log_cambio)

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

                # Obtener los datos anteriores del usuario
                cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
                datos_anteriores = cursor.fetchone()

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

                datos_anteriores_sin_password = {
                    key: value for key, value in datos_anteriores.items() if key != 'pass_user'
                }

                # Convertir objetos datetime a cadena antes de serializar a JSON
                datos_anteriores_json = {
                    key: value.strftime('%Y-%m-%d %H:%M:%S') if isinstance(value, datetime) else value
                    for key, value in datos_anteriores_sin_password.items()
                }
                datos_nuevos = {
                    'name_surname': name_surname,
                    'id_rol': id_rol
                }
                log_cambio = {
                    'tabla': 'users',
                    'accion': 'actualización',
                    'datos_anteriores': json.dumps(datos_anteriores_json),
                    'datos_nuevos': json.dumps(datos_nuevos),
                    'usuario_id': session['usuario_id']
                }
                insertar_log_cambio(log_cambio)

        return cursor.rowcount or []
    except Exception as e:
        print(f"Ocurrió un error en procesar_actualizacion_formUser: {e}")
        return None



# Eliminar usuario
def eliminarUsuario(id):
    try:
        print("Iniciando proceso de eliminación de usuario...")
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Obtener los datos anteriores del usuario
                cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
                datos_anteriores = cursor.fetchone()

                querySQL = "DELETE FROM users WHERE id=%s"
                cursor.execute(querySQL, (id,))
                conexion_MySQLdb.commit()
                resultado_eliminar = cursor.rowcount

                if resultado_eliminar:
                    datos_anteriores_json = {
                        key: value.strftime('%Y-%m-%d %H:%M:%S') if isinstance(value, datetime) else value
                        for key, value in datos_anteriores.items()
                    }
                    # Registrar el cambio en log_cambios
                    log_cambio = {
                        'tabla': 'users',
                        'accion': 'eliminación',
                        'datos_anteriores': json.dumps(datos_anteriores_json),
                        'datos_nuevos': None,
                        'usuario_id': session['usuario_id']  # Asegúrate de pasar el ID del usuario que realiza el cambio
                    }
                    insertar_log_cambio(log_cambio)

        return resultado_eliminar
    except Exception as e:
        print(f"Error en eliminarUsuario: {e}")
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
                mesa_id = cursor.lastrowid
                conexion_MySQLdb.commit()
                resultado_insert = cursor.rowcount

                # Registrar el cambio en log_cambios
                datos_nuevos = {
                    'id_mesa': mesa_id,
                    'nombre_mesa': dataForm['nombre_mesa'],
                    'cantidad_mesa': dataForm['cantidad_mesa'],
                    'id_mesero': dataForm['id_mesero']
                }
                log_cambio = {
                    'tabla': 'tbl_mesas',
                    'accion': 'inserción',
                    'datos_anteriores': None,
                    'datos_nuevos': json.dumps(datos_nuevos),
                    'usuario_id': session['usuario_id']
                }
                insertar_log_cambio(log_cambio)

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
                        e.fecha_mesa,
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

                # Obtener los datos anteriores de la mesa
                cursor.execute("SELECT * FROM tbl_mesas WHERE id_mesa = %s", (id_mesa,))
                datos_anteriores = cursor.fetchone()

                # Obtener el nombre del mesero a partir del id_mesero
                cursor.execute("SELECT name_surname FROM users WHERE id = %s", (id_mesero,))
                mesero = cursor.fetchone()
                nombre_mesero = mesero['name_surname'] if mesero else None

                # Obtener el estado de disponibilidad de la mesa
                disponibilidad = "Disponible" if disponible_mesa == "1" else "No disponible"

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

                # Registrar el cambio en log_cambios
                datos_nuevos = {
                    'id_mesa': id_mesa,
                    'nombre_mesa': nombre_mesa,
                    'cantidad_mesa': cantidad_mesa,
                    'disponible_mesa': disponibilidad,
                    'id_mesero': nombre_mesero
                }
                log_cambio = {
                    'tabla': 'tbl_mesas',
                    'accion': 'actualización',
                    'datos_anteriores': json.dumps(datos_anteriores),
                    'datos_nuevos': json.dumps(datos_nuevos),
                    'usuario_id': session['usuario_id']
                }
                insertar_log_cambio(log_cambio)

        return cursor.rowcount or []
    except Exception as e:
        print(f"Ocurrió un error en procesar_actualizacion_formMesa: {e}")
        return None



def eliminarMesa(id_mesa):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Obtener los datos anteriores de la mesa
                cursor.execute("SELECT * FROM tbl_mesas WHERE id_mesa = %s", (id_mesa,))
                datos_anteriores = cursor.fetchone()

                querySQL = "DELETE FROM tbl_mesas WHERE id_mesa=%s"
                cursor.execute(querySQL, (id_mesa,))
                conexion_MySQLdb.commit()
                resultado_eliminar = cursor.rowcount

                if resultado_eliminar:
                    # Registrar el cambio en log_cambios
                    log_cambio = {
                        'tabla': 'tbl_mesas',
                        'accion': 'eliminación',
                        'datos_anteriores': json.dumps(datos_anteriores),
                        'datos_nuevos': None,
                        'usuario_id': session['usuario_id']
                    }
                    insertar_log_cambio(log_cambio)

        return resultado_eliminar
    except Exception as e:
        print(f"Error en eliminarMesa : {e}")
        return []






def sql_lista_reservasBD():
    try:
        print("Iniciando conexión con la base de datos...")
        with connectionBD() as conexion_MySQLdb:
            print("Conexión establecida.")
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = ("""
                    SELECT
                        e.fecha_reserva,
                        e.cantidad_reserva,
                        u.name_surname AS nombre_usuario,
                        u.email_user AS emailuser
                    FROM tbl_reservas AS e
                    JOIN users AS u ON e.id_usuario = u.id
                    ORDER BY e.id_reserva DESC;

                    """)
                print(f"Ejecutando query: {querySQL}")
                cursor.execute(querySQL)
                reservasBD = cursor.fetchall()
                print(f"Resultados obtenidos: {reservasBD}")
        print("Cerrando conexión con la base de datos.")
        return reservasBD
    except Exception as e:
        print(f"Error en la función sql_lista_reservasBD: {e}")
        return None



def procesar_form_reserva(dataForm, id_usuario):
    try:
        print("Iniciando proceso de reserva...")
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Obtén la fecha actual
                fecha_actual = datetime.now().date()
                print(f"Fecha actual: {fecha_actual}")

                # Obtener el id_mesa del formulario
                id_mesa = dataForm['id_mesa']

                # Consulta para verificar si la mesa está disponible
                sql = """
                SELECT id_mesa FROM tbl_mesas
                WHERE id_mesa = %s
                AND (fecha_mesa != %s OR fecha_mesa IS NULL OR fecha_mesa < %s)
                """
                valores = (id_mesa, dataForm['fecha_reserva'], fecha_actual)
                print(f"Ejecutando consulta para verificar disponibilidad de mesa: {sql}")
                print(f"Valores: {valores}")
                cursor.execute(sql, valores)
                mesa_disponible = cursor.fetchone()

                # Si la mesa no está disponible, retorna un error
                if not mesa_disponible:
                    print("La mesa seleccionada no está disponible.")
                    return 'La mesa seleccionada no está disponible.'

                # Inserta la reserva en la base de datos
                sql = "INSERT INTO tbl_reservas (fecha_reserva, cantidad_reserva, id_mesa, id_usuario) VALUES (%s, %s, %s, %s)"
                valores = (
                dataForm['fecha_reserva'], dataForm['cantidad_reserva'], id_mesa, id_usuario)
                print(f"Ejecutando consulta para insertar reserva: {sql}")
                print(f"Valores: {valores}")
                cursor.execute(sql, valores)

                # Actualiza la fecha_mesa de la mesa seleccionada
                sql = "UPDATE tbl_mesas SET fecha_mesa = %s WHERE id_mesa = %s"
                valores = (dataForm['fecha_reserva'], id_mesa)
                print(f"Ejecutando consulta para actualizar fecha_mesa: {sql}")
                print(f"Valores: {valores}")
                cursor.execute(sql, valores)

                conexion_MySQLdb.commit()
                resultado_insert = cursor.rowcount
                print(f"Resultado de la inserción: {resultado_insert}")
                return resultado_insert

    except Exception as e:
        print(f"Se produjo un error en procesar_form_reserva: {str(e)}")
        return f'Se produjo un error en procesar_form_reserva: {str(e)}'


#carrito
def obtener_carrito_usuario(usuario_id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                query = "SELECT id FROM carritos WHERE usuario_id = %s"
                cursor.execute(query, (usuario_id,))
                carrito = cursor.fetchone()
                return carrito
    except Exception as e:
        print(f"Error al obtener el carrito del usuario: {e}")
        return None

def crear_carrito_usuario(usuario_id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                query = "INSERT INTO carritos (usuario_id) VALUES (%s)"
                cursor.execute(query, (usuario_id,))
                carrito_id = cursor.lastrowid
                conexion_MySQLdb.commit()
                return carrito_id
    except Exception as e:
        print(f"Error al crear el carrito del usuario: {e}")
        return None

def agregar_producto_carrito(carrito_id, id_producto, cantidad):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                # Verificar si el producto ya está en el carrito
                query = "SELECT id, cantidad FROM carrito_productos WHERE carrito_id = %s AND producto_id = %s"
                cursor.execute(query, (carrito_id, id_producto))
                producto_carrito = cursor.fetchone()

                if producto_carrito:
                    # Si el producto ya está en el carrito, actualizar la cantidad
                    nueva_cantidad = producto_carrito['cantidad'] + cantidad
                    query = "UPDATE carrito_productos SET cantidad = %s WHERE id = %s"
                    cursor.execute(query, (nueva_cantidad, producto_carrito['id']))
                else:
                    # Si el producto no está en el carrito, insertarlo
                    query = "INSERT INTO carrito_productos (carrito_id, producto_id, cantidad) VALUES (%s, %s, %s)"
                    cursor.execute(query, (carrito_id, id_producto, cantidad))

                conexion_MySQLdb.commit()
    except Exception as e:
        print(f"Error al agregar el producto al carrito: {e}")







def obtener_productos_carrito(usuario_id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                query = """
                    SELECT p.id_producto, p.nombre_producto, p.precio_producto, cp.cantidad
                    FROM carritos c
                    JOIN carrito_productos cp ON c.id = cp.carrito_id
                    JOIN tbl_productos p ON cp.producto_id = p.id_producto
                    WHERE c.usuario_id = %s
                """
                cursor.execute(query, (usuario_id,))
                productos_carrito = cursor.fetchall()
                return productos_carrito
    except Exception as e:
        print(f"Error al obtener los productos del carrito: {e}")
        return []

def calcular_total_carrito(productos_carrito):
    total = 0
    for producto in productos_carrito:
        total += producto['precio_producto'] * producto['cantidad']
    return total

def actualizar_cantidad_producto(usuario_id, id_producto, cantidad):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                query = """
                    UPDATE carrito_productos cp
                    JOIN carritos c ON cp.carrito_id = c.id
                    SET cp.cantidad = %s
                    WHERE c.usuario_id = %s AND cp.producto_id = %s
                """
                cursor.execute(query, (cantidad, usuario_id, id_producto))
            conexion_MySQLdb.commit()
    except Exception as e:
        print(f"Error al actualizar la cantidad del producto: {e}")

def eliminar_producto_carrito(usuario_id, id_producto):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                query = """
                    DELETE cp
                    FROM carrito_productos cp
                    JOIN carritos c ON cp.carrito_id = c.id
                    WHERE c.usuario_id = %s AND cp.producto_id = %s
                """
                cursor.execute(query, (usuario_id, id_producto))
            conexion_MySQLdb.commit()
    except Exception as e:
        print(f"Error al eliminar el producto del carrito: {e}")












#PAGO
def generar_orden_compra(usuario_id, productos_carrito, total_carrito):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                # Insertar la orden de compra en la tabla de órdenes
                query = "INSERT INTO ordenes (usuario_id, total) VALUES (%s, %s)"
                cursor.execute(query, (usuario_id, total_carrito))
                orden_id = cursor.lastrowid

                # Insertar los productos de la orden en la tabla de detalles de la orden
                for producto in productos_carrito:
                    query = "INSERT INTO ordenes_detalles (orden_id, producto_id, cantidad, precio) VALUES (%s, %s, %s, %s)"
                    cursor.execute(query, (orden_id, producto['id_producto'], producto['cantidad'], producto['precio_producto']))

                conexion_MySQLdb.commit()
                return orden_id
    except Exception as e:
        print(f"Error al generar la orden de compra: {e}")
        return None

def vaciar_carrito(usuario_id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                query = "DELETE FROM carrito_productos WHERE carrito_id = (SELECT id FROM carritos WHERE usuario_id = %s)"
                cursor.execute(query, (usuario_id,))
                conexion_MySQLdb.commit()
    except Exception as e:
        print(f"Error al vaciar el carrito: {e}")












#FACTURA
def insertar_factura(factura):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                # Obtener el nombre de usuario de la tabla usuarios
                query_usuario = "SELECT name_surname FROM users WHERE id = %s"
                cursor.execute(query_usuario, (factura['usuario_id'],))
                usuario_nombre = cursor.fetchone()[0]

                # Insertar la factura con el nombre de usuario
                query = "INSERT INTO facturas (usuario_id, usuario_nombre, total) VALUES (%s, %s, %s)"
                valores = (factura['usuario_id'], usuario_nombre, factura['total'])
                cursor.execute(query, valores)
                factura_id = cursor.lastrowid
            conexion_MySQLdb.commit()
        return factura_id
    except Exception as e:
        print(f"Error al insertar la factura: {e}")
        return None

def insertar_detalle_factura(detalle):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                query = "INSERT INTO factura_productos (factura_id, producto_id, cantidad, precio) VALUES (%s, %s, %s, %s)"
                valores = (detalle['factura_id'], detalle['producto_id'], detalle['cantidad'], detalle['precio'])
                cursor.execute(query, valores)
            conexion_MySQLdb.commit()
    except Exception as e:
        print(f"Error al insertar el detalle de la factura: {e}")

def obtener_factura(factura_id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                query = """
                    SELECT f.id, f.usuario_id, u.name_surname AS usuario_nombre, f.fecha, f.total
                    FROM facturas f
                    JOIN users u ON f.usuario_id = u.id
                    WHERE f.id = %s
                """
                cursor.execute(query, (factura_id,))
                factura = cursor.fetchone()
                return factura
    except Exception as e:
        print(f"Error al obtener la factura: {e}")
        return None

def obtener_productos_factura(factura_id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                query = "SELECT fp.cantidad, p.nombre_producto, p.precio_producto FROM factura_productos fp JOIN tbl_productos p ON fp.producto_id = p.id_producto WHERE fp.factura_id = %s"
                cursor.execute(query, (factura_id,))
                productos_factura = cursor.fetchall()
                return productos_factura
    except Exception as e:
        print(f"Error al obtener los productos de la factura: {e}")
        return None




# Lista de facturas
def sql_lista_facturasBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = (f"""
                    SELECT 
                        e.id,
                        e.usuario_id,
                        e.usuario_nombre, 
                        e.fecha,
                        e.total
                    FROM facturas AS e
                    ORDER BY e.id DESC
                    """)
                cursor.execute(querySQL,)
                facturasBD = cursor.fetchall()
        return facturasBD
    except Exception as e:
        print(
            f"Error en la función sql_lista_facturasBD: {e}")
        return None




def buscarFacturaBD(search):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = ("""
                        SELECT 
                        e.id,
                        e.usuario_id, 
                        e.usuario_nombre,
                        e.fecha,
                        e.total
                    FROM facturas AS e
                    WHERE e.usuario_nombre LIKE %s 
                    ORDER BY e.id DESC
                    """)
                search_pattern = f"%{search}%"  # Agregar "%" alrededor del término de búsqueda
                mycursor.execute(querySQL, (search_pattern,))
                resultado_busqueda = mycursor.fetchall()
                return resultado_busqueda

    except Exception as e:
        print(f"Ocurrió un error en def buscarFacturaBD: {e}")
        return []


def eliminarFactura(id):
    try:
        print("Iniciando eliminación de factura...")
        with connectionBD() as conexion_MySQLdb:
            print("Conexión a la base de datos establecida.")
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                print(f"Obteniendo datos anteriores de la factura con id {id}...")
                cursor.execute("SELECT * FROM facturas WHERE id = %s", (id,))
                datos_anteriores = cursor.fetchone()
                print("Datos anteriores obtenidos:", datos_anteriores)

                querySQL = "DELETE FROM facturas WHERE id=%s"
                print("Ejecutando SQL para eliminación:", querySQL)
                cursor.execute(querySQL, (id,))
                conexion_MySQLdb.commit()
                resultado_eliminar = cursor.rowcount
                print("Resultado de eliminación:", resultado_eliminar)

                if resultado_eliminar:
                    print("Registrando log de cambio por eliminación...")
                    # Convertir objetos datetime a cadena antes de serializar a JSON
                    datos_anteriores_json = {
                        key: value.strftime('%Y-%m-%d %H:%M:%S') if isinstance(value, datetime) else value
                        for key, value in datos_anteriores.items()
                    }
                    log_cambio = {
                        'tabla': 'facturas',
                        'accion': 'eliminación',
                        'datos_anteriores': json.dumps(datos_anteriores),
                        'datos_nuevos': None,
                        'usuario_id': session['usuario_id']  # Asegúrate de que 'session' esté disponible y tenga 'usuario_id'
                    }
                    print("Datos del log de cambio:", log_cambio)
                    insertar_log_cambio(log_cambio)

        return resultado_eliminar
    except Exception as e:
        print(f"Error en eliminarFactura: {e}")
        return []




def sql_facturas_reporte(fecha_inicio=None, fecha_fin=None):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = (f"""
                    SELECT 
                        e.id,
                        e.usuario_id,
                        e.usuario_nombre, 
                        e.fecha,
                        e.total
                    FROM facturas AS e
                    WHERE 1=1
                """)
                if fecha_inicio:
                    querySQL += f" AND e.fecha >= '{fecha_inicio}'"
                if fecha_fin:
                    querySQL += f" AND e.fecha <= '{fecha_fin}'"
                querySQL += " ORDER BY e.id DESC"
                cursor.execute(querySQL)
                facturasBD = cursor.fetchall()
        return facturasBD
    except Exception as e:
        print(f"Error en la función sql_facturas_reporte: {e}")
        return None