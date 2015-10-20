DROP DATABASE IF EXISTS test;

CREATE DATABASE test;

USE test;

GRANT SELECT, INSERT, UPDATE, DELETE ON mywebapp.* TO 'root'@'localhost' IDENTIFIED BY 'root';

CREATE TABLE User(
	id varchar(50) not null,
	name varchar(50) not null,
	email varchar(50) not null,
	unique key idx_email (email),
	primary key (id)
)engine=innodb default charset=utf8;