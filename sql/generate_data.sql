SELECT 
	# play info
	pla.possessionTeamId as 'offense_id', 
	pla.nonpossessionTeamId as 'defense_id',
	gam.season 	as 'game_year', 
	gam.weekNameAbbr as 'game_week', 
	# passer info
	pas.nflID as 'passer_id', 
	pas.nameFull as 'passer_name', 
	pas.passPosition as 'passer_pos',
	# receiver info
	rec.nflID as 'receiver_id', 
	rec.nameFull as 'receiver_name', 
	rec.recPosition as 'receiver_pos', 
	# play info
	pas.passNull as 'play_null',
	pas.passOutcomes as 'play_result',
	# pass stats
	pas.passAtt as 'pass_attempt',
	pas.passComp as 'pass_complete',
	pas.passDirection as 'pass_direction',
	rec.recYards as 'pass_total_yards',
	pas.passLength as 'pass_throw_yards',
	pas.passTd as 'pass_td',
	pas.passInt as 'pass_int',
	pas.passSack as 'pass_sack',
	pas.passSackYds as 'pass_sack_yards',
	pas.passDef as 'pass_defensed',
	# reception stats
	rec.rec as 'rec_reception',
	rec.recYards as 'rec_total_yards', 
	pas.passLength as 'rec_throw_yards', 
	rec.recYac as 'rec_yac'
FROM 
	nfl.receptions_comb rec 
		JOIN 
	nfl.passes_comb pas ON rec.playID = pas.playID 
		JOIN
	nfl.games gam ON rec.gameId = gam.gameId
		JOIN
	nfl.plays pla ON pla.playID = rec.playID
	#(SELECT playID, nonpossessionTeamId FROM nfl.plays) pla ON pla.playID = rec.playID
#LIMIT 100
#;

INTO OUTFILE '/var/lib/mysql-files/proof_of_concept_data_v2.csv' 
FIELDS TERMINATED BY ';' 
LINES TERMINATED BY '\n';

SHOW VARIABLES LIKE 'secure_file_priv';