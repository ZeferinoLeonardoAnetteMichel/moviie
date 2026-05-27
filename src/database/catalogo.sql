-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         10.4.32-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.13.0.7147
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para catalogo
CREATE DATABASE IF NOT EXISTS `catalogo` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `catalogo`;

-- Volcando estructura para tabla catalogo.contenido
CREATE TABLE IF NOT EXISTS `contenido` (
  `id_contenido` int(11) NOT NULL AUTO_INCREMENT,
  `título` varchar(150) NOT NULL,
  `descripción` text DEFAULT NULL,
  `año_lanzamiento` year(4) DEFAULT NULL,
  `clasificación` varchar(20) DEFAULT NULL,
  `duración` int(11) DEFAULT NULL,
  `tipo_contenido` enum('Película','Serie') NOT NULL,
  `imagen_portada` varchar(255) DEFAULT NULL,
  `género` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_contenido`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla catalogo.contenido: ~0 rows (aproximadamente)
DELETE FROM `contenido`;

-- Volcando estructura para tabla catalogo.disponibilidad
CREATE TABLE IF NOT EXISTS `disponibilidad` (
  `id_disponibilidad` int(11) NOT NULL AUTO_INCREMENT,
  `id_contenido` int(11) NOT NULL,
  `id_plataforma` int(11) NOT NULL,
  `visualización_del_enlace` varchar(500) DEFAULT NULL,
  `calidad` varchar(50) DEFAULT NULL,
  `idioma` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_disponibilidad`),
  KEY `fk_disponibilidad_contenido` (`id_contenido`),
  KEY `fk_disponibilidad_plataforma` (`id_plataforma`),
  CONSTRAINT `fk_disponibilidad_contenido` FOREIGN KEY (`id_contenido`) REFERENCES `contenido` (`id_contenido`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_disponibilidad_plataforma` FOREIGN KEY (`id_plataforma`) REFERENCES `plataforma_streaming` (`id_plataforma`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla catalogo.disponibilidad: ~0 rows (aproximadamente)
DELETE FROM `disponibilidad`;

-- Volcando estructura para tabla catalogo.favoritos
CREATE TABLE IF NOT EXISTS `favoritos` (
  `id_favorito` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) NOT NULL,
  `id_contenido` int(11) NOT NULL,
  `fecha_agregado` date DEFAULT NULL,
  PRIMARY KEY (`id_favorito`),
  KEY `fk_favoritos_usuario` (`id_usuario`),
  KEY `fk_favoritos_contenido` (`id_contenido`),
  CONSTRAINT `fk_favoritos_contenido` FOREIGN KEY (`id_contenido`) REFERENCES `contenido` (`id_contenido`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_favoritos_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla catalogo.favoritos: ~0 rows (aproximadamente)
DELETE FROM `favoritos`;

-- Volcando estructura para tabla catalogo.pelicula
CREATE TABLE IF NOT EXISTS `pelicula` (
  `id_pelicula` int(11) NOT NULL,
  `recaudación` decimal(15,2) DEFAULT NULL,
  `estudio` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_pelicula`),
  CONSTRAINT `fk_pelicula_contenido` FOREIGN KEY (`id_pelicula`) REFERENCES `contenido` (`id_contenido`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla catalogo.pelicula: ~0 rows (aproximadamente)
DELETE FROM `pelicula`;

-- Volcando estructura para tabla catalogo.pelicula_favorita
CREATE TABLE IF NOT EXISTS `pelicula_favorita` (
  `id_favorito` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) NOT NULL,
  `titulo` varchar(255) DEFAULT NULL,
  `anio` varchar(10) DEFAULT NULL,
  `rating` varchar(10) DEFAULT NULL,
  `plataforma` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_favorito`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `pelicula_favorita_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla catalogo.pelicula_favorita: ~2 rows (aproximadamente)
DELETE FROM `pelicula_favorita`;
INSERT INTO `pelicula_favorita` (`id_favorito`, `id_usuario`, `titulo`, `anio`, `rating`, `plataforma`) VALUES
	(4, 2, 'Superman, Spiderman or Batman', '2011', 'N/A', 'Max'),
	(5, 2, 'Spiderman', '1990', 'N/A', 'Netflix');

-- Volcando estructura para tabla catalogo.plataforma_streaming
CREATE TABLE IF NOT EXISTS `plataforma_streaming` (
  `id_plataforma` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `logo` varchar(255) DEFAULT NULL,
  `url_principal` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_plataforma`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla catalogo.plataforma_streaming: ~0 rows (aproximadamente)
DELETE FROM `plataforma_streaming`;

-- Volcando estructura para tabla catalogo.serie
CREATE TABLE IF NOT EXISTS `serie` (
  `id_serie` int(11) NOT NULL,
  `cantidad_temporadas` int(11) DEFAULT NULL,
  `estado_serie` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_serie`),
  CONSTRAINT `fk_serie_contenido` FOREIGN KEY (`id_serie`) REFERENCES `contenido` (`id_contenido`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla catalogo.serie: ~0 rows (aproximadamente)
DELETE FROM `serie`;

-- Volcando estructura para tabla catalogo.usuario
CREATE TABLE IF NOT EXISTS `usuario` (
  `id_usuario` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `fecha_registro` date DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `apellido` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla catalogo.usuario: ~1 rows (aproximadamente)
DELETE FROM `usuario`;
INSERT INTO `usuario` (`id_usuario`, `nombre`, `fecha_registro`, `email`, `apellido`, `password`) VALUES
	(1, 'Anette Michel', '2026-05-13', 'anette@gmail.com', 'Zeferino Leonardo', '$2b$12$TxdiTbPQHvqcdeNdBCe2Au32mmwrogGoTTCz9L.B26qYevFrZNHDm'),
	(2, 'andrea', '2026-05-18', 'zeferinoo.anette@gmail.com', 'leonardo', '$2b$12$nHnpUC1NDRI0MzayCAXAI./PbhdS0g5McGTw0G7BpNHplalIWOzkW');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
