CREATE TABLE nfl.receptions (
	receiverId INT NOT NULL,
	playId INT NOT NULL,
	teamID INT NOT NULL,
	nflID VARCHAR(255) NOT NULL,
	recPosition VARCHAR(255) NOT NULL,
	recYards INT NOT NULL,
	rec INT NOT NULL,
	recYac INT NOT NULL,
	rec1down INT NOT NULL,
	recFumble INT NOT NULL,
	recPassDef INT NOT NULL,
	recPassInt INT NOT NULL,
	recEnd VARCHAR(255) NOT NULL,
	recNull INT NOT NULL
);

CREATE TABLE nfl.players_nflId (
	playerID INT NOT NULL,
	nflID VARCHAR(255) NOT NULL
);

CREATE TABLE nfl.passes (
	passID INT NOT NULL,
	playID INT NOT NULL,
	teamID INT NOT NULL,
	nflId VARCHAR(255) NULL,
	passPosition VARCHAR(255) NOT NULL,
	passOutcomes VARCHAR(255) NOT NULL,
	passDirection VARCHAR(255) NOT NULL,
	passDepth VARCHAR(255) NOT NULL,
	passLength INT NOT NULL,
	passAtt INT NOT NULL,
	passComp INT NOT NULL,
	passTd INT NOT NULL,
	passInt INT NOT NULL,
	passIntTd INT NOT NULL,
	passSack INT NOT NULL,
	passSackYds INT NOT NULL,
	passHit INT NOT NULL,
	passDef INT NOT NULL,
	passNull INT NOT NULL
);

CREATE TABLE nfl.teams (
	teamID INT NOT NULL,
	team VARCHAR(255) NOT NULL,
	teamAbrv VARCHAR(255) NOT NULL,
	addressLine1 VARCHAR(255) NOT NULL,
	city VARCHAR(255) NOT NULL,
	state VARCHAR(255) NOT NULL,
	zipCode INT NOT NULL,
	firstSeason INT NOT NULL,
	conference VARCHAR(255) NOT NULL,
	division VARCHAR(255) NOT NULL
);

CREATE TABLE nfl.players (
	playerID INT NOT NULL,
	nameFirst VARCHAR(255) NOT NULL,
	nameLast VARCHAR(255) NOT NULL,
	nameFull VARCHAR(255) NOT NULL,
	position VARCHAR(255) NOT NULL,
	collegeID VARCHAR(255) NOT NULL
);

CREATE TABLE nfl.games (
	gameId INT NOT NULL,
	season INT NOT NULL,
	week INT NOT NULL,
	gameDate VARCHAR(255) NOT NULL,
	gameTimeEastern VARCHAR(255) NOT NULL,
	gameTimeLocal VARCHAR(255) NOT NULL,
	homeTeamId INT NOT NULL,
	visitorTeamId INT NOT NULL,
	seasonType VARCHAR(255) NOT NULL,
	weekNameAbbr VARCHAR(255) NOT NULL,
	siteId INT NOT NULL,
	homeTeamDistance INT NOT NULL,
	visitingTeamDistance INT NOT NULL,
	homeTeamFinalScore INT NOT NULL,
	visitingTeamFinalScore INT NOT NULL,
	winningTeam INT NOT NULL
);

CREATE TABLE nfl.plays (
	playId INT NOT NULL,
	gameId INT NOT NULL,
	playSequence INT NOT NULL,
	quarter INT NOT NULL,
	possessionTeamId INT NOT NULL,
	nonpossessionTeamId INT NOT NULL,
	playType VARCHAR(255) NOT NULL,
	playType2  VARCHAR(255) NOT NULL,
	playTypeDetailed VARCHAR(255) NOT NULL,
	playNumberByTeam INT NOT NULL,
	gameClock VARCHAR(255) NOT NULL,
	gameClockSecondsExpired INT NOT NULL,
	gameClockStoppedAfterPlay INT NOT NULL,
	down INT NOT NULL,
	distance INT NOT NULL,
	fieldPosition VARCHAR(255) NOT NULL,
	distanceToGoalPre INT NOT NULL,
	noPlay INT NOT NULL,
	playDescription VARCHAR(255) NOT NULL,
	playStats VARCHAR(255) NOT NULL,
	playDescriptionFull VARCHAR(255) NOT NULL,
	typeOfPlay VARCHAR(255) NOT NULL,
	changePossession  INT NOT NULL,
	turnover INT NOT NULL,
	safety INT NOT NULL,
	offensiveYards INT NOT NULL,
	netYards INT NOT NULL,
	firstDown INT NOT NULL,
	efficientPlay INT NOT NULL,
	evPre FLOAT NOT NULL,
	evPost FLOAT NOT NULL,
	evPlay FLOAT NOT NULL,
	fourthDownConversion INT NOT NULL,
	thirdDownConversion INT NOT NULL,
	scorePossession INT NOT NULL,
	scoreNonpossession INT NOT NULL,
	homeScorePre INT NOT NULL,
	visitingScorePre INT NOT NULL,
	homeScorePost INT NOT NULL,
	visitingScorePost INT NOT NULL
);