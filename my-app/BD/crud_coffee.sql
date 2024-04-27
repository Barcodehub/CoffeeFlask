-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 27-04-2024 a las 23:12:06
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `crud_coffee`
--
CREATE DATABASE IF NOT EXISTS `crud_coffee` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `crud_coffee`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carritos`
--

CREATE TABLE `carritos` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carrito_productos`
--

CREATE TABLE `carrito_productos` (
  `id` int(11) NOT NULL,
  `carrito_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `edicion_dinamica`
--

CREATE TABLE `edicion_dinamica` (
  `id_edicion` int(11) NOT NULL,
  `nosotros_titulo` text DEFAULT NULL,
  `nosotros_parrafo` text DEFAULT NULL,
  `nosotros_imagen` mediumtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `edicion_dinamica`
--

INSERT INTO `edicion_dinamica` (`id_edicion`, `nosotros_titulo`, `nosotros_parrafo`, `nosotros_imagen`) VALUES
(1, 'Sobre Nosotross', 'Bienvenidos a Cafeé-Cafeé, un lugar donde la pasión por el café se encuentra con la comodidad de un hogar. Nuestra cafetería, ubicada en el corazón de la ciudad, es un espacio acogedor y vibrante que invita a los amantes del café a disfrutar de una taza de su bebida favorita en un ambiente relajado y amigable.En Café-Café, nos enorgullece servir café de la más alta calidad, seleccionado cuidadosamente de los mejores productores de café del mundo. Nuestros baristas expertos se dedican a preparar cada taza con precisión y amor, asegurando que cada sorbo que tomes sea una experiencia inolvidable.Ya sea que estés buscando un lugar para comenzar tu día con energía, una pausa tranquila en medio de una tarde ajetreada, o un espacio acogedor para encontrarte con amigos, Café-Café es tu destino. ¡Ven y únete a nosotros para una taza de café hoy! ¡Te esperamos con los brazos abiertos!', '0ebbf05a0622462498e1c81aa359b39239cd0ce16f094ab180a6f952b91a5b50.jpg'),
(2, 'Cafe-Cafe', 'Imaginamos un mundo donde el café no es solo una bebida, sino una puerta de entrada a un universo de sabores, aromas y conexiones significativas. Queremos liderar la revolución digital en la industria del café, siendo pioneros en la entrega de experiencias únicas a través de nuestra plataforma web y app.', 'cafeteria_nosotros.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `edicion_imagen`
--

CREATE TABLE `edicion_imagen` (
  `id_imagen` int(11) NOT NULL,
  `imagen1` mediumtext DEFAULT NULL,
  `imagen2` mediumtext DEFAULT NULL,
  `imagen3` mediumint(9) DEFAULT NULL,
  `imagen4` mediumtext DEFAULT NULL,
  `imagen5` mediumtext DEFAULT NULL,
  `imagen6` mediumtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `edicion_imagen`
--

INSERT INTO `edicion_imagen` (`id_imagen`, `imagen1`, `imagen2`, `imagen3`, `imagen4`, `imagen5`, `imagen6`) VALUES
(1, 'cafeteria_nosotros.jpg', NULL, NULL, NULL, NULL, NULL),
(2, '0ebbf05a0622462498e1c81aa359b39239cd0ce16f094ab180a6f952b91a5b50.jpg', NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `edicion_parrafo`
--

CREATE TABLE `edicion_parrafo` (
  `id_parrafo` int(11) NOT NULL,
  `parrafo1` text NOT NULL,
  `parrafo2` text NOT NULL,
  `parrafo3` text NOT NULL,
  `parrafo4` text NOT NULL,
  `parrafo5` text NOT NULL,
  `parrafo6` text NOT NULL,
  `parrafo7` text NOT NULL,
  `parrafo8` text NOT NULL,
  `parrafo9` text NOT NULL,
  `parrafo10` text NOT NULL,
  `parrafo11` text NOT NULL,
  `parrafo12` text NOT NULL,
  `parrafo13` text NOT NULL,
  `parrafo14` text NOT NULL,
  `parrafo15` text NOT NULL,
  `parrafo16` text NOT NULL,
  `parrafo17` text NOT NULL,
  `parrafon` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `edicion_parrafo`
--

INSERT INTO `edicion_parrafo` (`id_parrafo`, `parrafo1`, `parrafo2`, `parrafo3`, `parrafo4`, `parrafo5`, `parrafo6`, `parrafo7`, `parrafo8`, `parrafo9`, `parrafo10`, `parrafo11`, `parrafo12`, `parrafo13`, `parrafo14`, `parrafo15`, `parrafo16`, `parrafo17`, `parrafon`) VALUES
(1, 'En Cafe-Cafe, nuestra misión es brindar a nuestros clientes una experiencia única y acogedora, ofreciendo cafés de alta calidad y un servicio excepcional. Nos esforzamos por crear un ambiente donde nuestros clientes puedan relajarse, disfrutar de un buen café y sentirse como en casa.', 'Nuestra visión es ser reconocidos como la cafetería de elección en nuestra comunidad, conocidos por nuestra responsabilidad social y ambiental. Aspiramos a ser un lugar donde las personas se reúnan, se conecten y compartan ideas, todo mientras disfrutan de un delicioso café.', 'Cafe-Cafe fue fundada en 2020 por dos amantes del café con el sueño de crear un espacio donde la gente pudiera disfrutar de un buen café en un ambiente cálido y acogedor. Desde entonces, hemos crecido y nos hemos convertido en un punto de referencia en nuestra comunidad. Nuestra historia es una de pasión por el café, dedicación al servicio al cliente y compromiso con nuestra comunidad.', 'Hace unos años, un grupo apasionado por el café se unió con el objetivo de llevar la experiencia cafetera a nuevas alturas, fusionando la tradición del café con la innovación tecnológica. Así nació Cafe-Cafe, una cafetería que no solo ofrece exquisitas bebidas, sino que también transforma la forma en que disfrutas de tu café diario.', 'No es solo una cafetería; es una marca que representa la unión entre la artesanía del café y la comodidad moderna. Nuestra identidad se refleja en cada detalle, desde la cuidadosa selección de granos de café hasta la interfaz intuitiva de nuestra appweb. Nos enorgullece ser un espacio donde la tradición y la tecnología se abrazan, creando una experiencia única para nuestros clientes.', 'En Cafe-Cafe, nos comprometemos a proporcionar un servicio excepcional a todos nuestros clientes. Nuestra política de servicio incluye lo siguiente:', 'Nos esforzamos por ofrecer productos de la más alta calidad, utilizando solo los mejores ingredientes. Nuestro café es seleccionado cuidadosamente y preparado con precisión para garantizar un sabor excepcional en cada taza.', 'Nuestro personal está siempre disponible para ayudarte con cualquier pregunta o inquietud que puedas tener. Nos enorgullece nuestro amable y eficiente servicio al cliente, y estamos comprometidos a hacer que cada visita a Cafe-Cafe sea una experiencia positiva.', 'Nos esforzamos por mantener un ambiente limpio, cómodo y acogedor para todos nuestros clientes. Nuestra cafetería es un lugar donde puedes relajarte, trabajar o simplemente disfrutar de la compañía de amigos.', 'Nos tomamos muy en serio nuestra responsabilidad hacia nuestros clientes, nuestro personal y nuestro medio ambiente. Estamos comprometidos con prácticas comerciales éticas y sostenibles, y nos esforzamos por hacer una diferencia positiva en nuestra comunidad.', 'Gracias por elegir Cafe-Cafe. Valoramos tu apoyo y esperamos verte pronto.', 'En Cafe-Cafe, ofrecemos una variedad de cafés para satisfacer todos los gustos. Desde nuestro espresso fuerte y robusto hasta nuestro café con leche suave y cremoso, hay algo para todos. También ofrecemos una selección de cafés especiales y de temporada.', 'Sí, en Cafe-Cafe ofrecemos un conveniente servicio de entrega a domicilio a través de nuestra aplicación. Puedes disfrutar de nuestros deliciosos productos en la comodidad de tu hogar u oficina.', 'Puedes hacer una reservación directamente desde nuestra aplicación. Solo necesitas seleccionar la fecha y el número de personas para la reservación. Te recomendamos hacer la reservación con al menos 24 horas de anticipación para asegurar tu mesa.', 'Sí, en Cafe-Cafe ofrecemos un menú completo que incluye opciones para el desayuno, almuerzo y cena. Nuestro menú varía según la temporada y siempre incluye opciones frescas y deliciosas.', 'Sí, ofrecemos una variedad de opciones de panadería y postres. Desde croissants recién horneados hasta pasteles decadentes, hay algo para satisfacer cualquier antojo dulce.', 'Sí, puedes hacer un pedido en línea a través de nuestra aplicación. Simplemente selecciona los productos que deseas, añádelos a tu carrito y realiza el pago. Tu pedido estará listo para recoger en la cafetería o lo entregaremos en tu dirección.', 'Imaginamos un mundo donde el café no es solo una bebida, sino una puerta de entrada a un universo de sabores, aromas y conexiones significativas. Queremos liderar la revolución digital en la industria del café, siendo pioneros en la entrega de experiencias únicas a través de nuestra plataforma web y app.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `edicion_titulo`
--

CREATE TABLE `edicion_titulo` (
  `id_titulo` int(11) NOT NULL,
  `titulo1` text NOT NULL,
  `titulo2` text NOT NULL,
  `titulo3` text NOT NULL,
  `titulo4` text NOT NULL,
  `titulo5` text NOT NULL,
  `titulo6` text NOT NULL,
  `titulo7` text NOT NULL,
  `titulo8` text NOT NULL,
  `subtitulo1` text NOT NULL,
  `subtitulo2` text NOT NULL,
  `subtitulo3` text NOT NULL,
  `subtitulo4` text NOT NULL,
  `subtitulo5` text NOT NULL,
  `subtitulo6` text NOT NULL,
  `subtitulo7` text NOT NULL,
  `subtitulo8` text NOT NULL,
  `subtitulo9` text NOT NULL,
  `subtitulo10` text NOT NULL,
  `subtitulo11` text NOT NULL,
  `subtitulo12` text NOT NULL,
  `subtitulo13` text NOT NULL,
  `subtitulo14` text NOT NULL,
  `subtitulo15` text NOT NULL,
  `subtitulo16` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `edicion_titulo`
--

INSERT INTO `edicion_titulo` (`id_titulo`, `titulo1`, `titulo2`, `titulo3`, `titulo4`, `titulo5`, `titulo6`, `titulo7`, `titulo8`, `subtitulo1`, `subtitulo2`, `subtitulo3`, `subtitulo4`, `subtitulo5`, `subtitulo6`, `subtitulo7`, `subtitulo8`, `subtitulo9`, `subtitulo10`, `subtitulo11`, `subtitulo12`, `subtitulo13`, `subtitulo14`, `subtitulo15`, `subtitulo16`) VALUES
(1, 'Nuestra Historia', 'Política de Servicio', 'Preguntas Frecuentes', '', '', '', '', '', 'Misión', 'Visión', 'Historia', 'Calidad', 'Atención al cliente', 'Entorno', 'Responsabilidad', '¿Qué tipos de café ofrecen en Cafe-Cafe?', '¿Ofrecen servicio a domicilio?', '¿Cómo puedo hacer una reservación?', '¿Ofrecen opciones de comida para el desayuno, almuerzo y cena?', '¿Tienen opciones de panadería y postres?', '¿Puedo hacer un pedido en línea a través de la aplicación?', '', '', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `facturas`
--

CREATE TABLE `facturas` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `usuario_nombre` varchar(100) NOT NULL,
  `fecha` datetime NOT NULL DEFAULT current_timestamp(),
  `total` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `facturas`
--

INSERT INTO `facturas` (`id`, `usuario_id`, `usuario_nombre`, `fecha`, `total`) VALUES
(8, 7, 'Alexander', '2024-04-24 22:26:29', 7500.00),
(9, 7, 'Alexander', '2024-04-24 22:27:06', 62500.00),
(10, 10, 'eee eee2', '2024-04-24 22:28:01', 32500.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `factura_productos`
--

CREATE TABLE `factura_productos` (
  `id` int(11) NOT NULL,
  `factura_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `factura_productos`
--

INSERT INTO `factura_productos` (`id`, `factura_id`, `producto_id`, `cantidad`, `precio`) VALUES
(6, 8, 3, 3, 2500.00),
(7, 9, 1, 10, 5000.00),
(8, 9, 3, 5, 2500.00),
(9, 10, 1, 5, 5000.00),
(10, 10, 3, 3, 2500.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id_rol` int(11) NOT NULL,
  `descripcion` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id_rol`, `descripcion`) VALUES
(1, 'admin'),
(2, 'usuario'),
(3, 'mesero');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tbl_mesas`
--

CREATE TABLE `tbl_mesas` (
  `id_mesa` int(11) NOT NULL,
  `nombre_mesa` varchar(25) NOT NULL,
  `cantidad_mesa` int(11) NOT NULL,
  `disponible_mesa` tinyint(1) NOT NULL DEFAULT 1,
  `id_mesero` int(11) NOT NULL DEFAULT 7,
  `fecha_mesa` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `tbl_mesas`
--

INSERT INTO `tbl_mesas` (`id_mesa`, `nombre_mesa`, `cantidad_mesa`, `disponible_mesa`, `id_mesero`, `fecha_mesa`) VALUES
(8, 'Mesa Familiar', 4, 1, 7, '2023-12-07'),
(18, 'mesa22', 13, 1, 8, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tbl_productos`
--

CREATE TABLE `tbl_productos` (
  `id_producto` int(11) NOT NULL,
  `nombre_producto` varchar(50) NOT NULL,
  `precio_producto` double NOT NULL,
  `categoria_producto` int(11) DEFAULT NULL,
  `foto_producto` mediumtext DEFAULT NULL,
  `cantidad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `tbl_productos`
--

INSERT INTO `tbl_productos` (`id_producto`, `nombre_producto`, `precio_producto`, `categoria_producto`, `foto_producto`, `cantidad`) VALUES
(1, 'Capucchino', 5000, 8, '8773c1ed41424812975ebc69d24a2105d9710aa0d07f40ad873329a698f16baf.jpg', 0),
(3, 'Tinto', 2500, 8, '2ebeabc46d86427cb5cd8a5038db4882226987c37918447395f296d96c9ea48b.jpg', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tbl_reservas`
--

CREATE TABLE `tbl_reservas` (
  `id_reserva` int(11) NOT NULL,
  `fecha_reserva` date NOT NULL,
  `precio_reserva` double DEFAULT 80000,
  `cantidad_reserva` int(11) NOT NULL,
  `id_mesa` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `tbl_reservas`
--

INSERT INTO `tbl_reservas` (`id_reserva`, `fecha_reserva`, `precio_reserva`, `cantidad_reserva`, `id_mesa`, `id_usuario`) VALUES
(13, '2023-12-07', 80000, 4, 8, 9);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name_surname` varchar(100) NOT NULL,
  `email_user` varchar(50) NOT NULL,
  `pass_user` text NOT NULL,
  `created_user` timestamp NOT NULL DEFAULT current_timestamp(),
  `id_rol` int(11) DEFAULT 2
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `name_surname`, `email_user`, `pass_user`, `created_user`, `id_rol`) VALUES
(6, 'Brayan Barco', 'alex.barco.maicol@gmail.com', 'scrypt:32768:8:1$fcpPZONENIY0lYUt$f2ffea23b5e06838a998c8c77fbfdcb4cbf20b268706738ab5a44d7f5e1b2c3b8e6dbf5deb45e66c35299de37909583cda6cd8839708e4c0d359a7ce1e593ef2', '2023-11-05 22:20:46', 1),
(7, 'Alexander', 'elbarcosan@gmail.com', 'scrypt:32768:8:1$4FlJHUMLlS7XvE6J$d669f116f0b532bdd9ffe6ba464c4681900991748cac5498596f6aab13e9106ac85dce97bfb58ff8911bd8193f648463933594e83c2481fa2a4559a30fe898a9', '2023-11-05 22:21:50', 3),
(8, 'Claudia', 'claudiayamilegomez@gmail.com', 'scrypt:32768:8:1$XUa1fT9zGFABp2Me$25d1bd8d61a0c6c2292d35dd3f4746feb05aac7c7fcde4fb83ee7b6661402a6b8246dcd820e5bad041a0647b8ab0ff05fc9604911d54e77b5e4e506c18ad3fad', '2023-11-15 14:05:50', 3),
(9, 'Brayan Alexander Barco', 'brayanalexanderbc@ufps.edu.co', 'scrypt:32768:8:1$oXwqs2bkX34Iws5o$471f2cddd391c31cba5c9508a008cadcace9e7ae78f6b53c814c076f5b13e87bbe941ac8682f2c917c02f6e4fc6df22d9b8940647bd1a7e83fdf9fadfbb1a60f', '2023-12-05 19:23:31', 2),
(10, 'eee eee2', 'alexbarco28@gmail.com', 'scrypt:32768:8:1$TFCeAPJjGRDumf9h$c4f6c26232dfcb46e78c7d5c2a6aefdc7f2017f0f9dcbef1e5158fe50e0f54a2c6e75389f49403fa1d5759bd14d85d85a975b4db22059eff73fc959e91f015d1', '2024-04-24 00:09:22', 2);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `carritos`
--
ALTER TABLE `carritos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `carrito_productos`
--
ALTER TABLE `carrito_productos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `producto_id` (`producto_id`),
  ADD KEY `carrito_productos_ibfk_1` (`carrito_id`);

--
-- Indices de la tabla `edicion_dinamica`
--
ALTER TABLE `edicion_dinamica`
  ADD PRIMARY KEY (`id_edicion`);

--
-- Indices de la tabla `edicion_imagen`
--
ALTER TABLE `edicion_imagen`
  ADD PRIMARY KEY (`id_imagen`);

--
-- Indices de la tabla `edicion_parrafo`
--
ALTER TABLE `edicion_parrafo`
  ADD PRIMARY KEY (`id_parrafo`);

--
-- Indices de la tabla `edicion_titulo`
--
ALTER TABLE `edicion_titulo`
  ADD PRIMARY KEY (`id_titulo`);

--
-- Indices de la tabla `facturas`
--
ALTER TABLE `facturas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `usuario_nombre` (`usuario_nombre`);

--
-- Indices de la tabla `factura_productos`
--
ALTER TABLE `factura_productos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `producto_id` (`producto_id`),
  ADD KEY `factura_productos_ibfk_1` (`factura_id`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id_rol`);

--
-- Indices de la tabla `tbl_mesas`
--
ALTER TABLE `tbl_mesas`
  ADD PRIMARY KEY (`id_mesa`),
  ADD KEY `id_mesero` (`id_mesero`);

--
-- Indices de la tabla `tbl_productos`
--
ALTER TABLE `tbl_productos`
  ADD PRIMARY KEY (`id_producto`);

--
-- Indices de la tabla `tbl_reservas`
--
ALTER TABLE `tbl_reservas`
  ADD PRIMARY KEY (`id_reserva`),
  ADD KEY `id_mesa` (`id_mesa`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_rol` (`id_rol`),
  ADD KEY `name_surname` (`name_surname`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `carritos`
--
ALTER TABLE `carritos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `carrito_productos`
--
ALTER TABLE `carrito_productos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `edicion_dinamica`
--
ALTER TABLE `edicion_dinamica`
  MODIFY `id_edicion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `edicion_imagen`
--
ALTER TABLE `edicion_imagen`
  MODIFY `id_imagen` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `edicion_parrafo`
--
ALTER TABLE `edicion_parrafo`
  MODIFY `id_parrafo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `edicion_titulo`
--
ALTER TABLE `edicion_titulo`
  MODIFY `id_titulo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `facturas`
--
ALTER TABLE `facturas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `factura_productos`
--
ALTER TABLE `factura_productos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `tbl_mesas`
--
ALTER TABLE `tbl_mesas`
  MODIFY `id_mesa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de la tabla `tbl_productos`
--
ALTER TABLE `tbl_productos`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `tbl_reservas`
--
ALTER TABLE `tbl_reservas`
  MODIFY `id_reserva` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `carritos`
--
ALTER TABLE `carritos`
  ADD CONSTRAINT `carritos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `users` (`id`);

--
-- Filtros para la tabla `carrito_productos`
--
ALTER TABLE `carrito_productos`
  ADD CONSTRAINT `carrito_productos_ibfk_1` FOREIGN KEY (`carrito_id`) REFERENCES `carritos` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `carrito_productos_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `tbl_productos` (`id_producto`);

--
-- Filtros para la tabla `facturas`
--
ALTER TABLE `facturas`
  ADD CONSTRAINT `facturas_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `users` (`id`);

--
-- Filtros para la tabla `factura_productos`
--
ALTER TABLE `factura_productos`
  ADD CONSTRAINT `factura_productos_ibfk_1` FOREIGN KEY (`factura_id`) REFERENCES `facturas` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `factura_productos_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `tbl_productos` (`id_producto`);

--
-- Filtros para la tabla `tbl_mesas`
--
ALTER TABLE `tbl_mesas`
  ADD CONSTRAINT `tbl_mesas_ibfk_1` FOREIGN KEY (`id_mesero`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `tbl_mesas_ibfk_2` FOREIGN KEY (`id_mesero`) REFERENCES `users` (`id`);

--
-- Filtros para la tabla `tbl_reservas`
--
ALTER TABLE `tbl_reservas`
  ADD CONSTRAINT `tbl_reservas_ibfk_1` FOREIGN KEY (`id_mesa`) REFERENCES `tbl_mesas` (`id_mesa`),
  ADD CONSTRAINT `tbl_reservas_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `users` (`id`);

--
-- Filtros para la tabla `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
