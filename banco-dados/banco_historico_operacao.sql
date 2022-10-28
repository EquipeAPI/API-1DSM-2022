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
-- Table structure for table `historico_operacao`
--

DROP TABLE IF EXISTS `historico_operacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historico_operacao` (
  `id_operacao` int NOT NULL AUTO_INCREMENT,
  `data_hora_operacao` datetime NOT NULL,
  `data_hora_confirmacao` datetime DEFAULT NULL,
  `saldo_operacao` double NOT NULL,
  `valor_operacao` double NOT NULL,
  `tipo_operacao` set('Depósito','Saque','Transferência') DEFAULT NULL,
  `numero_conta` int NOT NULL,
  `numero_agencia` int NOT NULL,
  `status_operacao` set('Pendente','Aprovado','Negado') DEFAULT NULL,
  PRIMARY KEY (`id_operacao`),
  KEY `fk_conta_historico` (`numero_conta`),
  KEY `fk_agencia_historico` (`numero_agencia`),
  CONSTRAINT `fk_agencia_historico` FOREIGN KEY (`numero_agencia`) REFERENCES `conta` (`numero_agencia`),
  CONSTRAINT `fk_conta_historico` FOREIGN KEY (`numero_conta`) REFERENCES `conta` (`numero_conta`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historico_operacao`
--

LOCK TABLES `historico_operacao` WRITE;
/*!40000 ALTER TABLE `historico_operacao` DISABLE KEYS */;
/*!40000 ALTER TABLE `historico_operacao` ENABLE KEYS */;
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
