-- Active: 1709792405216@@127.0.0.1@3306@iot
CREATE TABLE products(  
    full_number varchar(30) NOT NULL PRIMARY KEY,
    category varchar(12) NOT NULL,
    hub_name varchar(4) NOT NULL,
    state varchar(4) DEFAULT '00',
    check_time time DEFAULT NULL,
) COMMENT '';