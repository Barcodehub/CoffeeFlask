
from app import app
from flask import render_template, request, flash, redirect, url_for, session
import smtplib
import secrets
from datetime import datetime, timedelta
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
# Importando mi conexión a BD
from conexion.conexionBD import connectionBD

# Para encriptar contraseña generate_password_hash
from werkzeug.security import check_password_hash

# Importando controllers para el modulo de login
from controllers.funciones_login import *
PATH_URL_LOGIN = "public/login"


@app.route('/', methods=['GET'])
def inicio():
    if 'conectado' in session:
        return render_template('public/base_cpanel.html', info_perfil_session=info_perfil_session())
    else:
        return redirect(url_for('inicio'))


@app.route('/mi-perfil', methods=['GET'])
def perfil():
    if session['id_rol'] == 3:
        id_mesero = session['usuario_id'] #id o usuario_id
        mesas = obtener_nombre_mesa(id_mesero)
        return render_template(f'public/perfil/perfil.html', info_perfil_session=info_perfil_session(), mesas=mesas)
    elif 'conectado' in session:
        return render_template(f'public/perfil/perfil.html', info_perfil_session=info_perfil_session())
    else:
        return redirect(url_for('inicio'))









@app.route('/mi-tienda', methods=['GET'])
def tienda():
    if 'conectado' in session:
        return render_template(f'public/library/tienda.html', info_perfil_session=info_perfil_session())
    else:
        return redirect(url_for('inicio'))






@app.route('/mi-contacto', methods=['GET'])
def contacto():
    if 'conectado' in session:
        return render_template(f'public/library/contacto.html', info_perfil_session=info_perfil_session())
    else:
        return redirect(url_for('inicio'))

@app.route('/mi-blog', methods=['GET'])
def blog():
        return render_template(f'public/library/blog.html')

@app.route('/mi-registerbook', methods=['GET'])
def registerbook():
    if 'conectado' in session:
        return render_template(f'public/library/registerbook.html', info_perfil_session=info_perfil_session())
    else:
        return redirect(url_for('inicio'))



# Crear cuenta de usuario
@app.route('/register-user', methods=['GET'])
def cpanelRegisterUser():
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    else:
        return render_template(f'{PATH_URL_LOGIN}/auth_register.html')


# Recuperar cuenta de usuario



# Crear cuenta de usuario
@app.route('/saved-register', methods=['POST'])
def cpanelResgisterUserBD():
    if request.method == 'POST' and 'name_surname' in request.form and 'pass_user' in request.form:
        name_surname = request.form['name_surname']
        email_user = request.form['email_user']
        pass_user = request.form['pass_user']

        resultData = recibeInsertRegisterUser(
            name_surname, email_user, pass_user)
        if (resultData != 0):
            flash('la cuenta fue creada correctamente.', 'success')
            return redirect(url_for('inicio'))
        else:
            flash('Datos mal escritos, revise el formato de email, la contraseña debe tener al menos 8 caracteres, su nombre no debe contener números.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/base_login.html')
    else:
        flash('el método HTTP es incorrecto', 'error')
        return render_template(f'{PATH_URL_LOGIN}/base_login.html')


