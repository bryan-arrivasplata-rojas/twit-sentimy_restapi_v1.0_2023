-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 23-10-2023 a las 09:34:24
-- Versión del servidor: 10.4.27-MariaDB
-- Versión de PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `twit_sentimy`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `card`
--

CREATE TABLE `card` (
  `idCard` int(10) NOT NULL,
  `number` varchar(20) NOT NULL,
  `date` varchar(6) NOT NULL,
  `ccv` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `card`
--

INSERT INTO `card` (`idCard`, `number`, `date`, `ccv`) VALUES
(1, '1111222233334444', '01/27', 253);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `profile`
--

CREATE TABLE `profile` (
  `idProfile` int(10) NOT NULL,
  `name_profile` varchar(100) NOT NULL,
  `lastname` varchar(100) NOT NULL,
  `birthdate` date NOT NULL,
  `idUser` int(10) NOT NULL,
  `idRole` int(10) NOT NULL,
  `idCard` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `profile`
--

INSERT INTO `profile` (`idProfile`, `name_profile`, `lastname`, `birthdate`, `idUser`, `idRole`, `idCard`) VALUES
(1, 'Bryan Daniell', 'Arrivasplata Rojas', '1999-02-15', 1, 1, NULL),
(2, 'Chrystian Alexander', 'Castro Tineo', '2023-10-02', 2, 2, NULL),
(3, 'Ricardo Daniel', 'Santibañez Ricra', '2023-10-01', 3, 3, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `role`
--

CREATE TABLE `role` (
  `idRole` int(10) NOT NULL,
  `name_role` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `role`
--

INSERT INTO `role` (`idRole`, `name_role`) VALUES
(1, 'admin'),
(2, 'user_basic'),
(3, 'user_premium');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `transaction`
--

CREATE TABLE `transaction` (
  `idTransaction` int(10) NOT NULL,
  `idProfile` int(10) NOT NULL,
  `created_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tweet`
--

CREATE TABLE `tweet` (
  `idTweet` int(10) NOT NULL,
  `identifier` varchar(100) NOT NULL,
  `name_tweet` varchar(100) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tweet`
--

INSERT INTO `tweet` (`idTweet`, `identifier`, `name_tweet`, `created_at`) VALUES
(2, '1234567489646465', 'prueba', '2023-10-22 20:47:36'),
(3, '5645641532fdg64dfg', 'prueba_2', '2023-10-22 20:48:16'),
(9, '12345674896464fg65abcdeee', 'prueba', '2023-10-23 01:03:55'),
(10, '1716114478528385189', 'prueba', '2023-10-23 01:29:53'),
(11, '1716117662449734067', 'prueba', '2023-10-23 01:51:50');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tweet_user`
--

CREATE TABLE `tweet_user` (
  `idTweetUser` int(10) NOT NULL,
  `idTweet` int(10) NOT NULL,
  `idUser` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tweet_user`
--

INSERT INTO `tweet_user` (`idTweetUser`, `idTweet`, `idUser`) VALUES
(1, 2, 2),
(2, 3, 3),
(3, 2, 3),
(9, 9, 3),
(10, 10, 3),
(11, 11, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user`
--

CREATE TABLE `user` (
  `idUser` int(10) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `user`
--

INSERT INTO `user` (`idUser`, `username`, `password`) VALUES
(1, 'admin', '123456'),
(2, 'userb', '123456'),
(3, 'userp', '123456');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `card`
--
ALTER TABLE `card`
  ADD PRIMARY KEY (`idCard`),
  ADD UNIQUE KEY `number` (`number`);

--
-- Indices de la tabla `profile`
--
ALTER TABLE `profile`
  ADD PRIMARY KEY (`idProfile`),
  ADD KEY `profile_user` (`idUser`),
  ADD KEY `profile_role` (`idRole`),
  ADD KEY `profile_card` (`idCard`);

--
-- Indices de la tabla `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`idRole`),
  ADD UNIQUE KEY `description_role` (`name_role`);

--
-- Indices de la tabla `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`idTransaction`),
  ADD KEY `transaction_profile` (`idProfile`);

--
-- Indices de la tabla `tweet`
--
ALTER TABLE `tweet`
  ADD PRIMARY KEY (`idTweet`);

--
-- Indices de la tabla `tweet_user`
--
ALTER TABLE `tweet_user`
  ADD PRIMARY KEY (`idTweetUser`),
  ADD KEY `tweet_user_user` (`idUser`),
  ADD KEY `tweet_user_tweet` (`idTweet`);

--
-- Indices de la tabla `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`idUser`),
  ADD UNIQUE KEY `user` (`username`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `card`
--
ALTER TABLE `card`
  MODIFY `idCard` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `profile`
--
ALTER TABLE `profile`
  MODIFY `idProfile` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `role`
--
ALTER TABLE `role`
  MODIFY `idRole` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `transaction`
--
ALTER TABLE `transaction`
  MODIFY `idTransaction` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tweet`
--
ALTER TABLE `tweet`
  MODIFY `idTweet` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `tweet_user`
--
ALTER TABLE `tweet_user`
  MODIFY `idTweetUser` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `user`
--
ALTER TABLE `user`
  MODIFY `idUser` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `profile`
--
ALTER TABLE `profile`
  ADD CONSTRAINT `profile_card` FOREIGN KEY (`idCard`) REFERENCES `card` (`idCard`),
  ADD CONSTRAINT `profile_role` FOREIGN KEY (`idRole`) REFERENCES `role` (`idRole`),
  ADD CONSTRAINT `profile_user` FOREIGN KEY (`idUser`) REFERENCES `user` (`idUser`);

--
-- Filtros para la tabla `transaction`
--
ALTER TABLE `transaction`
  ADD CONSTRAINT `transaction_profile` FOREIGN KEY (`idProfile`) REFERENCES `profile` (`idProfile`);

--
-- Filtros para la tabla `tweet_user`
--
ALTER TABLE `tweet_user`
  ADD CONSTRAINT `tweet_user_tweet` FOREIGN KEY (`idTweet`) REFERENCES `tweet` (`idTweet`),
  ADD CONSTRAINT `tweet_user_user` FOREIGN KEY (`idUser`) REFERENCES `user` (`idUser`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
