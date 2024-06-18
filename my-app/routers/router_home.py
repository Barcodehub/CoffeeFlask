import io

import pdfkit
from app import app
from flask import render_template, request, flash, redirect, url_for, session, jsonify, make_response
from mysql.connector.errors import Error


# Importando cenexión a BD
from controllers.funciones_home import *
from xhtml2pdf import pisa
from datetime import date
from datetime import datetime, timedelta
from flask_apscheduler import APScheduler
scheduler = APScheduler()
def init_scheduler(app):
    scheduler.init_app(app)
    scheduler.start()

    @scheduler.task('interval', id='liberar_mesas_task', hours=1, misfire_grace_time=900)
    def liberar_mesas_task():
        with app.app_context():
            liberar_mesas()



PATH_URL = "public/perfil"
PATH_URL2 = "public/library"
PATH_URL3 = "public/usuarios"
PATH_URL4 = "public/productos"
PATH_URL5 = "public/mesas"
PATH_URL6 = "public/reservas"
PATH_URL7 = "public/facturas"
PATH_URL8 = "public/logs"
PATH_URL_LOGIN = "public/login"

#################################
#CAMBIOS LOGS

@app.route('/log_cambios')
def mostrar_log_cambios():
    log_cambios = obtener_log_cambios()
    return render_template(f'{PATH_URL8}/log_cambios.html', log_cambios=log_cambios)





##################################

@app.route('/registrar-producto', methods=['GET'])
def viewFormProducto():
    if 'conectado' in session:
        return render_template(f'{PATH_URL4}/form_producto.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/form-registrar-producto', methods=['POST'])
def formProducto():
    if 'conectado' in session:
        if 'foto_producto' in request.files:
            foto_perfil = request.files['foto_producto']
            resultado = procesar_form_producto(request.form, foto_perfil)
            if resultado:
                return redirect(url_for('lista_productos'))
            else:
                flash('El producto NO fue registrado.', 'error')
                return render_template(f'{PATH_URL4}/form_producto.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/lista-de-productos', methods=['GET'])
def lista_productos():
    if 'conectado' in session:
        return render_template(f'{PATH_URL4}/lista_productos.html', productos=sql_lista_productosBD())
    else:
        flash('recuerde debe iniciar sesión.', 'error')
        return render_template(f'{PATH_URL_LOGIN}/base_login.html')



@app.route("/buscando-producto", methods=['POST'])
def viewBuscarProductoBD():
    resultadoBusqueda = buscarProductoBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL4}/resultado_busqueda_producto.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})


