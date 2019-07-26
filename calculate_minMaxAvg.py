#!/bin/python

if __name__ == '__main__':
    from python.pass_play import PassPlay
    from python.stat_minMaxAvg import StatMinMaxAvg
    from python.utils import *
    import numpy as np
    from matplotlib import pyplot as plt
    
    #---------------------------
    # SET UP STUFF
    #---------------------------

    # important paths and configuration variables
    #    in the future these will be read from a cfg file
    home_dir = '/home/will/Documents/NFL_Project/'
    cfg_dir  = home_dir+'config/'
    data_dir = home_dir+'data/'

    # read in player-id information
    lookup_id_to_player = make_player_lookup(data_dir+'playerIDs.csv') # key-value = id-player

    #---------------------------
    # read in data
    #---------------------------

    # set up list which will contain our completions separated by season
    seasons = []
    season_offset = 2004 # we subtract this from the play's season to get the proper index in the list
    for i in range(2004,2019):
        seasons.append({})

    # read in the data line by line from csv
    with open(data_dir+'proof_of_concept_data.csv') as input_data:
        # read first line
        line = input_data.readline()
        count = 1

        # loop over lines in csv
        while line:
            if count%25000 == 0:
                print "Reading in play #{}".format(count)

            line = line.strip()
            play = make_pass_play(count, line)

            # get proper index in seasons list
            season_index = play.get_season() - season_offset

            # store play in the dictionary if it was a completion during the regular season and not nullifed by penalty
            if (play.get_play_result().lower() == "complete") and ("week" in play.get_week().lower()) and (play.get_play_null() == 0):
                if play.get_receiver_id() in seasons[season_index]:
                    seasons[season_index][play.get_receiver_id()].append(play)
                else:
                    seasons[season_index][play.get_receiver_id()] = [play]
            else:
                del play

            # read next line
            line = input_data.readline()
            count += 1


    #---------------------------
    # Print out some stats year by year
    #---------------------------

    min_rec = 70 # minimum number of receptions to qualify, read this in from config later

    # open output file
    output_stats = open(data_dir+'stats_min{}rec.dat'.format(min_rec),'w')

    # loop over seasons
    season_stats = {}
    for i,data in enumerate(seasons):
        year = i+season_offset

        # set up annual stat trackers
        stat_receptions   = StatMinMaxAvg("Receptions")
        stat_recTotYards  = StatMinMaxAvg("Total reception yards")
        stat_recYac       = StatMinMaxAvg("Yards after catch")
        stat_recPassYards = StatMinMaxAvg("Yards from catch")

        # loop over players with more than min_rec receptions
        for pid,recs in data.iteritems():
            if len(recs) < min_rec: continue

            # calculate individual season totals
            player_rec_yards   = 0
            player_catch_yards = 0
            player_yac         = 0
            for rec in recs:
                player_rec_yards   += rec.get_play_yards()
                player_catch_yards += rec.get_pass_yards()
                player_yac         += rec.get_pass_yac()
            
            # add player totals to stat trackers
            stat_receptions  .add_entry(len(recs))
            stat_recTotYards .add_entry(player_rec_yards)
            stat_recYac      .add_entry(player_yac)
            stat_recPassYards.add_entry(player_catch_yards)

        # store season stats to dictionary for plotting
        season_stats[year] = [stat_receptions,stat_recTotYards,stat_recYac,stat_recPassYards]

        # print stat trackers
        print "  Stats for season {}  --------------------------------------------------------------".format(year)
        print stat_receptions  .to_string()
        print stat_recTotYards .to_string()
        print stat_recYac      .to_string()
        print stat_recPassYards.to_string()

        # write stats to file
        output_stats.write('[{} season]\n'.format(year))
        output_stats.write(stat_receptions.to_cfg())
        output_stats.write(stat_recTotYards.to_cfg())
        output_stats.write(stat_recYac.to_cfg())
        output_stats.write(stat_recPassYards.to_cfg())
        output_stats.write('\n')

    # close stat file
    output_stats.close()

    #---------------------------
    # Make some plots!
    #---------------------------
    
    # total receiving yards as proof of concept
    #   plot relative to NFL average? maybe flatter and easier to get meaningful info
    years = range(2004,2019)
    player_id  = "2495647"
    player_rec = []
    rec_avg = []
    rec_min = []
    rec_max = []
    for y,year in enumerate(years):
        #rec_avg.append(season_stats[year][1].get_average())
        rec_avg.append(1)
        if season_stats[year][2].get_average() == 0:
            rec_min.append(np.NaN)
            rec_max.append(np.NaN)
        else:
            rec_min.append(season_stats[year][2].get_min_value()/season_stats[year][2].get_average())
            rec_max.append(season_stats[year][2].get_max_value()/season_stats[year][2].get_average())

        if not player_id in seasons[y]:
            player_rec.append(np.NaN)
        else:
            player_season = seasons[y][player_id]
            player_stats = 0
            for play in player_season:
                player_stats += play.get_pass_yac()
            if season_stats[year][2].get_average() == 0:
                player_rec.append(np.NaN)
            else:
                player_rec.append(player_stats/season_stats[year][2].get_average())
            
    plt_player = plt.plot(years,player_rec, color='#000000', linestyle='-', linewidth=1.5, label=lookup_id_to_player[player_id])
    
    plt_avg  = plt.plot(years,rec_avg, color='#000099', linestyle=':', linewidth=1, label="NFL average (min {} rec)".format(min_rec))
    plt_min  = plt.plot(years,rec_min, color='#444444', linestyle='-',  linewidth=1, label="Low-high range (min {} rec)".format(min_rec))
    plt_max  = plt.plot(years,rec_max, color='#444444', linestyle='-',  linewidth=1, label="_noLabel")#label="High (min {} rec)".format(min_rec))
    plt_fill = plt.fill_between(years,rec_min,rec_max,color='#EEEEEE', label="Minimum-maximum range (min{} rec)".format(min_rec))
    plt_dummy = plt.fill(np.NaN, np.NaN, '#EEEEEE')

    plt.legend(loc='lower left')

    plt.xlim(years[0],years[-1])
    #plt.ylim(0,2500)
    #plt.ylim(0,2)

    plt.xlabel("NFL Season")
    plt.ylabel("Yards relative to NFL average")
    plt.title("Total Receiving Yards for {}".format(lookup_id_to_player[player_id]), fontsize=16, fontweight='bold')
    plt.show()
