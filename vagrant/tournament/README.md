# P2: Tournament Results

This project was developed for the course [Intro to Relational Databases](https://www.udacity.com/course/intro-to-relational-databases--ud197).

It is the implementation of a [Swiss-system tournament](https://en.wikipedia.org/wiki/Swiss-system_tournament). This tournament system is used in a variety of games and sports like [Ultimate Frisbee](https://en.wikipedia.org/wiki/Ultimate_(sport)).

This implementantion supports games where a draw (tied game) is possible. It also supports more than one tournament in the database.

## Draw (tied game)

In order to consider ties, a points system was considered, inpired by soccer and the simple instructions from [Wizards of the Coast](http://www.wizards.com/dci/downloads/swiss_pairings.pdf) points are awarded for a match as follows:

Outcome | Points
---     | ---
Wins    | 3
Ties    | 1
Losses  | 0 

## Multiple tournaments

The allow multiple tournaments the following was considered:

- A player could participate in zero or more tournaments.
- Every match belongs to a tournament.


## Testing

Simply run:

	python tournament_test.py

The [original tests](https://github.com/udacity/fullstack-nanodegree-vm) were adjusted to take in account the possibility of tied games and multiple tournaments.
