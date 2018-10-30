-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: reanalysis
-- ------------------------------------------------------
-- Server version	5.1.73

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `data`
--

DROP TABLE IF EXISTS `data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data` (
  `id` int(11) NOT NULL,
  `TMP_2` int(2) DEFAULT NULL,
  `DPT_2` int(2) DEFAULT NULL,
  `RH_2` int(3) DEFAULT NULL,
  `RH_700` int(3) DEFAULT NULL,
  `MSLET_SF` int(4) DEFAULT NULL,
  `TMP_850` int(2) DEFAULT NULL,
  `CAPE_180` int(5) DEFAULT NULL,
  `CIN_180` int(4) DEFAULT NULL,
  `PWAT_CLM` int(3) DEFAULT NULL,
  `UGRD_10` int(2) DEFAULT NULL,
  `VGRD_10` int(2) DEFAULT NULL,
  `UGRD_850` int(2) DEFAULT NULL,
  `VGRD_850` int(2) DEFAULT NULL,
  `UGRD_500` int(3) DEFAULT NULL,
  `VGRD_500` int(3) DEFAULT NULL,
  `UGRD_300` int(3) DEFAULT NULL,
  `VGRD_300` int(3) DEFAULT NULL,
  `GUST_SF` int(2) DEFAULT NULL,
  `HGT_0C` int(4) DEFAULT NULL,
  `TMP_500` int(2) DEFAULT NULL,
  `HGT_850` int(4) DEFAULT NULL,
  `HGT_500` int(4) DEFAULT NULL,
  `VVEL_900` float(3,1) DEFAULT NULL,
  `VVEL_700` float(3,1) DEFAULT NULL,
  `SNOD_SF` int(3) DEFAULT NULL,
  `rdrmax` int(2) DEFAULT NULL,
  `cldave` int(3) DEFAULT NULL,
  `precave` float(4,1) DEFAULT NULL,
  `precpct` int(3) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `datetimes`
--

DROP TABLE IF EXISTS `datetimes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `datetimes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `datetime` datetime DEFAULT NULL,
  `data_id` int(11) NOT NULL,
  PRIMARY KEY (`id`,`data_id`),
  KEY `fk_datetimes_data_idx` (`data_id`),
  CONSTRAINT `fk_datetimes_data` FOREIGN KEY (`data_id`) REFERENCES `data` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `locations`
--

DROP TABLE IF EXISTS `locations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `locations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `latitude` float(6,4) NOT NULL,
  `longitude` float(7,4) NOT NULL,
  `locationscol` int(11) NOT NULL,
  `datetimes_id` int(11) NOT NULL,
  `datetimes_data_id` int(11) NOT NULL,
  PRIMARY KEY (`id`,`datetimes_id`,`datetimes_data_id`),
  UNIQUE KEY `name_UNIQUE` (`name`),
  KEY `fk_locations_datetimes1_idx` (`datetimes_id`,`datetimes_data_id`),
  CONSTRAINT `fk_locations_datetimes1` FOREIGN KEY (`datetimes_id`, `datetimes_data_id`) REFERENCES `datetimes` (`id`, `data_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `models`
--

DROP TABLE IF EXISTS `models`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `models` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `description` mediumtext,
  `locations_id` int(11) NOT NULL,
  `locations_datetimes_id` int(11) NOT NULL,
  `locations_datetimes_data_id` int(11) NOT NULL,
  PRIMARY KEY (`id`,`locations_id`,`locations_datetimes_id`,`locations_datetimes_data_id`),
  UNIQUE KEY `name_UNIQUE` (`name`),
  KEY `fk_models_locations1_idx` (`locations_id`,`locations_datetimes_id`,`locations_datetimes_data_id`),
  CONSTRAINT `fk_models_locations1` FOREIGN KEY (`locations_id`, `locations_datetimes_id`, `locations_datetimes_data_id`) REFERENCES `locations` (`id`, `datetimes_id`, `datetimes_data_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-10-30  8:39:04
