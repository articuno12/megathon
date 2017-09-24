SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
CREATE TABLE IF NOT EXISTS `chatbot` (
		`ticket` int(11) NOT NULL,
		`status` varchar(20) NOT NULL,
		`severity` int(4) NOT NULL,
		`client` varchar(20) NOT NULL,
		`date` varchar(20) NOT NULL,
		`comments` varchar(20) NOT NULL,
		`time` varchar(20) NOT NULL
		)ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=6 ;

