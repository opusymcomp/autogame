# coding: utf-8
import plugins.tools as tl
import datetime
import subprocess
from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply


@listen_to(r'^game$')
def listen_func(message):
    message.reply('Choose new or load for game setting. ( ex. new )\n new : start with new setting \n load : start with load your setting')

@listen_to(r'^new$')
def listen_func(message):
    branchlist = tl.getBranch()
    msg = 'Please set up to start the game.\n Choose your branch．( ex. br0 : master )\n'
    for i in range(len(branchlist)):
        msg = msg + 'br' + str(i) + ' : ' + branchlist[i] + ' \n'
    message.reply(msg)

@listen_to(r'^br\d+')
def listen_func(message):
    branch = message.body['text']
    tl.updateOption('branch', branch)
    opplist = tl.getOpponent()
    msg = 'You choose ' + branch + '.\n Choose the opponent team. ( ex. opp12345 )\n'
    for i in range(len(opplist)):
      msg = msg + 'opp'+ str(i) + ' : ' + opplist[i]+ '\n'
    message.reply(msg)

@listen_to(r'^opp\d')
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
    ip = subprocess.run(['./gametools/getIP.sh'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ip = ip.stdout.decode("utf8")
    print ("IP:",ip)
    msg = 'The game starts soon at IP:'+ str(ip) +'\n ORDER:' + dt_now + '\n I will notify you when the all game finished. \n Do you want to save your setting? If you want, type the file name.　(ex. save:FILENAME.txt )'
    message.reply(msg)
    message.react('+1')
    tl.storeOption('./slackbot/order/'+dt_now+'.txt', './slackbot/order/ORDER.txt')
    subprocess.run(['./gametools/execute.sh', dt_now, ip])
    msg = 'ORDER:'+dt_now+' finish!'
    message.reply(msg)

@listen_to(r'^save:\w+.txt$')
def listen_func(message):
    savedir = message.body['text'].replace('save:','')
    tl.storeOption('./slackbot/setting/'+savedir)
    msg = 'Save the option to ' + savedir + '.'
    message.reply(msg)
