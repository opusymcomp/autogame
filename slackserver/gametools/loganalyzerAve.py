# -*- coding: utf-8 -*-
import numpy as np
import itertools
import ggssapi_gameresult
import sys

args = sys.argv
order = args[1]
branch = args[2]
logdir = args[3]

result_map = {}
num_dict = {}
win = {}
lose = {}
draw = {}
tmp_list = list()
tmp_ave = list()

fiftystorms = {
    'win':0.0,
    'lose':0.0,
    'draw':0.0,
    'our_score':0.0,
    'opp_score':0.0}

helios2018 = {
    'win':0.0,
    'lose':0.0,
    'draw':0.0,
    'our_score':0.0,
    'opp_score':0.0}

hillstone2019 = {
    'win':0.0,
    'lose':0.0,
    'draw':0.0,
    'our_score':0.0,
    'opp_score':0.0}

opuscom2018 = {
    'win':0.0,
    'lose':0.0,
    'draw':0.0,
    'our_score':0.0,
    'opp_score':0.0}

rione2019 = {
    'win':0.0,
    'lose':0.0,
    'draw':0.0,
    'our_score':0.0,
    'opp_score':0.0}

toyosugalaxy = {
    'win':0.0,
    'lose':0.0,
    'draw':0.0,
    'our_score':0.0,
    'opp_score':0.0}

helios2019 = {
    'win':0.0,
    'lose':0.0,
    'draw':0.0,
    'our_score':0.0,
    'opp_score':0.0}

gliders2d = {
    'win':0.0,
    'lose':0.0,
    'draw':0.0,
    'our_score':0.0,
    'opp_score':0.0}

heliosbase = {
    'win':0.0,
    'lose':0.0,
    'draw':0.0,
    'our_score':0.0,
    'opp_score':0.0}

jyosen = {
    'win':0.0,
    'lose':0.0,
    'draw':0.0,
    'our_score':0.0,
    'opp_score':0.0}

lineCount = 0

for line in open( "../log/"+logdir+"/TEAMNAME.csv", "r" ):

    lineCount += 1
    if lineCount > 1:
        tmp = line[:-1].split("\n")[0].split(",")
        key = tmp[ 2 ]
        if key not in result_map:
            result_map[key] = np.zeros(35)
            num_dict[key] = 0
            win[key] = 0
            lose[key] = 0
            draw[key] = 0
        tmp_list = result_map[key]
        tmp_list += np.array( list(map( float,tmp[3:] )) )
        result_map[key] = tmp_list
        num_dict[key] += 1
        if tmp[3] > tmp[4]:
            win[key] += 1
        if tmp[3] == tmp[4]:
            draw[key] += 1
        if tmp[3] < tmp[4]:
            lose[key] += 1

for key in open( "team_list.txt", "r" ):
    key = key.split("\n")[0]
    if key not in result_map:
        print (key)
        continue
    tmp_list = result_map[key]
    tmp_count = num_dict[key]
    tmp_ave = tmp_list / tmp_count
    result_map[key] = tmp_ave
    print (key, tmp_count, win[key], lose[key], draw[key])
    print (result_map[key])

    if key == "Fifty-Storms":
        fiftystorms['win'] = win[key]
        fiftystorms['lose'] = lose[key]
        fiftystorms['draw'] = draw[key]
        fiftystorms['our_score'] = result_map[key][0]
        fiftystorms['opp_score'] = result_map[key][1]
    elif key == "HELIOS2018":
        helios2018['win'] = win[key]
        helios2018['lose'] = lose[key]
        helios2018['draw'] = draw[key]
        helios2018['our_score'] = result_map[key][0]
        helios2018['opp_score'] = result_map[key][1]
    elif key == "HillStone":
        hillstone2019['win'] = win[key]
        hillstone2019['lose'] = lose[key]
        hillstone2019['draw'] = draw[key]
        hillstone2019['our_score'] = result_map[key][0]
        hillstone2019['opp_score'] = result_map[key][1]
    elif key == "opuSCOM2018":
        opuscom2018['win'] = win[key]
        opuscom2018['lose'] = lose[key]
        opuscom2018['draw'] = draw[key]
        opuscom2018['our_score'] = result_map[key][0]
        opuscom2018['opp_score'] = result_map[key][1]
    elif key == "Ri-one2019":
        rione2019['win'] = win[key]
        rione2019['lose'] = lose[key]
        rione2019['draw'] = draw[key]
        rione2019['our_score'] = result_map[key][0]
        rione2019['opp_score'] = result_map[key][1]
    elif key == "Toyosu-Galaxy":
        toyosugalaxy['win'] = win[key]
        toyosugalaxy['lose'] = lose[key]
        toyosugalaxy['draw'] = draw[key]
        toyosugalaxy['our_score'] = result_map[key][0]
        toyosugalaxy['opp_score'] = result_map[key][1]
    elif key == "HELIOS2019":
        helios2019['win'] = win[key]
        helios2019['lose'] = lose[key]
        helios2019['draw'] = draw[key]
        helios2019['our_score'] = result_map[key][0]
        helios2019['opp_score'] = result_map[key][1]
    elif key == "Gliders2d":
        gliders2d['win'] = win[key]
        gliders2d['lose'] = lose[key]
        gliders2d['draw'] = draw[key]
        gliders2d['our_score'] = result_map[key][0]
        gliders2d['opp_score'] = result_map[key][1]
    elif key == "HELIOS_base":
        heliosbase['win'] = win[key]
        heliosbase['lose'] = lose[key]
        heliosbase['draw'] = draw[key]
        heliosbase['our_score'] = result_map[key][0]
        heliosbase['opp_score'] = result_map[key][1]
    elif key == "Jyo_sen2019":
        jyosen['win'] = win[key]
        jyosen['lose'] = lose[key]
        jyosen['draw'] = draw[key]
        jyosen['our_score'] = result_map[key][0]
        jyosen['opp_score'] = result_map[key][1]

ggssapi_gameresult.main(order, branch, fiftystorms, helios2018, hillstone2019, opuscom2018, rione2019, toyosugalaxy, helios2019, gliders2d, heliosbase, jyosen)
