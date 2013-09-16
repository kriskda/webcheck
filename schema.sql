drop table if exists sites;

create table sites (
  id integer primary key autoincrement,
  url text not null,
  last_check text not null,
  status_code text not null
);
