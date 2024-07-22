# Importandopaquetes desde flask
from flask import session, flash

# Importando conexion a BD
from conexion.conexionBD import connectionBD
# Para  validar contraseña
from werkzeug.security import check_password_hash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import url_for
import re
# Para encriptar contraseña generate_password_hash
from werkzeug.security import generate_password_hash

from routers.router_login import *
from controllers.funciones_logs import *
import json

def recibeInsertRegisterUser(name_surname, email_user, pass_user):
    print("Iniciando registro de usuario...")
    respuestaValidar = validarDataRegisterLogin(name_surname, email_user, pass_user)
    print("Resultado de validación de datos:", respuestaValidar)

    if respuestaValidar:
        nueva_password = generate_password_hash(pass_user, method='scrypt')
        print("Password hash generada:", nueva_password)
        try:
            with connectionBD() as conexion_MySQLdb:
                print("Conexión a la base de datos establecida.")
                with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                    sql = "INSERT INTO users(name_surname, email_user, pass_user) VALUES (%s, %s, %s)"
                    valores = (name_surname, email_user, nueva_password)
                    print("Ejecutando SQL para inserción:", sql)
                    print("Valores a insertar:", valores)
                    mycursor.execute(sql, valores)
                    usuario_insertado_id = mycursor.lastrowid
                    conexion_MySQLdb.commit()
                    resultado_insert = mycursor.rowcount
                    print("Usuario insertado con ID:", usuario_insertado_id)
                    print("Resultado de la inserción:", resultado_insert)

                    # Registrar el cambio en log_cambios
                    datos_nuevos = {
                        'id': usuario_insertado_id,
                        'name_surname': name_surname,
                        'email_user': email_user
                    }
                    log_cambio = {
                        'tabla': 'users',
                        'accion': 'Creacion de Cuenta',
                        'datos_anteriores': None,
                        'datos_nuevos': json.dumps(datos_nuevos),
                        'usuario_id': usuario_insertado_id  # Asegúrate de que 'session' esté disponible y tenga 'usuario_id'
                    }
                    print("Datos del log de cambio:", log_cambio)
                    insertar_log_cambio(log_cambio)

                    return resultado_insert
        except Exception as e:
            print(f"Error en el Insert users: {e}")
            return []
    else:
        print("Validación de datos fallida.")
        return False



# Validando la data del Registros para el login
def validarDataRegisterLogin(name_surname, email_user, pass_user):
    print("Validando datos del registro...")
    print(f"Nombre y apellido: {name_surname}")
    print(f"Correo electrónico: {email_user}")
    print(f"Contraseña: {pass_user}")

    if not name_surname or not email_user or not pass_user:
        print("Error: Algunos campos están vacíos.")
        return False

    if '@' not in email_user or '.' not in email_user:
        print("Error: Formato de correo electrónico no válido.")
        return False

    if len(pass_user) < 8:
        print("Error: La contraseña debe tener al menos 8 caracteres.")
        return False

    if any(char.isdigit() for char in name_surname):
        print("Error: El campo de nombre y apellido no debe contener números.")
        return False

    print("Todos los datos son válidos.")
    return True



def info_perfil_session():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT name_surname, email_user FROM users WHERE id = %s"
                cursor.execute(querySQL, (session['usuario_id'],))
                info_perfil = cursor.fetchall()
        return info_perfil
    except Exception as e:
        print(f"Error en info_perfil_session : {e}")
        return []


def procesar_update_perfil(data_form):
    # Extraer datos del diccionario data_form
    id_user = session['usuario_id']
    name_surname = data_form['name_surname']
    email_user = data_form['email_user']
    pass_actual = data_form['pass_actual']
    new_pass_user = data_form['new_pass_user']
    repetir_pass_user = data_form['repetir_pass_user']

    if not pass_actual or not email_user:
        return 3

    with connectionBD() as conexion_MySQLdb:
        with conexion_MySQLdb.cursor(dictionary=True) as cursor:
            querySQL = """SELECT * FROM users WHERE email_user = %s LIMIT 1"""
            cursor.execute(querySQL, (email_user,))
            account = cursor.fetchone()
            if account:
                if check_password_hash(account['pass_user'], pass_actual):
                    # Verificar si new_pass_user y repetir_pass_user están vacías
                    if not new_pass_user or not repetir_pass_user:
                        return updatePefilSinPass(id_user, name_surname)
                    else:
                        if new_pass_user != repetir_pass_user:
                            return 2
                        else:
                            try:
                                nueva_password = generate_password_hash(
                                    new_pass_user, method='scrypt')
                                with connectionBD() as conexion_MySQLdb:
                                    with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                                        querySQL = """
                                            UPDATE users
                                            SET 
                                                name_surname = %s,
                                                pass_user = %s
                                            WHERE id = %s
                                        """
                                        params = (name_surname,
                                                  nueva_password, id_user)
                                        cursor.execute(querySQL, params)
                                        conexion_MySQLdb.commit()

                                        # Enviar correo electrónico de confirmación
                                        subject = "Cambio de contraseña exitoso"
                                        body = f"Hola {name_surname},\n\nTu contraseña ha sido actualizada correctamente."
                                        send_reset_email2(email_user, subject, body)

                                return cursor.rowcount or []
                            except Exception as e:
                                print(
                                    f"Ocurrió en procesar_update_perfil: {e}")
                                return []
                else:
                    return 4
            else:
                return 0

