import mysql.connector
import os

def connectionBD():
    try:
        # Obtener las variables de entorno
        host = os.getenv("DB_HOST")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        database = os.getenv("DB_NAME")
        port = int(os.getenv("DB_PORT"))

        # Establecer la conexión
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
