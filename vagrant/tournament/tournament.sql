-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP TABLE IF EXISTS player CASCADE;

CREATE TABLE player (
	id SERIAL PRIMARY KEY,
	name VARCHAR(40)
);

DROP TABLE IF EXISTS match;

CREATE TABLE match (
	id SERIAL PRIMARY KEY,
	winner INTEGER REFERENCES player (id),
	loser INTEGER REFERENCES player (id),
	CHECK (loser != winner)
);


CREATE VIEW standings AS
SELECT player.id, player.name, wins, losses, (wins+losses) as matches FROM
player JOIN
(SELECT player.id as id, COUNT(match.winner) as wins
FROM player LEFT JOIN match ON player.id = match.winner
GROUP BY player.id) as wins ON player.id = wins.id
JOIN
(SELECT player.id as id, COUNT(match.loser) as losses
FROM player LEFT JOIN match ON player.id = match.loser
GROUP BY player.id) as loses ON wins.id = loses.id ORDER BY wins DESC, losses ASC;
