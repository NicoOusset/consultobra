-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 16-09-2021 a las 14:02:38
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
  `Oficial_especializado` float NOT NULL,
  `Oficial` float NOT NULL,
  `Medio_oficial` float NOT NULL,
  `Ayudante` float NOT NULL,
  `RubroId` int(11) NOT NULL,
  `Activo` varchar(2) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `items`
--

INSERT INTO `items` (`Id`, `Nombre`, `Unidad`, `Materiales`, `Obreros`, `Herramental`, `Cargas_sociales`, `Comentario`, `Oficial_especializado`, `Oficial`, `Medio_oficial`, `Ayudante`, `RubroId`, `Activo`) VALUES
(1001, 'Excavación en Espacios Abiertos', 'm3', 0, 1000.63, 49.4826, 943.603, 'Comentario\n\nIncluye Cava, Perfilado y Paleo de la tierra hasta un punto cercano a la excavación desde donde va a ser retirada o utilizada para relleno. No incluye movimiento de masas de tierra hasta otros sectores más lejanos (en tal caso tendrá que ser considerado por aparte). Dado que el Perfilado es considerado en este caso igual a la cava, la totalidad de lo aflojado se considera cava. Se considera a la tierra a palear como masa esponjada ya que se ha aflojado con la cava y no necesariamente debe conservar la cohesión de partículas. En este caso el ítem es realizado en espacios abiertos.\n\nNota: Los tiempos obreros son estimativos, no se debe considerar esto como una receta exacta, cada grupo constructor tiene su  rendimiento.\n\nIncidencias\n\nMano de Obra: \n\n-Medio Oficial Movimiento de Suelos: 4.33Hs\n\nHerramental:\n\n-Carretilla 90L\n-Pala Ancha, Pala de Punta y/o Pico \n-Guantes de Descarne\n-Lentes Protectores\n-Casco Amarillo (Personal Operativo)\n-Barbijo', 0, 0, 4.37, 0, 1, ''),
(1002, 'Excavación en Espacios Reducidos', 'm3', 0, 1240.78, 61.3584, 1170.07, 'Comentario\n\nIncluye Cava, Perfilado y Paleo de la tierra hasta un punto cercano a la excavación desde donde va a ser retirada o utilizada para relleno. No incluye movimiento de masas de tierra hasta otros sectores más lejanos (en tal caso tendrá que ser considerado por aparte). Dado que el Perfilado es considerado en este caso igual a la cava, la totalidad de lo aflojado se considera cava. Se considera a la tierra a palear como masa esponjada ya que se ha aflojado con la cava y no necesariamente debe conservar la cohesión de partículas.\n\nNota: Los tiempos obreros son estimativos, no se debe considerar esto como una receta exacta, cada grupo constructor tiene su  rendimiento.\n\nIncidencias\n\nMano de Obra: \n\n-Medio Oficial Movimiento de Suelos: 4.33Hs\n\nHerramental:\n\n-Carretilla 90L\n-Pala Ancha, Pala de Punta y/o Pico \n-Guantes de Descarne\n-Lentes Protectores\n-Casco Amarillo (Personal Operativo)\n-Barbijo', 0, 0, 5.41, 0, 1, ''),
(1003, 'Relleno y Compactación (relleno comprado)', 'm3', 1294.49, 1420.06, 95.1871, 1339.14, 'Comentario\n\nIncluye el movimiento de masas de relleno hasta el lugar de relleno y el costo de material de relleno comprado, el paleo de relleno de la tierra esponjada calculada con esponjamiento remanente y el apisonado de la cantidad de tierra necesaria que entraría en un perfil de 1m3.  \n\nMano de Obra:\n\n-Medio Oficial Movimiento de Suelos: 16.89 Hs\n-Ayudante Movimiento de Materiales: 2.33 Hs\n\n\nNota: Los tiempos obreros son estimativos, no se debe considerar esto como una receta exacta, cada grupo constructor tiene su rendimiento. Se encarece debido al movimiento de material que hay que hacer para poner la tierra comprada en el punto de relleno.\n\nMateriales: \n\n-Agua (para compactación): 10L\n-Tierra (para relleno): 1.15m3 \n\nNota: la cantidad utilizada es mínima y bajo la técnica del riego a aspersión.\n\nHerramental\n\n-Pisón Compactador Manual\n-Carretilla 90L\n-Carretel Enrollador de Manguera\n-Manguera de Riego x 30ml\n-Pala Ancha, Pala de Punta y/o Pico \n-Guantes de Descarne\n-Lentes Protectores\n-Casco Amarillo (Personal Operativo)\n-Barbijo', 0, 0, 5.13, 1.24, 1, ''),
(1004, 'Relleno y Compactación (relleno de obra)', 'm3', 0.0135076, 638.088, 33.4194, 601.722, 'Comentario\n\nIncluye el paleo de relleno de la tierra esponjada calculada con esponjamiento remanente y el apisonado de la cantidad de tierra necesaria que entraría en un perfil de 1m3. No tiene en cuenta el material ya que es reutilización de tierra de excavación.  \n\nMano de Obra\n\n-Medio Oficial Movimiento de Suelos: 5.78 Hs\n\nNota: Los tiempos obreros son estimativos, no se debe considerar esto como una receta exacta, cada grupo constructor tiene su  rendimiento.\n\nMateriales\n\nAgua (para compactación) \n\nNota: la cantidad utilizada es mínima y bajo la técnica del riego a aspersión.\n\nHerramental\n\n-Pisón Compactador Manual\n-Carretel Enrollador de Manguera\n-Manguera de Riego x 30ml\n-Pala Ancha, Pala de Punta y/o Pico \n-Guantes de Descarne\n-Lentes Protectores\n-Casco Amarillo (Personal Operativo)\n-Barbijo', 0, 0, 2.78, 0, 1, ''),
(1005, 'Retiro de Tierra Manual (Carretilla 130L)', 'm3', 0, 504.85, 39.5624, 476.082, 'Comentario\n\nIncluye el movimiento de masas de relleno hasta el lugar de relleno y el costo de material de relleno comprado, el paleo de relleno de la tierra esponjada calculada con esponjamiento remanente y el apisonado de la cantidad de tierra necesaria que entraría en un perfil de 1m3.  \n\nNota: Si no conoce la cantidad de tierra sobrante en la obra, es posible estimarla con una planilla de cálculo subida en página www.consultobra.com siguiendo el link  a continuación. Usted debe colocar los volúmenes que pide la planilla y luego calcular el retiro en función del valor de tierra sobrante aproximada. Recuerde que es un dato aproximado.\n\nMano de Obra:\n\n-Medio Oficial Movimiento de Suelos: 2.24 Hs\n-Ayudante Movimiento de Suelos: 1.93 Hs\n\n\nNota: Los tiempos obreros son estimativos, no se debe considerar esto como una receta exacta, cada grupo constructor tiene su rendimiento. Se encarece debido al movimiento de material que hay que hacer para poner la tierra comprada en el punto de relleno.\n\nHerramental\n\n-Pala Ancha, Pala de Punta\n-Carretilla 90L \n-Guantes de Descarne\n-Lentes Protectores\n-Casco Amarillo (Personal Operativo)\n-Barbijo', 0, 0, 1.42, 0.91, 1, ''),
(5001, 'Mamp. HCCA 10x25x50 Masa Adhesiva', 'm2', 2371.77, 284.223, 18.1519, 268.025, '', 0, 0, 0, 0, 5, ''),
(5010, 'Mamp.Bloques H° 19x19x39 Masa Adhesiva', 'm2', 1725.97, 461.143, 29.6231, 434.863, '', 0, 0, 0, 0, 5, ''),
(5011, 'Mamp.Bloques H° 19x19x39 Mezcla de Asiento', 'm2', 1122.91, 447.012, 37.7611, 421.65, '', 0, 0, 0, 0, 5, ''),
(5012, 'Mamp.L.Hueco 12x18x25 Masa Adhesiva', 'm2', 1169.07, 598.01, 36.8007, 563.929, '', 0, 0, 0, 0, 5, ''),
(5013, 'Mamp.L.Hueco 12x18x25 Mezcla de Asiento', 'm2', 875.319, 716.621, 68.3724, 676.091, '', 0, 0, 0, 0, 5, ''),
(5014, 'Mamp.L.Hueco 12x18x33 Masa Adhesiva', 'm2', 1249.53, 458.832, 28.1425, 432.683, '', 0, 0, 0, 0, 5, ''),
(5015, 'Mamp.L.Hueco 12x18x33 Mezcla de Asiento', 'm2', 926.004, 583.959, 56.4902, 550.943, '', 0, 0, 0, 0, 5, ''),
(5016, 'Mamp.L.Hueco 18x18x25 Masa Adhesiva', 'm2', 1523.08, 598.01, 36.8007, 563.929, '', 0, 0, 0, 0, 5, ''),
(5017, 'Mamp.L.Hueco 18x18x25 Mezcla de Asiento', 'm2', 1239.95, 773.91, 78.9196, 730.205, '', 0, 0, 0, 0, 5, ''),
(5018, 'Mamp.L.Hueco 18x18x33 Masa Adhesiva', 'm2', 1517.71, 458.832, 28.1425, 432.683, '', 0, 0, 0, 0, 5, ''),
(5019, 'Mamp.L.Hueco 18x18x33 Mezcla de Asiento', 'm2', 1215.72, 637.787, 66.1758, 601.785, '', 0, 0, 0, 0, 5, ''),
(5002, 'Mamp. HCCA 12.5x25x50 Masa Adhesiva', 'm2', 2524.26, 284.223, 18.1519, 268.025, '', 0, 0, 0, 0, 5, ''),
(5020, 'Mamp.L.Hueco 8x18x25 Masa Adhesiva', 'm2', 1091.63, 598.01, 36.8007, 563.929, '', 0, 0, 0, 0, 5, ''),
(5021, 'Mamp.L.Hueco 8x18x25 Mezcla de Asiento', 'm2', 768.039, 678.429, 61.341, 640.015, '', 0, 0, 0, 0, 5, ''),
(5022, 'Mamp.L.Hueco 8x18x33 Masa Adhesiva', 'm2', 1165.72, 458.832, 28.1425, 432.683, '', 0, 0, 0, 0, 5, ''),
(5023, 'Mamp.L.Hueco 8x18x33 Mezcla de Asiento', 'm2', 815.699, 548.073, 50.033, 517.048, '', 0, 0, 0, 0, 5, ''),
(5024, 'Mamp.L.Hueco Port.12x19x33 Mezc.de Asiento', 'm2', 1512.21, 426.885, 35.2965, 402.671, '', 0, 0, 0, 0, 5, ''),
(5025, 'Mamp.L.Hueco Port.18x19x33 Mezc.de Asiento', 'm2', 1776.73, 426.885, 35.2965, 402.671, '', 0, 0, 0, 0, 5, ''),
(5026, 'Mamp.L.Macizo 0.05 Mez.Asiento no vista', 'm2', 435.708, 240.653, 20.5761, 227.024, '', 0, 0, 0, 0, 5, ''),
(5027, 'Mamp.L.Macizo 0.15 Mez.Asiento no vista', 'm2', 1074.05, 607.619, 65.97, 573.38, '', 0, 0, 0, 0, 5, ''),
(5028, 'Mamp.L.Macizo 0.20 Mez.Asiento no vista', 'm2', 1598.14, 898.716, 112.141, 848.251, '', 0, 0, 0, 0, 5, ''),
(5029, 'Mamp.L.Macizo 0.30 Mez.Asiento no vista', 'm2', 2209.51, 1220.03, 139.948, 1151.37, '', 0, 0, 0, 0, 5, ''),
(5003, 'Mamp. HCCA 15x25x50 Masa Adhesiva', 'm2', 3078.05, 284.223, 18.1519, 268.025, '', 0, 0, 0, 0, 5, ''),
(5004, 'Mamp. HCCA 15x25x60 Masa Adhesiva', 'm2', 2612.76, 239.743, 15.2579, 226.08, '', 0, 0, 0, 0, 5, ''),
(5005, 'Mamp. HCCA 17.5x25x50 Masa Adhesiva', 'm2', 3519.47, 284.223, 18.1519, 268.025, '', 0, 0, 0, 0, 5, ''),
(5006, 'Mamp. HCCA 20x25x50 Masa Adhesiva', 'm2', 3976.95, 284.223, 18.1519, 268.025, '', 0, 0, 0, 0, 5, ''),
(5007, 'Mamp. HCCA 7.5x25x50 Masa Adhesiva', 'm2', 1689.57, 284.223, 18.1519, 268.025, '', 0, 0, 0, 0, 5, ''),
(5008, 'Mamp.Bloques H° 13x19x39 Masa Adhesiva', 'm2', 1553.26, 461.143, 29.6231, 434.863, '', 0, 0, 0, 0, 5, ''),
(5009, 'Mamp.Bloques H° 13x19x39 Mezcla de Asiento', 'm2', 968.401, 447.012, 37.7611, 421.65, '', 0, 0, 0, 0, 5, ''),
(7001, 'Azotado Hidrófugo', 'm2', 285.663, 110.791, 13.2946, 104.564, '', 0, 0, 0, 0, 7, ''),
(7002, 'Rev. Grueso + Azot. Hid. Fratasado', 'm2', 347.083, 344.468, 32.0065, 325.011, '', 0, 0, 0, 0, 7, ''),
(7003, 'Rev. Grueso + Azot. Hid. Mandilado', 'm2', 347.083, 363.365, 32.8142, 342.831, '', 0, 0, 0, 0, 7, ''),
(7004, 'Rev. Grueso + Azot. Hid. Regleado', 'm2', 347.083, 269.153, 28.776, 253.989, '', 0, 0, 0, 0, 7, ''),
(7005, 'Rev. Grueso Hid. + Azotado Hid. Fratasado', 'm2', 396.358, 350.838, 34.4305, 331.041, '', 0, 0, 0, 0, 7, ''),
(7006, 'Rev. Grueso Hid. + Azotado Hid. Mandilado', 'm2', 396.358, 369.735, 35.2382, 348.861, '', 0, 0, 0, 0, 7, ''),
(7007, 'Rev. Grueso Hid. + Azotado Hid. Regleado', 'm2', 396.358, 275.523, 31.2, 260.02, '', 0, 0, 0, 0, 7, ''),
(7008, 'Rev. Fino Exterior a la Cal Prem. Mandil.', 'm2', 85.1059, 105.269, 5.38203, 99.2718, '', 0, 0, 0, 0, 7, ''),
(7009, 'Rev. Fino Interior a la Cal Prem. Mandil.', 'm2', 66.0725, 105.269, 5.38203, 99.2718, '', 0, 0, 0, 0, 7, '');

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

--
-- Volcado de datos para la tabla `rubros`
--

INSERT INTO `rubros` (`Id`, `Nombre`, `Activo`) VALUES
(1, 'MOVIMINTO DE SUELOS', 'Si'),
(5, 'MAMPOSTERÍAS', 'Si'),
(7, 'REVOQUES', 'Si');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
