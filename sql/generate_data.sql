SELECT 
	pas.nflID as 'passer_nflId', 
	pas.nameFull as 'passer_name', 
	rec.nflID as 'receiver_nflId', 
	rec.nameFull as 'receiver_name', 
	rec.recPosition as 'receiver_pos', 
	rec.teamID as 'receiver_teamId', 
	pas.passOutcomes as 'pass_result', 
	pas.passNull as 'pass_null', 
	rec.recYards as 'rec_totYards', 
	pas.passLength as 'rec_passYards', 
	rec.recYac as 'rec_yac', 
	gam.season 	as 'game_year', 
	gam.weekNameAbbr as 'game_week'#, 
	#rec.playDescription as 'play_description' 
FROM 
	nfl.receptions_comb rec 
		JOIN 
	nfl.passes_comb pas ON rec.playID = pas.playID 
		JOIN
	nfl.games gam ON rec.gameId = gam.gameId
#LIMIT 100
#;

INTO OUTFILE '/var/lib/mysql-files/proof_of_concept_data_no_descr	.csv' 
FIELDS TERMINATED BY ';' 
LINES TERMINATED BY '\n';

SHOW VARIABLES LIKE 'secure_file_priv';