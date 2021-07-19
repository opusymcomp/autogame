# coding: utf-8
import plugins.tools as tl
import time
import datetime
import subprocess
import shutil
from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply

import os
import sys
sys.path.append("{}/gametools".format(os.getcwd()))
import ggssapi_gameresult as ggssapi

@listen_to(r'^game$')
def listen_func(message):
    message.reply('Choose new or load for game setting. ( ex. new )\n new : start with new setting \n load : start with load your setting')


@listen_to(r'^new$')
def listen_func(message):
    branchlist = tl.getBranch()
    msg = 'Please set up to start the game.\n Choose your branch．( ex. br0br5 )\n'
    for i in range(len(branchlist)):
        msg = msg + 'br' + str(i) + ' : ' + branchlist[i] + ' \n'
    message.reply(msg)


@listen_to(r'^br\d')
def listen_func(message):
    branch = message.body['text']
    tl.updateOption('branch', branch)
    msg = 'You choose ' + branch + '.\n Choose the opponent team. ( ex. opp1opp12opp13 )\n When you choose \"opp\", you can select all teams\n'

    opplist = tl.getOpponent()
    for i in range(len(opplist)):
      msg = msg + 'opp'+ str(i) + ' : ' + opplist[i]+ '\n'
    message.reply(msg)


@listen_to(r'^opp')
def listen_func(message):
    opponent = message.body['text']
    tl.updateOption('opponent', opponent)

    msg = 'You choose '+ opponent + ' for the opponent team.\n How many games do you want to run? ( ex. 100 )'
    message.reply(msg)


@listen_to(r'^\d+$')
def listen_func(message):
    gamenum = message.body['text']
    tl.updateOption('gamenum', gamenum)
    msg = 'We run ' + gamenum + ' games.'
    message.reply(msg)

    msg = tl.confirmSetting()
    message.reply(msg)


@listen_to(r'^load$')
def listen_func(message):
    settinglist = tl.getSetting()
    msg = 'Choose your setting．( ex. set5 )\n'
    for i in range(len(settinglist)):
        msg = msg + 'set' + str(i+1) + ' : ' + settinglist[i] + ' \n'
    message.reply(msg)


@listen_to(r'^set\d$')
def listen_func(message):
    set = message.body['text']
    loadpath = tl.getLoadPath(set)

    msg = tl.confirmSetting(loadpath)
    message.reply(msg)


