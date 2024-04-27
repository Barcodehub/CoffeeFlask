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









#Listar de edicion namica - Nosotros
def sql_lista_nosotrosBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = (f"""
                    SELECT 
                        e.id_edicion,
                        e.nosotros_titulo,
                        e.nosotros_parrafo,
                        e.nosotros_imagen
                    FROM edicion_dinamica AS e
                    WHERE e.id_edicion = 1
                    ORDER BY e.id_edicion DESC
                    """)
                cursor.execute(querySQL,)
                nosotrosBD = cursor.fetchall()
        return nosotrosBD
    except Exception as e:
        print(
            f"Errro en la función sql_lista_nosotrosBD: {e}")
        return None





def procesar_imagen_edit(foto):
    try:
        # Nombre original del archivo
        filename = secure_filename(foto.filename)
        extension = os.path.splitext(filename)[1]

        # Creando un string de 50 caracteres
        nuevoNameFile = (uuid.uuid4().hex + uuid.uuid4().hex)[:100]
        nombreFile = nuevoNameFile + extension

        # Construir la ruta completa de subida del archivo
        basepath = os.path.abspath(os.path.dirname(__file__))
        upload_dir = os.path.join(basepath, f'../static/foto_edits/')

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








def buscarNosotroUnico(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = ("""
                        SELECT 
                        e.id_edicion,
                        e.nosotros_titulo,
                        e.nosotros_parrafo,
                        e.nosotros_imagen
                        FROM edicion_dinamica AS e
                        WHERE e.id_edicion =%s LIMIT 1
                    """)
                mycursor.execute(querySQL, (id,))
                nosotro = mycursor.fetchone()
                return nosotro

    except Exception as e:
        print(f"Ocurrió un error en def buscarNosotroUnico: {e}")
        return []

def procesar_actualizacion_formNosotro(data):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                nosotros_titulo = data.form['nosotros_titulo']
                nosotros_parrafo = data.form['nosotros_parrafo']
                id_edicion = data.form['id_edicion']

                if data.files['nosotros_imagen']:
                    file = data.files['nosotros_imagen']
                    fotoForm = procesar_imagen_edit(file)

                    querySQL = """
                        UPDATE edicion_dinamica
                        SET 
                            nosotros_titulo = %s,
                            nosotros_parrafo = %s,
                            nosotros_imagen = %s
                        WHERE id_edicion = %s
                    """
                    values = (nosotros_titulo, nosotros_parrafo, fotoForm, id_edicion)
                else:
                    querySQL = """
                        UPDATE edicion_dinamica
                        SET 
                            nosotros_titulo = %s,
                            nosotros_parrafo = %s
                        WHERE id_edicion = %s
                    """
                    values = (nosotros_titulo, nosotros_parrafo, id_edicion)

                cursor.execute(querySQL, values)
                conexion_MySQLdb.commit()

        return cursor.rowcount or []
    except Exception as e:
        print(f"Ocurrió un error en procesar_actualizacion_formNosotro: {e}")
        return None
































    #edicion Dinamica NUESTRA HISTORIA
def sql_lista_historiaBD():
        try:
            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                    querySQL = (f"""
                        SELECT 
                            e.id_edicion,
                            e.nosotros_titulo,
                            e.nosotros_parrafo,
                            e.nosotros_imagen
                        FROM edicion_dinamica AS e
                        WHERE e.id_edicion = 2
                        ORDER BY e.id_edicion DESC
                        """)
                    cursor.execute(querySQL, )
                    nosotrosBD = cursor.fetchall()
            return nosotrosBD
        except Exception as e:
            print(
                f"Errro en la función sql_lista_historiaBD: {e}")
            return None


def sql_lista_titulosBD():
    try:

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = (f"""
                        SELECT 
                            e.id_titulo,
                            e.titulo1,
                            e.titulo2,
                            e.titulo3,
                            e.titulo4,
                            e.titulo5,
                            e.titulo6,
                            e.titulo7,
                            e.titulo8,
                            e.subtitulo1,
                            e.subtitulo2,
                            e.subtitulo3,
                            e.subtitulo4,
                            e.subtitulo5,
                            e.subtitulo6,
                            e.subtitulo7,
                            e.subtitulo8,
                            e.subtitulo9,
                            e.subtitulo10,
                            e.subtitulo11,
                            e.subtitulo12,
                            e.subtitulo13,
                            e.subtitulo14,
                            e.subtitulo15,
                            e.subtitulo16
                        FROM edicion_titulo AS e
                        ORDER BY e.id_titulo DESC
                        """)
                cursor.execute(querySQL, )
                titulosBD = cursor.fetchall()
        return titulosBD
    except Exception as e:
        print(
            f"Errro en la función sql_lista_titulosBD: {e}")
        return None




def sql_lista_parrafosBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = (f"""
                        SELECT 
                            e.id_parrafo,
                            e.parrafo1,
                            e.parrafo2,
                            e.parrafo3,
                            e.parrafo4,
                            e.parrafo5,
                            e.parrafo6,
                            e.parrafo7,
                            e.parrafo8,
                            e.parrafo9,
                            e.parrafo10,
                            e.parrafo11,
                            e.parrafo12,
                            e.parrafo13,
                            e.parrafo14,
                            e.parrafo15,
                            e.parrafo16,
                            e.parrafo17
                        FROM edicion_parrafo AS e
                        ORDER BY e.id_parrafo DESC
                        """)
                cursor.execute(querySQL, )
                parrafosBD = cursor.fetchall()
        return parrafosBD
    except Exception as e:
        print(
            f"Errro en la función sql_lista_parrafosBD: {e}")
        return None


def sql_lista_imagenesBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = (f"""
                        SELECT 
                            e.id_imagen,
                            e.imagen1,
                            e.imagen2,
                            e.imagen3,
                            e.imagen4,
                            e.imagen5,
                            e.imagen6
                        FROM edicion_imagen AS e
                        WHERE e.id_imagen = 1
                        ORDER BY e.id_imagen DESC
                        """)
                cursor.execute(querySQL, )
                imagenesBD = cursor.fetchall()
        return imagenesBD
    except Exception as e:
        print(
            f"Errro en la función sql_lista_imagenesBD: {e}")
        return None









#WHERE e.id_edicion = 1 ; tener en cuenta y buscar como NO repetir codigo aqui, sino enviar el id de alguna forma dinamicamente

















def buscarHistoriaUnico(id, tabla):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                if tabla == 'edicion_imagen':
                    querySQL = (f"""
                        SELECT 
                        e.id_imagen,
                        e.imagen1,
                        e.imagen2,
                        e.imagen3,
                        e.imagen4,
                        e.imagen5,
                        e.imagen6
                        FROM {tabla} AS e
                        WHERE e.id_imagen =%s LIMIT 1
                    """)
                elif tabla == 'edicion_parrafo':
                    querySQL = (f"""
                        SELECT 
                         e.id_parrafo,
                            e.parrafo1,
                            e.parrafo2,
                            e.parrafo3,
                            e.parrafo4,
                            e.parrafo5,
                            e.parrafo6,
                            e.parrafo7,
                            e.parrafo8,
                            e.parrafo9,
                            e.parrafo10,
                            e.parrafo11,
                            e.parrafo12,
                            e.parrafo13,
                            e.parrafo14,
                            e.parrafo15,
                            e.parrafo16,
                            e.parrafo17,
                            e.parrafon
                        FROM {tabla} AS e
                        WHERE e.id_parrafo =%s LIMIT 1
                    """)
                elif tabla == 'edicion_titulo':
                    querySQL = (f"""
                        SELECT 
                        e.id_titulo,
                            e.titulo1,
                            e.titulo2,
                            e.titulo3,
                            e.titulo4,
                            e.titulo5,
                            e.titulo6,
                            e.titulo7,
                            e.titulo8,
                            e.subtitulo1,
                            e.subtitulo2,
                            e.subtitulo3,
                            e.subtitulo4,
                            e.subtitulo5,
                            e.subtitulo6,
                            e.subtitulo7,
                            e.subtitulo8,
                            e.subtitulo9,
                            e.subtitulo10,
                            e.subtitulo11,
                            e.subtitulo12,
                            e.subtitulo13,
                            e.subtitulo14,
                            e.subtitulo15,
                            e.subtitulo16
                        FROM {tabla} AS e
                        WHERE e.id_titulo =%s LIMIT 1
                    """)
                mycursor.execute(querySQL, (id,))
                historia = mycursor.fetchone()
                return historia

    except Exception as e:
        print(f"Ocurrió un error en def buscarHistoriaUnico: {e}")
        return []






def procesar_actualizacion_formHistoria(data, tabla):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                if tabla == 'edicion_imagen':
                    id_imagen = data.form['id_imagen']
                    imagen1 = data.form['imagen1']
                    imagen2 = data.form['imagen2']
                    # ... y así sucesivamente para todas las imágenes
                    querySQL = """
                        UPDATE edicion_imagen
                        SET 
                            imagen1 = %s,
                            imagen2 = %s
                            # ... y así sucesivamente para todas las imágenes
                        WHERE id_imagen = %s
                    """
                    values = (imagen1, imagen2, id_imagen)
                elif tabla == 'edicion_parrafo':
                    id_parrafo = data.form['id_parrafo']
                    parrafo1 = data.form['parrafo1']
                    parrafo2 = data.form['parrafo2']
                    # ... y así sucesivamente para todos los párrafos
                    querySQL = """
                        UPDATE edicion_parrafo
                        SET 
                            parrafo1 = %s,
                            parrafo2 = %s
                            # ... y así sucesivamente para todos los párrafos
                        WHERE id_parrafo = %s
                    """
                    values = (parrafo1, parrafo2, id_parrafo)
                elif tabla == 'edicion_titulo':
                    id_titulo = data.form['id_titulo']
                    titulo1 = data.form['titulo1']
                    titulo2 = data.form['titulo2']
                    # ... y así sucesivamente para todos los títulos
                    querySQL = """
                        UPDATE edicion_titulo
                        SET 
                            titulo1 = %s,
                            titulo2 = %s
                            # ... y así sucesivamente para todos los títulos
                        WHERE id_titulo = %s
                    """
                    values = (titulo1, titulo2, id_titulo)

                cursor.execute(querySQL, values)
                conexion_MySQLdb.commit()

        return cursor.rowcount or []
    except Exception as e:
        print(f"Ocurrió un error en procesar_actualizacion_formHistoria: {e}")
        return None


