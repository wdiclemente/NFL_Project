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
            print("Requested statistic '{}' not available!  Returning -1. . .".format(stat))
            return -1
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
    
    lookup = {'num_seasons'     :0,
              'seasons'         :1,
              'pass_attempt'    :2,
              'pass_complete'   :3,
              'pass_comp_pct'   :4,
              'pass_total_yards':5,
              'pass_throw_yards':6,
              'pass_td'         :7,
              'pass_int'        :8,
              'pass_sack'       :9,
              'pass_sack_yards' :10,
              'pass_defensed'   :11,
              'rec_reception'   :12,
              'rec_total_yards' :13,
              'rec_throw_yards' :14,
              'rec_yac'         :15,
              'rec_td'          :16,
              'metric_rec'      :17,
              'metric_pass'     :18}

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
        self.pass_comp_pct    = []
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
        self.metric_rec       = []
        self.metric_pass      = []

    # set player info
    def set_player(self, player_id, player_name, player_pos):
        self.p_id   = player_id
        self.p_name = player_name
        self.p_pos  = player_pos

    def get_player_name(self):
        return self.p_name

    def get_player_id(self):
        return self.p_id

    def get_player_pos(self):
        return self.p_pos

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

    def prepare_calculate(self):
        # if stats have already been calculated, clear them
        if self.calculated:
            self.seasons          = []
            self.pass_attempt     = [] 
            self.pass_complete    = [] 
            self.pass_comp_pct    = []
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
            self.pass_comp_pct    .append(0)
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

    # calculate yearly totals for stats
    def calculate(self):
        self.prepare_calculate()
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
            # calculate completion percent
            if self.pass_attempt[y] == 0:
                self.pass_comp_pct[y] = 0.0
            else:
                self.pass_comp_pct[y] = self.pass_complete[y]/float(self.pass_attempt[y])
            y += 1
        
        self.calculated = True

    def get_all_calculated_stats(self):
        if not self.calculated:
            self.calculate()

        return [self.num_seasons,
                self.seasons,
                self.pass_attempt,
                self.pass_complete,
                self.pass_comp_pct,
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
                self.rec_td,
                self.metric_rec,
                self.metric_pass]

    def get_calculated_stat(self, stat):
        if not stat in self.lookup:
            print("Requested statistic '{}' not available!  Returning empty list. . .".format(stat))
            return []
        else:
            return self.get_all_calculated_stats()[self.lookup[stat]]

    def add_pass_metric(self, pass_metric):
        self.metric_pass = pass_metric

    def add_rec_metric(self, rec_metric):
        self.metric_rec = rec_metric
        

#---------------------------------------------------------------------------------------------------------

