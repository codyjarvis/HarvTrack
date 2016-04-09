drop table if exists users;
create table users (
    id integer primary key,
    username text not null
);

drop table if exists activityType;
create table activityType (
id integer primary key,
activityType text not null
);

drop table if exists activity;
create table activity (
id integer primary key,
inputUser integer not null,
activityType integer not null,
activityDescription text,
activityLengthSec integer,
entryDatetime numeric
,FOREIGN KEY(inputUser) REFERENCES users(id)
,FOREIGN KEY(activityType) REFERENCES activityType(id)
);

