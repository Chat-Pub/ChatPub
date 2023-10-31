CREATE TABLE `YP_all_overview` (
  `YP` varchar(15) NOT NULL COMMENT 'CRIS CT ID',
  `title` varchar(255) DEFAULT NULL,
  `R-number` varchar(30) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `create_date` datetime NOT NULL,
  `update_date` datetime NOT NULL,
  PRIMARY KEY (`YP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
