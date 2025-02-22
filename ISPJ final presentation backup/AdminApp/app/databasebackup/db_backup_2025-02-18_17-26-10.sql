-- MySQL dump 10.13  Distrib 8.0.37, for Win64 (x86_64)
--
-- Host: ispj-db.cxruucec3o8o.us-east-1.rds.amazonaws.com    Database: ISPJ_DB
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `comment_failures`
--

DROP TABLE IF EXISTS `comment_failures`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment_failures` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ip_address` varchar(45) NOT NULL,
  `failure_count` int DEFAULT NULL,
  `last_failed_at` datetime DEFAULT NULL,
  `reason` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment_failures`
--

LOCK TABLES `comment_failures` WRITE;
/*!40000 ALTER TABLE `comment_failures` DISABLE KEYS */;
INSERT INTO `comment_failures` VALUES (1,'127.0.0.1',26,'2025-02-18 09:11:10','name validation error: Name must contain only alphabetic characters and spaces.'),(2,'127.0.0.1',1,'2025-02-09 15:55:01','email validation error: The domain name gm123123.com does not accept email.'),(3,'127.0.0.1',21,'2025-02-18 09:11:13','screenshot validation error: Allowed file types are png, jpg, jpeg, gif'),(4,'127.0.0.1',2,'2025-02-09 18:28:08','email validation error: The domain name hot213321231mail.com does not exist.'),(5,'127.0.0.1',3,'2025-02-09 18:36:26','email validation error: The domain name hotm213112323ail.com does not exist.'),(6,'127.0.0.1',9,'2025-02-15 12:47:55','reCAPTCHA verification failed'),(7,'127.0.0.1',2,'2025-02-10 06:08:51','email validation error: The domain name gmaqweqweil.com does not exist.'),(8,'127.0.0.1',2,'2025-02-10 06:35:46','email validation error: The domain name gm231213123ai123213312123123l.com does not exist.'),(9,'127.0.0.1',1,'2025-02-10 07:30:26','email validation error: The domain name g2131231ma21321321321il.com does not exist.'),(10,'127.0.0.1',1,'2025-02-15 12:42:31','File upload exceeded limit: 21345061 bytes (Max: 16777216 bytes)'),(11,'127.0.0.1',3,'2025-02-18 09:11:59','File upload exceeded limit: 20.36MB (Max: 16.00MB)'),(12,'127.0.0.1',1,'2025-02-18 06:40:05','email validation error: The domain name g231321mail.com does not exist.'),(13,'127.0.0.1',1,'2025-02-18 06:44:56','email validation error: The domain name gm231123213ail.com does not exist.'),(14,'127.0.0.1',2,'2025-02-18 06:50:11','email validation error: The domain name gma231321il.com does not exist.'),(15,'127.0.0.1',1,'2025-02-18 06:50:30','email validation error: The domain name gma231213321il.com does not exist.'),(16,'127.0.0.1',1,'2025-02-18 09:03:41','email validation error: The domain name h123123321otmail.com does not exist.'),(17,'127.0.0.1',1,'2025-02-18 09:05:11','email validation error: The domain name gmiqwe123.com does not exist.'),(18,'127.0.0.1',1,'2025-02-18 09:09:32','email validation error: The domain name gm132321321ail.com does not exist.'),(19,'127.0.0.1',1,'2025-02-18 09:11:12','email validation error: The domain name virus213.com does not exist.');
/*!40000 ALTER TABLE `comment_failures` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctor_patient_assignment`
--

