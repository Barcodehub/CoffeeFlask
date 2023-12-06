-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 06-12-2023 a las 22:04:56
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.0.28

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
  `foto_producto` mediumtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `tbl_productos`
--

INSERT INTO `tbl_productos` (`id_producto`, `nombre_producto`, `precio_producto`, `categoria_producto`, `foto_producto`) VALUES
(1, 'Capucchino', 5000, 8, '8773c1ed41424812975ebc69d24a2105d9710aa0d07f40ad873329a698f16baf.jpg'),
(3, 'Tinto', 2500, 8, '2ebeabc46d86427cb5cd8a5038db4882226987c37918447395f296d96c9ea48b.jpg');

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
(9, 'Brayan Alexander Barco', 'brayanalexanderbc@ufps.edu.co', 'scrypt:32768:8:1$oXwqs2bkX34Iws5o$471f2cddd391c31cba5c9508a008cadcace9e7ae78f6b53c814c076f5b13e87bbe941ac8682f2c917c02f6e4fc6df22d9b8940647bd1a7e83fdf9fadfbb1a60f', '2023-12-05 19:23:31', 2);

--
-- Índices para tablas volcadas
--

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
  ADD KEY `id_rol` (`id_rol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Restricciones para tablas volcadas
--

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
