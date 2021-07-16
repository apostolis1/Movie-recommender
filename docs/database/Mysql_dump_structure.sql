CREATE DATABASE  IF NOT EXISTS `movie_recommender` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `movie_recommender`;
-- MySQL dump 10.13  Distrib 8.0.25, for Linux (x86_64)
--
-- Host: localhost    Database: movie_recommender
-- ------------------------------------------------------
-- Server version	8.0.25

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
-- Table structure for table `name_basics`
--

DROP TABLE IF EXISTS `name_basics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `name_basics` (
  `nconst` varchar(20) NOT NULL,
  `PrimaryName` text,
  PRIMARY KEY (`nconst`),
  CONSTRAINT `fk_name_basics_1` FOREIGN KEY (`nconst`) REFERENCES `title_principals` (`nconst`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `title_basics`
--

DROP TABLE IF EXISTS `title_basics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `title_basics` (
  `tconst` varchar(20) NOT NULL,
  `primaryTitle` text,
  `startYear` text,
  `genres` text,
  PRIMARY KEY (`tconst`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `title_keywords`
--

DROP TABLE IF EXISTS `title_keywords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `title_keywords` (
  `tconst` varchar(20) NOT NULL,
  `keywords` text,
  PRIMARY KEY (`tconst`),
  CONSTRAINT `fk_title_keywords_1` FOREIGN KEY (`tconst`) REFERENCES `title_basics` (`tconst`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `title_principals`
--

DROP TABLE IF EXISTS `title_principals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `title_principals` (
  `tconst` varchar(20) NOT NULL,
  `nconst` varchar(20) NOT NULL,
  PRIMARY KEY (`tconst`,`nconst`),
  KEY `NCONST_INDEX` (`nconst`),
  CONSTRAINT `fk_title_principals_1` FOREIGN KEY (`tconst`) REFERENCES `title_basics` (`tconst`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `title_ratings`
--

DROP TABLE IF EXISTS `title_ratings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `title_ratings` (
  `tconst` varchar(20) NOT NULL,
  `averageRating` float DEFAULT NULL,
  `numVotes` bigint DEFAULT NULL,
  PRIMARY KEY (`tconst`),
  CONSTRAINT `fk_title_ratings_1` FOREIGN KEY (`tconst`) REFERENCES `title_basics` (`tconst`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `title_soup`
--

DROP TABLE IF EXISTS `title_soup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `title_soup` (
  `tconst` varchar(20) NOT NULL,
  `soup` text,
  PRIMARY KEY (`tconst`),
  CONSTRAINT `fk_title_soup_1` FOREIGN KEY (`tconst`) REFERENCES `title_basics` (`tconst`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-15 16:24:33
