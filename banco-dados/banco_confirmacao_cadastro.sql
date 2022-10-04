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
-- Table structure for table `confirmacao_cadastro`
--

DROP TABLE IF EXISTS `confirmacao_cadastro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `confirmacao_cadastro` (
  `id_cadastro` int NOT NULL AUTO_INCREMENT,
  `nome_cadastro` varchar(100) NOT NULL,
  `cpf_cadastro` varchar(14) NOT NULL,
  `data_naascimento_cadastro` date NOT NULL,
  `genero_cadastro` set('Feminino','Masculino','Outros','Prefiro não informar') NOT NULL,
  `senha_cadastro` varchar(16) NOT NULL,
  `rua_avenida_cadastro` varchar(100) NOT NULL,
  `numero_casa_cadastro` varchar(5) NOT NULL,
  `bairro_cadastro` varchar(50) NOT NULL,
  `cidade_cadastro` varchar(50) NOT NULL,
  `estado_cadastro` varchar(20) NOT NULL,
  `numero_agencia` int NOT NULL,
  PRIMARY KEY (`id_cadastro`),
  KEY `fk_cadastro_agencia` (`numero_agencia`),
  CONSTRAINT `fk_cadastro_agencia` FOREIGN KEY (`numero_agencia`) REFERENCES `gerente_agencia` (`numero_agencia`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `confirmacao_cadastro`
--

LOCK TABLES `confirmacao_cadastro` WRITE;
/*!40000 ALTER TABLE `confirmacao_cadastro` DISABLE KEYS */;
/*!40000 ALTER TABLE `confirmacao_cadastro` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-10-04 18:48:53
