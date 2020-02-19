-- MySQL dump 10.17  Distrib 10.3.22-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: services.lsk.gaorel.ru    Database: cfp
-- ------------------------------------------------------
-- Server version	10.4.8-MariaDB-1:10.4.8+maria~bionic

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cfp_church`
--

DROP TABLE IF EXISTS `cfp_church`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cfp_church` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `locality_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `locality_id_idx` (`locality_id`),
  CONSTRAINT `fk_cfp_locality` FOREIGN KEY (`locality_id`) REFERENCES `cfp_locality` (`id`) ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cfp_doc`
--

DROP TABLE IF EXISTS `cfp_doc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cfp_doc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `church_id` int(11) NOT NULL,
  `doctype_id` int(11) NOT NULL,
  `fund_id` int(11) NOT NULL,
  `inventory` varchar(50) NOT NULL,
  `unit` varchar(50) NOT NULL,
  `sheets` int(11) NOT NULL,
  `comment` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_cfp_church` (`church_id`),
  KEY `fk_cfp_doctype` (`doctype_id`),
  KEY `fk_cfp_fund` (`fund_id`),
  CONSTRAINT `fk_cfp_church` FOREIGN KEY (`church_id`) REFERENCES `cfp_church` (`id`),
  CONSTRAINT `fk_cfp_doctype` FOREIGN KEY (`doctype_id`) REFERENCES `cfp_doctype` (`id`),
  CONSTRAINT `fk_cfp_fund` FOREIGN KEY (`fund_id`) REFERENCES `cfp_fund` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=277 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cfp_docflag`
--

DROP TABLE IF EXISTS `cfp_docflag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cfp_docflag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `default` int(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cfp_docflags`
--

DROP TABLE IF EXISTS `cfp_docflags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cfp_docflags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `doc_id` int(11) NOT NULL,
  `docflag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cfp_docFlags_FK_1` (`docflag_id`),
  KEY `cfp_docFlags_FK` (`doc_id`),
  CONSTRAINT `cfp_docFlags_FK` FOREIGN KEY (`doc_id`) REFERENCES `cfp_doc` (`id`) ON DELETE CASCADE,
  CONSTRAINT `cfp_docFlags_FK_1` FOREIGN KEY (`docflag_id`) REFERENCES `cfp_docflag` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=543 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cfp_doctype`
--

DROP TABLE IF EXISTS `cfp_doctype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cfp_doctype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `default` int(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cfp_docyears`
--

DROP TABLE IF EXISTS `cfp_docyears`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cfp_docyears` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `doc_id` int(11) NOT NULL,
  `year` int(4) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cfp_docyears_UN` (`year`,`doc_id`),
  KEY `fk_cfp_doc` (`doc_id`),
  CONSTRAINT `fk_cfp_doc` FOREIGN KEY (`doc_id`) REFERENCES `cfp_doc` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=887 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cfp_fund`
--

DROP TABLE IF EXISTS `cfp_fund`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cfp_fund` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cfp_fund_UN` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cfp_gubernia`
--

DROP TABLE IF EXISTS `cfp_gubernia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cfp_gubernia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=133 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cfp_locality`
--

DROP TABLE IF EXISTS `cfp_locality`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cfp_locality` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uezd_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `locality_id_idx` (`uezd_id`),
  CONSTRAINT `fk_cfp_uezd` FOREIGN KEY (`uezd_id`) REFERENCES `cfp_uezd` (`id`) ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cfp_uezd`
--

DROP TABLE IF EXISTS `cfp_uezd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cfp_uezd` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gub_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gub_id_idx` (`gub_id`),
  CONSTRAINT `fk_cfp_gub` FOREIGN KEY (`gub_id`) REFERENCES `cfp_gubernia` (`id`) ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'cfp'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-02-19 13:17:46
