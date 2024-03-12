-- Active: 1709792405216@@127.0.0.1@3306@iot
CREATE TABLE products (  
    barcode varchar(30) NOT NULL PRIMARY KEY,
    size_category varchar(12) NOT NULL,
    hub_name varchar(4) NOT NULL,
    state varchar(4) DEFAULT '00',
    treatment varchar(12) NOT NULL,
    start_time datetime NULL,
    end_time datetime DEFAULT NULL
) COMMENT '';