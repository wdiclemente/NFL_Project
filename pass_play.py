class PassPlay:

    pass_play_id = 10 # ID number for play
    # info about the passer
    passer_nflId = ""
    passer_name  = ""
    # info about the receiver
    receiver_nflId  = ""
    receiver_name   = ""
    receiver_pos    = "" # position
    receiver_teamId = 0
    # info about the passing play
    play_result   = ""   # complete/incomplete/interception, etc
    play_null     = 0    # play nullified by penalty
    play_totYards = 0    # total yards for the play
    # info about the pass itself
    pass_passYards = 0   # distance the ball traveled in the air
    pass_yac       = 0   # yards after catch
    # info about the game
    game_season = 0
    game_week   = ""     # week in the season (week 1, preseason week 1, etc)
    # text description of the play (optional)
    pass_play_descr = ""

    def __init__(self,ID):
        pass_play_id = ID

    # set values
    def set_play_id(self, ID):
        self.pass_play_id = ID
    def set_passer_id(self, ID):
        self.passer_nflId = ID
    def set_passer_name(self, name):
        self.passer_name = name
    def set_receiver_id(self, ID):
        self.receiver_nflId = ID
    def set_receiver_name(self, ID):
        self.receiver_name = ID
    def set_receiver_position(self, pos):
        self.receiver_pos = pos
    def set_team(self, team):
        self.receiver_teamId = team
    def set_play_result(self, res):
        self.play_result = res
    def set_play_null(self, nul):
        self.play_null = nul
    def set_play_yards(self, yard):
        self.play_totYards = yard
    def set_pass_yards(self, yard):
        self.pass_passYards = yard
    def set_pass_yac(self, yac):
        self.pass_yac = yac
    def set_season(self, sea):
        self.game_season = sea
    def set_week(self, wk):
        self.game_week = wk
    def set_description(self, des):
        self.pass_play_descr = des

    # get values
    def get_play_id(self):
        return self.pass_play_id
    def get_passer_id(self):
        return self.passer_nflId
    def get_passer_name(self):
        return self.passer_name
    def get_receiver_id(self):
        return self.receiver_nflId
    def get_receiver_name(self):
        return self.receiver_name
    def get_receiver_position(self):
        return self.receiver_pos
    def get_team(self):
        return self.receiver_teamId
    def get_play_result(self):
        return self.play_result
    def get_play_null(self):
        return self.play_null
    def get_play_yards(self):
        return self.play_totYards
    def get_pass_yards(self):
        return self.pass_passYards
    def get_pass_yac(self):
        return self.pass_yac
    def get_season(self):
        return self.game_season
    def get_week(self):
        return self.game_week
    def get_description(self):
        return self.pass_play_descr
