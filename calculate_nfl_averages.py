if __name__ == '__main__':
    # framework includes
    from python.classes import *
    from python.stat_minMaxAvg import *
    from python.utils import *
    # python includes
    import time
    import configparser
    import numpy as np
    from matplotlib import pyplot as plt

    #---------------------------
    # SET UP STUFF
    #---------------------------
    
    config = configparser.ConfigParser()
    config.readfp(open(r'config/config.cfg'))

    # paths
    project_dir = config.get('Paths', 'project_dir')
    data_dir    = config.get('Paths', 'data_dir')

    # configurables
    min_rec  = config.getint('Config', 'minimum_receptions') # minimum catches to be considered for nfl average
    min_pass = config.getint('Config', 'minimum_passes')     # minimum passes to be considered for nfl average

    players_of_interest = parse_PoI(config.get('Config', 'players'))
    #---------------------------
    # READ IN DATA
    #---------------------------
    plays = []
    players = {}
    
    # read in data line by line
    read_data_start = time.time()
    with open(data_dir+'proof_of_concept_data_v2.csv') as input_data:
        # first line
        line = input_data.readline()
        count = 1
        
        # loop over remaining lines
        while line:
            if count % 25000 == 0:
                print("Processing play #{}".format(count))

            play = Play(count,line)
            plays.append(play)

            # add play to relevant players, create if necessary
            # only if NOT nullified by penalty and during regular season!
            if (not play.is_nullified()) and (play.is_regular_season()):
                pass_id = play.get_stat('passer_id')
                if not pass_id in players:
                    passer = Player()
                    passer.set_player(pass_id, 
                                      play.get_stat('passer_name'), 
                                      play.get_stat('passer_pos'))
                    passer.add_stat(play)
                    players[pass_id] = passer
                else:
                    players[pass_id].add_stat(play)

                rec_id  = play.get_stat('receiver_id')
                if not rec_id in players:
                    receiver = Player()
                    receiver.set_player(rec_id, 
                                        play.get_stat('receiver_name'), 
                                        play.get_stat('receiver_pos'))
                    receiver.add_stat(play)
                    players[rec_id] = receiver
                else:
                    players[rec_id].add_stat(play)

            # next line
            line = input_data.readline()
            count += 1
    read_data_end = time.time()
    print("Finished reading {} plays in {:0.2f} seconds.".format(count,read_data_end-read_data_start))

    #---------------------------
    # PROCESS PLAYER STATS
    #---------------------------
    calculate_start = time.time()
    count = 1
    for p_id in players:
        if count % 1000 == 0:
            print("Calculating stats for player #{}".format(count))
        count += 1
        
        players[p_id].calculate()
    calculate_end = time.time()
    print("Finished calculating stats for {} players in {:0.2f} seconds.".format(count,calculate_end-calculate_start))

    #---------------------------
    # CALCULATE LEAGUE AVERAGES
    #---------------------------
    NFL = LeagueAverages(range(2004,2019),min_rec,min_pass)

    ave_start = time.time()
    for p_id in players:
        NFL.add_player(players[p_id])
    ave_end = time.time()
    print("Finished calculating league averages in {:0.2f} seconds.".format(ave_end-ave_start))

    #---------------------------
    # CALCULATE METRICS FOR ALL PLAYERS AND LEAGUE AVERAGE
    #---------------------------
    metric_start = time.time()

    rec_weights = [config.getfloat('Metric', 'weight_rec_reception'),
                   config.getfloat('Metric', 'weight_rec_total_yards'),
                   config.getfloat('Metric', 'weight_rec_yac'),
                   config.getfloat('Metric', 'weight_rec_td')]
    pass_weights = [config.getfloat('Metric', 'weight_pass_complete'),
                    config.getfloat('Metric', 'weight_pass_attempt'),
                    config.getfloat('Metric', 'weight_pass_comp_pct'),
                    config.getfloat('Metric', 'weight_pass_total_yards'),
                    config.getfloat('Metric', 'weight_pass_throw_yards'),
                    config.getfloat('Metric', 'weight_pass_td'),
                    config.getfloat('Metric', 'weight_pass_int')]
    met_calc = MetricCalculator(rec_weights,pass_weights)

    # this will store the leaguemin/max/average of the metrics
    NFL_Metric = LeagueAveragesMetric(range(2004,2019),min_rec,min_pass)

    # calculate player metrics and insert into league
    for p_id in players:
        players[p_id].add_pass_metric(met_calc.calculate_passer  (players[p_id],NFL))
        players[p_id].add_rec_metric (met_calc.calculate_receiver(players[p_id],NFL))
        NFL_Metric.add_player(players[p_id])

    metric_end = time.time()
    print("Finished calculating metric for all players in {:0.2f} sec.".format(metric_end-metric_start))

    #---------------------------
    # MAKE PLOTS FOR REQUESTED PLAYERS
    #---------------------------

    for poi in players_of_interest:
        plot_start = time.time()
        # gather stats for this PoI
        this_player = players[poi]
        this_passer = YearlyPasser(this_player.seasons)
        print("Making plots for player {}.".format(this_player.get_player_info()))

        for year in this_player.seasons:
            # get all passers who threw to this PoI in this season
            yearly_passers = []
            for play in this_player.get_season_stats(year):
                if not play.get_stat('passer_id') in yearly_passers:
                    yearly_passers.append(play.get_stat('passer_id'))
            # for each passer, aggregate their stats
            for passer_id in yearly_passers:
                this_passer.add_passer(players[passer_id], year)

        # we are ready for plotting!
        rec_stats = ['rec_reception',
                     'rec_total_yards',
                     'rec_throw_yards',
                     'rec_yac',
                     'rec_td']
        for rec_stat in rec_stats:
            #print "Now plotting {}.".format(rec_stat)
            make_plot_with_ratio(this_player.get_player_id(),
                                 rec_stat,
                                 this_player.seasons, 
                                 this_player.get_calculated_stat(rec_stat),
                                 NFL        .get_calculated_stat(rec_stat),
                                 [this_player.get_player_name(), 
                                  "{} vs NFL average (min {} rec)".format(this_player.get_player_name(),min_rec)])
        
        pass_stats = ['pass_attempt',
                      'pass_complete',
                      'pass_comp_pct',
                      'pass_total_yards',
                      'pass_throw_yards',
                      'pass_td',
                      'pass_int']
        for pass_stat in pass_stats:
            #print "Now plotting {}.".format(pass_stat)
            make_plot_with_ratio(this_player.get_player_id(),
                                 pass_stat,
                                 this_passer.seasons, 
                                 this_passer.get_calculated_stat(pass_stat),
                                 NFL        .get_calculated_stat(pass_stat),
                                 [this_player.get_player_name(),
                                  "{}'s passers vs NFL average (min {} pass)".format(this_player.get_player_name(),min_pass)])
        
        metric_passer   = met_calc.calculate_passer(this_passer,NFL)
        make_metric_plot(this_player.get_player_id(),
                         this_player.seasons,
                         this_player.get_calculated_stat('metric_rec'),
                         metric_passer,
                         NFL_Metric.get_calculated_stat('metric_rec'),
                         NFL_Metric.get_calculated_stat('metric_pass'),
                         [this_player.get_player_name(),
                          "{} & associated passer (min {} rec/{} pass)".format(this_player.get_player_name(),min_rec,min_pass)])

        plot_end = time.time()
        print("Done in {:0.2f} sec.".format(plot_end-plot_start))
