drop table if exists dbutil;
drop table if exists sites;

create table dbutil (
    id integer primary key,
	db_code text not null
);

create table sites (
	id integer primary key autoincrement,
	url text not null,
	last_check text not null,
	status_code text not null
);

INSERT INTO dbutil (id, db_code) VALUES (1, 0);
