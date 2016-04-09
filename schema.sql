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

drop view if exists activity_view;
create view activity_view as select b.username as Observer, c.activityType as Activity, a.ActivityDescription as Notes, strftime('%m/%d/%Y',datetime(a.entryDatetime, 'unixepoch', 'localtime')) as Date, strftime('%H:%M',datetime(a.entryDatetime, 'unixepoch', 'localtime')) as Time, a.ActivityLengthSec as LengthInSec from activity as a join users as b on b.id = a.inputUser join activityType c on a.activityType = c.id;