DROP TABLE IF EXISTS `doctor_patient_assignment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctor_patient_assignment` (
  `doctor_id` varchar(7) NOT NULL,
  `patient_id` varchar(9) NOT NULL,
  PRIMARY KEY (`doctor_id`,`patient_id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `doctor_patient_assignment_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`license_number`),
  CONSTRAINT `doctor_patient_assignment_ibfk_2` FOREIGN KEY (`patient_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor_patient_assignment`
--

LOCK TABLES `doctor_patient_assignment` WRITE;
/*!40000 ALTER TABLE `doctor_patient_assignment` DISABLE KEYS */;
INSERT INTO `doctor_patient_assignment` VALUES ('M04637Z','T0110907Z'),('M04637Z','T1234567A'),('M04637Z','T1234567S');
/*!40000 ALTER TABLE `doctor_patient_assignment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors`
--

DROP TABLE IF EXISTS `doctors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors` (
  `license_number` varchar(7) NOT NULL,
  `id` varchar(9) NOT NULL,
  `specialisation` varchar(50) NOT NULL,
  `facility` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`license_number`),
  UNIQUE KEY `license_number` (`license_number`),
  KEY `id` (`id`),
  CONSTRAINT `doctors_ibfk_1` FOREIGN KEY (`id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors`
--

LOCK TABLES `doctors` WRITE;
/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
INSERT INTO `doctors` VALUES ('M04637Z','S1234567A','Family Medicine','Manadr BoonLay');
/*!40000 ALTER TABLE `doctors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `files`
--

DROP TABLE IF EXISTS `files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `files` (
  `id` int NOT NULL AUTO_INCREMENT,
  `filename` varchar(255) NOT NULL,
  `file_path` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `license_no` varchar(100) NOT NULL,
  `date` datetime NOT NULL,
  `time` datetime NOT NULL,
  `facility` varchar(255) NOT NULL,
  `patient_nric` varchar(50) NOT NULL,
  `type` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `files`
--

LOCK TABLES `files` WRITE;
/*!40000 ALTER TABLE `files` DISABLE KEYS */;
INSERT INTO `files` VALUES (1,'chapt3r5.pdf','uploads\\chapt3r5.pdf','BalaC','Beerncurry','2025-02-06 00:00:00','0000-00-00 00:00:00','Balaclinic','t0422495C','MC'),(2,'chapt3r5 (1).pdf','uploads\\chapt3r5 (1).pdf','BalaC','balancurry','2025-02-06 00:00:00','0000-00-00 00:00:00','Curryclinic','t012345t','Currytopsy'),(3,'Cyber Analyst Singtel Group.pdf','uploads/Cyber Analyst Singtel Group.pdf','Amy','abc','2025-02-06 00:00:00','0000-00-00 00:00:00','curryclinic','T0110907Z','mc'),(4,'chapt3r5 (1) (1).pdf','uploads\\chapt3r5 (1) (1).pdf','ffewq','qff','2025-02-06 00:00:00','0000-00-00 00:00:00','fqefqe','qfqwff','BAsba'),(5,'CFORT Practical Assignment.pdf','uploads/CFORT Practical Assignment.pdf','Amy','M04637Z','2025-02-18 00:00:00','0000-00-00 00:00:00','Manadr BoonLay','T0110907Z','Report'),(6,'P10 - Linux File System – Security and File Ownership.pdf','uploads/P10 - Linux File System – Security and File Ownership.pdf','Amy','M04637Z','2025-02-18 00:00:00','0000-00-00 00:00:00','Manadr BoonLay','T1234567A','Report'),(7,'chapt3r5 (1).pdf','uploads\\chapt3r5 (1).pdf','Dr Amy','S1234567A','2025-02-18 00:00:00','0000-00-00 00:00:00','CurryCLinic','T1234567A','MC'),(8,'medical-examination-report.pdf','uploads\\medical-examination-report.pdf','Amy','M04637Z','2025-02-18 00:00:00','0000-00-00 00:00:00','Manadr BoonLay','T1234567A','medical'),(9,'chapt3r5 (5).pdf','uploads\\chapt3r5 (5).pdf','Amy','M04637Z','2025-02-18 00:00:00','0000-00-00 00:00:00','Manadr BoonLay','T12345678A','TestDoc'),(10,'[Celebration of Learning]- Irfan.pdf','uploads\\[Celebration of Learning]- Irfan.pdf','Amy','M04637Z','2025-02-18 00:00:00','0000-00-00 00:00:00','Manadr BoonLay','T1234567A','TestDoc'),(11,'842470761727-9061540319-ticket.pdf','uploads/842470761727-9061540319-ticket.pdf','Amy','M04637Z','2025-02-18 00:00:00','0000-00-00 00:00:00','Manadr BoonLay','S1234567Z','Report'),(12,'842470761727-9061540319-ticket.pdf','uploads/842470761727-9061540319-ticket.pdf','Amy','M04637Z','2025-02-18 00:00:00','0000-00-00 00:00:00','Manadr BoonLay','T1234567S','Report'),(13,'T1234567A_Medical report.pdf','uploads\\T1234567A_Medical report.pdf','Amy','M04637Z','2025-02-18 00:00:00','0000-00-00 00:00:00','Manadr BoonLay','T1234567A','Medical Report');
/*!40000 ALTER TABLE `files` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `email` varchar(256) NOT NULL,
  `message` varchar(1000) NOT NULL,
  `date_added` datetime DEFAULT NULL,
  `screenshot` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (24,'ken','GGvfGCCXQfLCikiAdbUOtt0GJBExL2x/Yd4wiuBgSnY=','+kwQumGcfZ40Cfb9P7b8FkVBFvt9lsJmlpkT4UPWIGE=','2025-02-10 06:51:16','0d57121fdda242648086f13ed017bd98.gif'),(27,'ken','gHwxNPjat3tedJAJkSLylTBUUtcFP0t7oAXC7L4E49o=','Y+/T5HDtUezh4Q9DnZMuAarb4qiY9hKpYTKgj3ul4M+o0WKxP2GkC48v9xg8n05U/+8sIBnpxa9ZjWFlGxKoYQ==','2025-02-10 07:36:04','cac16c57e49040a4bff14d044da330d0.png'),(30,'qwe','/+s0LFYgzqLQQkTFmxia2dAasH05D+Vb72y1J1S9f6xcVJGArMRAHR0FUW0cs1rC','t3uT+fw5yOL9UylJORA5TLCorELOfpmkiX1YBbw8rkg=','2025-02-18 06:51:26','47bf28000db24e6183c80a98366c91d3.gif'),(32,'kenzie','Ya8KgsPNxAvfEclYJmHCutDdj0cqz0MbRaBCkx2LjEwK+za741XcbbZSiExNfmXC','zEHqJxvRqpvd1xOPYoN6gkiAZnGsG4TnBZTwqxdc6WkpOyuNSX3ZxraM/OdBeZIq6yg02aXRmRHcDwKcLmlaUA==','2025-02-18 09:12:43','71e30864b45a47948497360bed58b34b.png');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient_records`
--

DROP TABLE IF EXISTS `patient_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient_records` (
  `record_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` varchar(9) DEFAULT NULL,
  `record_data` varchar(255) DEFAULT NULL,
  `record_time` datetime DEFAULT NULL,
  `attending` varchar(7) DEFAULT NULL,
  PRIMARY KEY (`record_id`),
  KEY `patient_id` (`patient_id`),
  KEY `attending` (`attending`),
  CONSTRAINT `patient_records_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `users` (`id`),
  CONSTRAINT `patient_records_ibfk_2` FOREIGN KEY (`attending`) REFERENCES `doctors` (`license_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient_records`
--

LOCK TABLES `patient_records` WRITE;
/*!40000 ALTER TABLE `patient_records` DISABLE KEYS */;
/*!40000 ALTER TABLE `patient_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `twofa`
--

DROP TABLE IF EXISTS `twofa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `twofa` (
  `id` varchar(9) NOT NULL,
  `user_secret` varchar(32) NOT NULL,
  `twofa_enabled` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `user_secret` (`user_secret`),
  CONSTRAINT `twofa_ibfk_1` FOREIGN KEY (`id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `twofa`
--

LOCK TABLES `twofa` WRITE;
/*!40000 ALTER TABLE `twofa` DISABLE KEYS */;
INSERT INTO `twofa` VALUES ('S1234567A','ASSW3TFHDVTEUYSUIGCVS3XJTNKQDMHS',1),('T0110907Z','IYWAX2EYXAVUZE67PEBAQ6OCN5LGN7CR',1),('T1234567A','NGBUS5GLBPO4UOXNTO6MQH5BUY3S2ML2',1),('T1234567S','XDLIH52ZXTYWH3FPZJ66NBV2DHFXVH4K',1);
/*!40000 ALTER TABLE `twofa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` varchar(9) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phoneNumber` int DEFAULT NULL,
  `role` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phoneNumber` (`phoneNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('S1234567A','Amy','$2b$12$BKJ5FhyebY80/mIxTl/Ts.CHFnpTVl6fSJ3eUumHMaJ9dhspUsRIu',NULL,NULL,'Doctor'),('T0110907Z','Lucian','$2b$12$Qkh1wtsIxANHQizZOKcwP.hjsAjvxayvJuKsNW5AvN96bqMzyztJe',NULL,NULL,'Patient'),('T0621069J','Jane Doe','$2b$12$LSH8jo5OxjO1Mktjkkbo7./2HK3zhA.sujpfdTAV8uzovhf9dVVa.','kohkady@gmail.com',89448485,'Patient'),('T1234567A','Kady','$2b$12$akNYEV95Hx1V292PViJPQeYBpFuMPG7S4jAniDgsJJiYXVnSEMHe.',NULL,NULL,'Patient'),('T1234567S','Irfan','$2b$12$vYzid.YHm7Txy9jRyRLL2.Zw/wH33F2jXmHXMihWNiyy2PhzA2F2e',NULL,NULL,'Patient');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-02-18 17:26:45