@listen_to(r'^ok$')
def cool_func(message):
    dt_now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    shutil.copy('./slackbot/order/ORDER.pkl', './slackbot/order/'+dt_now+'.pkl')

    opt = tl.getOption('./slackbot/order/'+dt_now+'.pkl')
    msg = "ORDER:{}\n   Options:\n   branches:{}\n   n_games:{}\n   opponents:{}\n".format(dt_now, opt[0], opt[1], opt[2])
    msg += "   total: {} games".format(len(opt[0])*int(opt[1])*len(opt[2]))
    message.reply(msg)

    available_hostlist = tl.getHost()

    working_procs = {
        "proc": [],
        "setting": []
    }
    finished_procs = {
        "proc": [],
        "setting": []
    }
    all_settings = []

    # -------- #
    # execution
    # -------- #
    total_count = 0

    # branch loop
    for br_name in opt[0]:
        # send my team branch binary
        subprocess.run(['./gametools/branchcompile.sh', br_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # opponent loop
        for opp_name in opt[2]:

            # dir name can be specified by dt_now, br_name and opp_name
            dirname = "{}/{}_{}".format(dt_now, br_name.split("/")[-1], opp_name.replace("/", "-"))

            # append setting information
            all_settings.append([dirname, br_name, opp_name])

            # game loop
            for game in range(int(opt[1])):

                # check host
                # loop until next host is found
                host = None
                while True:
                    # the order should be reversed for pop
                    for i in reversed(range(len(working_procs["proc"]))):
                        if working_procs["proc"][i].poll() is not None:
                            p = working_procs["proc"].pop(i)
                            s = working_procs["setting"].pop(i)
                            finished_procs["proc"].append(p)
                            finished_procs["setting"].append(s)

                            # recover available hostlist
                            available_hostlist.append(s[1])

                            # progress report
                            total_count += 1
                            if total_count % 1000 == 0:
                                msg = "Progress Report\n  {} games are finished.\n  {} games left.".format(total_count, len(opt[0]) * int(opt[1]) * len(opt[2]) - total_count)
                                message.reply(msg)

                    # if finished processes are found, "endgame.sh" will be executed
                    while finished_procs["proc"] and finished_procs["setting"]:
                        p = finished_procs["proc"].pop(0)
                        s = finished_procs["setting"].pop(0)
                        subprocess.Popen(['./gametools/endgame.sh', s[0], s[1], s[2], str(s[3]), s[4]])

                    for i, h in enumerate(available_hostlist):
                        check = subprocess.run(['./gametools/getHost.sh', h], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf8").strip("\n")
                        if check == "1":
                            # the host is available
                            host = available_hostlist.pop(i)
                            break
                    if host is not None:
                        break

                msg = "Host {} is assigned (Settings: branch {} gameID {} opp {})\n".format(host, br_name, game, opp_name)
                # message.reply(msg)
                print(msg)

                # execute a game at a host
                proc = subprocess.Popen(['./gametools/startgame.sh', dirname, host, br_name, str(game), opp_name],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                # append process information
                working_procs["proc"].append(proc)
                working_procs["setting"].append([dirname, host, br_name, game, opp_name])


    # wait all process
    for subproc in working_procs["proc"]:
        subproc.wait()

    # all working processes are finished
    while working_procs["proc"] and working_procs["setting"]:
        p = working_procs["proc"].pop(0)
        s = working_procs["setting"].pop(0)
        subprocess.run(['./gametools/endgame.sh', s[0], s[1], s[2], str(s[3]), s[4]])
        # recover available hostlist (but not needed)
        available_hostlist.append(s[1])

    # write results in ggss
    read_count = 0
    write_count = 0
    for setting in all_settings:
        dirname = setting[0]
        br_name = setting[1]
        opp_name = setting[2]

        # initialize
        count = 0
        result_map = {
            'n_games': 0,
            'win': 0.0,
            'draw': 0.0,
            'lose': 0.0,
            'win_rate': 0.0,
            'our_score': 0.0,
            'opp_score': 0.0,
            'our_possession': 0.0,
            'our_passes': 0.0,
            'opp_passes': 0.0,
            'our_through_passes': 0.0,
            'opp_through_passes': 0.0,
            'our_shoot': 0.0,
            'opp_shoot': 0.0,
            'dead_players': []
        }

        # calculate analyzed results
        for i, line in enumerate(open("./log/{}/results.csv".format(dirname), "r")):
            tmp = line.split("\n")[0].split(",")
            result_map["win"] += 1.0 if tmp[7] == "3" else 0
            result_map["win_rate"] += 1.0 if tmp[7] == "3" else 0
            result_map["draw"] += 1.0 if tmp[7] == "1" else 0
            result_map["lose"] += 1.0 if tmp[7] == "0" else 0
            result_map["our_score"] += float(tmp[3])
            result_map["opp_score"] += float(tmp[4])
            result_map["our_possession"] += float(tmp[10])
            result_map["our_passes"] += float(tmp[14])
            result_map["opp_passes"] += float(tmp[19])
            result_map["our_through_passes"] += float(tmp[24])
            result_map["opp_through_passes"] += float(tmp[25])
            result_map["our_shoot"] += float(tmp[30])
            result_map["opp_shoot"] += float(tmp[31])
            if int(tmp[38]) > 0:
                result_map["dead_players"].append(tmp[0]) 
            count += 1

        result_map["n_games"] = count

        # average
        for key in result_map.keys():
            if key == "win" or key == "draw" or key == "lose" or key == "n_games" or key == "dead_players":
                continue
            result_map[key] /= float(count)

        # reformat
        result_map["dead_players"] = ",".join(result_map["dead_players"])

        # write result_map to ggss
        if write_count >= 80 or read_count >= 80:
            # write requests are restricted per 100 seconds
            print("Requests for Google Spread Sheet are restricted per 100 seconds. Please wait...")
            time.sleep(100)
            write_count = 0
            read_count = 0
        tmp_read_count, tmp_write_count = ggssapi.writeResults(dt_now, br_name, opp_name, result_map)
        read_count += tmp_read_count
        write_count += tmp_write_count
        print('r:', read_count)
        print('w:', write_count)

    msg = 'ORDER:'+dt_now+' finish!\nDo you want to save your setting? If you want, type the file name.　(ex. save:FILENAME )'
    message.reply(msg)


@listen_to(r'^save:\w+$')
def listen_func(message):
    savepath = message.body['text'].replace('save:', '')
    shutil.copy('./slackbot/setting/option.pkl', './slackbot/setting/'+savepath)
    msg = 'Save the option to ' + savepath + '.'
    message.reply(msg)