# Actualizar datos de mi perfil
@app.route("/actualizar-datos-perfil", methods=['POST'])
def actualizarPerfil():
    if request.method == 'POST':
        if 'conectado' in session:
            respuesta = procesar_update_perfil(request.form)
            if respuesta == 1:
                flash('Los datos fuerón actualizados correctamente.', 'success')
                return redirect(url_for('inicio'))
            elif respuesta == 0:
                flash(
                    'La contraseña actual esta incorrecta, por favor verifique.', 'error')
                return redirect(url_for('perfil'))
            elif respuesta == 2:
                flash('Ambas claves deben se igual, por favor verifique.', 'error')
                return redirect(url_for('perfil'))
            elif respuesta == 3:
                flash('La Clave actual es obligatoria.', 'error')
                return redirect(url_for('perfil'))
            elif respuesta == 4:
                flash('La Clave actual esta incorrecta.', 'error')
                return redirect(url_for('perfil'))
        else:
            flash('primero debes iniciar sesión.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Validar sesión
@app.route('/login', methods=['GET', 'POST'])
def loginCliente():
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    else:
        if request.method == 'POST' and 'email_user' in request.form and 'pass_user' in request.form:

            email_user = str(request.form['email_user'])
            pass_user = str(request.form['pass_user'])

            # Comprobando si existe una cuenta
            conexion_MySQLdb = connectionBD()
            if conexion_MySQLdb is None:
                # Handle the case where connection failed, log an error, or raise an exception
                print("Failed to establish database connection.")
                # Optionally raise an exception or return an error response
            else:
                # Proceed with executing SQL queries
                cursor = conexion_MySQLdb.cursor(dictionary=True)
                cursor.execute("SELECT * FROM users WHERE email_user = %s", [email_user])
                account = cursor.fetchone()
            cursor = conexion_MySQLdb.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM users WHERE email_user = %s", [email_user])
            account = cursor.fetchone()

            if account:
                if check_password_hash(account['pass_user'], pass_user):
                    # Crear datos de sesión, para poder acceder a estos datos en otras rutas
                    session['conectado'] = True
                    #session['id'] = account['id']
                    session['usuario_id'] = account['id']
                    session['name_surname'] = account['name_surname']
                    session['email_user'] = account['email_user']


                    #autentificacion de ROLES
                    session['id_rol'] = account['id_rol']
                    if session['id_rol']==1:
                        flash('la sesión fue correcta.', 'success')
                        return render_template('public/base_cpanel.html')
                    elif session['id_rol']==2:
                        return render_template('public/base_cpanel.html')
                    else:
                        return render_template('public/base_cpanel.html')

                   # flash('la sesión fue correcta.', 'success')
                    #return redirect(url_for('inicio'))
                else:
                    # La cuenta no existe o el nombre de usuario/contraseña es incorrecto
                    flash('datos incorrectos por favor revise.', 'error')
                    return render_template(f'{PATH_URL_LOGIN}/base_login.html')
            else:
                flash('el usuario no existe, por favor verifique.', 'error')
                return render_template(f'{PATH_URL_LOGIN}/base_login.html')
        else:
            flash('primero debes iniciar sesión.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/base_login.html')


@app.route('/closed-session',  methods=['GET'])
def cerraSesion():
    if request.method == 'GET':
        if 'conectado' in session:
            # Eliminar datos de sesión, esto cerrará la sesión del usuario
            session.pop('conectado', None)
            session.pop('usuario_id', None)
            session.pop('name_surname', None)
            session.pop('email', None)
            flash('tu sesión fue cerrada correctamente.', 'success')
            return render_template(f'{PATH_URL_LOGIN}/base_login.html')
        else:
            flash('recuerde debe iniciar sesión.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/base_login.html')
















@app.route('/recovery-password', methods=['GET', 'POST'])
def cpanelRecoveryPassUser():
    print("Iniciando cpanelRecoveryPassUser...")
    if request.method == 'POST':
        print("Método POST detectado.")
        email_user = request.form.get('email_user')
        print(f"Email de usuario recibido: {email_user}")

        user = get_user_by_email(email_user)
        print(f"Usuario obtenido: {user}")

        if user:
            print("Usuario encontrado, generando token...")
            # Generar un token de restablecimiento de contraseña
            token = secrets.token_urlsafe(32)
            expiration_date = datetime.now() + timedelta(hours=24)  # Token válido por 24 horas
            print(f"Token generado: {token}, Fecha de expiración: {expiration_date}")

            # Guardar el token en la base de datos
            save_reset_token(user['id'], token, expiration_date)
            print("Token de restablecimiento guardado en la base de datos.")

            # Enviar correo electrónico con el enlace de restablecimiento de contraseña
            reset_link = url_for('reset_password', token=token, _external=True)
            send_reset_email(user['email_user'], reset_link)
            print(f"Enlace de restablecimiento enviado: {reset_link}")

            flash('Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña.', 'success')
        else:
            print("No se encontró una cuenta con ese correo electrónico.")
            flash('No se encontró una cuenta con ese correo electrónico.', 'error')

    return render_template(f'{PATH_URL_LOGIN}/auth_forgot_password.html')


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    print("Iniciando reset_password...")
    print(f"Token recibido: {token}")

    if request.method == 'GET':
        print("Método GET detectado.")
        # Verifica si el token es válido
        valid_token = check_token_validity(token)
        print(f"Token válido: {valid_token}")

        if valid_token:
            return render_template(f'{PATH_URL_LOGIN}/reset_password.html', token=token)
        else:
            flash('El token de restablecimiento de contraseña no es válido o ha expirado.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/base_login.html')

    if request.method == 'POST':
        print("Método POST detectado.")
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        print(f"Nueva contraseña: {new_password}")
        print(f"Confirmar contraseña: {confirm_password}")

        if new_password == confirm_password:
            print("Las contraseñas coinciden.")
            # Actualiza la contraseña del usuario en la base de datos
            hashed_password = generate_password_hash(new_password)
            print(f"Contraseña hasheada: {hashed_password}")

            user_id = get_user_id_by_token(token)
            print(f"ID de usuario obtenido por token: {user_id}")

            update_user_password(user_id, hashed_password)
            print("Contraseña del usuario actualizada en la base de datos.")

            # Elimina el token de restablecimiento de contraseña de la base de datos
            delete_reset_token(token)
            print("Token de restablecimiento eliminado de la base de datos.")

            flash('Tu contraseña ha sido actualizada correctamente.', 'success')
            return render_template(f'{PATH_URL_LOGIN}/base_login.html')
        else:
            print("Las contraseñas no coinciden.")
            flash('Las contraseñas no coinciden.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/reset_password.html', token=token)

