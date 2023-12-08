from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error


# Importando cenexión a BD
from controllers.funciones_home import *

PATH_URL = "public/perfil"
PATH_URL2 = "public/library"
PATH_URL3 = "public/usuarios"
PATH_URL4 = "public/productos"
PATH_URL5 = "public/mesas"
PATH_URL6 = "public/reservas"
PATH_URL_LOGIN = "public/login"


@app.route('/mi-historia', methods=['GET'])
def historia():
        return render_template(f'public/library/historia.html')







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
        return render_template(f'{PATH_URL4}/lista_productos.html', productos=sql_lista_productosBD())
   



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
        return render_template(f'{PATH_URL5}/lista_mesas.html', mesas=sql_lista_mesasBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route("/buscando-mesa", methods=['POST'])
def viewBuscarMesaBD():

    resultadoBusqueda = buscarMesaBD(request.json['busqueda'])
    if resultadoBusqueda:
        print(resultadoBusqueda)
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
    resultData = procesar_actualizacion_formMesa(request)
    if resultData:
        return redirect(url_for('lista_mesas'))

@app.route('/borrar-mesa/<string:id_mesa>', methods=['GET'])
def borrarMesa(id_mesa):
    resp = eliminarMesa(id_mesa)
    if resp:
        flash('El mesa fue eliminado correctamente', 'success')
        return redirect(url_for('lista_mesas'))








#RESERVAS






@app.route('/registrar-reserva', methods=['GET'])
def viewFormReserva():
    if 'conectado' in session:
        return render_template(f'{PATH_URL6}/form_reserva.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return render_template(f'{PATH_URL_LOGIN}/base_login.html')




@app.route('/form-registrar-reserva', methods=['POST'])
def formReserva():
            resultado = procesar_form_reserva(request.form, session['id'])
            if resultado:
                return redirect(url_for('inicio')) #vista de factura, porque lista es para admin
            else:
                flash('El mesa NO fue registrado.', 'error')
                return render_template(f'{PATH_URL6}/form_reserva.html')


































