# Merge game ID and play description into receptions / passes tables
DROP TABLE nfl.receptions_comb;

CREATE TABLE nfl.receptions_comb
SELECT 
	re.receiverID,
	ga.gameID,
	re.playId,
	re.teamID,
	re.nflID,
	pa.nameFull,
	recPosition,
	re.recYards,
	re.rec,
	re.recYac,
	re.rec1down,
	re.recFumble,
	re.recPassDef,
	re.recPassInt,
	re.recEnd,
	re.recNull,
	pl.playDescriptionFull
FROM 
	nfl.receptions re
		LEFT JOIN
	nfl.plays pl ON re.playID = pl.playID
		LEFT JOIN
	nfl.players_comb pa ON re.nflID = pa.nflID
		JOIN
	nfl.games ga ON pl.gameId = ga.gameId;
#WHERE
	#re.nflID LIKE "M0%";

DROP TABLE nfl.passes_comb;
CREATE TABLE nfl.passes_comb
SELECT
	pa.passID,
	ga.gameID,
	pa.playId,
	pa.teamID,
	pa.nflID,
	pq.nameFull,
	pa.passPosition,
	pa.passOutcomes,
	pa.passDirection,
	pa.passDepth,
	pa.passLength,
	pa.passAtt,
	pa.passComp,
	pa.passTd,
	pa.passInt,
	pa.passIntTd,
	pa.passSack,
	pa.passSackYds,
	pa.passHit,
	pa.passDef,
	pa.passNull,
	pl.playDescriptionFull
FROM 
	nfl.passes pa
		LEFT JOIN
	nfl.plays pl ON pa.playID = pl.playID
		JOIN
	nfl.games ga ON pl.gameId = ga.gameId
		JOIN
	nfl.players_comb pq ON pa.nflID = pq.nflID;