# this collects the yearly passer stats for all players who threw to a given player
#   ( ideally this would be broken up by game, but not yet )
class YearlyPasser(object):
    
    lookup = {'num_seasons'     :0,
              'seasons'         :1,
              'pass_attempt'    :2,
              'pass_complete'   :3,
              'pass_comp_pct'   :4,
              'pass_total_yards':5,
              'pass_throw_yards':6,
              'pass_td'         :7,
              'pass_int'        :8,
              'pass_sack'       :9,
              'pass_sack_yards' :10,
              'pass_defensed'   :11,
              'metric_pass'     :12}

    def __init__(self, seasons):
        self.calculated       = False
        self.num_seasons      = len(seasons)
        self.seasons          = sorted(seasons)
        self.pass_attempt     = [0]*self.num_seasons
        self.pass_complete    = [0]*self.num_seasons
        self.pass_comp_pct    = [0]*self.num_seasons
        self.pass_total_yards = [0]*self.num_seasons
        self.pass_throw_yards = [0]*self.num_seasons
        self.pass_td          = [0]*self.num_seasons
        self.pass_int         = [0]*self.num_seasons
        self.pass_sack        = [0]*self.num_seasons
        self.pass_sack_yards  = [0]*self.num_seasons
        self.pass_defensed    = [0]*self.num_seasons
        self.metric_pass      = [0]*self.num_seasons

        #print("Initialized YearlyPasser with {} seasons: {}".format(self.num_seasons,self.seasons))

    def add_passer(self, passer, season):
        # p_y -> index in player object
        # y   -> index in this object (may not be the same)
        p_y = passer.seasons.index(season)
        y   = self.seasons.index(season)
        self.pass_attempt[y]     += passer.pass_attempt[p_y]
        self.pass_complete[y]    += passer.pass_complete[p_y]
        self.pass_total_yards[y] += passer.pass_total_yards[p_y]
        self.pass_throw_yards[y] += passer.pass_throw_yards[p_y]
        self.pass_td[y]          += passer.pass_td[p_y]
        self.pass_int[y]         += passer.pass_int[p_y]
        self.pass_sack[y]        += passer.pass_sack[p_y]
        self.pass_sack_yards[y]  += passer.pass_sack_yards[p_y]
        self.pass_defensed[y]    += passer.pass_defensed[p_y]
        # calculate completion percent
        if self.pass_attempt[y] == 0:
            self.pass_comp_pct[y] = 0.0 
        else:
            self.pass_comp_pct[y] = self.pass_complete[y]/float(self.pass_attempt[y])
        
    def get_all_calculated_stats(self):
        return [self.num_seasons,
                self.seasons,
                self.pass_attempt,
                self.pass_complete,
                self.pass_comp_pct,
                self.pass_total_yards,
                self.pass_throw_yards,
                self.pass_td,
                self.pass_int,
                self.pass_sack,
                self.pass_sack_yards,
                self.pass_defensed,
                self.metric_pass]
    
    def get_calculated_stat(self, stat):
        if not stat in self.lookup:
            print("Requested statistic '{}' not available!  Returning empty list. . .".format(stat))
            return []
        else:
            return self.get_all_calculated_stats()[self.lookup[stat]]

    def add_pass_metric(self, pass_metric):
        self.metric_pass = pass_metric

