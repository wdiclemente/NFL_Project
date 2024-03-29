from python.pass_play import *
from matplotlib import pyplot as plt
import numpy as np

def parse_PoI(config):
    config = config.strip()
    config = config.split(',')
    PoI = []
    for pid in config:
        try:
            PoI.append(int(pid))
        except ValueError:
            print("Player ID '{}' from config is not an int! Exiting. . .".format(pid))
            exit()
    return PoI

def make_pass_play(ID,line):
    output = PassPlay(ID)

    line = line.strip()
    line = line.split(';') # csv separated by ;

    #set_play_id(ID)
    output.set_passer_id(line[0])
    output.set_passer_name(line[1])
    output.set_receiver_id(line[2])
    output.set_receiver_name(line[3])
    output.set_receiver_position(line[4])
    output.set_team(int(line[5]))
    output.set_play_result(line[6])
    output.set_play_null(int(line[7]))
    output.set_play_yards(int(line[8]))
    output.set_pass_yards(int(line[9]))
    output.set_pass_yac(int(line[10]))
    output.set_season(int(line[11]))
    output.set_week(line[12])
    if len(line) > 13:
        output.set_description(line[13])

    return output

def make_player_lookup(input_path):
    output_dict = {}

    with open(input_path) as player_id:
        line = player_id.readline()

        while line:
            line = line.strip()
            line = line.split(';')

            if not line[0] in output_dict:
                output_dict[line[0]] = line[1]

            else:
                print("Warning, ID {} ({}) already in dictionary for player {}! Skipping...".format(line[0],line[1],output_dict[line[0]]))

            line = player_id.readline()

    return output_dict

def get_min_max_avg(catches, min_rec = 0):
    pass

def divide_lists(numerator, denominator):
    output = []
    for i in range(len(numerator)):
        if denominator[i] == 0:
            output.append(0.0)
        else:
            output.append(numerator[i]/float(denominator[i]))
    return output

# ----------------------------------------------------------------------
# This function will make a plot with ratio subplot of a given stat 
# for a chosen player compared to the nfl average and min/max
#
# This function is ONLY compatible with v2 of the code, the original
#  code `calculate_minMaxAvg.py` is obsolete and will crash
# 
# Input:
#   player_id -- unique int defining the player
#   stat_id -- string describing the stat of interest
#   player_years -- list of seasons in which the player has stats recorded
#   player_stats -- list containing the stats of the player
#   season_stats -- list of StatMinMaxAvg objects for the stat of interest
#   plot_text -- plot-specific text formatted as follows:
#                [ Player name, plot title ]
#-----------------------------------------------------------------------
def make_plot_with_ratio(player_id, stat_id, player_years, player_stats, season_stats, plot_text):
    # set up canvas
    figure = plt.figure(figsize=(12,7))
    grid   = plt.GridSpec(8,1,hspace=0)

    # set up plots
    main_plot  = figure.add_subplot(grid[:6,:],xticklabels=[])
    ratio_plot = figure.add_subplot(grid[6:,:])

    # clean player stats -- we need to fill in missing years
    stat_name = season_stats[0].get_stat_name()
    years = range(2004,2019)
    new_player_stats = []
    for year in years:
        if year not in player_years:
            new_player_stats.append(np.NaN)
        else:
            new_player_stats.append(player_stats[player_years.index(year)])

    # get league stats
    average = [s.get_average()   for s in season_stats]
    minimum = [s.get_min_value() for s in season_stats]
    maximum = [s.get_max_value() for s in season_stats]

    # get ratio stats
    r_new_player_stats = divide_lists(new_player_stats,average)
    r_average = divide_lists(average,average)
    r_minimum = divide_lists(minimum,average)
    r_maximum = divide_lists(maximum,average)        

    #--------------
    # MAIN PLOT
    #--------------
    # player of interest's stats
    main_plot.plot(years,new_player_stats, color='#010101', linestyle='', marker='o', linewidth=1.5, label=plot_text[0])
    main_plot.plot(years,new_player_stats, color='#010101', linestyle='-', linewidth=1.5, alpha=0.5)
    # nfl average
    main_plot.plot(years,average, color='#000099', linestyle=':', linewidth=1, label="NFL average")
    # nfl min/max and fill the area in between
    main_plot.plot(years,minimum, color='#2222CC', linestyle='-', linewidth=1, label="Low-high range")
    main_plot.plot(years,maximum, color='#2222CC', linestyle='-', linewidth=1, label="_noLabel")
    main_plot.fill_between(years,minimum,maximum,color='#EEEEFF', label="Minimum-maximum range")

    #--------------
    # RATIO PLOT
    #--------------
    # player of interest's stats
    ratio_plot.plot(years,r_new_player_stats, color='#010101', marker='o', linestyle='', linewidth=1.5)
    ratio_plot.plot(years,r_new_player_stats, color='#010101', linestyle='-', linewidth=1.5, alpha=0.5)
    # nfl average
    ratio_plot.plot(years,r_average, color='#000099', linestyle=':', linewidth=1)
    # nfl min/max and fill the area in between
    ratio_plot.plot(years,r_minimum, color='#2222CC', linestyle='-', linewidth=1)
    ratio_plot.plot(years,r_maximum, color='#2222CC', linestyle='-', linewidth=1)
    ratio_plot.fill_between(years,r_minimum,r_maximum,color='#EEEEFF')

    # labels and stuff
    ratio_plot.set_ylim(0,1.99)
    ratio_plot.set_xlabel("NFL Season")
    ratio_plot.set_ylabel("ratio")

    main_plot.set_ylim(0.1,main_plot.get_ylim()[1]*1.2)
    main_plot.set_ylabel(stat_name)
    main_plot.set_title(plot_text[1], fontsize=16, fontweight='bold')
    main_plot.legend(loc='upper left')

    #plt.show()
    # save figure and close it
    figure.savefig("plots/{}_{}.pdf".format(player_id,stat_id), bbox_inches='tight')
    figure.savefig("plots/{}_{}.png".format(player_id,stat_id), bbox_inches='tight')
    del figure
    plt.close()

