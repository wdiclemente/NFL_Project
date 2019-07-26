# This is meant to join the players and players_nflID tables 
# because it's stupid to  have them in two different tables
# creates the table nfl.players_comb

SELECT * FROM nfl.players;
SELECT * FROM nfl.players_nflId;

CREATE TABLE nfl.players_comb
SELECT 
	pi.nflID,
	pl.playerID,
	pl.nameFirst,
	pl.nameLast,
	pl.nameFull,
	pl.position,
	pl.collegeID
FROM
	nfl.players pl
		JOIN 
	nfl.players_nflId pi ON pl.playerID = pi.playerID;


SELECT * FROM nfl.players_comb WHERE nflId LIKE "M0%";