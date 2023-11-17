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

CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `userinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `birth` varchar(16) NOT NULL,
  `gender` varchar(255) NOT NULL,
  `job` varchar(255) NOT NULL,
  `region` varchar(255) NOT NULL,
  `money` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `userinfo_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `folder` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `folder_name` varchar(1024) NOT NULL,
  `create_date` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `folder_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `folder_content` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_date` datetime NOT NULL,
  `question` text NOT NULL,
  `answer` text DEFAULT NULL,
  `references` text DEFAULT NULL,
  `folder_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `folder_id` (`folder_id`),
  CONSTRAINT `folder_content_ibfk_1` FOREIGN KEY (`folder_id`) REFERENCES `folder` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;