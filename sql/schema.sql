DROP DATABASE IF EXISTS poemsdb;
CREATE DATABASE poemsdb
DEFAULT CHARACTER SET utf8
DEFAULT COLLATE utf8_general_ci;
USE poemsdb;

CREATE TABLE IF NOT EXISTS sense (
  id bigint unsigned not null,
  mark1 double,
  mark2 double,
  mark3 double,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS item (
  id serial,
  sense_id bigint unsigned not null,
  name varchar(200) not null,
  PRIMARY KEY (id),
  FOREIGN KEY (sense_id) REFERENCES sense (id)
);

CREATE TABLE IF NOT EXISTS synonym (
  id serial,
  sense_id_first bigint unsigned not null,
  sense_id_second bigint unsigned not null,
  PRIMARY KEY (id),
  FOREIGN KEY (sense_id_first) REFERENCES sense (id),
  FOREIGN KEY (sense_id_second) REFERENCES sense (id)
);

CREATE TABLE IF NOT EXISTS sentence (
  id serial,
  name varchar(200) not null,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS sense_in_sentence (
  id serial,
  sentence_id bigint unsigned not null,
  sense_id bigint unsigned not null,
  PRIMARY KEY (id),
  FOREIGN KEY (sentence_id) REFERENCES sentence (id),
  FOREIGN KEY (sense_id) REFERENCES sense (id)
);