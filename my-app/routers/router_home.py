from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error


# Importando cenexión a BD
from controllers.funciones_home import *

PATH_URL = "public/empleados"
PATH_URL2 = "public/library"
PATH_URL3 = "public/usuarios"
PATH_URL4 = "public/productos"
PATH_URL5 = "public/mesas"


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
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))



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














@app.route('/registrar-empleado', methods=['GET'])
def viewFormEmpleado():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/form_empleado.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/form-registrar-empleado', methods=['POST'])
def formEmpleado():
    if 'conectado' in session:
        if 'foto_producto' in request.files:
            foto_perfil = request.files['foto_producto']
            resultado = procesar_form_empleado(request.form, foto_perfil)
            if resultado:
                return redirect(url_for('lista_empleados'))
            else:
                flash('El empleado NO fue registrado.', 'error')
                return render_template(f'{PATH_URL}/form_empleado.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/lista-de-empleados', methods=['GET'])
def lista_empleados():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/lista_empleados.html', empleados=sql_lista_empleadosBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route("/detalles-empleado/", methods=['GET'])
@app.route("/detalles-empleado/<int:idEmpleado>", methods=['GET'])
def detalleEmpleado(idEmpleado=None):
    if 'conectado' in session:
        # Verificamos si el parámetro idEmpleado es None o no está presente en la URL
        if idEmpleado is None:
            return redirect(url_for('inicio'))
        else:
            detalle_empleado = sql_detalles_empleadosBD(idEmpleado) or []
            return render_template(f'{PATH_URL}/detalles_empleado.html', detalle_empleado=detalle_empleado)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Buscadon de empleados
@app.route("/buscando-empleado", methods=['POST'])
def viewBuscarEmpleadoBD():
    resultadoBusqueda = buscarEmpleadoBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL}/resultado_busqueda_empleado.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})


@app.route("/editar-empleado/<int:id>", methods=['GET'])
def viewEditarEmpleado(id):
    if 'conectado' in session:
        respuestaEmpleado = buscarEmpleadoUnico(id)
        if respuestaEmpleado:
            return render_template(f'{PATH_URL}/form_empleado_update.html', respuestaEmpleado=respuestaEmpleado)
        else:
            flash('El empleado no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Recibir formulario para actulizar informacion de empleado
@app.route('/actualizar-empleado', methods=['POST'])
def actualizarEmpleado():
    resultData = procesar_actualizacion_form(request)
    if resultData:
        return redirect(url_for('lista_empleados'))


@app.route("/lista-de-usuarios", methods=['GET'])
def usuarios():
    if 'conectado' in session:
        resp_usuariosBD = lista_usuariosBD()
        return render_template('public/usuarios/lista_usuarios.html', resp_usuariosBD=resp_usuariosBD)
    else:
        return redirect(url_for('inicioCpanel'))





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


@app.route('/borrar-empleado/<string:id_empleado>/<string:foto_producto>', methods=['GET'])
def borrarEmpleado(id_empleado, foto_producto):
    resp = eliminarEmpleado(id_empleado, foto_producto)
    if resp:
        flash('El Empleado fue eliminado correctamente', 'success')
        return redirect(url_for('lista_empleados'))


@app.route("/descargar-informe-empleados/", methods=['GET'])
def reporteBD():
    if 'conectado' in session:
        return generarReporteExcel()
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))











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
        return render_template(f'{PATH_URL5}/lista_mesas.html', mesas=sql_lista_mesasBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route("/buscando-mesa", methods=['POST'])
def viewBuscarMesaBD():

    resultadoBusqueda = buscarMesaBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL5}/resultado_busqueda_mesa.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})


@app.route("/editar-mesa/<int:id>", methods=['GET'])
def viewEditarMesa(id):
    if 'conectado' in session:
        meseros = obtener_meseros()
        respuestaMesa = buscarMesaUnico(id)
        if respuestaMesa:
            return render_template(f'{PATH_URL5}/form_mesa_update.html', respuestaMesa=respuestaMesa, meseros=meseros)
        else:
            flash('La mesa no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Recibir formulario para actulizar informacion de mesa
@app.route('/actualizar-mesa', methods=['POST'])
def actualizarMesa():
    print("pasoooooooooooo")
    resultData = procesar_actualizacion_formMesa(request)
    if resultData:
        return redirect(url_for('lista_mesas'))

@app.route('/borrar-mesa/<string:id_mesa>', methods=['GET'])
def borrarMesao(id_mesa):
    resp = eliminarMesa(id_mesa)
    if resp:
        flash('El mesa fue eliminado correctamente', 'success')
        return redirect(url_for('lista_mesas'))






























#LIBROS


@app.route('/registrar-libro', methods=['GET'])
def viewFormLibro():
    if 'conectado' in session:
        return render_template(f'{PATH_URL2}/form_libro.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))




@app.route('/form-registrar-libro', methods=['POST'])
def formLibro():

            resultado = procesar_form_libro(request.form)
            if resultado:
                return redirect(url_for('lista_libros'))
            else:
                flash('El libro NO fue registrado.', 'error')
                return render_template(f'{PATH_URL2}/form_libro.html')

@app.route('/lista-de-libros-user', methods=['GET'])
def lista_libros2():
    if 'conectado' in session:
        return render_template(f'{PATH_URL2}/lista_libros2.html', libros=sql_lista_librosBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/lista-de-libros', methods=['GET'])
def lista_libros():
    if 'conectado' in session:
        return render_template(f'{PATH_URL2}/lista_libros.html', libros=sql_lista_librosBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))



###############################

@app.route("/detalles-libro/", methods=['GET'])
@app.route("/detalles-libro/<int:idLibro>", methods=['GET'])
def detalleLibro(idLibro=None):
    if 'conectado' in session:
        # Verificamos si el parámetro idLibro es None o no está presente en la URL
        if idLibro is None:
            return redirect(url_for('inicio'))
        else:
            detalle_libro = sql_detalles_librosBD(idLibro) or []
            return render_template(f'{PATH_URL2}/detalles_libro.html', detalle_libro=detalle_libro)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))



###

# Buscadon de libros
@app.route("/buscando-libro", methods=['POST'])
def viewBuscarLibroBD():

    resultadoBusqueda = buscarLibroBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL2}/resultado_busqueda_libro.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})


@app.route("/editar-libro/<int:id>", methods=['GET'])
def viewEditarLibro(id):
    if 'conectado' in session:
        respuestaLibro = buscarLibroUnico(id)
        if respuestaLibro:
            return render_template(f'{PATH_URL2}/form_libro_update.html', respuestaLibro=respuestaLibro)
        else:
            flash('El libro no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Recibir formulario para actulizar informacion de libro
@app.route('/actualizar-libro', methods=['POST'])
def actualizarLibro():
    resultData = procesar_actualizacion_formlib(request)
    if resultData:
        return redirect(url_for('lista_libros'))

@app.route('/borrar-libro/<string:id_libro>', methods=['GET'])
def borrarLibro(id_libro):
    resp = eliminarLibro(id_libro)
    if resp:
        flash('El Libro fue eliminado correctamente', 'success')
        return redirect(url_for('lista_libros'))
























