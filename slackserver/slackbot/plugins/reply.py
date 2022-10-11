# coding: utf-8
import tools as tl
import time
import datetime
import subprocess
import shutil
import re
# from slackbot.bot import respond_to
# from slackbot.bot import listen_to
# from slackbot.bot import default_reply

import os
import sys
sys.path.append("{}/gametools".format(os.getcwd()))
import ggssapi_gameresult as ggssapi

branchflag = "false"
synchflag = "true"

def numCheck(str, sp):
    if not str[-1].isdecimal():
        print(f"  ***ERROR***:{sp}[{str[-1]}] is {sp}(Num){sp}(Num)...")
        return False
    else:
        return True


def chooseNewOrLoad():
    print(f'1:Choose new or load for game setting. ( ex. new )\n  new : start with new setting \n  load : start with load your setting')
    while True:
        ans = input(" new or load: ")
        if ans in ["new", "load"]:
            return ans
        else:
            print(f" ***ERROR***:answer is \"new\" or \"load\"")

def chooseOurTeam():
    print(f'2:Choose the our team. ( ex. our1our12our13 )\n  When you choose \"our\", you can select all teams')

    ourlist = tl.getOur()
    for i in range(len(ourlist)):
      print(f'  our{str(i)}:{ourlist[i]}')

    while True:
        ans = input("  our: ")
        ours = ans.split('our')
        if not numCheck(ours, "our"):
            continue
        for our in ours[1:]:
            if not our.isdecimal():
                print(f"  ***ERROR***:our[{our}] is our(Num)our(Num)...")
                break
            our = int(our)
            if not our in list(range(len(ourlist))):
                print(f"  ***ERROR***:our[{our}] is no ours")
                break
            if our == int(ours[-1]):
                tl.updateOption('our', ans)
                return ans

def chooseBranch(ours):
    if "our0" in ours:
        tl.updateOption('our', ours)
        print(f"3:Please set up to start the game.\n  Choose your branch.( ex. br0br5 )")
        branchlist = tl.getBranch()
        for i in range(len(branchlist)):
            print(f"  br{str(i)} : {branchlist[i]}")

        while True:
            ans = input("  br: ")
            branches = ans.split('br')
            if not numCheck(branches, "br"):
                continue
            for branch in branches[1:]:
                if not branch.isdecimal():
                    print(f"  ***ERROR***:br[{branch}] is br(Num)br(Num)...")
                    break
                branch = int(branch)
                if not branch in list(range(len(branchlist))):
                    print(f"  ***ERROR***:br[{branch}] is no ours")
                    break
                if branch == int(branches[-1]):
                    tl.updateOption('branch', ans)
                    return ans


    else:
        print(f"3:No exist branch team")

def chooseOppTeam():
    print(f"4:Choose the opponent team. ( ex. opp1opp12opp13 )\n  When you choose \"opp\", you can select all teams")

    opplist = tl.getOpponent()
    for i in range(len(opplist)):
      print(f'  opp{str(i)}:{opplist[i]}')

    while True:
        ans = input("  opp: ")
        opps = ans.split('opp')
        if not numCheck(opps, "opp"):
            continue
        for opp in opps[1:]:
            if not opp.isdecimal():
                print(f"  ***ERROR***:opp[{opp}] is opp(Num)opp(Num)...")
                break
            opp = int(opp)
            if not opp in list(range(len(opplist))):
                print(f"  ***ERROR***:opp[{opp}] is no opps")
                break
            if opp == int(opps[-1]):
                tl.updateOption('opponent', ans)
                return ans

def chooseGameNum():
    print(f"5:How many games do you want to run? ( ex. 100 )")

    while True:
        print("  num: ", end="")
        ans = input()
        if not ans.isdecimal():
            print(f"  ***ERROR***:num[{ans}] is int")
        else:
            tl.updateOption('gamenum', ans)
            return ans

def checkTime(ours, branches, opps, num):
    print(f"We run {num} games.")
    msg = tl.confirmSetting()
    print(f'{msg}')

def doGame():
    dt_now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    shutil.copy('./slackbot/order/ORDER.pkl', './slackbot/order/'+dt_now+'.pkl')

    opt = tl.getOption('./slackbot/order/'+dt_now+'.pkl')
    print(f"ORDER:{dt_now}\n   Options:\n   ours:{opt[0]}\n   n_games:{opt[1]}\n   opponents:{opt[2]}")
    print(f"total: {len(opt[0])*int(opt[1])*len(opt[2])} games")

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
    for our_name in opt[0]:
        # check our team is branch or teams
        branchlist = tl.getBranch()
        if our_name in branchlist:
            branchflag = "true"
            print(our_name,"is branch")
            # send my team branch binary
            branchproc = subprocess.Popen(['./gametools/branchcompile.sh', our_name]) #, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            branchflag = "false"
            print(our_name,"is not branch")

        # opponent loop
        for opp_name in opt[2]:
            if our_name == opp_name:
                print(our_name,opp_name,"same team")
                continue

            # check opp team can use synce
            if ("fractals" in our_name) or ("fractals" in opp_name):
                synchflag = "false"
                print(our_name, opp_name, ":synchflag ", synchflag)
            elif ("fraunited" in our_name) or ("fraunited" in opp_name):
                synchflag = "false"
                print(our_name, opp_name, ":synchflag ", synchflag)
            elif ("oxsy" in our_name) or ("oxsy" in opp_name):
                synchflag = "false"
                print(our_name, opp_name, ":synchflag ", synchflag)
            else:
                synchflag = "true"
                print(our_name, opp_name, ":synchflag ", synchflag)

            # dir name can be specified by dt_now, our_name and opp_name
            dirname = "{}/{}_{}".format(dt_now, our_name.split("/")[-1], opp_name.replace("/", "-"))

            # append setting information
            all_settings.append([dirname, our_name, opp_name])

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
                                print(msg)

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

                msg = "Host {} is assigned (Settings: our {} gameID {} opp {})\n".format(host, our_name, game, opp_name)
                # message.reply(msg)
                print(msg)

                # execute a game at a host
                if branchflag == "true":
                    branchproc.wait()
                proc = subprocess.Popen(['./gametools/startgame.sh', dirname, host, our_name, str(game), opp_name, branchflag, synchflag],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                # append process information
                working_procs["proc"].append(proc)
                working_procs["setting"].append([dirname, host, our_name, game, opp_name])


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
        our_name = setting[1]
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
        tmp_read_count, tmp_write_count = ggssapi.writeResults(dt_now, our_name, opp_name, result_map)
        read_count += tmp_read_count
        write_count += tmp_write_count
        print('r:', read_count)
        print('w:', write_count)

    msg = 'ORDER:'+dt_now+' finish!\nDo you want to save your setting? If you want, type the file name.　(ex. save:FILENAME )'
    print(msg)


def main():
    option = chooseNewOrLoad()
    ours = chooseOurTeam()
    branches = chooseBranch(ours)
    opps = chooseOppTeam()
    num = chooseGameNum()
    checkTime(ours, branches, opps, num)
    doGame()

if __name__ == "__main__":
    print('start autogame')
    main()