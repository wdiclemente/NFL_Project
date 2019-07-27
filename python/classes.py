class Play(object):

    lookup = {'play_id':0,
              # team info
              'offense_id':1,
              'defense_id':2,
              # game info
              'game_year':3,
              'game_week':4,
              # passer info
              'passer_id'  :5,
              'passer_name':6,
              'passer_pos' :7,
              # receiver info
              'receiver_id'  :8,
              'receiver_name':9,
              'receiver_pos' :10,
              # play result
              'play_nullified':11,
              'play_outcome'  :12,
              # pass stats
              'pass_attempt'    :13,
              'pass_complete'   :14,
              'pass_direction'  :15,
              'pass_total_yards':16,
              'pass_throw_yards':17,
              'pass_td'         :18,
              'pass_int'        :19,
              'pass_sack'       :20,
              'pass_sack_yards' :21,
              'pass_defensed'   :22,
              # reception stats
              'rec_reception'  :23,
              'rec_total_yards':24,
              'rec_throw_yards':25,
              'rec_yac'        :26}

    def __init__(self, play_id, input_csv):
        input_csv.strip()
        data = input_csv.split(';')

        self.data = [play_id]

        # team info
        self.data.append(int(data[0]))
        self.data.append(int(data[1]))

        # play info
        self.data.append(int(data[2]))
        self.data.append(data[3])

        # passer info
        self.data.append(int(data[4]))
        self.data.append(data[5])
        self.data.append(data[6])

        # receiver info
        self.data.append(int(data[7]))
        self.data.append(data[8])
        self.data.append(data[9])

        # play result
        self.data.append(int(data[10]))
        self.data.append(data[11])

        # pass stats
        self.data.append(int(data[12]))
        self.data.append(int(data[13]))
        self.data.append(data[14])
        self.data.append(int(data[15]))
        self.data.append(int(data[16]))
        self.data.append(int(data[17]))
        self.data.append(int(data[18]))
        self.data.append(int(data[19]))
        self.data.append(int(data[20]))
        self.data.append(int(data[21]))

        # reception stats
        self.data.append(int(data[22]))
        self.data.append(int(data[23]))
        self.data.append(int(data[24]))
        self.data.append(int(data[25]))

    def get_stat(self,stat):
        stat = stat.lower()
        if not stat in self.lookup:
            print "Requested statistic '{}' not available!  Returning -1. . .".format(stat)
        else:
            return self.data[self.lookup[stat]]

    def is_nullified(self):
        return self.data[self.lookup['play_nullified']]

    def is_regular_season(self):
        if 'week' in self.data[self.lookup['game_week']].lower():
            return True
        else:
            return False

    def to_string(self):
        return self.data

#---------------------------------------------------------------------------------------------------------

class Player(object):
    
    def __init__(self):
        # these are the basic variables
        self.p_id   = 0
        self.p_name = ''
        self.p_pos  = ''
        self.stats  = {}
        # these variables are filled when requested in calculate()
        self.calculated       = False
        self.num_seasons      = 0
        self.seasons          = []
        self.pass_attempt     = [] 
        self.pass_complete    = [] 
        self.pass_total_yards = []
        self.pass_throw_yards = []
        self.pass_td          = [] 
        self.pass_int         = [] 
        self.pass_sack        = []
        self.pass_sack_yards  = [] 
        self.pass_defensed    = [] 
        self.rec_reception    = [] 
        self.rec_total_yards  = [] 
        self.rec_throw_yards  = [] 
        self.rec_yac          = [] 
        self.rec_td           = []

    # set player info
    def set_player(self, player_id, player_name, player_pos):
        self.p_id   = player_id
        self.p_name = player_name
        self.p_pos  = player_pos

    def get_player_info(self):
        out = "{} -- {} ({})".format(self.p_id,self.p_name,self.p_pos)
        return out

    # add a new stat to the stats dictionary
    def add_stat(self, stat):
        year = stat.get_stat('game_year')
        if not year in self.stats:
            self.stats[year] = [stat]
            self.num_seasons += 1
        else:
            self.stats[year].append(stat)

    # return the dictionary of stats
    def get_all_stats(self):
        return self.stats

    # return a list of stats for a season
    def get_season_stats(self, year):
        if year in self.stats:
            return self.stats[year]
        else:
            return []

    # calculate yearly totals for stats
    def calculate(self):
        # if stats have already been calculated, clear them
        if self.calculated:
            self.seasons          = []
            self.pass_attempt     = [] 
            self.pass_complete    = [] 
            self.pass_total_yards = []
            self.pass_throw_yards = []
            self.pass_td          = [] 
            self.pass_int         = [] 
            self.pass_sack        = []
            self.pass_sack_yards  = [] 
            self.pass_defensed    = [] 
            self.rec_reception    = [] 
            self.rec_total_yards  = [] 
            self.rec_throw_yards  = [] 
            self.rec_yac          = [] 
            self.rec_td           = []
        
        for y in range(self.num_seasons):
            self.pass_attempt     .append(0) 
            self.pass_complete    .append(0) 
            self.pass_total_yards .append(0)
            self.pass_throw_yards .append(0)
            self.pass_td          .append(0) 
            self.pass_int         .append(0) 
            self.pass_sack        .append(0)
            self.pass_sack_yards  .append(0) 
            self.pass_defensed    .append(0) 
            self.rec_reception    .append(0) 
            self.rec_total_yards  .append(0) 
            self.rec_throw_yards  .append(0) 
            self.rec_yac          .append(0)
            self.rec_td           .append(0)

        y = 0
        for year in sorted(self.stats):
            self.seasons.append(year)
            for play in self.stats[year]:
                # check if player is passer or receiver and fill stats accordingly
                if play.get_stat('passer_id') == self.p_id:
                    self.pass_attempt[y]     += play.get_stat('pass_attempt')
                    self.pass_complete[y]    += play.get_stat('pass_complete')
                    self.pass_total_yards[y] += play.get_stat('pass_total_yards')
                    if play.get_stat('play_outcome').lower() == 'complete':
                        self.pass_throw_yards[y] += play.get_stat('pass_throw_yards')
                    self.pass_td[y]          += play.get_stat('pass_td')
                    self.pass_int[y]         += play.get_stat('pass_int')
                    self.pass_sack[y]        += play.get_stat('pass_sack')
                    self.pass_sack_yards[y]  += play.get_stat('pass_sack_yards')
                    self.pass_defensed[y]    += play.get_stat('pass_defensed')
                if play.get_stat('receiver_id') == self.p_id:
                    self.rec_reception[y]    += play.get_stat('rec_reception')
                    self.rec_total_yards[y]  += play.get_stat('rec_total_yards')
                    if play.get_stat('play_outcome').lower() == 'complete':
                        self.rec_throw_yards[y]  += play.get_stat('rec_throw_yards')
                    self.rec_yac[y]          += play.get_stat('rec_yac')
                    self.rec_td[y]           += play.get_stat('pass_td')
            y += 1
        
        self.calculated = True

    def get_calculated_stats(self):
        if self.calculated:
            return [self.num_seasons,
                    self.seasons,
                    self.pass_attempt,
                    self.pass_complete,
                    self.pass_total_yards,
                    self.pass_throw_yards,
                    self.pass_td,
                    self.pass_int,
                    self.pass_sack,
                    self.pass_sack_yards,
                    self.pass_defensed,
                    self.rec_reception,
                    self.rec_total_yards,
                    self.rec_throw_yards,
                    self.rec_yac,
                    self.rec_td]
        else:
            return []