@app.route("/editar-producto/<int:id>", methods=['GET'])
def viewEditarProducto(id):
    if 'conectado' in session:
        respuestaProducto = buscarProductoUnico(id)
        if respuestaProducto:
            return render_template(f'{PATH_URL4}/form_producto_update.html', respuestaProducto=respuestaProducto)
        else:
            flash('El producto no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Recibir formulario para actulizar informacion de producto
@app.route('/actualizar-producto', methods=['POST'])
def actualizarProducto():
    resultData = procesar_actualizacion_formProducto(request)
    if resultData:
        return redirect(url_for('lista_productos'))


@app.route('/borrar-producto/<string:id_producto>/<string:foto_producto>', methods=['GET'])
def borrarProducto(id_producto, foto_producto):
    resp = eliminarProducto(id_producto, foto_producto)
    if resp:
        flash('El Producto fue eliminado correctamente', 'success')
        return redirect(url_for('lista_productos'))













#USUARIOS


@app.route("/lista-de-usuarios", methods=['GET'])
def usuarios():
    if 'conectado' in session:
        resp_usuariosBD = lista_usuariosBD()
        return render_template('public/usuarios/lista_usuarios.html', resp_usuariosBD=resp_usuariosBD)
    else:
        return redirect(url_for('inicio'))





@app.route("/editar-usuario/<int:id>", methods=['GET'])
def viewEditarUsuario(id):
    if 'conectado' in session:
        respuestaUsuario = buscarUsuarioUnico(id)
        if respuestaUsuario:
            return render_template(f'{PATH_URL3}/form_usuario_update.html', respuestaUsuario=respuestaUsuario)
        else:
            flash('El usuario no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Recibir formulario para actulizar informacion de user
@app.route('/actualizar-usuario', methods=['POST'])
def actualizarUsuario():
    resultData = procesar_actualizacion_formUser(request)
    if resultData:
        return redirect(url_for('usuarios'))



@app.route('/borrar-usuario/<string:id>', methods=['GET'])
def borrarUsuario(id):
    resp = eliminarUsuario(id)
    if resp:
        flash('El Usuario fue eliminado correctamente', 'success')
        return redirect(url_for('usuarios'))



@app.route("/buscando-usuario", methods=['POST'])
def viewBuscarUsuarioBD():

    resultadoBusqueda = buscarUsuarioBD(request.json['busqueda'])
    if resultadoBusqueda:
        print(resultadoBusqueda)
        return render_template(f'{PATH_URL3}/resultado_busqueda_usuario.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})











#MESAS

@app.route('/registrar-mesa', methods=['GET'])
def viewFormMesa():
    if 'conectado' in session:
        meseros = obtener_meseros()
        return render_template(f'{PATH_URL5}/form_mesa.html', meseros=meseros)
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))




@app.route('/form-registrar-mesa', methods=['POST'])
def formMesa():
            resultado = procesar_form_mesa(request.form)
            if resultado:
                return redirect(url_for('lista_mesas'))
            else:
                flash('El mesa NO fue registrado.', 'error')
                return render_template(f'{PATH_URL5}/form_mesa.html')


@app.route('/lista-de-mesas', methods=['GET'])
def lista_mesas():
    if 'conectado' in session:
        rol_usuario = session['id_rol']
        return render_template(f'{PATH_URL5}/lista_mesas.html', mesas=sql_lista_mesasBD(rol_usuario))
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route("/buscando-mesa", methods=['POST'])
def viewBuscarMesaBD():
    print(buscarMesaBD)
    resultadoBusqueda = buscarMesaBD(request.json['busqueda'])
    if resultadoBusqueda:
        print(resultadoBusqueda)
        return render_template(f'{PATH_URL5}/resultado_busqueda_mesa.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})


@app.route("/editar-mesa/<int:id>", methods=['GET'])
@app.route("/editar-mesa/<int:id>", methods=['GET'])
def viewEditarMesa(id):
    if 'conectado' in session:
        meseros = obtener_meseros()
        respuestaMesa = buscarMesaUnico(id)
        if respuestaMesa:
            respuestaMesa['hora_inicio'] = obtener_hora_disponibilidad(respuestaMesa['id_mesa'], 'hora_inicio')
            respuestaMesa['hora_fin'] = obtener_hora_disponibilidad(respuestaMesa['id_mesa'], 'hora_fin')
            return render_template(f'{PATH_URL5}/form_mesa_update.html', respuestaMesa=respuestaMesa, meseros=meseros)
        else:
            flash('La mesa no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

def obtener_hora_disponibilidad(id_mesa, campo):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                query = f"SELECT {campo} FROM tbl_disponibilidad_mesas WHERE id_mesa = %s LIMIT 1"
                cursor.execute(query, (id_mesa,))
                resultado = cursor.fetchone()
                return resultado[campo] if resultado else None
    except Exception as e:
        print(f"Error en obtener_hora_disponibilidad: {e}")
        return None

@app.route('/actualizar-mesa', methods=['POST'])
def actualizarMesa():
    resultData = procesar_actualizacion_formMesa(request.form)
    if resultData:
        return redirect(url_for('lista_mesas'))
    else:
        flash('Error al actualizar la mesa.', 'error')
        return redirect(url_for('viewEditarMesa', id=request.form['id_mesa']))

@app.route('/borrar-mesa/<string:id_mesa>', methods=['GET'])
def borrarMesa(id_mesa):
    resp = eliminarMesa(id_mesa)
    if resp:
        flash('El mesa fue eliminado correctamente', 'success')
        return redirect(url_for('lista_mesas'))


@app.route('/borrar-reserva/<string:id_reserva>', methods=['GET'])
def borrarReserva(id_reserva):
    resp = eliminarReserva(id_reserva)
    if resp:
        flash('La reservacion fue cancelada correctamente', 'success')
    if session['id_rol'] == 1:
        return redirect(url_for('lista_reservas'))
    else:
        return redirect(url_for('lista_reservas2'))



#RESERVAS

@app.route('/lista-de-reservas', methods=['GET'])
def lista_reservas():
    if 'conectado' in session:
        return render_template(f'{PATH_URL6}/lista_reservas.html', reservas=sql_lista_reservasBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return render_template(f'{PATH_URL_LOGIN}/base_login.html')

@app.route('/lista-de-reservasUser', methods=['GET'])
def lista_reservas2():
    if 'conectado' in session:
        usuario_id = session.get('usuario_id')
        return render_template(f'{PATH_URL6}/lista_reservasuser.html', reservas=sql_lista_reservasUSER(usuario_id))
    else:
        flash('primero debes iniciar sesión.', 'error')
        return render_template(f'{PATH_URL_LOGIN}/base_login.html')


@app.route('/form-reserva', methods=['GET', 'POST'])
def viewFormReserva():
    if 'conectado' in session:
        if request.method == 'POST':
            resultado = procesar_form_reserva(request.form)
            if resultado:
                flash('La reserva fue registrada correctamente.', 'success')
            else:
                flash('Error: La mesa no está disponible para el horario seleccionado.', 'error')
            return redirect(url_for('lista_mesas'))
        else:
            id_mesa = request.args.get('id_mesa')
            cantidad_mesa = request.args.get('cantidad_mesa')
            fecha_minima = date.today().isoformat()
            fecha_actual = fecha_minima
            return render_template(f'{PATH_URL6}/form_reserva.html', id_mesa=id_mesa, cantidad_mesa=cantidad_mesa, fecha_minima=fecha_minima, fecha_actual=fecha_actual)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/liberar-mesa/<int:id_mesa>')
def liberar_mesa(id_mesa):
    if session['id_rol'] == 1:  # Solo para administradores
        try:
            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                    querySQL = "UPDATE tbl_disponibilidad_mesas SET disponible = 1 WHERE id_mesa = %s"
                    cursor.execute(querySQL, (id_mesa,))
                    conexion_MySQLdb.commit()
            flash('Mesa liberada correctamente.', 'success')
        except Exception as e:
            print(f"Error en liberar_mesa: {e}")
            flash('Error al liberar la mesa.', 'error')
    else:
        flash('No tienes permiso para realizar esta acción.', 'error')
    return redirect(url_for('lista_mesas'))





@app.route('/form-registrar-reserva', methods=['POST'])
def formReserva():
            resultado = procesar_form_reserva(request.form)
            if resultado:
                flash('Reserva registrada correctamente.', 'success')
                return redirect(url_for('lista_reservas2'))
            else:
                flash('El mesa NO fue registrado.', 'error')
                return render_template(f'{PATH_URL6}/form_reserva.html')


@app.route('/form-registrar-reserva-admin', methods=['GET', 'POST'])
def formReservaAdmin():
    if request.method == 'POST':
        resultado = procesar_form_reserva_admin(request.form)
        if resultado:
            flash('Reserva registrada correctamente.', 'success')
            return redirect(url_for('lista_reservas'))
        else:
            flash('Error al registrar la reserva.', 'error')
        return redirect(url_for('inicio'))


    fecha_minima = date.today().isoformat()
    fecha_actual = fecha_minima
    usuarios = obtener_usuarios()
    mesas = obtener_mesas()
    return render_template(f'{PATH_URL6}/form_reserva_admin.html', usuarios=usuarios, mesas=mesas, fecha_minima=fecha_minima, fecha_actual=fecha_actual)


@app.route('/horas-disponibles/<int:mesa_id>', methods=['GET'])
def obtener_horas_disponibles(mesa_id):
    fecha_reserva = request.args.get('fechaReserva')
    fecha_reserva = datetime.strptime(fecha_reserva, '%a %b %d %Y %H:%M:%S GMT-0500 (hora estándar de Colombia)')
    fecha_actual = datetime.now()
    print('Fecha de reserva:', fecha_reserva)
    print('Fecha actual:', fecha_actual)

    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Consulta SQL para obtener las horas disponibles
                if fecha_reserva.date() == date.today():
                    querySQL = """
                    SELECT id, hora_inicio, hora_fin 
                    FROM tbl_disponibilidad_mesas 
                    WHERE id_mesa = %s AND disponible = 1
                    """
                else:
                    querySQL = """
                    SELECT id, hora_inicio, hora_fin 
                    FROM tbl_disponibilidad_mesas 
                    WHERE id_mesa = %s
                    """

                cursor.execute(querySQL, (mesa_id,))
                horas = cursor.fetchall()

                # Convertir las horas a formato deseado (por ejemplo, HH:MM)
                for hora in horas:
                    hora['hora_inicio'] = str(hora['hora_inicio'])
                    hora['hora_fin'] = str(hora['hora_fin'])

    except Exception as e:
        print(f"Error al obtener horas disponibles: {e}")
        response = {
            'error': str(e),
            'message': 'Error al obtener las horas disponibles'
        }
        return make_response(jsonify(response), 500)

    return jsonify(horas)

@app.route('/horas-disponibles2/<int:mesa_id>', methods=['GET'])
def obtener_horas_disponibles2(mesa_id):
    horas = []
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT id, hora_inicio, hora_fin FROM tbl_disponibilidad_mesas WHERE id_mesa = %s"
                cursor.execute(querySQL, (mesa_id,))
                horas = cursor.fetchall()

                # Convertir timedelta a string antes de serializar a JSON
                for hora in horas:
                    if isinstance(hora['hora_inicio'], timedelta):
                        hora['hora_inicio'] = str(hora['hora_inicio'])
                    if isinstance(hora['hora_fin'], timedelta):
                        hora['hora_fin'] = str(hora['hora_fin'])

    except Exception as e:
        print(f"Error al obtener horas disponibles: {e}")

    return jsonify(horas)

@app.errorhandler(500)
def internal_server_error(error):
    response = {
        'error': str(error),
        'message': 'Se produjo un error en el servidor'
    }
    return make_response(jsonify(response), 500)
#CARRITO

@app.route('/agregar-al-carrito/<int:id_producto>', methods=['GET'])
def agregar_al_carrito(id_producto):
    if 'usuario_id' not in session:
        return redirect(url_for('blog'))  # Si no hay usuario autenticado, redirigir al login


    usuario_id = session['usuario_id']
    producto = buscarProductoUnico(id_producto)

    # Obtener o crear el carrito para el usuario
    carrito = obtener_carrito_usuario(usuario_id)
    if not carrito:

        carrito_id = crear_carrito_usuario(usuario_id)
    else:
        carrito_id = carrito['id']

    # Agregar el producto al carrito
    agregar_producto_carrito(carrito_id, id_producto, producto['cantidad'])

    return redirect(url_for('carrito'))


@app.route('/carrito')
def carrito():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    usuario_id = session['usuario_id']
    productos_carrito = obtener_productos_carrito(usuario_id)
    total_carrito = calcular_total_carrito(productos_carrito)

    return render_template(f'{PATH_URL4}/carrito.html', carrito=productos_carrito, total_carrito=total_carrito)

@app.route('/actualizar_cantidad/<int:id_producto>', methods=['POST'])
def actualizar_cantidad(id_producto):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    usuario_id = session['usuario_id']
    cantidad = int(request.form.get('cantidad', 0))

    actualizar_cantidad_producto(usuario_id, id_producto, cantidad)

    return redirect(url_for('carrito'))

@app.route('/eliminar_del_carrito/<int:id_producto>', methods=['GET'])
def eliminar_del_carrito(id_producto):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    usuario_id = session['usuario_id']

    eliminar_producto_carrito(usuario_id, id_producto)

    return redirect(url_for('carrito'))

@app.route('/checkout', methods=['GET'])
def checkout():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    usuario_id = session['usuario_id']

    productos_carrito = obtener_productos_carrito(usuario_id)
    total_carrito = calcular_total_carrito(productos_carrito)

    if request.method == 'GET':
        # Lógica para procesar el pago
        # ...

        # Insertar nueva factura
        nueva_factura = {'usuario_id': usuario_id, 'total': total_carrito}
        factura_id = insertar_factura(nueva_factura)

        # Insertar productos de la factura
        for producto in productos_carrito:
            detalle_factura = {
                'factura_id': factura_id,
                'producto_id': producto['id_producto'],
                'cantidad': producto['cantidad'],
                'precio': producto['precio_producto']
            }
            insertar_detalle_factura(detalle_factura)

        # Vaciar carrito
        vaciar_carrito(usuario_id)

        return redirect(url_for('factura_exito', factura_id=factura_id))





    # Lógica para procesar el pago y generar la orden de compra

    return render_template(f'{PATH_URL7}/checkout.html', carrito=productos_carrito, total_carrito=total_carrito)




@app.route('/factura_exito/<int:factura_id>')
def factura_exito(factura_id):
    print("entro a factura_exito")
    factura = obtener_factura(factura_id)
    productos_factura = obtener_productos_factura(factura_id)
    return render_template(f'{PATH_URL7}/factura_exito.html', factura=factura, productos_factura=productos_factura)


@app.route('/factura_pdf/<int:factura_id>', methods=['GET'])
def factura_pdf(factura_id):
    if factura_id is None:
        flash('Debes seleccionar la fecha y darle al  boton buscar', 'danger')
        return redirect(url_for('viewReporteVentas'))
    else:

        factura = obtener_factura(factura_id)
        productos_factura = obtener_productos_factura(factura_id)

        # Renderizar la plantilla HTML de la factura
        html = render_template(f'{PATH_URL7}/factura_exito.html', factura=factura, productos_factura=productos_factura)

        # Crear un objeto BytesIO para almacenar el PDF
        pdf = io.BytesIO()

        # Generar el PDF a partir del HTML
        pisa.CreatePDF(html, dest=pdf)
        # Mover el cursor al inicio del buffer
        pdf.seek(0)

        # Configurar la respuesta para descargar el PDF
        response = make_response(pdf.getvalue())
        response.headers.set('Content-Type', 'application/pdf')
        response.headers.set('Content-Disposition', 'attachment', filename=f'factura_{factura_id}.pdf')

        return response




@app.route('/reporte_ventas_pdf', methods=['GET'])
def reporte_ventas_pdf():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    if fecha_inicio is None:
        flash('Debes seleccionar la fecha y darle al  boton buscar', 'danger')
        return redirect(url_for('viewReporteVentas'))

    else:
        print("fechainicooooo"+fecha_inicio)
        facturas = sql_facturas_reporte(fecha_inicio, fecha_fin)

        # Renderizar la plantilla HTML del reporte de ventas
        html = render_template(f'{PATH_URL7}/reporte_ventas.html', facturas=facturas, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)

        # Crear un objeto BytesIO para almacenar el PDF
        pdf = io.BytesIO()

        # Generar el PDF a partir del HTML
        pisa.CreatePDF(html, dest=pdf)
        # Mover el cursor al inicio del buffer
        pdf.seek(0)

        # Configurar la respuesta para descargar el PDF
        response = make_response(pdf)
        response.headers.set('Content-Type', 'application/pdf')
        response.headers.set('Content-Disposition', 'attachment', filename='reporte_ventas.pdf')

        return response

@app.route('/lista-de-facturas', methods=['GET'])
def lista_facturas():
    if 'conectado' in session:
        return render_template(f'{PATH_URL7}/lista_facturas.html', facturas=sql_lista_facturasBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route("/buscando-factura", methods=['POST'])
def viewBuscarFacturaBD():

    resultadoBusqueda = buscarFacturaBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL7}/resultado_busqueda_factura.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})

@app.route('/borrar-factura/<string:id>', methods=['GET'])
def borrarFactura(id):
    resp = eliminarFactura(id)
    if resp:
        flash('la factura fue eliminada correctamente', 'success')
        return redirect(url_for('lista_facturas'))
    else:
        flash('Hubo un error al eliminar la factura', 'danger')
        return redirect(url_for('lista_facturas'))



@app.route('/lista-de-reportes', methods=['GET'])
def viewReporteVentas():
    if 'conectado' in session:
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        facturas = sql_facturas_reporte(fecha_inicio, fecha_fin)
        return render_template(f'{PATH_URL7}/lista_reportes.html', facturas=facturas, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))




#PAGO
@app.route('/procesar_pago', methods=['POST'])
def procesar_pago():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    nombre = request.form.get('nombre')
    email = request.form.get('email')
    tarjeta = request.form.get('tarjeta')
    expiracion = request.form.get('expiracion')
    cvv = request.form.get('cvv')

    usuario_id = session['usuario_id']
    productos_carrito = obtener_productos_carrito(usuario_id)
    total_carrito = calcular_total_carrito(productos_carrito)

    # Lógica para procesar el pago con un proveedor de pasarela de pago
    pago_exitoso = procesar_pago_pasarela(nombre, email, tarjeta, expiracion, cvv, total_carrito)

    if pago_exitoso:
        # Lógica para generar la orden de compra en la base de datos
        orden_id = generar_orden_compra(usuario_id, productos_carrito, total_carrito)

        # Limpiar el carrito después de generar la orden de compra
        vaciar_carrito(usuario_id)

        # Redirigir a una página de confirmación de compra
        return redirect(url_for('confirmacion_compra', orden_id=orden_id))
    else:
        # Mostrar un mensaje de error si el pago falla
        flash('El pago no se pudo procesar. Por favor, inténtalo de nuevo.', 'error')
        return redirect(url_for('checkout'))
