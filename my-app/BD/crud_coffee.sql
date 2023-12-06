-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 06-12-2023 a las 02:33:46
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
-- Estructura de tabla para la tabla `tbl_empleados`
--

CREATE TABLE `tbl_empleados` (
  `id_empleado` int(11) NOT NULL,
  `nombre_empleado` varchar(50) DEFAULT NULL,
  `apellido_empleado` varchar(50) DEFAULT NULL,
  `sexo_empleado` int(11) DEFAULT NULL,
  `telefono_empleado` varchar(50) DEFAULT NULL,
  `email_empleado` varchar(50) DEFAULT NULL,
  `profesion_empleado` varchar(50) DEFAULT NULL,
  `foto_empleado` mediumtext DEFAULT NULL,
  `salario_empleado` bigint(20) DEFAULT NULL,
  `fecha_registro` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `tbl_empleados`
--

INSERT INTO `tbl_empleados` (`id_empleado`, `nombre_empleado`, `apellido_empleado`, `sexo_empleado`, `telefono_empleado`, `email_empleado`, `profesion_empleado`, `foto_empleado`, `salario_empleado`, `fecha_registro`) VALUES
(4, 'Urian', 'Viera', 1, '54544454', 'programadorphp2017@gmail.com', 'Ingeniero de Sistemas', 'fda30f83ebbc4fb1a2ce2609b2b1e34c6614c1dff6e44460b9ba27ed5bb8e927.png', 3500000, '2023-08-23 17:04:49'),
(5, 'Brenda', 'Viera', 2, '323543543', 'brenda@gmail.com', 'Dev', '22c055aeec314572a0046ec50b84f21719270dac6ea34c91b8380ac289fff9e5.png', 1200000, '2023-08-23 17:05:34'),
(6, 'Alejandro', 'Torres', 1, '324242342', 'alejandro@gmail.com', 'Tecnico', '7b84aceb56534d27aa2e8b727a245dca9f60156a070a47c491ff2d21da1742e5.png', 2100, '2023-08-23 17:06:13'),
(7, 'Karla', 'Ramos', 2, '345678', 'karla@gmail.com', 'Ingeniera', '248cc9c38cfb494bb2300d7cbf4a3b317522f295338b4639a8e025e6b203291c.png', 2300, '2023-08-23 17:07:28'),
(8, 'juan', 'sas', 1, '551515', 'ess@dd.com', 'empleado', 'f0d7f7fc718d40cd816f8a85bb57b7a9efa99fd7e1df422590952e06756e3cb8', 200, '2023-11-03 03:04:09');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tbl_libro`
--

CREATE TABLE `tbl_libro` (
  `id_libro` int(11) NOT NULL,
  `codigo_libro` varchar(45) DEFAULT NULL,
  `nombre_libro` varchar(45) DEFAULT NULL,
  `autor_libro` varchar(45) DEFAULT NULL,
  `genero_libro` int(45) DEFAULT NULL,
  `fecha_libro` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `tbl_libro`
--

INSERT INTO `tbl_libro` (`id_libro`, `codigo_libro`, `nombre_libro`, `autor_libro`, `genero_libro`, `fecha_libro`) VALUES
(3, 'hh1', 'solo leveling', 'aughun', 1, '2023-10-30'),
(5, 'sasman', 'ses', 'sas', 1, '2023-11-15'),
(6, 'hh2', 'solo leveling 2', 'aughun', 1, '2023-11-08'),
(7, 'hh22', 'One Piece', 'Furione', 1, '2023-10-30'),
(8, 'hh3', 'Voldemort', 'Furione', 1, '2023-10-30'),
(9, 'hh4', 'Haruhi Suzumiya', 'Furione', 1, '2023-10-30'),
(10, 'hh5', 'Sirenoman y chico percebe', 'Furione', 1, '2023-10-30'),
(11, 'hh6', 'Alasyrstruka', 'Mao Hmmmand', 2, '2023-10-30'),
(12, 'hh7', 'cleancode', 'Furione', 1, '2023-10-30'),
(13, 'hh8', 'Coffe book', 'Furione', 1, '2023-10-30'),
(17, 'hh12', '100 años de soledad', 'Furione', 1, '2023-10-30'),
(18, 'hh13', 'coronel', 'Furione', 1, '2023-10-30'),
(19, 'hh14', 'Hojarazca22', 'Furione22', 3, '2023-10-30'),
(21, 'h335', 'La divina Comedia', 'Dante alighari', 1, '2023-11-25');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tbl_mesas`
--

CREATE TABLE `tbl_mesas` (
  `id_mesa` int(11) NOT NULL,
  `nombre_mesa` varchar(25) NOT NULL,
  `cantidad_mesa` int(11) NOT NULL,
  `disponible_mesa` tinyint(1) NOT NULL DEFAULT 1,
  `id_mesero` int(11) NOT NULL DEFAULT 7
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `tbl_mesas`
--

INSERT INTO `tbl_mesas` (`id_mesa`, `nombre_mesa`, `cantidad_mesa`, `disponible_mesa`, `id_mesero`) VALUES
(8, 'Mesa Familiar', 4, 1, 7),
(18, 'mesa22', 13, 1, 8);

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
(3, 'Tinto', 2500, 1, '2ebeabc46d86427cb5cd8a5038db4882226987c37918447395f296d96c9ea48b.jpg');

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
-- Indices de la tabla `tbl_empleados`
--
ALTER TABLE `tbl_empleados`
  ADD PRIMARY KEY (`id_empleado`);

--
-- Indices de la tabla `tbl_libro`
--
ALTER TABLE `tbl_libro`
  ADD PRIMARY KEY (`id_libro`);

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
-- AUTO_INCREMENT de la tabla `tbl_empleados`
--
ALTER TABLE `tbl_empleados`
  MODIFY `id_empleado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `tbl_libro`
--
ALTER TABLE `tbl_libro`
  MODIFY `id_libro` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

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
-- Filtros para la tabla `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
