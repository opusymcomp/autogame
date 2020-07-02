=====================================

#  __Performance-Evaluation System__

=====================================

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
Install all required libraries
```
$ pip install numpy
$ pip install slackbot
$ pip install gspread
$ pip install oauth2client
```
## Usage
```
$ cd autogame/slackserver
$ ./start-server.sh

```
Start the slackbot.
You can send a request to the slackbot.

Input "game" to start interacting with slackbot in your workspace.

## License
[MIT](https://github.com/opusymcomp/autogame/blob/master/LICENSE)

## Author
- Ryota Kuga (Osaka Prefecture University)
- Yudai Suzuki (Osaka Prefecture University)
