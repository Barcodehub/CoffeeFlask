import mysql.connector
import os

def connectionBD():
    try:
        host = "roundhouse.proxy.rlwy.net"
        user = "root"
        password = "PfZTYRCskvvFoLJFfFSSKsqKXQmAPxqu"
        database = "railway"
        port = 12437

        connection = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            database=database,
            port=port,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            raise_on_warnings=True
        )

        if connection.is_connected():
            print("Conexión exitosa a la BD")
            return connection
        else:
            print("No se pudo establecer la conexión con la base de datos.")
            return None

    except mysql.connector.Error as error:
        print(f"No se pudo conectar a MySQL: {error}")
        return None
