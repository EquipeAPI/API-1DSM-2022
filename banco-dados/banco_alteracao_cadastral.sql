CREATE DATABASE  IF NOT EXISTS `banco` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `banco`;
-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: banco
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alteracao_cadastral`
--

DROP TABLE IF EXISTS `alteracao_cadastral`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alteracao_cadastral` (
  `id_alteracao` int NOT NULL AUTO_INCREMENT,
  `nome_alteracao` varchar(100) DEFAULT NULL,
  `genero_alteracao` set('Feminino','Masculino','Outro','Prefiro não informar') DEFAULT NULL,
  `rua_avenida_alteracao` varchar(100) DEFAULT NULL,
  `numero_alteracao` varchar(5) DEFAULT NULL,
  `bairro_alteracao` varchar(50) DEFAULT NULL,
  `cidade_alteracao` varchar(50) DEFAULT NULL,
  `estado_alteracao` varchar(20) DEFAULT NULL,
  `senha_alteracao` varchar(16) DEFAULT NULL,
  `data_nascimento_alteracao` date DEFAULT NULL,
  `id_usuario` int NOT NULL,
  `numero_agencia` int NOT NULL,
  PRIMARY KEY (`id_alteracao`),
  KEY `fk_alteracao_usuario` (`id_usuario`),
  KEY `fk_alteracao_agencia` (`numero_agencia`),
  CONSTRAINT `fk_alteracao_agencia` FOREIGN KEY (`numero_agencia`) REFERENCES `gerente_agencia` (`numero_agencia`),
  CONSTRAINT `fk_alteracao_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


ALTER TABLE alteracao_cadastral ADD data_nascimento_alteracao date;

--
-- Dumping data for table `alteracao_cadastral`
--

LOCK TABLES `alteracao_cadastral` WRITE;
/*!40000 ALTER TABLE `alteracao_cadastral` DISABLE KEYS */;
/*!40000 ALTER TABLE `alteracao_cadastral` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-10-06 19:00:56
