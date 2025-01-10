=====================================================

#  __Performance-Evaluation System__

=====================================================

## Overview
This system enables the automation of the performance evaluation process in the team development flow of RoboCup Soccer Simulation 2D.

## Requirement
- OS
  - Ubuntu 18.04 or later (for all host)
- tool
  - [rcssserver](https://github.com/rcsoccersim/rcssserver)
  - [loganalyzer3](https://github.com/opusymcomp/loganalyzer3)
- library
  - Python3
  - NumPy
  - slackbot
  - gspread
  - oauth2client

## Install (for example)
Note that we expect that the following install procedure is set according to `config`.
If you want to install with your setting, please modify `config` and replace the following explanation into your setting.


Install all required libraries.
```
$ pip install numpy
$ pip install slackbot
$ pip install gspread
$ pip install oauth2client
```

Change to your working directory.

```
$ cd /path/to/install_dir
$ git clone http://github.com/opusymcomp/autogame
```

Please change `HOST_AUTOGAME_DIR`, `LOGANALYZER3_DIR`, `LOG_DIR`, `LIBRCSC_DIR`, `OUR_TEAM`, `OPP_TEAMS`, `HOST_NAMES` in `config` file if you want.
We explain this install procedure with default settings.

```
$ cd autogame/common
```

You must exchange ssh-key in all hosts.
Please change `hostnames` to your environment.
(All hosts must have same superuser.)

```
$ cd ./auto_sshkey.sh
```

Setup all hosts.
The following install directories are same as the place described at `config`.
__Do not forget__ to replace to your settings.

Install loganalyzer3 (the place is same as `LOGANALYZER3_DIR` in `config`)
```
$ ./cmd_to_all_hosts.sh "cd /home/fukushima/rcss/HELIOS/; git clone https://github.com/opusymcomp/loganalyzer3.git"
```
Install loganalyzer3 (the place is same as `OUR_TEAM` in `config`)
```
$ ./cmd_to_all_hosts.sh "cd /home/fukushima/rcss/opuSCOM/; git clone (team_repository)"
```
Make a log directory (the place is same as `LOG_DIR` in `config`)
```
$ ./cmd_to_all_hosts.sh "cd /home/fukushima/rcss/log"
```
Send all team-binaries from your current PC to all hosts.
Please setup the all team-binaries before sending.
(All team-binaries must have `start.sh` and `kill` in their binaries. Explained at `config` in detail.)
After team-binaries setting, you send the binaries to all hosts.
```
$ ./send_files_to_all_hosts.sh /path/to/team-binary-dir /home/fukushima/rcss/teams/
```

Send this `autogame` to all hosts (the place is same as `HOST_AUTOGAME_DIR`)
```
$ ./send_files_to_all_hosts.sh /path/to/autogame /home/fukushima/rcss/
```

Create Slack workspace, and get Slack API Token (https://rctools.slack.com/apps/new/A0F7YS25R-bots).
After that, invite this slack bot to a channel.
Please write the API token to `SLACK_API_TOKEN` in `config`.


Create a Google Spread sheet in your google drive, and get google spread sheet json (https://tanuhack.com/operate-spreadsheet (in Japanese)).
Please write the json file to `GGSS_JSON` and `GGSS_KEY` in `config`.
Put the json file to autogame server.
```
$ mv /path/to/json /path/to/autogame/slackserver/gametools/
```

## Usage
You can select hosts, opp_teams, google spread sheet name from `config`.

Start the Slackbot.
```
$ cd /path/to/autogame/slackserver
$ ./start-server.sh
```
You can send a request to the Slackbot.
Input `game` to start interacting with Slackbot in your channel.

## License
[MIT](https://github.com/opusymcomp/autogame/blob/master/LICENSE)

## Author
- Ryota Kuga (Osaka Prefecture University)
- Yudai Suzuki (Osaka Prefecture University)
- Tomoharu Nakashima (Osaka Prefecture University)

Forked by
- Takuya Fukushima (Osaka Prefecture University)
