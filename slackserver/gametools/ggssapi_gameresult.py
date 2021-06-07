# -*- coding:utf-8 -*-
import os
import json
import gspread
import sys
import subprocess
from oauth2client.service_account import ServiceAccountCredentials


def writeResults(order, branch, opp, result_map):
    doc_id = subprocess.Popen(
        'source ../config; echo ${GGSS_KEY}', stdout=subprocess.PIPE,
        shell=True, executable='/bin/bash').communicate()[0].decode("utf8").strip("\n")
    jsonfile = subprocess.Popen(
        'source ../config; echo ${GGSS_JSON}', stdout=subprocess.PIPE,
        shell=True, executable='/bin/bash').communicate()[0].decode("utf8").strip("\n")
    sheetname = subprocess.Popen(
        'source ../config; echo ${GGSS_SPREAD_SHEET_NAME}', stdout=subprocess.PIPE,
        shell=True, executable='/bin/bash').communicate()[0].decode("utf8").strip("\n")

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    path = os.path.expanduser("./gametools/{}".format(jsonfile))  # set json file
    doc_id = doc_id  # documents id of google spread sheet
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scope)
    client = gspread.authorize(credentials)
    gfile = client.open_by_key(doc_id)

    worksheet_list = gfile.worksheets()
    write_count = 0
    read_count = len([wks for wks in worksheet_list])

    if sheetname not in [wks.title for wks in worksheet_list]:
        # create sheet
        gfile.add_worksheet(title=sheetname, rows=1000, cols=100, index=0)
        tmp_rows = []

        # ----- pre-format ----- #
        # opplist = subprocess.run(
        #     'source ../config; echo ${OPP_TEAMS[@]}', stdout=subprocess.PIPE,
        #     shell=True, executable='/bin/bash').stdout.decode("utf8").strip().split()
        # for i, o in enumerate(opplist):
        #     if i == 0:
        #         tmp_rows.append(["", ""])
        #         tmp_rows.append(["ORDER", "branch"])
        #         write_count += 4
        #     tmp_rows[0].extend([o, "", "", "", "", ""])
        #     tmp_rows[1].extend(["win", "draw", "lose", "our_score", "opp_score", "dead_players"])
        #     write_count += 12
        # gfile.worksheet(sheetname).append_rows(tmp_rows)
        # ----- new-format ----- #
        tmp_rows.extend(["ORDER", "branch", "opp_name", "comment/memo"])
        tmp_rows.extend(result_map.keys())
        write_count += len(tmp_rows)

        gfile.worksheet(sheetname).append_row(tmp_rows)

    worksheet = gfile.worksheet(sheetname)  # choose your worksheet
    read_count *= 2

    # ----- pre-format ----- #
    # order_cell_list = worksheet.findall(order)
    # read_count += len(order_cell_list)
    # branch_cell_list = worksheet.findall(branch)
    # read_count += len(branch_cell_list)
    # opp_cell = worksheet.find(opp)
    # read_count += 1

    # target_cell_col = opp_cell.col
    # target_cell_row = 0
    # for order_cell in order_cell_list:
    #     for branch_cell in branch_cell_list:
    #         if order_cell.row == branch_cell.row:
    #             target_cell_row = order_cell.row

    # # initial write
    # if target_cell_row == 0:
    #     worksheet.insert_row([order, branch], 3)
    #     target_cell_row = 3
    #     read_count += 1
    #     write_count += 2

    # cell_list = worksheet.range(target_cell_row, target_cell_col, target_cell_row, target_cell_col+6)
    # read_count += 1
    # for cell, result in zip(cell_list, result_map.values()):
    #     cell.value = result
    #     read_count += 1
    # worksheet.update_cells(cell_list)
    # read_count += 6
    # write_count += 6

    # ------ new-format ----- #
    write_info = [order, branch, opp, ""]
    write_info.extend(result_map.values())
    worksheet.insert_row(write_info, 2)
    write_count += len(write_info)
    read_count += len(write_info)

    return read_count, write_count
