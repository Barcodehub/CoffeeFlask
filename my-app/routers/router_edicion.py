from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error


# Importando cenexión a BD
from controllers.funciones_edicion import *


PATH_URL2 = "public/library"





#edicion dinamica - Nosotros

# @app.route('/mi-nosotros', methods=['GET'])
# def nosotros():
#     return render_template(f'public/library/nosotros.html')
@app.route('/mi-nosotros', methods=['GET'])
def lista_nosotros():
    return render_template(f'{PATH_URL2}/nosotros.html', nosotros=sql_lista_nosotrosBD())


@app.route("/editar-nosotros/<int:id>", methods=['GET'])
def viewEditarNosotros(id):
    if 'conectado' in session:
        respuestaNosotro = buscarNosotroUnico(id)
        if respuestaNosotro:
            return render_template(f'{PATH_URL2}/form_nosotros_update.html', respuestaNosotro=respuestaNosotro)
        else:
            flash('no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Recibir formulario para actulizar informacion de Nosotros
@app.route('/actualizar-nosotro', methods=['POST'])
def actualizarNosotro():
    resultData = procesar_actualizacion_formNosotro(request)
    if resultData:
        return redirect(url_for('lista_nosotros'))























#edicion dinamica - Historia

@app.route('/mi-historia', methods=['GET'])
def lista_historia():
    return render_template(f'{PATH_URL2}/historia.html',  titulos=sql_lista_titulosBD(), parrafos=sql_lista_parrafosBD(), imagenes=sql_lista_imagenesBD())

@app.route("/editar-historia/<int:id_titulos>/<int:id_imagenes>/<int:id_parrafos>", methods=['GET'])
def viewEditarHistoria(id_titulos, id_imagenes, id_parrafos):
    if 'conectado' in session:
        respuestaHistoria = buscarHistoriaUnico(id_titulos, 'edicion_titulo')
        respuestaImagenes = buscarHistoriaUnico(id_imagenes, 'edicion_imagen')
        respuestaParrafos = buscarHistoriaUnico(id_parrafos, 'edicion_parrafo')

        if respuestaHistoria and respuestaImagenes and respuestaParrafos:
            return render_template(f'{PATH_URL2}/form_historia_update.html', respuestaHistoria=respuestaHistoria, respuestaImagenes=respuestaImagenes, respuestaParrafos=respuestaParrafos)
        else:
            flash('no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Recibir formulario para actulizar informacion de Historias

@app.route('/actualizar-historia', methods=['POST'])
def actualizarHistoria():
    resultDataTitulo = procesar_actualizacion_formHistoria(request, 'edicion_titulo')
    resultDataParrafo = procesar_actualizacion_formHistoria(request, 'edicion_parrafo')
    resultDataImagen = procesar_actualizacion_formHistoria(request, 'edicion_imagen')
    if resultDataTitulo and resultDataParrafo and resultDataImagen:
        return redirect(url_for('lista_historia'))

