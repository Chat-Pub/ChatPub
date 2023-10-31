CREATE TABLE `YP_all_overview` (
  `YP` varchar(15) NOT NULL COMMENT 'YP ID',
  `title` varchar(255) DEFAULT NULL,
  `R-number` varchar(15) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `main_title` varchar(255) DEFAULT NULL,
  `short_description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`YP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `YP_summary` (
  `YP` varchar(15) NOT NULL COMMENT 'YP ID',
  `policy_area` varchar(15) DEFAULT NULL,
  `support_content` varchar(255) DEFAULT NULL,
  `operation_period` varchar(255) DEFAULT NULL,
  `application_period` varchar(255) DEFAULT NULL,
  `supprot_scale` varchar(255) DEFAULT NULL,
  `remarks` varchar(255) DEFAULT NULL, 
  PRIMARY KEY (`YP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

