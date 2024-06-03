from conexion.conexionBD import connectionBD  # Conexión a BD
#################################33

def insertar_log_cambio(log_cambio):
    try:
        print("sas")
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                query = "INSERT INTO log_cambios (tabla, accion, datos_anteriores, datos_nuevos, usuario_id) VALUES (%s, %s, %s, %s, %s)"
                valores = (log_cambio['tabla'], log_cambio['accion'], log_cambio['datos_anteriores'], log_cambio['datos_nuevos'], log_cambio['usuario_id'])
                cursor.execute(query, valores)
            conexion_MySQLdb.commit()
    except Exception as e:
        print(f"Error al insertar el registro de cambio: {e}")

def obtener_log_cambios():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                query = "SELECT lc.*, u.name_surname AS usuario_nombre FROM log_cambios lc JOIN users u ON lc.usuario_id = u.id ORDER BY lc.fecha_hora DESC"
                cursor.execute(query)
                log_cambios = cursor.fetchall()
                return log_cambios
    except Exception as e:
        print(f"Error al obtener los registros de cambios: {e}")
        return []
###########################333