=====================================================

#  __Performance-Evaluation System__

=====================================================

## Overview
This system enables the automation of the performance evaluation process in the team development flow of RoboCup Soccer Simulation 2D.

## Requirement
- OS
  - Ubuntu
- tool
  - [rcssserver](https://github.com/rcsoccersim/rcssserver)
  - [loganalyzer3](https://github.com/opusymcomp/loganalyzer3)
- library
  - Python3
  - NumPy
  - slackbot
  - gspread
  - oauth2client

## Install
```
$ git clone http://github.com/opusymcomp/autogame
```
Install all required libraries.
```
$ pip install numpy
$ pip install slackbot
$ pip install gspread
$ pip install oauth2client
```
## Usage
First, you need to create a [Slack](https://slack.com/get-started#/create)
account.

Next, you need to create a [Slackbot](https://my.slack.com/services/new/bot).

At that time, an API token is generated, so write it in the following file.
```
autogame/slackserver/slackbot/slackbot_settings.py
```
Finally, add a Slackbot to the channel(e.g. #general) and you are ready to go.
```
$ cd autogame/slackserver
$ ./start-server.sh
```
Start the Slackbot.
You can send a request to the Slackbot.

Input "game" to start interacting with Slackbot in your channel.

## License
[MIT](https://github.com/opusymcomp/autogame/blob/master/LICENSE)

## Author
- Ryota Kuga (Osaka Prefecture University)
- Yudai Suzuki (Osaka Prefecture University)
- Tomoharu Nakashima (Osaka Prefecture University)
