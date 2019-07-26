from pass_play import *

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
                print "Warning, ID {} ({}) already in dictionary for player {}! Skipping...".format(line[0],line[1],output_dict[line[0]])

            line = player_id.readline()

    return output_dict

def get_min_max_avg(catches, min_rec = 0):
    pass
