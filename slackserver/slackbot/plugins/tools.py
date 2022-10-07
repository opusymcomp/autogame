# coding: utf-8
import os
import shutil
import subprocess
import pickle


def updateOption(option, data, path='./slackbot/setting/option.pkl'):
    if option == 'our':
        ind = 0
        our = getOur()
        if data == "our":
            data = [opp[int(i)] for i in range(len(opp))]
        else:
            data = data.split("our")[1:]
            data = [i for i in data if i != '0']
            data = [our[int(datum)] for datum in data if datum]
    elif option == 'branch':
        ind = 0
        branch = getBranch()
        data = data.split("br")[1:]
        data = [branch[int(datum)] for datum in data]
    elif option == 'gamenum':
        ind = 1
    elif option == 'opponent':
        ind = 2
        opp = getOpponent()
        if data == "opp":
            data = [opp[int(i)] for i in range(len(opp))]
        else:
            data = data.split("opp")[1:]
            data = [opp[int(datum)] for datum in data]
    else:
        raise ValueError

    # 0: ours, 1: games, 2: opponents
    datalist = [[], 0, []]
    if os.path.exists(path):
        # read previous option
        datalist = getOption(path)

    if option == 'branch':
        datalist[ind] = data + datalist[ind]
    else:
        datalist[ind] = data

    with open(path, mode='wb+') as f:
        pickle.dump(datalist, f)


def getOption(path='./slackbot/setting/option.pkl'):
    with open(path, mode='rb+') as f:
        datalist = pickle.load(f)
    return datalist


def getLoadPath(set):
    num = int(set.split('set')[1]) - 1
    settinglist = getSetting()
    loadpath = './slackbot/setting/'+settinglist[num]
    return loadpath


def confirmSetting(path='./slackbot/setting/option.pkl'):
    opt = getOption(path)
    msg = 'Confirmation \n   - ours : ' + ",".join([b for b in opt[0]]) + '\n   - opponent : ' + ",".join([o for o in opt[2]]) + '\n   - gamenum : ' + str(opt[1]) + '\n ok？'
    shutil.copy(path, './slackbot/order/ORDER.pkl')
    return msg


def resCmd(cmd):
  return subprocess.Popen(
      cmd, stdout=subprocess.PIPE,
      shell=True, executable='/bin/bash').communicate()[0]


def getBranch():
    exepath = os.getcwd()
    cmd = ("source ../config; echo ${OUR_TEAM}")
    our_team = resCmd(cmd).decode('utf-8').strip('\n')
    os.chdir(our_team)
    os.system("git fetch -p")
    cmd = ("git branch -r")
    branchlist = resCmd(cmd).decode('utf-8').replace("  origin/", "").replace("\nHEAD -> origin/master", "").split("\n")[:-1]
    os.chdir(exepath)
    return branchlist


def getSetting():
    cmd = ("ls ./slackbot/setting/")
    settinglist = resCmd(cmd).decode('utf-8').strip().split()
    return settinglist


def getOur():
    cmd = ("source ../config; echo ${OUR_TEAM} ${OPP_TEAMS[@]}")
    ourlist = resCmd(cmd).decode('utf-8').strip().split()
    return ourlist


def getOpponent():
    cmd = ("source ../config; echo ${OPP_TEAMS[@]}")
    opplist = resCmd(cmd).decode('utf-8').strip().split()
    return opplist


def getHost():
    cmd = ("source ../config; echo ${HOST_NAMES[@]}")
    hostlist = resCmd(cmd).decode('utf-8').strip().split()
    return hostlist


if __name__ == '__main__':
    getBranch()
