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
  `affair_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `affair_num` int unsigned NOT NULL,
  `part_id` int(8) unsigned zerofill NOT NULL,
  `part_name` char(16) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`affair_id`),
  KEY `part_id` (`part_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

/*Data for the table `cyc_affair` */

insert  into `cyc_affair`(`affair_id`,`affair_type`,`affair_time`,`affair_num`,`part_id`,`part_name`) values (00000010,0,'2020-05-12 13:05:27',11,00000012,'零件1');

/*Table structure for table `cyc_order` */

DROP TABLE IF EXISTS `cyc_order`;

CREATE TABLE `cyc_order` (
  `order_id` int(8) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `order_num` int NOT NULL,
  `order_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `part_id` int(8) unsigned zerofill NOT NULL,
  PRIMARY KEY (`order_id`),
  KEY `part_id` (`part_id`),
  CONSTRAINT `cyc_order_ibfk_1` FOREIGN KEY (`part_id`) REFERENCES `cyc_part` (`part_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

/*Data for the table `cyc_order` */

insert  into `cyc_order`(`order_id`,`order_num`,`order_time`,`part_id`) values (00000006,40,'2020-05-17 16:58:54',00000018),(00000007,80,'2020-05-17 17:31:25',00000016);

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
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;

/*Data for the table `cyc_part` */

insert  into `cyc_part`(`part_id`,`part_name`,`part_price`,`p_supplier_id`,`s_supplier_id`) values (00000013,'零件2',9,00000001,NULL),(00000014,'零件3',11.2,00000001,NULL),(00000016,'lingjian5',20,00000001,NULL),(00000018,'11111',1,00000001,NULL),(00000019,'2222',22,00000001,NULL),(00000020,'3333',3,00000001,NULL),(00000021,'4444',4,00000001,NULL),(00000022,'5555',5,00000001,NULL);

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

insert  into `cyc_store_list`(`store_id`,`store_num`,`store_cv`,`part_id`,`store_max`) values (00000001,50,10,00000013,50),(00000003,10,20,00000018,50),(00000004,20,50,00000016,100);

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
