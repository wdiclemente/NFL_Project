#!/bin/python

if __name__ == '__main__':
    from pass_play import PassPlay
    from utils import *
    import numpy as np
    
    

    catches_HinesWard = []
    catches_dict_2008 = {}

    # read in data
    with open('/home/will/Documents/NFL_Project/proof_of_concept_data.csv') as input_data:
        line = input_data.readline()
        count = 1
        while line:
            if count%25000 == 0:
                print "Reading in play #{}".format(count)

            line = line.strip()
            play = make_pass_play(count, line)

            if (play.get_season() == 2008) and (play.get_play_result().lower() == "complete") and ("week" in play.get_week().lower()):
                if play.get_receiver_name() in catches_dict_2008:
                    catches_dict_2008[play.get_receiver_name()].append(play)
                else:
                    catches_dict_2008[play.get_receiver_name()] = [play]
            else:
                del play

            line = input_data.readline()
            count += 1

    leaders_2008 = []
    for k,v in catches_dict_2008.iteritems():
        if len(v) < 20:
            continue
        leaders_2008.append([len(v),k])
    leaders_2008.sort()
    for player in leaders_2008:
        print "Player {} caught {} passes in 2008".format(player[1],player[0])

    #for catch in catches_HinesWard:
    #    if catch.get_season() == 2006:
    #        print catch.get_play_yards(),catch.get_pass_yards(),catch.get_pass_yac(),catch.get_description()

    