#---------------------------------------------------------------------------------------------------------
from python.stat_minMaxAvg import *
class LeagueAverages(object):
    
    def __init__(self, years, min_rec, min_pass):
        # minimum numbers of receptions/passes to qualify for averages
        self.min_rec  = min_rec
        self.min_pass = min_pass

        self.seasons = sorted(years)
        self.pass_attempt     = [StatMinMaxAvg('Pass attempts')         for s in self.seasons]
        self.pass_complete    = [StatMinMaxAvg('Pass completions')      for s in self.seasons]
        self.pass_total_yards = [StatMinMaxAvg('Pass total yards')      for s in self.seasons]
        self.pass_throw_yards = [StatMinMaxAvg('Pass throw yards')      for s in self.seasons]
        self.pass_td          = [StatMinMaxAvg('Pass TDs')              for s in self.seasons]
        self.pass_int         = [StatMinMaxAvg('Pass INTs')             for s in self.seasons]
        self.pass_sack        = [StatMinMaxAvg('Pass sacks')            for s in self.seasons]
        self.pass_sack_yards  = [StatMinMaxAvg('Pass sack yards')       for s in self.seasons]
        self.pass_defensed    = [StatMinMaxAvg('Pass defensed')         for s in self.seasons]
        self.rec_reception    = [StatMinMaxAvg('Receptions')            for s in self.seasons]
        self.rec_total_yards  = [StatMinMaxAvg('Reception total yards') for s in self.seasons]
        self.rec_throw_yards  = [StatMinMaxAvg('Reception throw yards') for s in self.seasons]
        self.rec_yac          = [StatMinMaxAvg('Reception YAC')         for s in self.seasons]
        self.rec_td           = [StatMinMaxAvg('Reception TDs')         for s in self.seasons]

    def add_player(self,player):
        # check if player stats have been calculated (they should be, but just in case)
        if not player.calculated:
            player.calculate()

        for p_y,year in enumerate(player.seasons):
            # p_y -> index in player object
            # y   -> index in this object (may not be the same)
            y = self.seasons.index(year)

            # check that minimum requirements are met
            if player.pass_attempt[p_y] >= self.min_pass:
                self.pass_attempt[y]    .add_entry(player.pass_attempt[p_y])
                self.pass_complete[y]   .add_entry(player.pass_complete[p_y])
                self.pass_total_yards[y].add_entry(player.pass_total_yards[p_y])
                self.pass_throw_yards[y].add_entry(player.pass_throw_yards[p_y])
                self.pass_td[y]         .add_entry(player.pass_td[p_y])
                self.pass_int[y]        .add_entry(player.pass_int[p_y])
                self.pass_sack[y]       .add_entry(player.pass_sack[p_y])
                self.pass_sack_yards[y] .add_entry(player.pass_sack_yards[p_y])
                self.pass_defensed[y]   .add_entry(player.pass_defensed[p_y])
            if player.rec_reception[p_y] >= self.min_rec:
                self.rec_reception[y]   .add_entry(player.rec_reception[p_y])
                self.rec_total_yards[y] .add_entry(player.rec_total_yards[p_y])
                self.rec_throw_yards[y] .add_entry(player.rec_throw_yards[p_y])
                self.rec_yac[y]         .add_entry(player.rec_yac[p_y])
                self.rec_td[y]          .add_entry(player.rec_td[p_y])