# ----------------------------------------------------------------------
# This function will plot the Metric for a given player and his associated
#  passer compared to the nfl average with a ratio plot
#
# Input:
#   player_id -- unique int defining the player
#   player_years -- list of seasons in which the player has stats recorded
#   player_stats -- list containing the stats of the player
#   metric_rec -- list of the player's receiving metric
#   metric_pass -- list of the player's passers' passing metric
#   plot_text -- plot-specific text formatted as follows:
#                [ Player name, plot title ]
#-----------------------------------------------------------------------
def make_metric_plot(player_id, player_years, metric_rec, metric_pass, nfl_metric_rec, nfl_metric_pass, plot_text):
    # set up canvas
    figure = plt.figure(figsize=(12,7))
    grid   = plt.GridSpec(8,1,hspace=0)

    # set up plots
    main_plot  = figure.add_subplot(grid[:6,:],xticklabels=[])
    ratio_plot = figure.add_subplot(grid[6:,:])

    # clean player stats -- we need to fill in missing years
    years = range(2004,2019)
    new_metric_rec  = []
    new_metric_pass = []
    for year in years:
        if year not in player_years:
            new_metric_rec .append(np.NaN)
            new_metric_pass.append(np.NaN)
        else:
            new_metric_rec .append(metric_rec [player_years.index(year)])
            new_metric_pass.append(metric_pass[player_years.index(year)])

    # plot of zeros
    zero_years = range(2003,2020)
    zero_metric  = [0 for y in zero_years]

    # get ratio stats
    difference  = [new_metric_rec[i]-new_metric_pass[i] for i in range(len(new_metric_rec))]

    #--------------
    # MAIN PLOT
    #--------------
    # receiving metric
    main_plot.plot(years,new_metric_rec,  color='#010101', marker='o', linestyle='', linewidth=1.5,
                   label="{}'s receiving metric".format(plot_text[0]))
    main_plot.plot(years,new_metric_rec,  color='#222222', linestyle='-', linewidth=1.5, alpha=.5)
    main_plot.plot(years,new_metric_pass, color='#990000', marker='s', linestyle='', linewidth=1.5, 
                   label="{}'s passers' metric".format(plot_text[0]))
    main_plot.plot(years,new_metric_pass, color='#990000', linestyle='-', linewidth=1.5, alpha=.5)
    # dashed line at 0 for average
    main_plot.plot(zero_years,zero_metric, color='#000000', linestyle=':')


    #--------------
    # RATIO PLOT
    #--------------
    # player of interest's stats
    ratio_plot.bar (years,difference,  color='#010101', alpha=.5, linewidth=1.5, align='center')
    ratio_plot.plot(zero_years,zero_metric, color='#000000', linestyle='-', linewidth=0.5) 

    # labels and stuff
    ratio_plot.set_xlabel("NFL Season")
    ratio_plot.set_ylabel("difference")
    r_lims = ratio_plot.get_ylim()
    r_max_val = max(abs(r_lims[0]),abs(r_lims[1]))*1.1
    ratio_plot.set_ylim(-r_max_val,r_max_val)
    ratio_plot.set_xlim(2003,2019)
    ratio_plot.grid(axis='y')

    main_plot.set_xlim(2003,2019)#years[0],years[-1])
    main_plot.set_ylim(main_plot.get_ylim()[0],main_plot.get_ylim()[1]*1.45)
    main_plot.set_ylabel("Metric score")
    main_plot.set_title(plot_text[1], fontsize=16, fontweight='bold')
    main_plot.legend(loc='upper left')

    #plt.show()
    # save figure and close it
    figure.savefig("plots/{}_metric.pdf".format(player_id), bbox_inches='tight')
    figure.savefig("plots/{}_metric.png".format(player_id), bbox_inches='tight')
    del figure
    plt.close()
