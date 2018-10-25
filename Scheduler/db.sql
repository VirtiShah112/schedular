DROP table users;
DROP table eventt;
CREATE TABLE users (username VARCHAR2(25) PRIMARY KEY, fname VARCHAR2(30), lname VARCHAR2(30), gender VARCHAR2(10), address1 VARCHAR2(200), address2 VARCHAR2(200), city VARCHAR2(50), zip VARCHAR2(10), email VARCHAR2(100), password VARCHAR2(50),mobile1 VARCHAR2(10),mobile2 VARCHAR2(10),mobile3 VARCHAR2(10));
CREATE TABLE eventt (username VARCHAR2(25), enentname VARCHAR2(50), edate VARCHAR2(30), remdate VARCHAR2(30), status NUMBER(1));

