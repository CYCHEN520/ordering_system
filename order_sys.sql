/*
SQLyog Ultimate v12.08 (64 bit)
MySQL - 8.0.19 : Database - order_sys
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`order_sys` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `order_sys`;

/*Table structure for table `cyc_affair` */

DROP TABLE IF EXISTS `cyc_affair`;

CREATE TABLE `cyc_affair` (
  `affair_id` int(8) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `affair_type` int NOT NULL,
  `affair_commit_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `affair_finish_time` datetime DEFAULT NULL,
  `affair_num` int unsigned NOT NULL,
  `part_id` int(8) unsigned zerofill NOT NULL,
  `order_id` int(8) unsigned zerofill DEFAULT NULL,
  `affair_status` int NOT NULL,
  PRIMARY KEY (`affair_id`),
  KEY `part_id` (`part_id`),
  KEY `affair_type` (`affair_type`),
  KEY `affair_status` (`affair_status`),
  CONSTRAINT `cyc_affair_ibfk_1` FOREIGN KEY (`affair_type`) REFERENCES `cyc_affair_type` (`affair_type`),
  CONSTRAINT `cyc_affair_ibfk_2` FOREIGN KEY (`affair_status`) REFERENCES `cyc_affair_status` (`status_type`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;

/*Data for the table `cyc_affair` */

insert  into `cyc_affair`(`affair_id`,`affair_type`,`affair_commit_time`,`affair_finish_time`,`affair_num`,`part_id`,`order_id`,`affair_status`) values (00000027,0,'2020-05-20 15:16:30','2020-05-20 15:23:59',5,00000016,NULL,1),(00000028,1,'2020-05-20 15:25:30','2020-05-20 15:27:03',10,00000016,00000027,1),(00000029,0,'2020-05-20 15:28:23','2020-05-20 15:29:07',10,00000016,NULL,1);

/*Table structure for table `cyc_affair_status` */

DROP TABLE IF EXISTS `cyc_affair_status`;

CREATE TABLE `cyc_affair_status` (
  `status_type` int NOT NULL,
  `status_explain` varchar(3) CHARACTER SET utf16 COLLATE utf16_general_ci NOT NULL,
  PRIMARY KEY (`status_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `cyc_affair_status` */

insert  into `cyc_affair_status`(`status_type`,`status_explain`) values (0,'未处理'),(1,'已处理');

/*Table structure for table `cyc_affair_type` */

DROP TABLE IF EXISTS `cyc_affair_type`;

CREATE TABLE `cyc_affair_type` (
  `affair_type` int NOT NULL,
  `type_explain` varchar(2) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`affair_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `cyc_affair_type` */

insert  into `cyc_affair_type`(`affair_type`,`type_explain`) values (0,'出库'),(1,'入库');

/*Table structure for table `cyc_order` */

DROP TABLE IF EXISTS `cyc_order`;

CREATE TABLE `cyc_order` (
  `order_id` int(8) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `order_num` int NOT NULL,
  `purchased_num` int unsigned NOT NULL,
  `order_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `part_id` int(8) unsigned zerofill NOT NULL,
  `order_status` int unsigned NOT NULL,
  PRIMARY KEY (`order_id`),
  KEY `part_id` (`part_id`),
  KEY `order_status` (`order_status`),
  CONSTRAINT `cyc_order_ibfk_1` FOREIGN KEY (`part_id`) REFERENCES `cyc_part` (`part_id`),
  CONSTRAINT `cyc_order_ibfk_2` FOREIGN KEY (`order_status`) REFERENCES `cyc_order_status` (`status_type`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;

/*Data for the table `cyc_order` */

insert  into `cyc_order`(`order_id`,`order_num`,`purchased_num`,`order_time`,`part_id`,`order_status`) values (00000026,35,0,'2020-05-20 15:24:09',00000018,1),(00000027,100,10,'2020-05-20 15:27:03',00000016,1),(00000028,10,0,'2020-05-20 15:30:07',00000016,1);

/*Table structure for table `cyc_order_status` */

DROP TABLE IF EXISTS `cyc_order_status`;

CREATE TABLE `cyc_order_status` (
  `status_type` int unsigned NOT NULL,
  `status_explain` varchar(7) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`status_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `cyc_order_status` */

insert  into `cyc_order_status`(`status_type`,`status_explain`) values (0,'未写入订货报表'),(1,'已写入订货报表');

/*Table structure for table `cyc_part` */

DROP TABLE IF EXISTS `cyc_part`;

CREATE TABLE `cyc_part` (
  `part_id` int(8) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `part_name` char(16) NOT NULL,
  `part_price` float NOT NULL,
  `p_supplier_id` int(8) unsigned zerofill NOT NULL,
  `s_supplier_id` int(8) unsigned zerofill DEFAULT NULL,
  PRIMARY KEY (`part_id`),
  UNIQUE KEY `part_name` (`part_name`),
  KEY `p_supplier_id` (`p_supplier_id`),
  KEY `s_supplier_id` (`s_supplier_id`),
  CONSTRAINT `cyc_part_ibfk_1` FOREIGN KEY (`p_supplier_id`) REFERENCES `cyc_supplier` (`supplier_id`),
  CONSTRAINT `cyc_part_ibfk_2` FOREIGN KEY (`s_supplier_id`) REFERENCES `cyc_supplier` (`supplier_id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;

/*Data for the table `cyc_part` */

insert  into `cyc_part`(`part_id`,`part_name`,`part_price`,`p_supplier_id`,`s_supplier_id`) values (00000013,'零件4',9.2,00000001,NULL),(00000014,'零件3',11.2,00000001,NULL),(00000016,'lingjian5',20,00000001,NULL),(00000018,'11111',1,00000001,NULL),(00000019,'2222',22,00000001,NULL),(00000020,'3333',3,00000001,NULL),(00000021,'4444',4,00000001,NULL),(00000022,'5555',5,00000001,NULL),(00000025,'零件2',111,00000001,00000005);

/*Table structure for table `cyc_store_list` */

DROP TABLE IF EXISTS `cyc_store_list`;

CREATE TABLE `cyc_store_list` (
  `store_id` int(8) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `store_num` int NOT NULL DEFAULT '0',
  `store_cv` int NOT NULL DEFAULT '0',
  `part_id` int(8) unsigned zerofill NOT NULL,
  `store_max` int unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`store_id`),
  UNIQUE KEY `part_id` (`part_id`),
  CONSTRAINT `cyc_store_list_ibfk_1` FOREIGN KEY (`part_id`) REFERENCES `cyc_part` (`part_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

/*Data for the table `cyc_store_list` */

insert  into `cyc_store_list`(`store_id`,`store_num`,`store_cv`,`part_id`,`store_max`) values (00000001,46,10,00000013,50),(00000003,15,20,00000018,50),(00000004,0,50,00000016,100);

/*Table structure for table `cyc_supplier` */

DROP TABLE IF EXISTS `cyc_supplier`;

CREATE TABLE `cyc_supplier` (
  `supplier_id` int(8) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `supplier_name` char(16) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `supplier_contact` char(11) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `supplier_address` char(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `supplier_contact_name` char(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`supplier_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

/*Data for the table `cyc_supplier` */

insert  into `cyc_supplier`(`supplier_id`,`supplier_name`,`supplier_contact`,`supplier_address`,`supplier_contact_name`) values (00000001,'ccc','13333333333','xxxxxxxxxxxxxxxxxxx','ccc公司'),(00000005,'xxx','13333333333','xxxxxxxxxxxxxxxxxxx','ddd公司'),(00000012,'1111','13313313313','7777777777777','aaaa');

/*Table structure for table `cyc_users` */

DROP TABLE IF EXISTS `cyc_users`;

CREATE TABLE `cyc_users` (
  `user_id` int(8) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `username` char(6) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `password` char(16) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Data for the table `cyc_users` */

insert  into `cyc_users`(`user_id`,`username`,`password`) values (00000001,'admin','admin');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
