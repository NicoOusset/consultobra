-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 30-11-2021 a las 15:51:24
-- Versión del servidor: 5.7.31
-- Versión de PHP: 7.3.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `consultobra`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `a_quien_llamo`
--

DROP TABLE IF EXISTS `a_quien_llamo`;
CREATE TABLE IF NOT EXISTS `a_quien_llamo` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Categoria` int(11) NOT NULL,
  `Nombre` varchar(60) NOT NULL,
  `Apellido` varchar(60) NOT NULL,
  `Telefono` varchar(60) NOT NULL,
  `Direccion` varchar(500) NOT NULL,
  `Facebook` varchar(200) NOT NULL,
  `Instagram` varchar(200) NOT NULL,
  `Activo` varchar(2) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `a_quien_llamo`
--

INSERT INTO `a_quien_llamo` (`Id`, `Categoria`, `Nombre`, `Apellido`, `Telefono`, `Direccion`, `Facebook`, `Instagram`, `Activo`) VALUES
(1, 2, 'Martin', 'Aguirre', '381732165488', 'Mendoza 654', 'Facebook/martinAguirre', 'Instagram/martin_aguirre', 'Si'),
(2, 1, 'Juan Pedro', 'Gomez', '38199571512', 'Salta 1584', 'Facebook/JuanGomez', 'Instagram/Juan_Gomez', 'Si'),
(3, 3, 'Alberto', 'Lopez', '3819951629', 'Maipu 972', 'Facebook/AlbertoLopez', 'Instagram/Alberto_Lopez', 'Si');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

DROP TABLE IF EXISTS `categorias`;
CREATE TABLE IF NOT EXISTS `categorias` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `NombreCategoria` varchar(60) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`Id`, `NombreCategoria`) VALUES
(1, 'Electricista'),
(2, 'Plomero'),
(3, 'Carpintero'),
(4, 'Gasista');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `items`
--

DROP TABLE IF EXISTS `items`;
CREATE TABLE IF NOT EXISTS `items` (
  `Id` int(11) NOT NULL,
  `Nombre` varchar(60) NOT NULL,
  `Unidad` varchar(15) NOT NULL,
  `Materiales` float NOT NULL,
  `Obreros` float NOT NULL,
  `Herramental` float NOT NULL,
  `Cargas_sociales` float NOT NULL,
  `Comentario` varchar(5000) NOT NULL,
  `RubroId` int(11) NOT NULL,
  `Activo` varchar(2) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rubros`
--

DROP TABLE IF EXISTS `rubros`;
CREATE TABLE IF NOT EXISTS `rubros` (
  `Id` int(11) NOT NULL,
  `Nombre` varchar(60) NOT NULL,
  `Activo` varchar(2) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
