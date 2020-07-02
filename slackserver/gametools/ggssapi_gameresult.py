# -*- coding:utf-8 -*-
import os
import json
import gspread
import sys

from oauth2client.service_account import ServiceAccountCredentials

def main(order, branch, fiftystorms, helios2018, hillstone2019, opuscom2018, rione2019, toyosugalaxy, helios2019, gliders2d, heliosbase, jyosen):
    scope = ['https://spreadsheets.google.com/feeds']
    path = os.path.expanduser("./sample.json") # set json file
    doc_id = '' # documents id of google spread sheet
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scope)
    client = gspread.authorize(credentials)
    gfile   = client.open_by_key(doc_id)
    worksheet = gfile.worksheet('sheet1') # choose your worksheet

    column = [order, branch,
            float(fiftystorms['win']),
            float(fiftystorms['lose']),
            float(fiftystorms['draw']),
            float(fiftystorms['our_score']),
            float(fiftystorms['opp_score']),
            float(helios2018['win']),
            float(helios2018['lose']),
            float(helios2018['draw']),
            float(helios2018['our_score']),
            float(helios2018['opp_score']),
            float(hillstone2019['win']),
            float(hillstone2019['lose']),
            float(hillstone2019['draw']),
            float(hillstone2019['our_score']),
            float(hillstone2019['opp_score']),
            float(opuscom2018['win']),
            float(opuscom2018['lose']),
            float(opuscom2018['draw']),
            float(opuscom2018['our_score']),
            float(opuscom2018['opp_score']),
            float(rione2019['win']),
            float(rione2019['lose']),
            float(rione2019['draw']),
            float(rione2019['our_score']),
            float(rione2019['opp_score']),
            float(toyosugalaxy['win']),
            float(toyosugalaxy['lose']),
            float(toyosugalaxy['draw']),
            float(toyosugalaxy['our_score']),
            float(toyosugalaxy['opp_score']),
            float(helios2019['win']),
            float(helios2019['lose']),
            float(helios2019['draw']),
            float(helios2019['our_score']),
            float(helios2019['opp_score']),
            float(gliders2d['win']),
            float(gliders2d['lose']),
            float(gliders2d['draw']),
            float(gliders2d['our_score']),
            float(gliders2d['opp_score']),
            float(heliosbase['win']),
            float(heliosbase['lose']),
            float(heliosbase['draw']),
            float(heliosbase['our_score']),
            float(heliosbase['opp_score']),
            float(jyosen['win']),
            float(jyosen['lose']),
            float(jyosen['draw']),
            float(jyosen['our_score']),
            float(jyosen['opp_score'])]

    worksheet.append_row(column)

if __name__ == '__main__':
    main("ORDER","branch",0,1,2,3,4,5,6,7,8,9)
