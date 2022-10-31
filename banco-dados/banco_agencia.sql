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
-- Table structure for table `agencia`
--

DROP TABLE IF EXISTS `agencia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `agencia` (
  `numero_agencia` int NOT NULL AUTO_INCREMENT,
  `numero_matricula` int NOT NULL,
  `nome_agencia` varchar(50) NOT NULL,
  `rua_avenida_agencia` varchar(100) NOT NULL,
  `numero_local_agencia` varchar(5) NOT NULL,
  `bairro_agencia` varchar(50) NOT NULL,
  `cidade_agencia` varchar(50) NOT NULL,
  `estado_agencia` varchar(20) NOT NULL,
  PRIMARY KEY (`numero_agencia`),
  KEY `fk_agencia_gerente` (`numero_matricula`),
  CONSTRAINT `fk_agencia_gerente` FOREIGN KEY (`numero_matricula`) REFERENCES `gerente_geral` (`numero_matricula`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

update agencia set nome_agencia = 'Guará São Paulo', rua_avenida_agencia = 'Avenida Paulista', numero_local_agencia = 80, bairro_agencia = 'Centro', cidade_agencia = 'São Paulo', estado_agencia = 'SP' where numero_matricula = 2;
update agencia set nome_agencia = 'Guará Jacareí', rua_avenida_agencia = 'Barão de Jacareí', numero_local_agencia = 21, bairro_agencia = 'Centro', cidade_agencia = 'Jacareí', estado_agencia = 'SP' where numero_matricula = 3;
/*!40101 SET character_set_client = @saved_cs_client */;
--
-- Dumping data for table `agencia`
--


LOCK TABLES `agencia` WRITE;
/*!40000 ALTER TABLE `agencia` DISABLE KEYS */;
INSERT INTO `agencia` VALUES (1,2,'','','','','',''),(2,3,'','','','','','');
/*!40000 ALTER TABLE `agencia` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-10-28 15:51:13
