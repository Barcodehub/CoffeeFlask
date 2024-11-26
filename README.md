# SystemCoffee

## Table of Contents

1. [Project Overview](#project-overview)
2. [Endpoints API](#endpoints-api)
   1. [Nosotros](#nosotros)
   2. [Historia](#historia)
   3. [Productos](#productos)
   4. [Usuarios](#usuarios)
   5. [Mesas](#mesas)
   6. [Reservas](#reservas)
   7. [Carrito](#carrito)
   8. [Facturas](#facturas)
3. [Installation and Setup](#installation-and-setup)
   1. [Requisitos previos](#requisitos-previos)
   2. [Pasos de instalación](#pasos-de-instalación)
4. [Documentación Adicional](#documentación-adicional)
5. [Demostración](#demostración)

---

# Project Overview

Este proyecto es una aplicación web dinámica diseñada para gestionar varios aspectos de una cafeteria, incluyendo la administración de usuarios, productos, mesas, reservas, y facturación. Ofrece un flujo completo para usuarios autenticados, desde agregar productos a un carrito hasta completar un proceso de checkout con generación de facturas en PDF.

## Características principales:
- Gestión dinámica de secciones como "Nosotros" e "Historia".
- CRUD para usuarios, productos, mesas y reservas.
- Carrito de compras integrado con proceso de pago y generación de facturas.
- Administración de menú y categorías de productos
- Funcionalidades específicas para roles administrativos, como liberar mesas y generar reportes.
- Recuperación y actualización de contraseñas con tokens seguros.
- API modular basada en Flask, con endpoints organizados para facilitar futuras expansiones.

## Tecnologías utilizadas:
- **Backend:** Flask (Python).
- **Base de datos:** MySQL.
- **Frontend:** Jinja2 para plantillas dinámicas.
- **Dependencias adicionales:** Generación de PDFs, conexión segura a bases de datos y manejo de sesiones.

# Endpoints API

## Nosotros
- **GET** `/mi-nosotros`: Muestra la lista de información de "Nosotros".
- **GET** `/editar-nosotros/<int:id>`: Carga el formulario para editar un elemento específico de "Nosotros".
- **POST** `/actualizar-nosotro`: Recibe datos para actualizar un elemento de "Nosotros".

## Historia
- **GET** `/mi-historia`: Muestra la información de "Historia".
- **GET** `/editar-historia/<int:id_titulos>/<int:id_imagenes>/<int:id_parrafos>`: Carga el formulario para editar la "Historia".
- **POST** `/actualizar-historia`: Actualiza la información de la "Historia".

## Productos
- **GET** `/registrar-producto`: Carga el formulario para registrar un producto.
- **POST** `/form-registrar-producto`: Recibe datos para registrar un nuevo producto.
- **GET** `/lista-de-productos`: Lista todos los productos disponibles.
- **POST** `/buscando-producto`: Busca productos en la base de datos.
- **GET** `/editar-producto/<int:id>`: Carga el formulario para editar un producto específico.
- **POST** `/actualizar-producto`: Actualiza los datos de un producto.
- **GET** `/borrar-producto/<string:id_producto>/<string:foto_producto>`: Elimina un producto y su imagen asociada.

## Usuarios
- **GET** `/lista-de-usuarios`: Lista todos los usuarios registrados.
- **GET** `/editar-usuario/<int:id>`: Carga el formulario para editar un usuario específico.
- **POST** `/actualizar-usuario`: Actualiza los datos de un usuario.
- **GET** `/borrar-usuario/<string:id>`: Elimina un usuario.
- **POST** `/buscando-usuario`: Busca usuarios en la base de datos.

## Mesas
- **GET** `/registrar-mesa`: Carga el formulario para registrar una mesa.
- **POST** `/form-registrar-mesa`: Recibe datos para registrar una nueva mesa.
- **GET** `/lista-de-mesas`: Lista todas las mesas disponibles.
- **POST** `/buscando-mesa`: Busca mesas en la base de datos.
- **GET** `/editar-mesa/<int:id>`: Carga el formulario para editar una mesa específica.
- **POST** `/actualizar-mesa`: Actualiza los datos de una mesa.
- **GET** `/borrar-mesa/<string:id_mesa>`: Elimina una mesa.

## Reservas
- **GET** `/lista-de-reservas`: Lista todas las reservas.
- **GET** `/lista-de-reservasUser`: Lista reservas específicas de un usuario.
- **POST** `/form-registrar-reserva`: Registra una nueva reserva.
- **GET** `/liberar-mesa/<int:id_mesa>`: Libera una mesa ocupada.

## Carrito
- **GET** `/agregar-al-carrito/<int:id_producto>`: Agrega un producto al carrito.
- **GET** `/carrito`: Muestra el contenido del carrito.
- **POST** `/actualizar_cantidad/<int:id_producto>`: Actualiza la cantidad de un producto en el carrito.
- **GET** `/eliminar_del_carrito/<int:id_producto>`: Elimina un producto del carrito.

## Facturas
- **GET** `/lista-de-facturas`: Lista todas las facturas.
- **GET** `/factura_exito/<int:factura_id>`: Muestra el detalle de una factura específica.
- **GET** `/factura_pdf/<int:factura_id>`: Genera un PDF de una factura.

# Installation and Setup

## Requisitos previos
1. **Python 3.8.5** (especificado en `runtime.txt`).
2. **MySQL Server** instalado y configurado.
3. Administrador de paquetes `pip` para instalar las dependencias desde `requirements.txt`.

## Pasos de instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/Barcodehub/CoffeeFlask.git
   ```
   
2. **Instalar las dependencias: Asegúrate de estar en un entorno virtual antes de instalar**:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Configurar las variables de entorno: Crea un archivo .env en la raíz del proyecto con el siguiente contenido**:

   ```bash
   DB_HOST=localhost
   DB_USER=tu_usuario
   DB_PASSWORD=tu_contraseña
   DB_NAME=nombre_de_la_base_datos
   DB_PORT=3306
   SECRET_KEY=clave_secreta_segura
   ```
Asegúrate de reemplazar tu_usuario, tu_contraseña, y nombre_de_la_base_datos con las credenciales correctas.

4. **Configurar la base de datos**:

- Crea la base de datos en MySQL.
- Ejecutar la aplicación en localhost

La aplicación estará disponible en http://localhost:5000.

6. **(Opcional) entorno de producción**: La aplicación está lista para ser desplegada en un entorno de producción como Railway

## Documentación Adicional

La documentación completa del proyecto está disponible en [este PDF](./my-app/static/Documentacion.docx.pdf).

## Demostración

Para ver una demostración de la aplicación en funcionamiento, puedes ver este video:

[![SystemCoffee](https://img.youtube.com/vi/OsYlgKAi5ZA/0.jpg)](https://www.youtube.com/watch?v=OsYlgKAi5ZA)
