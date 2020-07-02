# coding: utf-8
import os
import subprocess

def updateOption(option, data, path = './slackbot/setting/option.txt'):
    if option == 'branch':
        num = 0
        data = data.strip().split(':')[1]
    elif option == 'gamenum':
        num = 1
    elif option == 'opponent':
        num = slice(2,None)
        data = data.split("opp")
        data = ''.join(data[1:])
        print('data:',data)
    else:
        raise ValueError
    f = open(path, mode='r+')
    datalist = [s.split(',') for s in f.readlines()][0]
    datalist[num] = data
    str_ = ','.join(datalist)
    f = open(path, mode='w+')
    f.write(str_)

def getOption(path='./slackbot/setting/option.txt'):
    f = open(path, mode='r+')
    datalist = [s.split(',') for s in f.readlines()][0]
    return datalist

def storeOption(savedir,path='./slackbot/setting/option.txt'):
    datalist = getOption(path)
    str_ = ','.join(datalist)
    f = open(savedir, mode='w+')
    f.write(str_)

def getLoadPath(set):
    num = int(set.split('set')[1]) - 1
    settinglist = getSetting()
    loadpath = './slackbot/setting/'+settinglist[num]
    return loadpath

def confirmSetting(path = './slackbot/setting/option.txt'):
    opt = getOption(path)
    msg = 'Confirmation \n   - branch : ' + str(opt[0]) + '\n   - opponent : ' + str(opt[2:]) + '\n   - gamenum : ' + str(opt[1]) + '\n ok？'
    storeOption('./slackbot/order/ORDER.txt',path)
    return msg

def resCmd(cmd):
  return subprocess.Popen(
      cmd, stdout=subprocess.PIPE,
      shell=True).communicate()[0]

def getBranch():
    exepath = os.getcwd()
    home = os.environ['HOME']
    os.chdir(home+"/teamdir") # team's dir
    os.system("git fetch -p")
    cmd = ("git branch -r")
    branchlist = resCmd(cmd).decode('utf-8').strip().strip("*  ").split('\n  ')
    os.chdir(exepath)
    return branchlist

def getSetting():
    cmd = ("ls ./slackbot/setting/")
    settinglist = resCmd(cmd).decode('utf-8').strip().split()
    return settinglist

def getOpponent():
    cmd = ("cat ./gametools/team_list.txt")
    settinglist = resCmd(cmd).decode('utf-8').strip().split()
    return settinglist

if __name__ == '__main__':
    getBranch()
