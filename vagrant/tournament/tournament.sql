-- Table definitions for the tournament project.

--
-- PLAYER
--
DROP TABLE IF EXISTS player CASCADE;

CREATE TABLE player (
	id SERIAL PRIMARY KEY,
	name VARCHAR(40)
);

--
-- TOURNAMENT
--
DROP TABLE IF EXISTS tournament CASCADE;

CREATE TABLE tournament (
	id SERIAL PRIMARY KEY,
	name VARCHAR(40)
);

--
-- TOURNAMENT_PLAYER
--
DROP TABLE IF EXISTS tournament_player;

CREATE TABLE tournament_player (
	tournament INTEGER REFERENCES tournament (id),
	player INTEGER REFERENCES player (id),
	PRIMARY KEY (tournament, player)
);

--
-- MATCH
--
DROP TABLE IF EXISTS match;

CREATE TABLE match (
	id SERIAL PRIMARY KEY,
	winner INTEGER REFERENCES player (id),
	loser INTEGER REFERENCES player (id),
	p1_ties INTEGER REFERENCES player (id),
	p2_ties INTEGER REFERENCES player (id),
	tournament INTEGER REFERENCES tournament (id) NOT NULL,

	-- Player is not alowed to play against him/herself.
	CHECK (winner != loser AND p1_ties != p2_ties),
	-- There can't be a winner without a loser and viceversa.
	CHECK ( (winner  IS NOT NULL AND loser   IS NOT NULL)
		 OR (p1_ties IS NOT NULL AND p2_ties IS NOT NULL)
	),
	-- The match outcome is either won/lost or tied.  Can't be both!
	CHECK ( (winner  IS NOT NULL AND p1_ties IS NULL AND p2_ties IS NULL)
		 OR (p1_ties IS NOT NULL AND winner IS  NULL AND loser   IS NULL)
	)
);

--
-- STANDINGS
--
CREATE VIEW standings AS
	SELECT tournament_player.tournament, player.id, player.name,
	       (wins+losses+ties1+ties2) AS matches, wins, losses,
	       (ties1+ties2) AS ties, (3*wins+ties1+ties2) AS points
	FROM tournament_player JOIN player ON tournament_player.player = player.id
	JOIN (
		-- WINS
		SELECT player.id AS id, COUNT(match.winner) AS wins
		FROM player LEFT JOIN match ON player.id = match.winner
		GROUP BY player.id
	) AS wins ON player.id = wins.id JOIN (
		-- LOSSES
		SELECT player.id AS id, COUNT(match.loser) AS losses
		FROM player LEFT JOIN match ON player.id = match.loser
		GROUP BY player.id
	) AS losses ON wins.id = losses.id JOIN (
		-- TIES AS PLAYER 1
		SELECT player.id AS id, COUNT(match.p1_ties) AS ties1
		FROM player LEFT JOIN match ON player.id = match.p1_ties
		GROUP BY player.id
	) AS ties1 ON player.id = ties1.id JOIN (
		-- TIES AS PLAYER 2
		SELECT player.id AS id, COUNT(match.p2_ties) AS ties2
		FROM player LEFT JOIN match ON player.id = match.p2_ties
		GROUP BY player.id
	) AS ties2 ON player.id = ties2.id
	ORDER BY tournament_player.tournament, points DESC, losses ASC;
