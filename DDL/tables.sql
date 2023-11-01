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

CREATE TABLE `yp_qualification` (
  `yp` int NOT NULL COMMENT 'YP ID',
  `age` text DEFAULT NULL,
  `residence_income` text DEFAULT NULL,
  `education` text DEFAULT NULL,
  `major` text DEFAULT NULL,
  `employment_status` text DEFAULT NULL,
  `specialization` text DEFAULT NULL,
  `additional_info` text DEFAULT NULL, 
  `eligibility` text DEFAULT NULL, 
  PRIMARY KEY (`yp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `yp_methods` (
  `yp` int NOT NULL COMMENT 'YP ID',
  `application_procedure` text DEFAULT NULL,
  `evaluation_announcement` text DEFAULT NULL,
  `application_website` text DEFAULT NULL,
  `required_documents` text DEFAULT NULL,
  PRIMARY KEY (`yp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `yp_etc` (
  `yp` int NOT NULL COMMENT 'YP ID',
  `other_info` text DEFAULT NULL,
  `host_organization` text DEFAULT NULL,
  `operating_organization` text DEFAULT NULL,
  `reference_1` text DEFAULT NULL,
  `reference_2` text DEFAULT NULL,
  `attachments` text DEFAULT NULL,
  PRIMARY KEY (`yp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;