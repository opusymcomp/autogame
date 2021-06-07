# coding: utf-8
import subprocess

# API Token
# Check your slack workspace settings
API_TOKEN = subprocess.Popen( 'source ../config; echo ${SLACK_API_TOKEN}', stdout=subprocess.PIPE, shell=True, executable='/bin/bash').communicate()[0].decode('utf-8').strip('\n')
# Default Reply (when @bot)
DEFAULT_REPLY = 'Sorry, I don\'t understand...'

# Subdirectory name of plugin scripts
PLUGINS = ['plugins']