#---------------------------------------------------------------------------------------------------------
from python.stat_minMaxAvg import *
class LeagueAverages(object):
    
    lookup = {'seasons'         :0,
              'pass_attempt'    :1,
              'pass_complete'   :2,
              'pass_comp_pct'   :3,
              'pass_total_yards':4,
              'pass_throw_yards':5,
              'pass_td'         :6,
              'pass_int'        :7,
              'pass_sack'       :8,
              'pass_sack_yards' :9,
              'pass_defensed'   :10,
              'rec_reception'   :11,
              'rec_total_yards' :12,
              'rec_throw_yards' :13,
              'rec_yac'         :14,
              'rec_td'          :15}

    def __init__(self, years, min_rec, min_pass):
        # minimum numbers of receptions/passes to qualify for averages
        self.min_rec  = min_rec
        self.min_pass = min_pass

        self.seasons = sorted(years)
        self.pass_attempt     = [StatMinMaxAvg('Pass attempts')         for s in self.seasons]
        self.pass_complete    = [StatMinMaxAvg('Pass completions')      for s in self.seasons]
        self.pass_comp_pct    = [CompMinMaxAvg('Pass completion pct')   for s in self.seasons]
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
                self.pass_comp_pct[y]   .add_entry(player.pass_comp_pct[p_y],
                                                   player.pass_attempt[p_y],
                                                   player.pass_complete[p_y])
            if player.rec_reception[p_y] >= self.min_rec:
                self.rec_reception[y]   .add_entry(player.rec_reception[p_y])
                self.rec_total_yards[y] .add_entry(player.rec_total_yards[p_y])
                self.rec_throw_yards[y] .add_entry(player.rec_throw_yards[p_y])
                self.rec_yac[y]         .add_entry(player.rec_yac[p_y])
                self.rec_td[y]          .add_entry(player.rec_td[p_y])

    def get_all_calculated_stats(self):
        return [self.seasons,
                self.pass_attempt,
                self.pass_complete,
                self.pass_comp_pct,
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

    def get_calculated_stat(self, stat):
        if not stat in self.lookup:
            print("Requested statistic '{}' not available!  Returning empty list. . .".format(stat))
            return []
        else:
            return self.get_all_calculated_stats()[self.lookup[stat]]

#---------------------------------------------------------------------------------------------------------

class LeagueAveragesMetric(object):
    
    lookup = {'seasons'     :0,
              'metric_pass' :1,
              'metric_rec'  :2}

    def __init__(self, years, min_rec, min_pass):
        # minimum numbers of receptions/passes to qualify for averages
        self.min_rec  = min_rec
        self.min_pass = min_pass

        self.seasons = sorted(years)
        self.metric_pass = [StatMinMaxAvg('Receiving Metric') for s in self.seasons]
        self.metric_rec  = [StatMinMaxAvg('Passing Metric')   for s in self.seasons]

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
                self.metric_pass[y].add_entry(player.metric_pass[p_y])

            if player.rec_reception[p_y] >= self.min_rec:
                self.metric_rec[y]   .add_entry(player.metric_rec[p_y])

    def get_all_calculated_stats(self):
        return [self.seasons,
                self.metric_pass,
                self.metric_rec]

    def get_calculated_stat(self, stat):
        if not stat in self.lookup:
            print("Requested statistic '{}' not available!  Returning empty list. . .".format(stat))
            return []
        else:
            return self.get_all_calculated_stats()[self.lookup[stat]]

#---------------------------------------------------------------------------------------------------------

class MetricCalculator(object):
    
    def __init__(self, rec_weights, pass_weights):
        # weights for recievers
        if not len(rec_weights) == 4:
            print("MetricCalculator -- Error: expected 4 receiving stat weights, got {}! Initializing weights to 1.".format(len(rec_weights)))
            self.weight_rec_reception   = 1.
            self.weight_rec_total_yards = 1.
            self.weight_rec_yac         = 1.
            self.weight_rec_td          = 1.
        else:
            self.weight_rec_reception   = rec_weights[0]
            self.weight_rec_total_yards = rec_weights[1]
            self.weight_rec_yac         = rec_weights[2]
            self.weight_rec_td          = rec_weights[3]

        # weights for passers
        if not len(pass_weights) == 7:
            print("MetricCalculator -- Error: expected 7 passing stat weights, got {}! Initializing weights to 1.".format(len(pass_weights)))
            self.weight_pass_complete    = 1.
            self.weight_pass_attempt     = 1.
            self.weight_pass_comp_pct    = 1.
            self.weight_pass_total_yards = 1.
            self.weight_pass_throw_yards = 1.
            self.weight_pass_td          = 1.
            self.weight_pass_int         = 1.
        else:
            self.weight_pass_complete    = pass_weights[0]
            self.weight_pass_attempt     = pass_weights[1]
            self.weight_pass_comp_pct    = pass_weights[2]
            self.weight_pass_total_yards = pass_weights[3]
            self.weight_pass_throw_yards = pass_weights[4]
            self.weight_pass_td          = pass_weights[5]
            self.weight_pass_int         = pass_weights[6]

    # this is the metric calculation for a single stat. they will be a weighted sum
    # based off of the Z-score of each stat (number of standard deviations from the mean)
    # z_i = (x_i-mu)/sigma
    def stat_ratio(self, stat, stat_mean, stat_stdev):
        if stat_stdev == 0:
            return 0.0
        else:
            #return (stat_num-stat_den)/float(stat_den)
            return (stat-stat_mean)/stat_stdev

    def calculate_passer(self, passer, league):
        metric = []
        for p_y,year in enumerate(passer.seasons):
            # p_y -> index in player object
            # l_y -> index in league (may not be the same)
            l_y = league.seasons.index(year)
            
            pass_complete = self.stat_ratio(passer.get_calculated_stat('pass_complete')[p_y],
                                            league.get_calculated_stat('pass_complete')[l_y].get_average(),
                                            league.get_calculated_stat('pass_complete')[l_y].get_stdev())
            val =  self.weight_pass_complete*pass_complete

            pass_attempt = self.stat_ratio(passer.get_calculated_stat('pass_attempt')[p_y],
                                           league.get_calculated_stat('pass_attempt')[l_y].get_average(),
                                           league.get_calculated_stat('pass_attempt')[l_y].get_stdev())
            val += self.weight_pass_attempt*pass_attempt

            pass_comp_pct = self.stat_ratio(passer.get_calculated_stat('pass_comp_pct')[p_y],
                                            league.get_calculated_stat('pass_comp_pct')[l_y].get_average(),
                                            league.get_calculated_stat('pass_comp_pct')[l_y].get_stdev())
            val += self.weight_pass_total_yards*pass_comp_pct

            pass_total_yards = self.stat_ratio(passer.get_calculated_stat('pass_total_yards')[p_y],
                                               league.get_calculated_stat('pass_total_yards')[l_y].get_average(),
                                               league.get_calculated_stat('pass_total_yards')[l_y].get_stdev())
            val += self.weight_pass_total_yards*pass_total_yards

            pass_throw_yards = self.stat_ratio(passer.get_calculated_stat('pass_throw_yards')[p_y],
                                               league.get_calculated_stat('pass_throw_yards')[l_y].get_average(),
                                               league.get_calculated_stat('pass_throw_yards')[l_y].get_stdev())
            val += self.weight_pass_throw_yards*pass_throw_yards
            
            pass_td = self.stat_ratio(passer.get_calculated_stat('pass_td')[p_y],
                                      league.get_calculated_stat('pass_td')[l_y].get_average(),
                                      league.get_calculated_stat('pass_td')[l_y].get_stdev())
            val += self.weight_pass_td*pass_td

            pass_int = self.stat_ratio(passer.get_calculated_stat('pass_int')[p_y],
                                       league.get_calculated_stat('pass_int')[l_y].get_average(),
                                       league.get_calculated_stat('pass_int')[l_y].get_stdev())
            val += self.weight_pass_int*pass_int

            metric.append(val)
        return metric

    def calculate_receiver(self, receiver, league):
        metric = []
        for r_y,year in enumerate(receiver.seasons):
            # r_y -> index in player object
            # l_y -> index in league (may not be the same)
            l_y = league.seasons.index(year)
            
            rec_reception = self.stat_ratio(receiver.get_calculated_stat('rec_reception')[r_y],
                                             league.get_calculated_stat('rec_reception')[l_y].get_average(),
                                             league.get_calculated_stat('rec_reception')[l_y].get_stdev())
            val =  self.weight_rec_reception*rec_reception

            rec_total_yards = self.stat_ratio(receiver.get_calculated_stat('rec_total_yards')[r_y],
                                              league.get_calculated_stat('rec_total_yards')[l_y].get_average(),
                                              league.get_calculated_stat('rec_total_yards')[l_y].get_stdev())
            val += self.weight_rec_total_yards*rec_total_yards

            rec_yac = self.stat_ratio(receiver.get_calculated_stat('rec_yac')[r_y],
                                      league.get_calculated_stat('rec_yac')[l_y].get_average(),
                                      league.get_calculated_stat('rec_yac')[l_y].get_stdev())
            val += self.weight_rec_yac*rec_yac

            rec_td = self.stat_ratio(receiver.get_calculated_stat('rec_td')[r_y],
                                     league.get_calculated_stat('rec_td')[l_y].get_average(),
                                     league.get_calculated_stat('rec_td')[l_y].get_stdev())
            val += self.weight_rec_td*rec_td

            metric.append(val)
        return metric
        pass
