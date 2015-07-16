# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.6.23)
# Database: hextechprojectx
# Generation Time: 2015-07-16 16:43:17 +0000
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
  `game_id` int(11) NOT NULL,
  `summoner_id` int(11) NOT NULL,
  PRIMARY KEY (`game_id`,`summoner_id`),
  KEY `summoner_id` (`summoner_id`),
  CONSTRAINT `game_summoners_ibfk_1` FOREIGN KEY (`game_id`) REFERENCES `games` (`gameId`),
  CONSTRAINT `game_summoners_ibfk_2` FOREIGN KEY (`summoner_id`) REFERENCES `summoners` (`summonerId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table games
# ------------------------------------------------------------

DROP TABLE IF EXISTS `games`;

CREATE TABLE `games` (
  `gameId` int(11) NOT NULL,
  `gameMode` varchar(50) DEFAULT NULL,
  `gameQueueId` int(11) DEFAULT NULL,
  `gameType` varchar(50) DEFAULT NULL,
  `mapId` int(11) DEFAULT NULL,
  `platformId` int(11) DEFAULT NULL,
  PRIMARY KEY (`gameId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table summoner_champion_stats
# ------------------------------------------------------------

DROP TABLE IF EXISTS `summoner_champion_stats`;

CREATE TABLE `summoner_champion_stats` (
  `summonerId` int(11) NOT NULL,
  `championId` int(11) NOT NULL,
  `championImageUrl` varchar(255) DEFAULT NULL,
  `totalSessionsWon` int(11) DEFAULT NULL,
  `totalSessionsLost` int(11) DEFAULT NULL,
  PRIMARY KEY (`summonerId`,`championId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table summoners
# ------------------------------------------------------------

DROP TABLE IF EXISTS `summoners`;

CREATE TABLE `summoners` (
  `summonerId` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `iconId` int(11) DEFAULT NULL,
  `lastModified` int(11) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `totalSessionsWon` int(11) DEFAULT NULL,
  `totalSessionsLost` int(11) DEFAULT NULL,
  PRIMARY KEY (`summonerId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
