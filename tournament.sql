-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

\c postgres
drop database if exists tournament;
create database tournament;
\c tournament

drop table if exists tournaments;
drop table if exists matches;
drop table if exists players;

create table tournaments (
	id serial primary key
);

create table players (
	name text,
	id serial primary key,
	matches int default 0
);

create table matches (
	winner integer references players(id),
	loser integer references players(id)
);

\c postgres
\q