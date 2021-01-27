create schema baoninhbinh collate utf8mb4_unicode_ci;
create table article
(
	id char(32) not null
		primary key,
	title varchar(256) not null,
	slug varchar(256) not null,
	thump varchar(512) null,
	description varchar(4096) null,
	publish datetime not null,
	media varchar(1024) null,
	content mediumtext null,
	keywords varchar(512) null,
	category_id int not null
);

create table category
(
	id int auto_increment
		primary key,
	title varchar(128) not null,
	slug varchar(128) not null,
	locked int null
);
