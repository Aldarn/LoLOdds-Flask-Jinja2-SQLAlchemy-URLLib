# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.6.23)
# Database: hextechprojectx
# Generation Time: 2015-07-18 02:56:43 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table game_summoners
# ------------------------------------------------------------

DROP TABLE IF EXISTS `game_summoners`;

CREATE TABLE `game_summoners` (
  `gameId` bigint(20) NOT NULL,
  `summonerId` bigint(20) NOT NULL,
  `totalSessionsWon` int(11) DEFAULT NULL,
  `totalSessionsLost` int(11) DEFAULT NULL,
  `totalChampionSessionsWon` int(11) DEFAULT NULL,
  `totalChampionSessionsLost` int(11) DEFAULT NULL,
  `teamId` int(11) DEFAULT NULL,
  `championId` int(11) DEFAULT NULL,
  `championImageUrl` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`gameId`,`summonerId`),
  KEY `summonerId` (`summonerId`),
  CONSTRAINT `game_summoners_ibfk_1` FOREIGN KEY (`gameId`) REFERENCES `games` (`gameId`),
  CONSTRAINT `game_summoners_ibfk_2` FOREIGN KEY (`summonerId`) REFERENCES `summoners` (`summonerId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table games
# ------------------------------------------------------------

DROP TABLE IF EXISTS `games`;

CREATE TABLE `games` (
  `gameId` bigint(20) NOT NULL,
  `gameMode` varchar(50) DEFAULT NULL,
  `gameQueueId` int(11) DEFAULT NULL,
  `gameType` varchar(50) DEFAULT NULL,
  `mapId` int(11) DEFAULT NULL,
  `platformId` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`gameId`),
  KEY `ix_games_gameType` (`gameType`),
  KEY `ix_games_platformId` (`platformId`),
  KEY `ix_games_gameMode` (`gameMode`),
  KEY `ix_games_mapId` (`mapId`),
  KEY `ix_games_gameQueueId` (`gameQueueId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table summoner_champion_stats
# ------------------------------------------------------------

DROP TABLE IF EXISTS `summoner_champion_stats`;

CREATE TABLE `summoner_champion_stats` (
  `summonerId` bigint(20) NOT NULL,
  `championId` bigint(20) NOT NULL,
  `totalSessionsWon` int(11) DEFAULT NULL,
  `totalSessionsLost` int(11) DEFAULT NULL,
  PRIMARY KEY (`summonerId`,`championId`),
  CONSTRAINT `summoner_champion_stats_ibfk_1` FOREIGN KEY (`summonerId`) REFERENCES `summoners` (`summonerId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table summoners
# ------------------------------------------------------------

DROP TABLE IF EXISTS `summoners`;

CREATE TABLE `summoners` (
  `summonerId` bigint(20) NOT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `platformId` varchar(10) DEFAULT NULL,
  `iconImageUrl` varchar(255) DEFAULT NULL,
  `lastModified` bigint(20) DEFAULT NULL,
  `lastStatsModified` bigint(20) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `totalSessionsWon` int(11) DEFAULT NULL,
  `totalSessionsLost` int(11) DEFAULT NULL,
  PRIMARY KEY (`summonerId`),
  KEY `ix_summoners_name` (`name`),
  KEY `ix_summoners_lastModified` (`lastModified`),
  KEY `ix_summoners_lastStatsModified` (`lastStatsModified`),
  KEY `ix_summoners_platformId` (`platformId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
