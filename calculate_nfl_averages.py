if __name__ == '__main__':
    # framework includes
    from python.classes import *
    from python.stat_minMaxAvg import *
    from python.utils import *
    # python includes
    import time

    #---------------------------
    # SET UP STUFF
    #---------------------------

    # paths
    home_dir = '/home/will/Documents/NFL_Project/'
    cfg_dir  = home_dir+'config/'
    data_dir = home_dir+'data/'

    # configurables (read in from cfg in the future)
    min_rec  = 50  # minimum catches to be considered for nfl average
    min_pass = 150 # minimum passes to be considered for nfl average

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
                print "Processing play #{}".format(count)

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
    print "Finished reading {} plays in {} seconds.".format(count,read_data_end-read_data_start)

    #---------------------------
    # PROCESS PLAYER STATS
    #---------------------------
    calculate_start = time.time()
    count = 1
    for p_id in players:
        if count % 1000 == 0:
            print "Calculating stats for player #{}".format(count)
        count += 1
        
        players[p_id].calculate()
    calculate_end = time.time()
    print "Finished calculating stats for players in {} seconds.".format(calculate_end-calculate_start)

    #---------------------------
    # CALCULATE LEAGUE AVERAGES
    #---------------------------
    NFL = LeagueAverages(range(2004,2019),min_rec,min_pass)

    ave_start = time.time()
    for p_id in players:
        NFL.add_player(players[p_id])
    ave_end = time.time()
    print "Finished calculating league averages in {} seconds.".format(ave_end-ave_start)

    