def send_reset_email2(email, subject, body):
    sender_email = "brayanalexanderbc@ufps.edu.co"  # Cambia esto por tu dirección de correo electrónico
    receiver_email = email

    # Crea el mensaje
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Configura los detalles del servidor SMTP
    smtp_server = "smtp.gmail.com"  # Cambia esto si estás usando otro proveedor de correo
    smtp_port = 587
    smtp_username = "mmmmm@gmail.co"  # Cambia esto por tu dirección de correo electrónico
    smtp_password = "1234567"  # Cambia esto por tu contraseña de correo electrónico

    # Envía el correo electrónico
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        print("Correo electrónico enviado correctamente.")
    except Exception as e:
        print(f"Error al enviar el correo electrónico: {e}")







    # ... (resto del código para enviar el correo electrónico)
def updatePefilSinPass(id_user, name_surname):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    UPDATE users
                    SET 
                        name_surname = %s
                    WHERE id = %s
                """
                params = (name_surname, id_user)
                cursor.execute(querySQL, params)
                conexion_MySQLdb.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"Ocurrió un error en la funcion updatePefilSinPass: {e}")
        return []


def dataLoginSesion():
    inforLogin = {
        "id": session['id'],
        "name_surname": session['name_surname'],
        "email_user": session['email_user']
    }
    return inforLogin



def obtener_nombre_mesa(id_mesero):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                SELECT tbl_mesas.nombre_mesa
                FROM tbl_mesas
                INNER JOIN users ON tbl_mesas.id_mesero = users.id
                WHERE users.id = %s AND users.id_rol = 3
                """
                cursor.execute(querySQL, (id_mesero,))
                resultado = cursor.fetchall()
        return resultado
    except Exception as e:
        print(f"Error en obtener_nombre_mesa : {e}")
        return []























#Reestablecer contraseña
def send_reset_email(email, reset_link):
    # Configura los detalles del correo electrónico
    print("entra")
    sender_email = "brayanalexanderbc@ufps.edu.co"  # Cambia esto por tu dirección de correo electrónico
    receiver_email = email
    subject = "Restablecimiento de Contraseña"
    body = f"Hola, has solicitado restablecer tu contraseña. Por favor, haz clic en el siguiente enlace para continuar: {reset_link}"

    # Crea el mensaje
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Configura los detalles del servidor SMTP
    smtp_server = "smtp.gmail.com"  # Cambia esto si estás usando otro proveedor de correo
    smtp_port = 587
    smtp_username = "brayanalexanderbc@ufps.edu.co"  # Cambia esto por tu dirección de correo electrónico
    smtp_password = "DIANAcardenas30"  # Cambia esto por tu contraseña de correo electrónico

    # Envía el correo electrónico
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        print("Correo electrónico enviado correctamente.")
    except Exception as e:
        print(f"Error al enviar el correo electrónico: {e}")

def get_user_by_email(email):
    # Consulta a la base de datos para obtener el usuario por su correo electrónico
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email_user = %s", [email])
    user = cursor.fetchone()
    conexion_MySQLdb.close()
    return user

def save_reset_token(user_id, token, expiration_date):
    # Guarda el token de restablecimiento de contraseña en la base de datos
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor()
    cursor.execute("INSERT INTO password_reset_tokens (user_id, token, expiration_date) VALUES (%s, %s, %s)", (user_id, token, expiration_date))
    conexion_MySQLdb.commit()
    conexion_MySQLdb.close()

def check_token_validity(token):
    # Verifica si el token es válido y no ha expirado
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM password_reset_tokens WHERE token = %s AND expiration_date > NOW()", [token])
    valid_token = cursor.fetchone()
    conexion_MySQLdb.close()
    return valid_token

def get_user_id_by_token(token):
    # Obtiene el ID del usuario a partir del token
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor(dictionary=True)
    cursor.execute("SELECT user_id FROM password_reset_tokens WHERE token = %s", [token])
    result = cursor.fetchone()
    conexion_MySQLdb.close()
    return result['user_id'] if result else None

def update_user_password(user_id, new_password):
    # Actualiza la contraseña del usuario en la base de datos
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor()
    cursor.execute("UPDATE users SET pass_user = %s WHERE id = %s", (new_password, user_id))
    conexion_MySQLdb.commit()
    conexion_MySQLdb.close()

def delete_reset_token(token):
    # Elimina el token de restablecimiento de contraseña de la base de datos
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor()
    cursor.execute("DELETE FROM password_reset_tokens WHERE token = %s", [token])
    conexion_MySQLdb.commit()
    conexion_MySQLdb.close()





