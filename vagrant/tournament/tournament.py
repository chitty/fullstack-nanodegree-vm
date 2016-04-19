#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import psycopg2.extras
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def createTournament(name):
    """Adds a tournament to the tournament database.

    Args:
      name: the tournament name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    # @todo: get and return the id of the created tournament
    c.execute("INSERT INTO tournament (id, name) VALUES (1, %s);", 
        (bleach.clean(name),))
    conn.commit()
    conn.close()


def deleteTournaments():
    """Remove all the tournaments from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("TRUNCATE tournament CASCADE;")
    conn.commit()
    conn.close()


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("TRUNCATE match;")
    conn.commit()
    conn.close()


def deletePlayers(id_tournament=None):
    """Remove all the player records from the database.

    If id_tournament is passed, deletes player from that tournament

    Args:
      id_tournament: id of the tournament the player will be deleted from.
    """
    query = "TRUNCATE player CASCADE;"
    if id_tournament:
        query = "DELETE FROM tournament_player WHERE tournament = 1;"
        # @todo: Real ID
    conn = connect()
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()


def countPlayers(id_tournament=None):
    """Returns the number of players in the database.

    If id_tournament is passed, returns the number of players registered in
    that tournament.

    Args:
      id_tournament: id of the tournament where the player count will be
                     performed.
    """
    query = "SELECT COUNT(*) FROM player;"
    if id_tournament:
        query = ("SELECT COUNT(*) FROM tournament_player WHERE tournament = 1;"
            # (bleach.clean(id_tournament),) @todo: use real value    
        )
    conn = connect()
    c = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    c.execute(query)
    result = c.fetchone()
    conn.close()

    return result['count']


def registerPlayerInTournament(id_player, id_tournament):
    """Registers a player in a tournament

    Args:
      name: the player's full name (need not be unique).
      id_tournament: id of the tournament the player should be registered to.
                     None if player should not be registered in a tournament
                     yet.
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO tournament_player (tournament, player) VALUES (%s,%s);",
        (bleach.clean(id_tournament), bleach.clean(id_player)))
    conn.commit()
    conn.close()


def registerPlayer(name, id_tournament=None):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player. This is
    handled by the SQL database schema.

    Args:
      name: the player's full name (need not be unique).
      id_tournament: id of the tournament the player should be registered to.
                     None if player should not be registered in a tournament
                     yet.
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO player (name) VALUES (%s);", (bleach.clean(name),))
    conn.commit()
    # @todo: get and return the id of the created player
    if id_tournament is not None:
        c.execute("SELECT id FROM player ORDER BY id DESC LIMIT 1;")
        result = c.fetchone()
        registerPlayerInTournament(result[0], id_tournament)

    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win, tie records, sorted by
       points.

    Points are awarded according to the table below.

       ---------------------
       | WINS   | 3 points |
       | TIES   | 1 point  |
       | LOSSES | 0 points |
       ---------------------

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, ties, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        ties: the number of matches the player has tied
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT id, name, wins, ties, matches FROM standings;")
    result = c.fetchall()
    conn.close()

    return result


def reportMatch(winner, loser, tie1=None, tie2=None):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won. None if it was a tie.
      loser:  the id number of the player who lost. None if it was a tie.
      tie1:  the id number of one of the players who tied.
             None if it was not a tie.
      tie2:  the id number of the other player who tied.
             None if it was not a tie.
    """
    if winner is not None and loser is not None:
        query = "INSERT INTO match (winner, loser) VALUES (%s, %s);"
        values = (bleach.clean(winner), bleach.clean(loser))
    elif tie1 is not None and tie2 is not None:
        query = "INSERT INTO match (p1_ties, p2_ties) VALUES (%s, %s);"
        values = (bleach.clean(tie1), bleach.clean(tie2))
    else:
        return

    conn = connect()
    c = conn.cursor()
    c.execute(query, values)
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    standings = playerStandings()
    i = 0
    pairings = []

    for id, name, wins, ties, matches in standings:
        if (i % 2 == 0):
            last = (id, name)
        else:
            pairings.append(last + (id, name))
        i += 1

    return pairings
