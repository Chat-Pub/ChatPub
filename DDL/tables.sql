CREATE TABLE `yp_all_overview` (
  `yp` int NOT NULL COMMENT 'YP ID',
  `title` varchar(255) DEFAULT NULL,
  `r_number` varchar(15) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `main_title` varchar(255) DEFAULT NULL,
  `short_description` text DEFAULT NULL,
  PRIMARY KEY (`yp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `yp_summary` (
  `yp` int NOT NULL COMMENT 'YP ID',
  `policy_area` varchar(15) DEFAULT NULL,
  `support_content` text DEFAULT NULL,
  `operation_period` text DEFAULT NULL,
  `application_period` text DEFAULT NULL,
  `supprot_scale` text DEFAULT NULL,
  `remarks` text DEFAULT NULL, 
  PRIMARY KEY (`yp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

