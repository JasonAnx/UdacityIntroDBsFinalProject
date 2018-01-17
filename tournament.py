#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("delete from matches")
    c.execute("update players set matches = 0")
    conn.commit() 
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("delete from players")
    conn.commit() 
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("select count(*) from players;")
    res = c.fetchall()
    conn.commit() 
    conn.close()
    return res[0][0];

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    name = bleach.clean(name)
    # print(str(name))
    c.execute("insert into players values (%s)",(name,))
    conn.commit() 
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("""
    select  id, name, coalesce( W.wins, 0) as wins, matches
    from
        players p left join
        ( select winner, count(winner) as wins from matches group by winner) as W
        on id=W.winner
    group by (id, w.wins)
    order by wins desc
    ;
    """)

    res = c.fetchall()
    conn.close()
    return res;

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    if (winner==loser): return;
    conn = connect()
    c = conn.cursor()
    c.execute("""insert into matches values (%s, %s)""", (winner, loser))
    c.execute("""update players set matches = matches+1 where id in (%s, %s)""", (winner, loser))
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
    whatever = playerStandings()
    matches = []
    for row1, row2 in zip(whatever[0::2], whatever[1::2]):
        
        newtuple = (row1[0], row1[1], row2[0], row2[1])
        matches.append(newtuple)
        # print ( newtuple )

    return matches


